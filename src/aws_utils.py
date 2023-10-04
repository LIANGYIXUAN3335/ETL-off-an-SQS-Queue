import boto3

def get_sqs_client(endpoint_url, region, aws_access_key_id, aws_secret_access_key):
    return boto3.client(
        'sqs',
        endpoint_url=endpoint_url,
        region_name=region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )