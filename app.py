#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot                          # Bot API Library
from telebot import types               # Bot types API library
import time                             # Library for the time
import feedparser                       # Imports the feed reader
import threading                        # Library for the counter
import sys                              # Import system libraries
from string import digits, maketrans    # Import numbers function
from config import *                    # Imports the config file


###################################################################   INIT


# Make the bot
bot = telebot.TeleBot(API_TOKEN)


# Encode
reload(sys)
sys.setdefaultencoding('utf-8')


###################################################################   FUNCTIONS


# Listener
def listener(messages):
    for m in messages:
        cid = m.chat.id
        uid = m.from_user.id
        mid = m.message_id
        if m.content_type == 'text':
            if cid > 0:
                user_message = "Private Message - ID: " + str(mid) + "\n\"" + str(m.from_user.first_name) + " " + str(m.from_user.last_name) + "\" [" + str(uid) + "] \nExecuted Command: " + str(m.text) + "\n"
            else:
                user_message = "Group Messsage - ID: " + str(mid) + "\n\"" + str(m.from_user.first_name) + " " + str(m.from_user.last_name) + "\" [" + str(uid) + "] - Chat ID: " + str(cid) + "\nExecuted Command: " + str(m.text) + "\n"
            f = open('log.txt', 'a')
            f.write(user_message + "\n")
            f.close()
            print(user_message)
bot.set_update_listener(listener)

# Has Numbers Checker
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

# Update to get the latest topic in RSS
latest_topic_offline = 0
def update_rss():
    global latest_topic_offline
    threading.Timer(60.0, update_rss).start()
    rss_url = feedparser.parse(rss_main_feed)
    print("Aggiorno il feed RSS...")
    latest_topic_online = rss_url['entries'][0]['title']
    print(latest_topic_online)
    if str(latest_topic_online) != str(latest_topic_offline):
      print("Nuovo feed, lo invio")
      latest_topic_offline = latest_topic_online[:]
      bot.send_message(GROUP_ID, "*Nuova steam key:*"+ "\n" +
      "_Il gioco il questione è:_ " + "\n" + rss_url['entries'][0]['title'].replace("_", "\_") + "\n" +
      "_Link alla key:_" + "\n" + rss_url['entries'][0]['link'] + "\n",
      parse_mode="markdown")
update_rss()


###################################################################   MAIN COMMANDS


# Handle /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, """\
Salve o viandante,io sono il bot ufficiale per i post di SteamGamersInside.
Probabilmente non dovresti essere qui.
""", parse_mode="markdown")

# Handle /ping
@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message, "*pong*", parse_mode="markdown")

# Handle /help
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, """
*Salve o viandante*
Io sono il bot ufficiale per i post di SteamGamersInside. Probabilmente non dovresti essere qui, ma lascia che ti spieghi come funziono

*Lista dei comandi:*

  /start - _Mi avvia_
  /help - _Mostra l'help, ovvero questo messaggio_
  /ping - _Verifica che il bot stia funzionando_

Per qualsiasi domanda, sentiti libero di contattare *Il mio creatore*: """ + ADMIN_NAME + " " + ADMIN_NICKAME, parse_mode="markdown")



###################################################################   MANAGER

# Start the bot
print("Bot ON\n")
bot.polling()

# Close the bot
print("Bot OFF")
#db.close()
