import hashlib

def hash_data(data):
    """
    Hash the provided data using SHA256 for masking.

    :param data: Original string data to be hashed.
    :return: Hashed string.
    """
    hashed_data = hashlib.sha256(data.encode()).hexdigest()
    return hashed_data

def mask_data(data):
    """
    Hash the 'ip' and 'device_id' fields in the data.

    :param data: Dictionary containing user data.
    :return: Data with hashed 'ip' and 'device_id' fields.
    """
    data['ip'] = hash_data(data['ip'])
    data['device_id'] = hash_data(data['device_id'])
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
