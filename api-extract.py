import os
import json
import gzip
import time
import logging
from datetime import date, timedelta
from dotenv import load_dotenv
import requests

load_dotenv()

#time stamp string of yesterday's date for file name
yesterday = date.today() - timedelta(days=1)
yesterday_format = yesterday.strftime('%Y%m%d')

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

#reading .env file for the keys
api_key = os.getenv('AMP_API_KEY')
secret_key = os.getenv('AMP_SECRET_KEY')

data_dir = 'data'

#creating directory to save zip file into
os.makedirs(data_dir, exist_ok=True)
filename = f'{data_dir}/{yesterday_format}.zip'

#url that uses yesterday's date to bring back data
url = f'https://analytics.eu.amplitude.com/api/2/export?start={yesterday_format}T00&end={yesterday_format}T23'

#setting up attempts
attempts = 1
max_attempts = 3

#status code loop
while attempts <= max_attempts:
    #the actual api call
    response = response = requests.get(url,auth=(api_key, secret_key))
    status_code = response.status_code

    if status_code == 200:
        try:
            data = response.content
            with open(filename, 'wb') as file:
                file.write(data)
            print(f'file has been successfully saved as {filename}')
            logger.info(f'file has been successfully saved as {filename}')
        except Exception as e:
            print(f'error occured when saving the zip {e}')
            logger.error(f'')
        break

    elif 300< status_code <404:
        print(f'the request either is missing parameters or the api/secret key is no longer valid, status code: {status_code} - check and try again. review documentation here: https://amplitude.com/docs/apis/analytics/export#status-codes')
        logger.error(f'the request either is missing parameters or the api/secret key is no longer valid, status code: {status_code} - check and try again.')

    elif status_code==404:
        print(f'no export files exist for the requested range, status code {status_code}. review documentation here: https://amplitude.com/docs/apis/analytics/export#status-codes')
        logger.error(f'no export files exist for the requested range, status code {status_code}.')

    elif status_code==429:
        print(f'request exceeds the rate or concurrency limit, reduce concurrency or request frequency and try again, status code: {status_code}. review documentation here: https://amplitude.com/docs/apis/analytics/export#status-codes')
        logger.error(f'request exceeds the rate or concurrency limit, reduce concurrency or request frequency and try again, status code: {status_code}.')
        
    #adding retry logic
    else:
        if attempts==max_attempts:
            print(f'max attempts reached after retrying: {status_code}. review documentation here: https://amplitude.com/docs/apis/analytics/export#status-codes')
            logger.error(f'max attempts reached after retrying: {status_code}.')
        else:
            print(f'attempt {attempts}/{max_attempts} failed, status code {status_code}, will retry')
            logger.error(f'attempt {attempts}/{max_attempts} failed, status code {status_code}, will retry')
    attempts+=1
    time.sleep(60)






