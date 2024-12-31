import os
import random
import string
from dotenv import load_dotenv

load_dotenv()


class StaticConfig:
    MIN_TIME_SLEEP_HANDLER_SCRAPY = int(os.getenv("MIN_TIME_SLEEP_HANDLER_SCRAPY"))
    MAX_TIME_SLEEP_HANDLER_SCRAPY = int(os.getenv("MIN_TIME_SLEEP_HANDLER_SCRAPY"))
    MEDIA_FOLDER = os.getenv("MEDIA_FOLDER", "/home/zari/PycharmProjects/new_telegram_z/media_manager/media")
    MIN_TIME_SLEEP_MESSAGE_HANDLER = int(os.getenv("MIN_TIME_SLEEP_MESSAGE_HANDLER"))
    MAX_TIME_SLEEP_MESSAGE_HANDLER = int(os.getenv("MAX_TIME_SLEEP_MESSAGE_HANDLER"))

    TELEGRAM_CLIENTS = [
        {
            "session_name": os.getenv("SESSION_NAME1"),
            "api_id": int(os.getenv("API_ID1")),
            "api_hash": os.getenv("API_HASH1"),
            "phone_number": os.getenv("PHONE_NUMBER1"),
        },
        {
            "session_name": os.getenv("SESSION_NAME2"),
            "api_id": int(os.getenv("API_ID2")),
            "api_hash": os.getenv("API_HASH2"),
            "phone_number": os.getenv("PHONE_NUMBER2"),
        },
    ]

