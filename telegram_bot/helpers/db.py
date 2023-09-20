import logging
import mysql.connector as mysql_db
from telegram_bot.helpers.config import CONFIG

# get all db config form .config file
DB_HOST = CONFIG.get("database", "DB_HOST").strip('"')
DB_PORT = CONFIG.getint("database", "DB_PORT")
DB_NAME = CONFIG.get("database", "DB_NAME").strip('"')
DB_USER = CONFIG.get("database", "DB_USER").strip('"')
DB_PASSWORD = CONFIG.get("database", "DB_PASSWORD").strip('"')


def get_conn():
    try:
        connection = mysql_db.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        return connection
    except mysql_db.Error as error:
        logging.critical(f"Error occurred during connection: {error}")
        return None

DB = get_conn