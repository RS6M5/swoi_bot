import telebot
import requests
import os

API_TOKEN = '7487553161:AAFK1464gSwILqxPHq_nQE3tlgjftJ2esxs'
RAPIDAPI_KEY = 'fb7b02f248msh50bf1abfea420c9p1b2502jsn792cb0d50bf4'
EXCHANGE_RATE_API_KEY = '9e482e4dc7bd47dbdba75c70'

bot = telebot.TeleBot(API_TOKEN)

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот-помощник. Вот что я умею:\n"
                          "/weather [город] - Показать погоду\n"
                          "/joke - Рассказать шутку\n"
                          "/translate [текст] - Перевести текст\n"
                          "/rate [валюта] - Показать курс валюты")



# Команда /joke
@bot.message_handler(commands=['joke'])
def tell_joke(message):
    url = "https://v2.jokeapi.dev/joke/Any"
    response = requests.get(url)
    data = response.json()
    if data['type'] == 'single':
        bot.reply_to(message, data['joke'])
    else:
        bot.reply_to(message, f"{data['setup']} - {data['delivery']}")

# Команда /translate
@bot.message_handler(commands=['translate'])
def translate_text(message):
    try:
        text_to_translate = " ".join(message.text.split()[1:])
        url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "application/gzip",
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
        }
        payload = f"q={text_to_translate}&target=ru"
        response = requests.post(url, data=payload, headers=headers)
        data = response.json()
        translated_text = data['data']['translations'][0]['translatedText']
        bot.reply_to(message, translated_text)
    except IndexError:
        bot.reply_to(message, "Пожалуйста, укажите текст для перевода после команды /translate")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

# Команда /rate
@bot.message_handler(commands=['rate'])
def get_exchange_rate(message):
    try:
        currency = message.text.split()[1].upper()
        url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/USD"
        response = requests.get(url)
        data = response.json()
        if 'conversion_rates' in data and currency in data['conversion_rates']:
            rate = data['conversion_rates'][currency]
            bot.reply_to(message, f"Курс {currency} к USD: {rate}")
        else:
            bot.reply_to(message, "Валюта не найдена")
    except IndexError:
        bot.reply_to(message, "Пожалуйста, укажите валюту после команды /rate")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

bot.polling()