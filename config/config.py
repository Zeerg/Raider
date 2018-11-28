import logging
from os import getenv, environ

# https://raw.githubusercontent.com/errbotio/errbot/master/errbot/config-template.py

BACKEND = 'Slack' 
#.encode('unicode-escape').decode()
APP_DIR = getenv('APP_DIR')
BOT_DATA_DIR = f"{APP_DIR}/data"
BOT_EXTRA_PLUGIN_DIR = f"{APP_DIR}/plugins"

BOT_LOG_FILE = f"{APP_DIR}/errbot.log"
BOT_LOG_LEVEL = logging.getLevelName(getenv("LOG_LEVEL"))
BOT_IDENTITY = {
    'token': getenv("SLACK_API_KEY")
}

BOT_ADMINS = (getenv('BOT_ADMINS_LIST').split(','))
