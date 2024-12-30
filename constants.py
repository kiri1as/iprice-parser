import os

from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv('DB_URL')
PHONES_BASE_URL = os.getenv('RZTK_PHONES_BASE_URL')
APPLE_PRODUCER_PARAM = 'producer=apple'
APPLE_PHONES_BASE_URL = f'{PHONES_BASE_URL}/{APPLE_PRODUCER_PARAM}'