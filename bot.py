""""Main function of the bot"""

from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import datetime, time
from database import HBDatabase,SQLITE
from requests import get, post
from linkcs import fetch_linkcs_user
from config import client_id, client_secret, scope, username, password, database_path, auth_url, linkcs_api_url, bot_token

bot = Bot(bot_token)    

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    db = HBDatabase(SQLITE, dbname=database_path)
    
    db.create_db_tables()
    updater = Updater(bot_token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("sub", sub))

    # Start the Bot
    updater.start_polling()
    updater.idle()


def sub(update: Update, _: CallbackContext):
    #format : /sub 2019zucchet
    db = HBDatabase(SQLITE, dbname=database_path)
    idChat = update.message.chat_id
    login = update.message.text.split(' ', 1)[1]

    #create the subscription
    query = "INSERT INTO subscriptions (chan_id, login) VALUES ('{}', '{}');".format(idChat,login)
    db.execute_query(query)

    #fetch the user in LinkCS
    data = fetch_linkcs_user(login)["data"]["user"]
    first_name, last_name = data['firstName'],data['lastName']
    date = data['birthDate'].split('-')
    birth_year, birth_month, birth_day = date[0],date[1],date[2]

    #add the user to the people table
    query = "INSERT INTO people (login, first_name, last_name, birth_year, birth_month, birth_day) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');".format(login, first_name, last_name, birth_year, birth_month, birth_day)
    db.execute_query(query)

    bot.sendMessage(idChat,"Subscription ajoutée, son anniversaire est le "+birth_day+"/"+birth_month)


def is_login(login):
    #check whether a login is a LinkCS login
    return 0


if __name__ == '__main__' :
    main()