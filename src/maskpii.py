import hashlib
from Crypto.Cipher import DES
import base64
from . import credentials

 # DES requires an 8-byte key
DES_KEY = credentials.getDESKEY()
def pad(data):
    """Add padding to ensure data is a multiple of 8 bytes."""
    while len(data) % 8 != 0:
        data += ' '
    return data

def des_encrypt(data):
    """
    Encrypt the provided data using DES.

    :param data: Original string data to be encrypted.
    :return: Base64 encoded encrypted string.
    """
    cipher = DES.new(DES_KEY, DES.MODE_ECB)
    encrypted_data = cipher.encrypt(pad(data).encode())
    # Return the encrypted data as a base64 encoded string to ensure it's safe for string operations/storage
    return base64.b64encode(encrypted_data).decode('utf-8')

def mask_data(data):
    """
    Encrypt the 'ip' and 'device_id' fields in the data using DES.

    :param data: Dictionary containing user data.
    :return: Data with encrypted 'ip' and 'device_id' fields.
    """
    data['ip'] = des_encrypt(data['ip'])
    data['device_id'] = des_encrypt(data['device_id'])
    return data
def flatten_json(data):
    """
    Flattens and transforms the provided data to match the database schema.

    :param data: Dictionary containing user data.
    :return: Transformed data.
    """
    return {
        'user_id': data['user_id'],
        'device_type': data['device_type'],
        'masked_ip': data['ip'],
        'masked_device_id': data['device_id'],
        'locale': data['locale'],
        'app_version': int(''.join([i for i in data['app_version'] if i.isdigit()]))  # Convert version string to integer
    }
    
