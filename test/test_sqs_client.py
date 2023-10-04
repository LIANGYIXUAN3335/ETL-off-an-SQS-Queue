import unittest
from unittest.mock import patch, Mock
from src.sqs_client import receive_messages_from_sqs, delete_processed_message

class TestSQSClient(unittest.TestCase):

    @patch('src.sqs_client.boto3.client')
    def test_receive_messages_from_sqs(self, mock_boto3_client):
        # Mock the boto3 SQS client and its methods
        mock_sqs = Mock()
        mock_boto3_client.return_value = mock_sqs
        mock_sqs.receive_message.return_value = {
            'Messages': [{'Body': 'some_message_content'}]
        }

        queue_url = "mock_url"
        
        # Call the function being tested
        messages = receive_messages_from_sqs(mock_sqs, queue_url)

        # Assertions
        self.assertEqual(len(messages), 1)
        mock_sqs.receive_message.assert_called_once_with(QueueUrl=queue_url, MaxNumberOfMessages=1)

    @patch('src.sqs_client.boto3.client')
    def test_delete_processed_message(self, mock_boto3_client):
        # Mock the boto3 SQS client
        mock_sqs = Mock()
        mock_boto3_client.return_value = mock_sqs

        queue_url = "mock_url"
        receipt_handle = "mock_receipt_handle"

        # Call the function being tested
        delete_processed_message(mock_sqs, queue_url, receipt_handle)

        # Assertions
        mock_sqs.delete_message.assert_called_once_with(QueueUrl=queue_url, ReceiptHandle=receipt_handle)

if __name__ == '__main__':
    unittest.main()
