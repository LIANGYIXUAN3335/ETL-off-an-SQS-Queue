import json
from . import database
from . import maskpii
import logging
def process_message(message):
    """
    Process an individual message from SQS, filter it, and then mask its data.
    """
    logging.info(f"Starting to process message with ID: {message.get('MessageId')}.")

    try:
        masked_data = maskpii.mask_data(json.loads(message['Body']))
        processed_message = {
            'user_id': masked_data['user_id'],
            'device_type': masked_data['device_type'],
            'ip': masked_data['ip'],
            'device_id': masked_data['device_id'],
            'locale': masked_data['locale'],
            'app_version': int(''.join([f"{int(segment):03}" for segment in masked_data['app_version'].split('.')]))
        }
        return processed_message
    except Exception as e:
        logging.error(f"Error while processing message with ID: {message.get('MessageId')}. Error: {str(e)}")
        return None

def write_message_to_postgres(masked_messages, conn):
    """
    Write the processed message to the PostgreSQL database.

    Args:
        masked_message (dict): The processed (masked) message.
        cur (cursor): The PostgreSQL cursor.
    """
    database.insert_records(conn, _convert_records_to_tuples(masked_messages))

def process_and_store_messages(messages, conn):
    """Process messages from SQS and insert into the database."""
    logging.info(f"Received {len(messages)} messages to process.")
    process_messages = []
    for message in messages:
        process_messages.append(process_message(message))
    if process_messages:
        logging.info(f"Processing : {len(process_messages)} messages")
        write_message_to_postgres(process_messages, conn)
    else:
        logging.warning(f"Message was filtered out or failed processing.")

    logging.info("Finished processing all messages.")
    conn.commit()



def _convert_records_to_tuples(records):
    """Convert record dictionaries to tuples for database insertion."""
    return [
        (
            record['user_id'], record['device_type'], record['ip'],
            record['device_id'], record['locale'], record['app_version']
        )
        for record in records
    ]
