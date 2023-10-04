import json
from . import database
from . import maskpii
import logging
def process_message(message):
    """
    Process an individual message from SQS, filter it, and then mask its data.
    """
    logging.info(f"Starting to process message with ID: {message.get('MessageId')}.")

    # if not _filter_messages(message):
    #     logging.warning(f"Message with ID: {message.get('MessageId')} was filtered out.")
    #     return None

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

def _filter_messages(message):
    """Filter messages to only process 'login' type."""
    logging.info(f"Entire message: {json.dumps(message, indent=4)}")  # Log the entire message for debugging
    msg_type = message.get('msg_type')
    if msg_type != 'login':
        logging.info(f"Message with ID: {message.get('MessageId')} is of type '{msg_type}' and will be filtered out.")
        return False
    return True



def write_message_to_postgres(masked_message, conn):
    """
    Write the processed message to the PostgreSQL database.

    Args:
        masked_message (dict): The processed (masked) message.
        cur (cursor): The PostgreSQL cursor.
    """
    records = [masked_message]
    database.insert_records(conn, _convert_records_to_tuples(records))

def process_and_store_messages(messages, conn, sqs, queue_url):
    """Process messages from SQS and insert into the database."""
    logging.info(f"Received {len(messages)} messages to process.")
    
    for message in messages:
        processed_message = process_message(message)
        if processed_message:
            logging.info(f"Processing message with ID: {message['MessageId']}")
            write_message_to_postgres(processed_message, conn)
        else:
            logging.warning(f"Message with ID: {message['MessageId']} was filtered out or failed processing.")

    logging.info("Finished processing all messages.")



def _convert_records_to_tuples(records):
    """Convert record dictionaries to tuples for database insertion."""
    return [
        (
            record['user_id'], record['device_type'], record['ip'],
            record['device_id'], record['locale'], record['app_version']
        )
        for record in records
    ]
