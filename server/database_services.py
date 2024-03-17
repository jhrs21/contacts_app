import logging
import sqlite3

DB_FILE = 'app.db'


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def connect_to_database():
    return sqlite3.connect(DB_FILE)


def execute_query(query, params=None):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        conn.close()
        logger.info("Query executed: %s %s", query, params)
    except sqlite3.Error as e:
        logger.error("Error executing query: %s %s", query, params)
        logger.exception(e)


def fetch_all(query, params=None, set_row_factory=False):
    try:
        conn = connect_to_database()
        if set_row_factory:
            conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        logger.info("Fetch all query executed: %s %s", query, params)
        return result
    except sqlite3.Error as e:
        logger.error("Error fetching all: %s %s", query, params)
        logger.exception(e)
        return None
