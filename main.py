import os
from dotenv import load_dotenv
from datetime import date, timedelta
from modules.logging_function import logging_setup
from modules.amp_extraction import extract_to_zip

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

logging_setup('logs',timestamp)

extract_to_zip(url, data_dir, AMP_ACCESS_KEY, AMP_SECRET_KEY, timestamp, day_offset=1, max_attempts=3, delay=30)


