import unittest
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.maskpii import hash_data, mask_data, flatten_json

class TestMaskPii(unittest.TestCase):
    def test_hash_data(self):
        data = "hello"
        expected = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        self.assertEqual(hash_data(data), expected)

    def test_mask_data(self):
        data = {
            'ip': '127.0.0.1',
            'device_id': 'device123'
        }
        expected = {
            'ip': hash_data('127.0.0.1'),
            'device_id': hash_data('device123')
        }
        self.assertEqual(mask_data(data), expected)

    def test_flatten_json(self):
        data = {
            'user_id': 'user1',
            'device_type': 'iPhone',
            'ip': 'masked_ip',
            'device_id': 'masked_device_id',
            'locale': 'en_US',
            'app_version': 'v1.0.0'
        }
        expected = {
            'user_id': 'user1',
            'device_type': 'iPhone',
            'masked_ip': 'masked_ip',
            'masked_device_id': 'masked_device_id',
            'locale': 'en_US',
            'app_version': 100
        }
        self.assertEqual(flatten_json(data), expected)

if __name__ == '__main__':
    unittest.main()
