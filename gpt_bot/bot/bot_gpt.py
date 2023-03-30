import tiktoken

from asgiref.sync import sync_to_async

from bot.models import BotMessage


def num_tokens_from_string(string: str, encoding_model: str) -> int:
    """Возвращает количество токенов в строке."""
    encoding = tiktoken.encoding_for_model(encoding_model)
    num_tokens = len(encoding.encode(string))
    return num_tokens

@sync_to_async
def qustion_save(chat, role, content, content_tokens):
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
    queryset = BotMessage.objects.filter(chat_id=chat.id).values('role', 'content', 'content_tokens')
    print(queryset)
    return queryset

async def echo(update, context):
    """Отправляет ответ на текстовое входящее сообщение."""
    chat = update.effective_chat
    role = 'user'
    content = update.effective_message.text
    content_tokens = num_tokens_from_string(content, 'gpt-3.5-turbo')
    question = await qustion_save(chat, role, content, content_tokens )
    queryset = await get_queryset(chat)
    await update.message.reply_text(f'Тестируем бота. Количество токенов в строке: {content_tokens}')

