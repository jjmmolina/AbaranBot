import logging
import emoji
import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram.utils.promise import logger

# from config.authentication import API_TOKEN
from instance.config import API_TOKEN
from utils.weather import Weather, Forecast
from urllib.request import urlopen

#https://github.com/python-telegram-bot/python-telegram-bot/wiki/Transition-guide-to-Version-12.0
#https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot


# Info para bots en Slack https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
# https://github.com/slackapi/Slack-Python-Onboarding-Tutorial
# http://python-slackclient.readthedocs.io/en/latest/
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Code-snippets


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update: Update, context: CallbackContext):
    keyboard = [
                [InlineKeyboardButton("Feliz", callback_data='1'),
                 InlineKeyboardButton("Whatever", callback_data='2')],
                [InlineKeyboardButton("Triste", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Hey there! Bienvenido al primer Abaran Bot')
    update.message.reply_text('¿Cómo te sientes hoy?', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query
    if query.data == "1":
        em = emoji.emojize(':smile:', use_aliases=True)
        context.bot.editMessageText(text="Oh wow! %s " % em,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)

    if query.data == "2":
        em = emoji.emojize(':expressionless:', use_aliases=True)
        context.bot.editMessageText(text="¿Qué te ocurre? %s " % em,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)

    if query.data == "3":
        em = emoji.emojize(':disappointed:', use_aliases=True)
        context.bot.editMessageText(text="Oh man! %s " % em,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)


def weatherCity(city_name):
    city = Weather(city_name)
    return ("Weather |"+ city.name+"-"+ city.country+ " at "+
                datetime.datetime.fromtimestamp(int(city.dt)).strftime('%H:%M:%S %m-%d-%Y ')
                + " Temp: "+ str(city.temp) + " Celsius"
                + " Temp(min,max):("+ str(city.temp_min)+ ","+ str(city.temp_max)+") Celsius"
                + " Pressure: "+str(city.pressure)+" hPa"
                + " Humidity: " +str(city.humidity)#+#city.sky+
                + " Clouds: "+str(city.cloud)
                + " Wind speed: "+str(city.wind)
                + " mps: "+str(datetime.datetime.fromtimestamp(int(city.dt)).strftime('%H:%M:%S %m-%d-%Y ')))

def forecastCity(city_name):
    city = Forecast(city_name)
    return ("Forecast |"+ city.name+"-"+" at "+ city.dt
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


def help(update, context):
    update.message.reply_text("Use /start to test this bot.")
    update.message.reply_text("Use /weather City to obtain weather in the City that you want")
    update.message.reply_text("Use /forecast City to obtain forecast in the next 3 hours for the City that you want")


def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def getWeather(update, context):
    #em = emoji.emojize(':smile:', use_aliases=True)
    print("Weather in "+str(context.args[0]))
    eltiempo = weatherCity(str(context.args[0]))
    context.bot.send_message(chat_id=update.message.chat_id, text=eltiempo)
    print(eltiempo)

def getForecast(update, context):
    # em = emoji.emojize(':smile:', use_aliases=True)
    print("Forecast for the next hours in " + str(context.args[0]))
    eltiempo = forecastCity(str(context.args[0]))
    context.bot.send_message(chat_id=update.message.chat_id, text=eltiempo)
    print(eltiempo)

# Create the Updater and pass it your bot's token.
updater = Updater(API_TOKEN, use_context=True)
ud = updater.dispatcher

ud.add_handler(CommandHandler('start', start))
ud.add_handler(CommandHandler('weather', getWeather, pass_args=True))
ud.add_handler(CommandHandler('forecast', getForecast, pass_args=True))
ud.add_handler(CallbackQueryHandler(button))
ud.add_handler(CommandHandler('help', help))
ud.add_error_handler(error_callback)

# Start the Bot
updater.start_polling()

# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT
updater.idle()


