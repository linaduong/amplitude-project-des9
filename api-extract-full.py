import os
import json
import gzip
import time
import logging
import tempfile
import shutil
import zipfile
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
log_filename = f'{log_dir}/{yesterday_format}.log'

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

#------------------------------------------------------------------------

zip_data_dir = 'data_zip'

# Create a temporary directory for extraction
temp_dir = tempfile.mkdtemp()

# Create local output directory
os.makedirs(zip_data_dir, exist_ok=True)
logger.info("Environment Setup: beginning unzip process")

#gets the file path for the data folder
data_path = os.path.abspath('c:data')

#gets the name of zips within the folder
zf_names = os.listdir(data_path)
print(zf_names)

#does a loop to get the path names to the zip files
for zf_path_loop in zf_names:
    zf_path = (f'{data_path}\\{zf_path_loop}')
    print(zf_path)

    try:
        # Extract the main zip file into the temporary directory
        with zipfile.ZipFile(zf_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)
            logger.info(f"amp_events.zip extracted to temp directory: {temp_dir} ")
    except Exception as e:
        logger.error(f"Error extracting zip file: {str(e)}")
        raise

    try:
        # Locate the day folder (assumed to be the numeric folder)
        day_folder = next(f for f in os.listdir(temp_dir) if f.isdigit())
        day_path = os.path.join(temp_dir, day_folder)
    except Exception as e:
        logger.error(f"Error finding day folder: {str(e)}")
        raise

    # Walk through the day folder and decompress each .gz file to the data directory
    for root, _, files in os.walk(day_path):
        for file in files:
            if file.endswith('.gz'):
                try:
                    gz_path = os.path.join(root, file)
                    json_filename = file[:-3]  # Remove .gz extension
                    output_path = os.path.join(zip_data_dir, json_filename)

                    with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'wb') as out_file:
                        shutil.copyfileobj(gz_file, out_file)
                    
                    logger.info(f"Successfully processed: {file} -> {json_filename}")
                except Exception as e:
                    logger.error(f"Failed to process file {file}: {str(e)}")

    try:
        # Delete the temporary directory
        shutil.rmtree(temp_dir)
        logger.info("Temp directory deleted")

    except Exception as e:
        logger.error(f"Failed to delete temp directory: {str(e)}")

print("All files extracted to the 'data' directory!")


