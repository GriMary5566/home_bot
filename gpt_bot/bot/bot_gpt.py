import openai
import os
import tiktoken

from asgiref.sync import sync_to_async
from telegram import Chat
from typing import Dict, List, TypedDict, Tuple

from bot.models import BotMessage


SYSTEM_MESSAGE: Dict[str, str] = {
    'role': 'system',
    'content': 'You are a helpful assistant.'
}
ENCODING_MODEL: str = 'gpt-3.5-turbo'
MAX_NUM_TOKENS: int = 2000


class MessageQuerySet(TypedDict):
    role: str
    content: str
    content_tokens: int


def num_tokens_from_message(
    string: str,
    role: str,
    encoding_model: str
) -> int:
    """Возвращает количество токенов в сообщении."""
    encoding = tiktoken.encoding_for_model(encoding_model)
    num_tokens = 4 + len(encoding.encode(string)) + len(encoding.encode(role))
    return num_tokens


@sync_to_async
def message_save(
    chat: Chat,
    role: str,
    content: str,
    content_tokens: int
) -> BotMessage:
    """Сохраняет сообщение в базу данных и возвращает его."""
    question = BotMessage.objects.create(
        chat_id=chat.id,
        chat_name=chat.full_name,
        role=role,
        content=content,
        content_tokens=content_tokens
    )
    return question


@sync_to_async
def get_queryset(chat: Chat) -> List[MessageQuerySet]:
    """Возвращает все сообщения чата."""
    return BotMessage.objects.filter(chat_id=chat.id).values(
        'role',
        'content',
        'content_tokens'
    )


@sync_to_async
def get_pre_messages(
    queryset: List[MessageQuerySet],
    question: BotMessage
) -> Tuple[List[Dict[str, str]], int]:
    """Возвращает запрос к Chat API и количество токенов этого запроса."""
    last_message = {
        'role': question.role,
        'content': question.content
    }
    pre_messages: List[Dict[str, str]] = [SYSTEM_MESSAGE]
    system_message_tokens: int = num_tokens_from_message(
        SYSTEM_MESSAGE['content'],
        SYSTEM_MESSAGE['role'],
        ENCODING_MODEL
    )
    sum_tokens: int = system_message_tokens
    print(f'количество токенов в system: {sum_tokens}')
    if len(queryset) == 0:
        sum_tokens += question.content_tokens
        pre_messages.append(last_message)
        return pre_messages, sum_tokens

    if BotMessage.objects.filter(chat_id=question.chat_id).count() > 4:
        queryset = queryset[:4]
    print(queryset)
    for query in queryset:
        query_tokens: int = query['content_tokens']
        if sum_tokens + query_tokens >= MAX_NUM_TOKENS:
            print(pre_messages)
            print(sum_tokens)
            return pre_messages, sum_tokens
        sum_tokens += query['content_tokens']
        pre_message: Dict[str, str] = {}
        pre_message['role'] = query['role']
        pre_message['content'] = query['content']
        pre_messages.insert(1, pre_message)

    print(f'запрос к GPT: {pre_messages}')
    print(f'токенов в запросе к GPT: {sum_tokens}')
    return pre_messages, sum_tokens


@sync_to_async
def get_gpt_message(pre_messages) -> openai.ChatCompletion:
    """Возвращает ответ ChatGPT."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    completion = openai.ChatCompletion.create(
        model=ENCODING_MODEL,
        messages=pre_messages,
        max_tokens=1000
    )
    return completion


@sync_to_async
def content_tokens_correction(question, chat_response, sum_tokens) -> None:
    """Уточняет количество токенов в сообщении."""
    prompt_tokens = chat_response['usage']['prompt_tokens']
    print(f'prompt_tokens в ответе: {prompt_tokens}')
    correction = prompt_tokens - sum_tokens
    print(f'разница: {correction}')
    question.content_tokens += correction
    print(question.content_tokens)
    question.save()


async def echo(update, context) -> None:
    """Отправляет ответ на текстовое входящее сообщение."""
    chat: Chat = update.effective_chat
    role: str = 'user'
    content: str = update.effective_message.text
    content_tokens: int = num_tokens_from_message(
        content,
        role,
        ENCODING_MODEL
    )
    queryset = await get_queryset(chat)
    question = await message_save(chat, role, content, content_tokens)
    pre_messages, sum_tokens = await get_pre_messages(queryset, question)
    response = await get_gpt_message(pre_messages)
    response_content: str = response['choices'][0]['message']['content']
    response_tokens: int = response['usage']['completion_tokens'] + 5
    await message_save(
        chat=chat,
        role=response['choices'][0]['message']['role'],
        content=response_content,
        content_tokens=response_tokens
    )
    await content_tokens_correction(question, response, sum_tokens)
    await update.message.reply_text(f'ChatGPT: {response_content}')
