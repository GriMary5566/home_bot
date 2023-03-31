import tiktoken

from asgiref.sync import sync_to_async

from bot.models import BotMessage


SYSTEM_MESSAGE = {
    "role": "system",
    "content": "You are a helpful assistant."
}
ENCODING_MODEL = 'gpt-3.5-turbo'

def num_tokens_from_message(string: str, role: str, encoding_model: str) -> int:
    """Возвращает количество токенов в сообщении."""
    encoding = tiktoken.encoding_for_model(encoding_model)
    num_tokens = 4 + len(encoding.encode(string)) + len(encoding.encode(role))
    return num_tokens

@sync_to_async
def qustion_save(chat, role, content, content_tokens):
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
def get_queryset(chat):
    """Возвращает все сообщения чата."""
    queryset = BotMessage.objects.filter(chat_id=chat.id).values('role', 'content', 'content_tokens')
    return queryset

@sync_to_async
def get_pre_messages(queryset, question):
    """Возвращает запрос к Chat API и количество токенов этого запроса."""
    last_message = {
        "role": question.role,
        "content": question.content
    }
    pre_messages = [SYSTEM_MESSAGE]
    system_message_tokens = num_tokens_from_message(
        SYSTEM_MESSAGE["content"],
        SYSTEM_MESSAGE["role"],
        ENCODING_MODEL
    )
    sum_tokens = system_message_tokens + 4
    print(sum_tokens)
    print(queryset)
    if len(queryset) == 0:
        sum_tokens += question.content_tokens
        pre_messages.append(last_message)
        return pre_messages, sum_tokens

    for query in queryset:        
        if sum_tokens + query['content_tokens'] >= 2000:
            return pre_messages, sum_tokens
        sum_tokens += query['content_tokens'] + 4
        pre_message = {}
        pre_message["role"] = query["role"]
        pre_message["content"] = query["content"]
        pre_messages.insert(1, pre_message)
    
    print(pre_messages)
    print(sum_tokens)
    return pre_messages, sum_tokens 


async def echo(update, context):
    """Отправляет ответ на текстовое входящее сообщение."""
    chat = update.effective_chat
    role = 'user'
    content = update.effective_message.text
    content_tokens = num_tokens_from_message(content, role, ENCODING_MODEL)
    queryset = await get_queryset(chat)
    question = await qustion_save(chat, role, content, content_tokens )
    pre_messages, sum_tokens = await get_pre_messages(queryset, question)

    await update.message.reply_text(f'Тестируем бота. Количество токенов в строке: {content_tokens}')
