import unittest
import sys
import os
import json
from unittest.mock import patch, Mock
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.message_processing import _filter_messages, _convert_records_to_tuples, process_and_store_messages
from src.sqs_client import receive_messages_from_sqs, delete_processed_message

class TestMessageProcessing(unittest.TestCase):

    def test_filter_messages_valid(self):
        message = {'msg_type': 'login'}
        self.assertTrue(_filter_messages(message))

    def test_filter_messages_invalid(self):
        message = {'msg_type': 'register'}
        self.assertFalse(_filter_messages(message))

    def test_convert_records_to_tuples(self):
        records = [{
            'user_id': 'user123',
            'device_type': 'iPhone',
            'ip': 'masked_ip',
            'device_id': 'masked_device_id',
            'locale': 'en_US',
            'app_version': 1
        }]
        expected = [
            ('user123', 'iPhone', 'masked_ip', 'masked_device_id', 'en_US', 1, None)
        ]
        self.assertEqual(_convert_records_to_tuples(records), expected)

    @patch('src.message_processing._filter_messages')
    @patch('src.message_processing.maskpii')
    @patch('src.message_processing.database.insert_records')
    def test_process_and_store_messages(self, mock_insert, mock_mask, mock_filter):
        mock_messages = [{
            'Body': json.dumps({
                'msg_type': 'login',
                'user_id': 'user1',
                'device_type': 'iPhone',
                'ip': '127.0.0.1',
                'device_id': 'device123',
                'locale': 'en_US',
                'app_version': '1.0.0'
            }),
            'ReceiptHandle': 'receipt_handle'
        }]

        mock_filter.return_value = True
        mock_mask.mask_data.return_value = {
            'user_id': 'user1',
            'device_type': 'iPhone',
            'ip': 'masked_ip',
            'device_id': 'masked_device_id',
            'locale': 'en_US',
            'app_version': 1
        }

        mock_cur = Mock()
        mock_sqs = Mock()
        mock_queue_url = "mock_url"

        process_and_store_messages(mock_messages, mock_cur, mock_sqs, mock_queue_url)

        mock_filter.assert_called_once()
        mock_mask.mask_data.assert_called_once()
        mock_insert.assert_called_once()

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
        mock_sqs.receive_message.assert_called_once()

    @patch('src.sqs_client.boto3.client')
    def test_delete_processed_message(self, mock_boto3_client):
        mock_sqs = Mock()
        mock_boto3_client.return_value = mock_sqs

        queue_url = "mock_url"
        receipt_handle = "mock_receipt_handle"

        delete_processed_message(mock_sqs, queue_url, receipt_handle)
        mock_sqs.delete_message.assert_called_once_with(QueueUrl=queue_url, ReceiptHandle=receipt_handle)

if __name__ == '__main__':
    unittest.main()
