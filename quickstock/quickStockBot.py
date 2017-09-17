# -*- coding: utf-8 -*-

"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
"""

import sys

if sys.version_info < (3, 0):
    # sys.setdefaultencoding() does not exist, here!
    reload(sys)  # Reload does the trick!
    sys.setdefaultencoding('utf-8')

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import quickStock, common
from help import help_info

# Quick Stock logic class
qs = quickStock.QuickStock()

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi {}!\nTake a look to /help command for more info'.format(update.message.from_user.first_name))


def help(bot, update):
    update.message.reply_text(help_info)


def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    qs.logger.warn('Update "%s" caused error "%s"' % (update, error))


# -----------------------------------------------------
# Stock functions
# -----------------------------------------------------

def newStock(bot, update):
    qs.addStock(update.message.text.split(" ", 1)[1], update.message.chat_id)
    update.message.reply_text("'%s' created!" % (update.message.text.split(" ", 1)[1]))


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


def deleteStock(bot, update):
    stocks = qs.getChatStocks(update.message.chat_id)
    if common.validID(update.message.text.split(" ", 1)[1], stocks):
        target = qs.getStock(update.message.text.split(" ", 1)[1]).name
        qs.deleteStock(update.message.text.split(" ", 1)[1])
        update.message.reply_text("'%s' deleted!" % target)
    else:
        update.message.reply_text("ID '%s' invalid!" % (update.message.text.split(" ", 1)[1]))


def newItem(bot, update):
    stocks = qs.getChatStocks(update.message.chat_id)
    if common.validID(update.message.text.split(" ", 3)[1], stocks):
        qs.addItem(update.message.text.split(" ", 3)[3], update.message.text.split(" ", 3)[2],
                   update.message.text.split(" ", 3)[1])
        update.message.reply_text("'%s' --> %s created!" % (update.message.text.split(" ", 3)[3],
                                                            update.message.text.split(" ", 3)[2]))
    else:
        update.message.reply_text("ID '%s' invalid!" % (update.message.text.split(" ", 3)[1]))


def items(bot, update):
    stocks = qs.getChatStocks(update.message.chat_id)
    if common.validID(update.message.text.split(" ", 1)[1], stocks):
        items = qs.getStockItems(update.message.text.split(" ", 1)[1])
        update.message.reply_text(common.stringifyItemToList(items))
    else:
        update.message.reply_text("ID '%s' invalid!" % (update.message.text.split(" ", 1)[1]))


def updateItem(bot, update):
    stocks = qs.getChatStocks(update.message.chat_id)
    item = qs.getItem(update.message.text.split(" ", 2)[1])
    if item is not None and common.validID(item.stock_id, stocks):
        if update.message.text.split(" ", 2)[0] == "/updateItemAmount":
            items = qs.getStockItems(update.message.text.split(" ", 1)[1])
            qs.updateItem(id_item=update.message.text.split(" ", 2)[1], amount=update.message.text.split(" ", 2)[2])
            update.message.reply_text("'%s' --> %s updated!" % (item.name,
                                                                update.message.text.split(" ", 2)[2]))
        if update.message.text.split(" ", 2)[0] == "/updateItemName":
            items = qs.getStockItems(update.message.text.split(" ", 1)[1])
            qs.updateItem(id_item=update.message.text.split(" ", 2)[1], name=update.message.text.split(" ", 2)[2])
            update.message.reply_text("'%s' --> %s updated!" % (item.name,
                                                                update.message.text.split(" ", 2)[2]))
    else:
        update.message.reply_text("ID '%s' invalid!" % (update.message.text.split(" ", 2)[1]))

def deleteItem(bot, update):
    stocks = qs.getChatStocks(update.message.chat_id)
    item = qs.getItem(update.message.text.split(" ", 1)[1])
    if item is not None and common.validID(item.stock_id, stocks):
        target = qs.getItem(update.message.text.split(" ", 1)[1]).name
        qs.deleteItem(update.message.text.split(" ", 1)[1])
        update.message.reply_text("'%s' deleted!" % target)
    else:
        update.message.reply_text("ID '%s' invalid!" % (update.message.text.split(" ", 1)[1]))


# -----------------------------------------------------


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(qs.config["bot"]["token"])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("newStock", newStock))
    dp.add_handler(CommandHandler("stocks", stocks))
    dp.add_handler(CommandHandler("updateStock", updateStock))
    dp.add_handler(CommandHandler("deleteStock", deleteStock))
    dp.add_handler(CommandHandler("newItem", newItem))
    dp.add_handler(CommandHandler("items", items))
    dp.add_handler(CommandHandler("updateItemName", updateItem))
    dp.add_handler(CommandHandler("updateItemAmount", updateItem))
    dp.add_handler(CommandHandler("deleteItem", deleteItem))

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