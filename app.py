#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import database
import executer

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


class Snippyt:
    def __init__(self, token):
        self.updater = Updater(token, use_context=True)
        self.db = database.Storage('db.sqlite')
        self.sessions = {}

    def start(self, update, context):
        update.message.reply_text('Hi! Please send me some Python code.')

    def help(self, update, context):
        """Send a message when the command /help is issued"""
        update.message.reply_text('Help! Please send me more Python code.')

    def execute(self, update, context):
        """Execute user input"""
        try:
            username = str(update.message.from_user.username)
            # Get Python session from DB or create new
            if username in self.sessions:
                pysess = self.db.get_session(username, self.sessions[username])
                session_id = self.sessions[username]
                logger.info('{}: got session #{}'.format(username, session_id))
            else:
                pysess = ''
                session_id = None
                logger.info('{}: init new session'.format(username))
            # Execute Python code
            text = update.message.text
            result, pysess = executer.execute_snippet(text, pysess)
            logger.info(
                '{}: [In]:"{}"\t->\t[Out]:"{}"'.format(username, text, result)
            )
            # Store result
            session_id = self.db.store_session(username, session_id, pysess)
            logger.info('{}: stored session {}'.format(username, session_id))
            self.sessions[username] = session_id
        except BaseException as e:
            # anything could happen inside, even `exit()` call
            result = str(e)
            logger.warning(
                '{}: {} -- {}'.format(username, update.message.text, result)
            )
        if result:
            update.message.reply_text(result)

    def error(self, update, context):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    def main(self):
        """Start the bot."""
        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", self.start))
        dispatcher.add_handler(CommandHandler("help", self.help))
        dispatcher.add_handler(MessageHandler(Filters.text, self.execute))

        dispatcher.add_error_handler(self.error)

        self.updater.start_polling()

        self.updater.idle()


if __name__ == '__main__':
    with open('telegram.token') as token_file:
        token = token_file.read()
    app = Snippyt(token)
    app.main()
