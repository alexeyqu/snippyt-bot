#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import executer

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('Hi! Please send me some Python code.')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help! Please send me more Python code.')


def execute(update, context):
    """Echo the user message."""
    try:
        result, new_globals = executer.execute_snippet(update.message.text, globals())
        logger.info('{} -- {} -- {}'.format(update.message.text, result, new_globals))
        globals().update(new_globals)
    except BaseException as e:
        # anything could happen inside, even `exit()` call
        result = str(e)
        logger.warning('Exception {} -- {}'.format(update.message.text, result))
    if result:
        update.message.reply_text(result)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main(token):
    """Start the bot."""
    updater = Updater(token, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, execute))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    with open('telegram.token') as token:
        main(token.read())
