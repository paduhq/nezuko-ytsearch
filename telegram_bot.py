from __future__ import unicode_literals
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from time import sleep
import glob
import os
import requests
from bs4 import BeautifulSoup
import youtube_dl
import re


TOKEN = "1145995382:AAG7pDoNl2oAfkLiajJsCzyyClRg7dlB4ZA"
bot = telegram.Bot(TOKEN)

# Answering to the /start command
def start(bot, update):
    update.message.reply_text("please type /ytsearch and input a search items for YouTube videos")

# Validating the youtube URL
def youtube_url_validation(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)
    if youtube_regex_match:
        return True
    else:
        return False


# Replying with the first top 10 videos accourding to the /ytsearch keyword
def start_callback(bot, update, args):
    if len(args)==1:
        search="https://www.youtube.com/results?search_query="+args[0]
    else:
        search="https://www.youtube.com/results?search_query="+("+".join(args))
        print
    response = requests.get(search)
    page = response.text
    soup = BeautifulSoup(page,"lxml")
    links=[]
    for i in soup.find_all("a",{"aria-hidden":"true"}):
        links.append("https://www.youtube.com"+i.attrs['href'])

    for i in links[:10]:
        update.message.reply_text(i)
        sleep(1)
    update.message.reply_text("Top 10 youtube videos for the "+" ".join(args))
    update.message.reply_text("\n\nPowered by @LutfiHamka of @PaduHQ")




def main():
  # Create Updater object and attach dispatcher to it
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    print("Bot started")

# Add command handler to dispatcher

    start_handler = CommandHandler('ytsearch',start_callback, pass_args=True)
    dispatcher.add_handler(start_handler)

    start_handler = CommandHandler('start',start)
    dispatcher.add_handler(start_handler)


# Start the bot
    updater.start_polling()

# Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
