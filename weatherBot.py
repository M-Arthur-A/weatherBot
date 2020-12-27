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

    answer = "В городе " + message.text + " сейчас " + w.detailed_status + '.\n'
    answer += "Температура сейчас: " + str(temp) + "\n\n"

    if temp < 10:
        answer += "Сейчас холодно, одевайся максимально тепло!"
    elif temp < 20:
        answer += "Холодно, нужно одеться  теплее"
    else:
        answer += "Температура как надо!"

    bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True)
