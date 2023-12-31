Этот репозиторий содержит скрипты Python для автоматизированного создания интентов в DialogFlow и их использования в VK и Telegram ботах. 
## Как установить
Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```

### Настройка переменных окружения.
Часть настроек скрипта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.


Для Telegram-бота нужно зарегистрироваться у BotFather и получить токен. Больше информации можно получить на сайте [way23.ru](https://way23.ru/).

Доступные переменные:

`TG_TOKEN` — API ключ, который вы получаете при создании бота в Telegram

`VK_TOKEN` — API ключ, который вы получаете при создании группы в ВКонтакте

`PROJECT_ID` — ProjectID, который вы получили, когда создавали проект в DialogFlow

## Использование
Создание интентов в DialogFlow

Выполните скрипт create_dialogflow_intent.py для создания интентов в [DialogFlow](https://dialogflow.cloud.google.com/).

```
python create_dialogflow_intent.py
```
Также можете указать свой путь к json файлу с фразами:
```
python create_dialogflow_intent.py --phrases_file /path/to/your/phrases.json

```
Запуск скрипта в telegram командой:
```
python tg_bot.py
```

Запуск скрипта в VK командой:
```
python vk_bot.py
```
Пример использования в telegram:
![devman112](https://github.com/Kisly93/Game_verbs/assets/123402270/5c461aed-92e5-4fbc-bc3b-c4a0d05c0579)


## Цели проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/)

