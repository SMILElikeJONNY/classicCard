import os
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import schedule
import time
import json



import config.general as generalConfig
import config.texts as text

TOKEN = generalConfig.token


#initilize the conection to telegram
def initBot():
    global bot
    global updater
    global dispatcher

    bot = telegram.Bot(token=TOKEN)

    updater = Updater(bot=bot)
    dispatcher =  updater.dispatcher

    initHandler()

    #start the bot
    updater.start_polling()


def initHandler():
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text, echo)
    adress_handler = CommandHandler('adress',sendAdress)

    dispatcher.add_handler(adress_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(start_handler)


#Function if a user send a request
def start(bot,update):
    messageId = update.message.chat_id
    if(messageId not in users):
        users.append(messageId)
        writeUser(messageId)
        bot.send_message(chat_id=messageId, text= text.willkommen)
        #sendEventsToUser()
    else:
        print('User already registered!')

def echo(bot,update):
    bot.send_message(chat_id=update.message.chat_id,text="Ich bin gerade noch in der Entwicklung. Vielleicht kann ich dir später antworten. ")

def sendAdress(bot,update):
    bot.send_message(chat_id=update.message.chat_id,text="Adresse")



def readInUser():
    with open(generalConfig.userFile) as f:
        global users
        users = [int(x) for x in f]
        f.close()

    print(users)

def writeUser(user):
    file = open(generalConfig.userFile, 'a')
    file.writelines('\n' + str(user))
    file.close()

def readEvents():
    with open(generalConfig.eventsWeekFile) as f:
        events = f.read()
        f.close()
    return json.loads(events)['events']

#Event Handling
def sendEventsToUser():
    print('start Crawling')
    os.system('scrapy runspider classicCardCrawler.py --nolog')
    events = readEvents()
    eventsString = '\n\n'.join(events)
    for user in users:
        bot.send_message(chat_id=str(user),text=eventsString)

def initTimeSchedeling():
    schedule.every().sunday.at("18:00").do(sendEventsToUser)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    initBot()
    readInUser()
    initTimeSchedeling()
