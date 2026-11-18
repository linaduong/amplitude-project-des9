import os
import json
import time
import zipfile
import logging
from datetime import date, timedelta
import requests

logger = logging.getLogger(__name__)

def extract_to_zip(api_url: str, data_dir: str, AMP_ACCESS_KEY: str, AMP_SECRET_KEY:str, timestamp: str, day_offset: int, max_attempts: int, delay: int):
    """function to call api and save files in local system as zip files

    Args:
        api_url (str): put link to where the api call should be made
        data_dir (str): put location as to where you want to save your data
        AMP_ACCESS_KEY (str): reference .env file value
        AMP_SECRET_KEY (str): reference .env file value
        timestamp (str): set anchor date
        day_offset (int): how many days back you want to call data from based on timestamp date, e.g. 1 means yesterday's data
        max_attempts (int): maximum times that the script will retry to download the data
        delay (int): set the value in seconds how long to wait between each call
    """

    #time stamp string of yesterday's date for file name
    extract_date = timestamp - timedelta(days=day_offset)
    extract_format = extract_date.strftime('%Y%m%d')

    #creating directory to save zip file into
    os.makedirs(data_dir, exist_ok=True)
    filename = f'{data_dir}/{extract_format}.zip'

    attempts = 1

    params = {
        'start': f'{extract_format}T00',
        'end': f'{extract_format}T23'
    }

    #status code loop
    while attempts <= max_attempts:
        #the actual api call
        response = requests.get(api_url, params=params, auth=(AMP_ACCESS_KEY, AMP_SECRET_KEY))
        logger.info(f'{attempts}/{max_attempts}, api has been called')
        status_code = response.status_code

        if status_code == 200:
            try:
                data = response.content
                with open(filename, 'wb') as file:
                    file.write(data)
                print(f'file has been successfully saved as {filename}')
                logger.info(f'file has been successfully saved as {filename}')
                return True
            except Exception as e:
                print(f'error occured when saving the zip {e}')
                logger.error(f'error occured when saving the zip {e}')
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
        time.sleep(delay)
    return False