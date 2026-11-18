import logging
import os
import boto3


logger = logging.getLogger(__name__)


def load_to_s3(data_dir:str, AWS_ACCESS_KEY:str, AWS_SECRET_KEY:str, AWS_BUCKET:str):
    """loads extracted json files into s3

    Args:
        data_dir (str): directory as to where the json files are
        AWS_ACCESS_KEY (str): reference .env file value
        AWS_SECRET_KEY (str): reference .env file value
        AWS_BUCKET (str): reference .env file value

    """

    file_names = os.listdir(data_dir)

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
    else:
        logger.info(f'{file_names} is in the data folder and should have been deleted in the previous step, recommended to manually delete to reduce risk of it being uploaded to s3')