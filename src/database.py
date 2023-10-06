import psycopg2
import logging
from psycopg2 import pool
from . import credentials
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
db_pool = None  
def init_db_pool(db_params, minconn=1, maxconn=10):
    global db_pool
    db_pool = pool.SimpleConnectionPool(minconn, maxconn, **db_params)
def get_conn_from_pool():
    return db_pool.getconn()

def release_conn_to_pool(conn):
    db_pool.putconn(conn)
def connect_db():
    return get_conn_from_pool()
def create_table_if_not_exists(conn):
    try:
        conn.cursor().execute(
            """
            CREATE TABLE IF NOT EXISTS user_logins (
                user_id VARCHAR(128),
                device_type VARCHAR(32),
                masked_ip VARCHAR(256),
                masked_device_id VARCHAR(256),
                locale VARCHAR(32),
                app_version INTEGER,
                create_date DATE
            );
            """
        )
        conn.commit()  # Commit the transaction
    except Exception as e:
        logging.error(f"An error occurred while creating the database: {str(e)}")
        raise  # Re-raise the exception

def insert_records(conn, records):
    try:
        conn.cursor().executemany(
            """
            INSERT INTO user_logins (
                user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date
            ) VALUES (%s, %s, %s, %s, %s, %s, current_date);
            """,
            records
        )
        conn.commit()  # Commit the transaction
    except Exception as e:
        logging.error(f"An error occurred while inserting data: {str(e)}")
        raise  # Re-raise the exception
def close_db_pool():
    db_pool.closeall()
