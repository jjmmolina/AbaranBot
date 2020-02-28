import logging
import emoji
import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from config.authentication import API_TOKEN
from utils.weather import weather, forecast
from urllib.request import urlopen




# Info para bots en Slack https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
# https://github.com/slackapi/Slack-Python-Onboarding-Tutorial
# http://python-slackclient.readthedocs.io/en/latest/
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(bot, update):
    keyboard = [
                [InlineKeyboardButton("Feliz", callback_data='1'),
                 InlineKeyboardButton("Whatever", callback_data='2')],
                [InlineKeyboardButton("Triste", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Hey there! Bienvenido al primer Abaran Bot')
    update.message.reply_text('¿Cómo te sientes hoy?', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query
    if query.data == "1":
        em = emoji.emojize(':smile:', use_aliases=True)
        bot.editMessageText(text="Oh wow! %s " % em,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)

    if query.data == "2":
        em = emoji.emojize(':expressionless:', use_aliases=True)
        bot.editMessageText(text="¿Qué te ocurre? %s " % em,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)

    if query.data == "3":
        em = emoji.emojize(':disappointed:', use_aliases=True)
        bot.editMessageText(text="Oh man! %s " % em,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)


def weatherCity(name):
    city = weather(name)
    eltiempo = ("Weather |"+ city.name+"-"+ city.country+ " at "+
                datetime.datetime.fromtimestamp(int(city.dt)).strftime('%H:%M:%S %m-%d-%Y ')
                + " Temp: "+ str(city.temp) + " Celsius"
                + " Temp(min,max):("+ str(city.temp_min)+ ","+ str(city.temp_max)+") Celsius"
                + " Pressure: "+str(city.pressure)+" hPa"
                + " Humidity: " +str(city.humidity)#+#city.sky+
                + " Clouds: "+str(city.cloud)
                + " Wind speed: "+str(city.wind)
                + " mps: "+str(datetime.datetime.fromtimestamp(int(city.dt)).strftime('%H:%M:%S %m-%d-%Y ')))
    return(eltiempo)

def forecastCity(name):
    city = forecast(name)
    eltiempo = ("Forecast |"+ city.name+"-"+" at "+ city.dt
                #datetime.datetime.fromtimestamp(int(city.dt)).strftime('%H:%M:%S %m-%d-%Y ')
                + " Temp: "+ str(city.temp) + " Celsius "
                + " Temp(min,max):("+ str(city.temp_min)+ ","+ str(city.temp_max)+") Celsius "
                + " Pressure: "+str(city.pressure)+" hPa "
                + " Humidity: " +str(city.humidity)#+#city.sky+
                + " Weather: " + city.main_weather + "-->" + city.weather_description
                + " Clouds: "+str(city.cloud)
                + " Wind speed: "+str(city.wind)
                + " mps: "+city.dt#str(datetime.datetime.fromtimestamp(int(city.dt)).strftime('%H:%M:%S %m-%d-%Y '))
                )
    return(eltiempo)

def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")
    update.message.reply_text("Use /weather City to obtain weather in the City that you want")
    update.message.reply_text("Use /forecast City to obtain forecast in the next 3 hours for the City that you want")


def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))


def getWeather(bot, update, args):
    #em = emoji.emojize(':smile:', use_aliases=True)
    print("Weather in "+str(args[0]))
    eltiempo = weatherCity(str(args[0]))
    bot.send_message(chat_id=update.message.chat_id, text=eltiempo)
    print(eltiempo)

def getForecast(bot, update, args):
    # em = emoji.emojize(':smile:', use_aliases=True)
    print("Forecast for the next hours in " + str(args[0]))
    eltiempo = forecastCity(str(args[0]))
    bot.send_message(chat_id=update.message.chat_id, text=eltiempo)
    print(eltiempo)

# Create the Updater and pass it your bot's token.
updater = Updater(API_TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('weather', getWeather, pass_args=True))
updater.dispatcher.add_handler(CommandHandler('forecast', getForecast, pass_args=True))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_error_handler(error)

# Start the Bot
updater.start_polling()

# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT
updater.idle()


