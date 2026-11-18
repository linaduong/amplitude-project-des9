import os
import logging
from dotenv import load_dotenv
from datetime import date, timedelta
from modules.logging_function import logging_setup
from modules.amp_extraction import extract_to_zip
from modules.zip_extraction import zip_to_json
from modules.amp_load import load_to_s3

load_dotenv()

#reading .env file for the keys
AMP_ACCESS_KEY = os.getenv('AMP_API_KEY')
AMP_SECRET_KEY = os.getenv('AMP_SECRET_KEY')
AWS_ACCESS_KEY=os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY=os.getenv('AWS_SECRET_KEY')
AWS_BUCKET=os.getenv('AWS_BUCKET')

timestamp = date.today()
url = 'https://analytics.eu.amplitude.com/api/2/export'
data_dir = 'data'
zip_dir = 'unzip'

logging_setup('logs',timestamp)

extract_to_zip(url, data_dir, AMP_ACCESS_KEY, AMP_SECRET_KEY, timestamp, day_offset=1, max_attempts=3, delay=30)

if extract_to_zip:
    zip_to_json(data_dir, zip_dir)
    if zip_to_json:
        load_to_s3(zip_dir, AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_BUCKET)
        if load_to_s3:
           print('amplitude extract->load has run successfully')
           logging.info('amplitude extract->load has run successfully')
        else:
           print('amplitude extract->load was not successful, check logs {e}')
           logging.info('amplitude extract->load was not successful, {e}')
    else:
       logging.error(f'error in extracting data from zip -> gzip -> json and therefore aborted, check logs')
else:
    logging.error(f'error in extracting data from amplitude api, no data and therefore aborted, check logs')
    
        

