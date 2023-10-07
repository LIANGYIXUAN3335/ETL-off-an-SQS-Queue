import boto3
from botocore.exceptions import NoCredentialsError
import logging
def create_sqs_client(endpoint_url, region, aws_access_key, aws_secret_key):
    """Creates an SQS client with the provided credentials and endpoint URL."""
    session = boto3.Session(aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    return session.client('sqs', region_name=region, endpoint_url=endpoint_url)

def receive_messages_from_sqs(sqs, queue_url):
    """Receive messages from SQS queue. Currently fetches one message at a time."""
    try:
        response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10)
        return response.get('Messages', [])
    except NoCredentialsError:
        logging.error("No AWS credentials found.")
        return []

def delete_processed_message(sqs, queue_url, receipt_handle):
    """Delete the processed message from SQS to prevent reprocessing."""
    try:
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    except Exception as e:
        logging.error(f"Error deleting message: {str(e)}")
        raise
def delete_processed_messages_batch(sqs, queue_url, messages):
    """
    Delete processed messages in batch from SQS to prevent reprocessing.
    :param sqs: Boto3 SQS client.
    :param queue_url: URL of the SQS queue.
    :param messages: List of messages with their receipt handles to be deleted.
    """
    try:
        entries = [{'Id': str(idx), 'ReceiptHandle': msg['ReceiptHandle']} for idx, msg in enumerate(messages)]
        response = sqs.delete_message_batch(QueueUrl=queue_url, Entries=entries)
        
        if 'Failed' in str(response):
            logging.error(f"Failed to delete message")

    except Exception as e:
        logging.error(f"Error deleting messages: {str(e)}")
        raise
