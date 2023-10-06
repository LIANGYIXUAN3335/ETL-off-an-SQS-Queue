def get_aws_credentials():
    """
    Get AWS Access Key ID and Secret Access Key.

    Returns:
        tuple: A tuple containing AWS Access Key ID and Secret Access Key.
    """
    aws_access_key_id = 'test'
    aws_secret_access_key = 'test'
    return aws_access_key_id, aws_secret_access_key

def get_db_params():
    """
    Get PostgreSQL database connection parameters.

    Returns:
        dict: Dictionary containing database connection parameters.
    """
    db_params = {
        'dbname': 'postgres',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'localhost',
        'port': '5432',
    }
    return db_params
def getDESKEY():
    return  b'35870191'