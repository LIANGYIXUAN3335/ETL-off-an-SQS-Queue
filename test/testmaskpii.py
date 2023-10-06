import unittest
import os 
import sys
import base64
from Crypto.Cipher import DES
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.maskpii import hash_data, mask_data, flatten_json
from src.credentials import getDESKEY
DES_KEY = getDESKEY()

class TestMaskPii(unittest.TestCase):

    def test_pad(self):
        """Test the padding function."""
        self.assertEqual(pad('1234567'), '1234567 ')
        self.assertEqual(pad('12345678'), '12345678')  # No padding added if string is already a multiple of 8
        self.assertEqual(pad('123456789'), '123456789       ')

    def test_des_encrypt(self):
        """Test the DES encryption function."""
        data = "test_data"
        encrypted = des_encrypt(data)
        cipher = DES.new(DES_KEY, DES.MODE_ECB)
        # Decrypt and remove padding for verification
        decrypted = cipher.decrypt(base64.b64decode(encrypted)).decode('utf-8').rstrip()
        self.assertEqual(data, decrypted)

    def test_mask_data(self):
        """Test the masking function."""
        input_data = {
            'ip': '192.168.1.1',
            'device_id': 'device123',
            'other_field': 'keep_this'
        }
        masked = mask_data(input_data)
        self.assertNotEqual(masked['ip'], '192.168.1.1')
        self.assertNotEqual(masked['device_id'], 'device123')
        self.assertEqual(masked['other_field'], 'keep_this')

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
