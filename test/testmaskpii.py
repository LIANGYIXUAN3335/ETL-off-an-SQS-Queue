import unittest
import os 
import sys
import base64
from Crypto.Cipher import DES
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src import maskpii
from src.credentials import getDESKEY
DES_KEY = getDESKEY()

class TestMaskingFunctions(unittest.TestCase):
    
    def test_des_encrypt(self):
        original_data = "127.0.0.1"
        encrypted_data = maskpii.des_encrypt(original_data)
        self.assertNotEqual(original_data, encrypted_data)
    
    def test_mask_data(self):
        original_data = {
            'user_id': 'test_user',
            'device_type': 'test_device',
            'ip': '127.0.0.1',
            'device_id': 'test_device_id',
            'locale': 'en_US',
            'app_version': '1.0.0'
        }
        masked_data = maskpii.mask_data(original_data.copy())
        self.assertNotEqual(original_data['ip'], masked_data['ip'])
        self.assertNotEqual(original_data['device_id'], masked_data['device_id'])

    def test_flatten_json(self):
        original_data = {
            'user_id': 'test_user',
            'device_type': 'test_device',
            'ip': '127.0.0.1',
            'device_id': 'test_device_id',
            'locale': 'en_US',
            'app_version': '1.0.0'
        }
        flattened_data = maskpii.flatten_json(original_data)
        self.assertIn('masked_ip', flattened_data)
        self.assertIn('masked_device_id', flattened_data)
        self.assertEqual(flattened_data['app_version'], 100)
if __name__ == '__main__':
    unittest.main()