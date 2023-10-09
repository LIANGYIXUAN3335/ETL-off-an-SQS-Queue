import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from . import credentials
from . import database
from . import message_processing
from . import sqs_client

def main_function(endpoint_url, region, db_params):
    """Main function to handle the ETL process."""
    logging.info("Starting the ETL process...")
    
    aws_access_key, aws_secret_key = credentials.get_aws_credentials()
    sqs = sqs_client.create_sqs_client(endpoint_url, region, aws_access_key, aws_secret_key)
    
    conn = None
    try:
        conn = database.connect_db()
        with conn.cursor() as cur:
            logging.info("Creating table if not exists...")
            database.create_table_if_not_exists(conn)

            logging.info("Receiving messages from SQS...")
            while True:
                messages = sqs_client.receive_messages_from_sqs(sqs, queue_url)
                if not messages:
                    logging.warning("No messages received from SQS.")
                    break
                else:
                    logging.info(f"Received {len(messages)} messages from SQS. Processing...")
                    message_processing.process_and_store_messages(messages, conn)
                    logging.info("Messages processed and saved to database.")
                    try:
                        sqs_client.delete_processed_messages_batch(sqs, queue_url, messages)
                        logging.info(f"Deleted message with length: {len(messages)} from SQS.")
                    except Exception as e:
                        logging.error(f"Error while deleting message with length: {len(messages)} from SQS. Error: {str(e)}")     
    except Exception as e:
        logging.error(f"E: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    endpoint_url = 'http://localhost:4566'
    region = 'us-east-1'
    queue_url = f'{endpoint_url}/000000000000/login-queue'
    db_params = credentials.get_db_params()
    database.init_db_pool(db_params)
    
    try:
        main_function(endpoint_url, region, db_params)
    except Exception as e:
        logging.error(f"An error occurred in the main function: {str(e)}")
