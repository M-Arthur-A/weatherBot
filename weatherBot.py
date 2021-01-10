# -*- coding: utf-8 -*-
import pyowm
from pyowm.commons.enums import SubscriptionTypeEnum
import telebot

config = {
    'subscription_type': SubscriptionTypeEnum.FREE,
    'language': 'ru',
    'connection': {
        'use_ssl': True,
        'verify_ssl_certs': True,
        'use_proxy': False,
        'timeout_secs': 5
    },
    'proxies': {
        'http': 'http://user:pass@host:port',
        'https': 'socks5://user:pass@host:port'
    }
}
with open('!ADDS/req') as f:
    f = f.readlines()[0].split()
owm = pyowm.OWM(f[0], config=config)
bot = telebot.TeleBot(f[1])

@bot.message_handler(content_types=['text'])
def send_bot(message):
    mgr = owm.weather_manager()
    try:
        observation = mgr.weather_at_place(message.text)
    except:
        bot.send_message(message.chat.id, 'Такого города нет!')
        return None
    w = observation.weather
    temp = w.temperature('celsius')["temp"]
    temp = round(temp, 1)
    answer = "В городе " + message.text + " сейчас " + w.detailed_status + '.\n'
    answer += "Температура: " + str(temp) + "\n\n"

    if temp > 30:
        answer += "Жара! Не забывайте пить больше воды!"
    elif temp <= 30 and temp > 20:
        answer += "Погода что надо! Получайте удовольствие - надевайте плавки!"
    elif temp <= 20 and temp > 10:
        answer += "На улице свежо, не забудьте накинуть пальто!"
    elif temp <= 10 and temp > 0:
        answer += "Погода прохладная, не забудьте шапку!"
    elif temp <= 0 and temp > -10:
        answer += "Погода морозная. Даставайте штаны с начёсом!"
    elif temp <= -10 and temp > -20:
        answer += "На улице ппц холодрыга! Надевайте трусы с начосом!"
    elif temp <= -20 and temp > -30:
        answer += "Лютый мороз, надевайте всё, что есть!"
    else:
        answer += "Хозяин собаку на двор не выгонет, а вы куда собрались?"

    bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True)