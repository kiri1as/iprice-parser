import logging
import os
import sys

import psycopg
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def check_db_connect(connection_url):
    try:
        with psycopg.connect(connection_url) as conn:
            with conn.cursor() as cur:
                cur.execute("select 1;")
                result = cur.fetchone()
                if result is not None:
                    raise Exception('Connection check query failed!')

    except Exception as e:
        logger.error(f'Health check failed! Database connection error: {e}')
        sys.exit(1)

    logger.info('Database connection is OK!')
    sys.exit(0)


if __name__ == '__main__':
    load_dotenv()
    check_db_connect(os.getenv('DATABASE_URL'))