import unittest
from unittest.mock import patch, Mock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.sqs_client import receive_messages_from_sqs, delete_processed_message,create_sqs_client,delete_processed_messages_batch
from src.credentials import get_aws_credentials
class TestSQSClient(unittest.TestCase):

    @patch('src.sqs_client.boto3.Session')
    def test_create_sqs_client(self, mock_session):
        mock_client = Mock()
        mock_session.return_value.client.return_value = mock_client

        endpoint_url = 'http://localhost:4566'
        region = 'us-east-1'
        endpoint_url = f'{endpoint_url}/000000000000/login-queue'
        access_key,secret_key = get_aws_credentials()

        client = create_sqs_client(endpoint_url, region, access_key, secret_key)

        mock_session.assert_called_once_with(aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        mock_session.return_value.client.assert_called_once_with('sqs', region_name=region, endpoint_url=endpoint_url)
        self.assertEqual(client, mock_client)

    @patch('src.sqs_client.boto3.client')
    def test_receive_messages_from_sqs(self, mock_boto3_client):
        mock_sqs = Mock()
        mock_boto3_client.return_value = mock_sqs
        mock_sqs.receive_message.return_value = {
            'Messages': [{'Body': 'some_message_content'}]
        }

        queue_url = "mock_url"
        messages = receive_messages_from_sqs(mock_sqs, queue_url)

        self.assertEqual(len(messages), 1)
        mock_sqs.receive_message.assert_called_once_with(QueueUrl=queue_url, MaxNumberOfMessages=10)

    @patch('src.sqs_client.boto3.client')
    def test_delete_processed_message(self, mock_boto3_client):
        mock_sqs = Mock()
        mock_boto3_client.return_value = mock_sqs

        queue_url = "mock_url"
        receipt_handle = "mock_receipt_handle"
        delete_processed_message(mock_sqs, queue_url, receipt_handle)

        mock_sqs.delete_message.assert_called_once_with(QueueUrl=queue_url, ReceiptHandle=receipt_handle)

    @patch('src.sqs_client.boto3.client')
    def test_delete_processed_messages_batch(self, mock_boto3_client):
        mock_sqs = Mock()
        mock_boto3_client.return_value = mock_sqs

        queue_url = "mock_url"
        messages = [{'ReceiptHandle': 'mock_receipt_handle_1'}, {'ReceiptHandle': 'mock_receipt_handle_2'}]
        delete_processed_messages_batch(mock_sqs, queue_url, messages)

        entries = [
            {'Id': '0', 'ReceiptHandle': 'mock_receipt_handle_1'},
            {'Id': '1', 'ReceiptHandle': 'mock_receipt_handle_2'}
        ]
        mock_sqs.delete_message_batch.assert_called_once_with(QueueUrl=queue_url, Entries=entries)

if __name__ == '__main__':
    unittest.main()