# home_bot

### Как запустить проект:

Клонировать репозиторий и войти в него.


Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Войти в папку проекта и выполнить миграции:

```
cd gpt_bot
```

```
python3 manage.py migrate
```

Создать суперпользователя:

```
python3 manage.py createsuperuser
```

Для запуска проекта в зоне администратора:

```
python3 manage.py runserver
```

Адрес зоны администратора - [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)   


Для запуска бота необходимо его уже иметь в Telegram :+1:  
(как создать бота читай например [здесь](https://vc.ru/dev/530248-kak-sdelat-bota-v-telegram-poshagovaya-instrukciya)).  


В директории gpt_bot/ создать файл .env  
и в нем  
* в переменную TELEGRAM_TOKEN записать токен вашего бота.
* в переменную SECRET_KEY записать секретный ключ вашего Django-проекта(из settings.py)
* в переменную OPENAI_API_KEY записать APY key, сгенерированный в вашей учетной записи OpenAI

```
TELEGRAM_TOKEN = <ваш токен>
SECRET_KEY = <ключ вашего Django-проекта>
OPENAI_API_KEY = <ваш API key>
```


Из директории gpt_bot/ с файлом manage.py запустить бота:

```
python3 manage.py startbot
```

В Telegram в своём аккаунте зайти в чат своего бота и отправить запрос к ChatGPT.  

В терминале при запуске бота выводятся сообщения логирования.  
При отправке сообщения боту в терминале выводится служебная информация(это на время отладки, вывод можно удалить из функций). 

Остановить бота:  
> Ctrl+C  