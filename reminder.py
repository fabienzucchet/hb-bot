from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import datetime, time
from database import HBDatabase,SQLITE


#from database import Database
from config import bot_token, database_path

bot = Bot(bot_token)


def reminder():
    today_day = str(datetime.datetime.now().day)
    today_month = str(datetime.datetime.now().month)
    select_query='SELECT first_name,last_name,chan_id FROM people JOIN subscriptions ON people.login=subscriptions.login WHERE birth_day={} AND birth_month={};'.format(today_day,today_month)
    res = db.execute_select_query(select_query)
    for tuple in res:
        prenom,nom,idChat = tuple[0],tuple[1],tuple[2]
        bot.sendMessage(idChat, "Aujourd'hui, c'est l'anniversaire de "+prenom+" "+nom)

if __name__ == '__main__':
    
    db = HBDatabase(SQLITE, dbname=database_path)
    today_day = 19 #str(datetime.datetime.now().day)
    today_month = 5 #str(datetime.datetime.now().month)

    # Table creation
    db.create_db_tables()

    # Insert query
    # query = "INSERT INTO people (login, first_name, last_name, birth_year, birth_month, birth_day) VALUES ('2019zucchetf', 'Fabien', 'Zucchet', 1999, 5, 19);"
    # db.execute_query(query)
    # query = "INSERT INTO people (login, first_name, last_name, birth_year, birth_month, birth_day) VALUES ('2019gallieree', 'Emma', 'Galliere', 2000, 8, 5);"
    # db.execute_query(query)
    # query = "INSERT INTO subscriptions (chan_id, login) VALUES ('902516518', '2019zucchetf');"
    # db.execute_query(query)
    # query = "INSERT INTO subscriptions (chan_id, login) VALUES ('902516518', '2019gallieree');"
    # db.execute_query(query)
    reminder()