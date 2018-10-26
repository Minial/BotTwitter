#!/usr/bin/env python

import logging

from beepboop import resourcer
from beepboop import bot_manager

from bot.settings import config
from bot.slack_bot import SlackBot
from bot.slack_bot import spawn_bot

logger = logging.getLogger(__name__)


if __name__ == "__main__":

    log_level = config.log_level
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=log_level)

    slack_token = config.slack_token

    if slack_token == "":
        logging.info(
            "SLACK_TOKEN env var not set, expecting token to be provided by Resourcer events"
        )
        slack_token = None
        botManager = bot_manager.BotManager(spawn_bot)
        res = resourcer.Resourcer(botManager)
        res.start()
    else:
        # only want to run a single instance of the bot in dev mode
        bot = SlackBot(slack_token)
        bot.start({})
