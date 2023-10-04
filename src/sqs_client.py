import boto3
from botocore.exceptions import NoCredentialsError

def create_sqs_client(endpoint_url, region, aws_access_key, aws_secret_key):
    """Creates an SQS client with the provided credentials and endpoint URL."""
    session = boto3.Session(aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    return session.client('sqs', region_name=region, endpoint_url=endpoint_url)

def receive_messages_from_sqs(sqs, queue_url):
    """Receive messages from SQS queue. Currently fetches one message at a time."""
    try:
        response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)
        return response.get('Messages', [])
    except NoCredentialsError:
        print("No AWS credentials found.")
        return []

def delete_processed_message(sqs, queue_url, receipt_handle):
    """Delete the processed message from SQS to prevent reprocessing."""
    try:
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    except Exception as e:
        print(f"Error deleting message: {str(e)}")
        raise
