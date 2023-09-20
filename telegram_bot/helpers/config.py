from configparser import ConfigParser


# loading the config file and
# making it accessible by all the project
config = ConfigParser()
config.read('telegram_bot/.config')

CONFIG = config


# example usage
"""
from config import CONFIG
reading database config
CONFIG.get(sectionname(database),varname(db_password))
"""


