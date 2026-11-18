import os
import json
import logging
from datetime import date
from dotenv import load_dotenv
import boto3

load_dotenv()

#making logging directory
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
log_filename = f'{log_dir}/{date.today()}.log'

logging.basicConfig(
    filename = log_filename,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    level = logging.INFO
)

logger = logging.getLogger()
logger.info('logger was successfully initialised')

data_dir = 'data_zip'
file_names = os.listdir(data_dir)

#defining aws credentials for session
AWS_ACCESS_KEY=os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY=os.getenv('AWS_SECRET_KEY')
AWS_BUCKET=os.getenv('AWS_BUCKET')

s3_client = boto3.client(
    's3',
    aws_access_key_id = AWS_ACCESS_KEY,
    aws_secret_access_key = AWS_SECRET_KEY
)

for file in file_names:
    to_upload = f'{data_dir}/{file}'
    try:
        #function, location name, name of the file to be uploaded
        s3_client.upload_file(to_upload, AWS_BUCKET, file)
        print(f'file {file} successfully uploaded! 🥳')
        logger.info(f'file {file} successfully uploaded!')
        #removing uploaded files
        os.remove(to_upload)
        logger.info(f'file {file} was deleted locally')
    except Exception as e:
        print(f'something went wrong 🫪, error {e}')
        logger.error(f'something went wrong, error {e}')