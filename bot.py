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
    dispatcher.add_handler(CommandHandler("sub_list", sub_list))
    dispatcher.add_handler(CommandHandler("unsub", unsub))

    # Start the Bot
    updater.start_polling()
    updater.idle()


def sub(update: Update, _: CallbackContext):
    #format : /sub 2019zucchet
    db = HBDatabase(SQLITE, dbname=database_path)
    idChat = update.message.chat_id
    login = update.message.text.split(' ', 1)[1]

    #check if the subscription already exists and if not, create the subscription
    select_query = "SELECT * FROM subscriptions WHERE chan_id={} AND login='{}';".format(idChat,login)
    data = db.execute_select_query(select_query)
    if data !=[]:
        bot.sendMessage(idChat,"Cette subscription existe déjà.")
        return
    else:
        query = "INSERT INTO subscriptions (chan_id, login) VALUES ('{}', '{}');".format(idChat,login)
        db.execute_query(query)

        #check if the user is already in the db
        select_query = "SELECT * FROM people WHERE login='{}';".format(login)
        data = db.execute_select_query(select_query)
        
        if data != []:
            select_query = "SELECT birth_day,birth_month FROM people WHERE login='{}';".format(login)
            data = db.execute_select_query(select_query)
            bot.sendMessage(idChat,"Subscription ajoutée, son anniversaire est le "+str(data[0][0])+"/"+str(data[0][1]))

        else :
            #fetch the user in LinkCS
            data = fetch_linkcs_user(login)
            if data == None:
                bot.sendMessage(idChat, "Mauvais format")
            else :
                first_name, last_name = data['firstName'],data['lastName']
                date = data['birthDate'].split('-')
                birth_year, birth_month, birth_day = date[0],date[1],date[2]

                #add the user to the people table
                query = "INSERT INTO people (login, first_name, last_name, birth_year, birth_month, birth_day) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');".format(login, first_name, last_name, birth_year, birth_month, birth_day)
                db.execute_query(query)
                bot.sendMessage(idChat,"Subscription ajoutée, son anniversaire est le "+birth_day+"/"+birth_month)



def sub_list(update: Update, _: CallbackContext):
    db = HBDatabase(SQLITE, dbname=database_path)
    idChat = update.message.chat_id
    select_query = "SELECT first_name,last_name,login FROM people JOIN subscriptions ON people.login=subscriptions.login WHERE chan_id={};".format(idChat)
    data = db.execute_select_query(select_query)
    sub_list = [data[i][0:3] for i in range(len(data))]
    bot.sendMessage(idChat, "Vos abonnements sont : ")
    for i in range(len(sub_list)):
        bot.sendMessage(idChat, sub_list[i][0]+' '+sub_list[i][1]+' ('+sub_list[i][2]in+')')
    

def unsub(update: Update, _: CallbackContext):
    db = HBDatabase(SQLITE, dbname=database_path)
    idChat = update.message.chat_id
    login = update.message.text.split(' ', 1)[1]
    select_query = "SELECT * FROM subscriptions WHERE chan_id={} AND login='{}';".format(idChat,login)
    data = db.execute_select_query(select_query)
    print(data)
    select_query = "DELETE FROM subscriptions WHERE chan_id='{}' AND login='{}';".format(idChat,login)
    data = db.execute_query(select_query)
    bot.sendMessage(idChat,'Subscription supprimée')

if __name__ == '__main__' :
    main()