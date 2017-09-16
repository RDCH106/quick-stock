# -*- coding: utf-8 -*-

"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from quickstock import quickStock, common

# Quick Stock logic class
qs = quickStock.QuickStock()

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
#def start(bot, update):
    #update.message.reply_text('Hi!')
    #update.message.reply_text(
    #    'Hi {}!'.format(update.message.from_user.first_name))


def help(bot, update):
    update.message.reply_text('Help!')


def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    qs.logger.warn('Update "%s" caused error "%s"' % (update, error))


def newStock(bot, update):
    qs.addStock(update.message.text.split(" ", 1)[1], update.message.chat_id)
    update.message.reply_text("'%s' created!" % (update.message.text.split(" ", 1)[1]))
    #update.message.reply_text(qs.getAllStocks()[0].name)
    #update.message.reply_text('newStock')

def stocks(bot, update):
    stocks = qs.getChatStocks(update.message.chat_id)
    update.message.reply_text(common.stringifySotckToList(stocks))

def updateStock(bot, update):
    stocks = qs.getChatStocks(update.message.chat_id)
    if common.validID(update.message.text.split(" ", 2)[1], stocks):
        qs.updateStock(update.message.text.split(" ", 2)[1], update.message.text.split(" ", 2)[2])
        update.message.reply_text("'%s' updated!" % (update.message.text.split(" ", 2)[2]))
    else:
        update.message.reply_text("ID '%s' invalid!" % (update.message.text.split(" ", 1)[1]))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(qs.config["bot"]["token"])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    #dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("newStock", newStock))
    dp.add_handler(CommandHandler("stocks", stocks))
    dp.add_handler(CommandHandler("updateStock", updateStock))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()