import boto3
from botocore.exceptions import ClientError

def check_key_exists(bucket_name, key, aws_access_key_id, aws_secret_access_key, region_name):
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
    try:
        s3.head_object(Bucket=bucket_name, Key=key)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            # Handle other exceptions as needed
            raise

aws_access_key_id = 'AKIA6QR4X5D5UUHWU264'
aws_secret_access_key = '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'
bucket_name = 'ner-model'
model_key = 'output/model-last'
region_name = 'us-east-1'

s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

exists = check_key_exists(bucket_name, model_key, aws_access_key_id, aws_secret_access_key, region_name)
if exists:
    print(f"The key '{model_key}' exists within the bucket '{bucket_name}'.")
else:
    print(f"The key '{model_key}' does not exist within the bucket '{bucket_name}'.")

all_objects = s3.list_objects(Bucket = bucket_name) 
print(all_objects)