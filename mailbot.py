from re import search, IGNORECASE

from bot.bot import Bot
from bot.event import EventType
from bot.handler import MessageHandler
from icecream import ic
from telebot import TeleBot

from configs.bot_config import TG_TOKEN, MAILRU_TOKEN, MSG_REGEXP, CHAT_ID, API_BASE

mailru_bot = Bot(token=MAILRU_TOKEN, api_url_base=API_BASE, is_myteam=True)
tg_bot = TeleBot(TG_TOKEN, parse_mode="Markdown")


def sender(message):
    tg_bot.send_message(CHAT_ID, message)


def watcher(bot, event):
    ic(event)
    if event.type == EventType.NEW_MESSAGE and search(
        MSG_REGEXP, event.text, IGNORECASE
    ):
        ic("Message", event.text)
        ic("Sending message to", CHAT_ID)
        sender(f"*{event.data['chat']['title']}:*\n{event.text}")


mailru_bot.dispatcher.add_handler(MessageHandler(callback=watcher))
ic("Starting mailru")
mailru_bot.start_polling()
ic("Starting tg")
tg_bot.polling()
