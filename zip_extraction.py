import os
import json
import gzip
import time
import logging
import tempfile
import shutil
import zipfile

logger = logging.getLogger(__name__)

def zip_to_json(data_dir:str, ):

    # Create a temporary directory for extraction
    temp_dir = tempfile.mkdtemp()
    logger.info('temporary directory set up')

    #gets the file path for the data folder
    data_path = os.path.abspath(f'c:{data_dir}')

    #gets the name of zips within the folder
    zf_names = os.listdir(data_path)

    #does a loop to get the path names to the zip files
    for zf_path_loop in zf_names:
        zf_path = (f'{data_path}\\{zf_path_loop}')

        try:
            # Extract the main zip file into the temporary directory
            with zipfile.ZipFile(zf_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir)
                logger.info(f"{zf_names} extracted to temp directory: {temp_dir}")
        except Exception as e:
            logger.error(f"error extracting zip file: {str(e)}")
            raise

        try:
            # Locate the day folder (assumed to be the numeric folder)
            day_folder = next(f for f in os.listdir(temp_dir) if f.isdigit())
            day_path = os.path.join(temp_dir, day_folder)
        except Exception as e:
            logger.error(f"error finding day folder: {str(e)}")
            raise

        # Walk through the day folder and decompress each .gz file to the data directory
        for root, _, files in os.walk(day_path):
            for file in files:
                if file.endswith('.gz'):
                    try:
                        gz_path = os.path.join(root, file)
                        json_filename = file[:-3]  # Remove .gz extension
                        output_path = os.path.join(data_dir, json_filename)

                        with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'wb') as out_file:
                            shutil.copyfileobj(gz_file, out_file)
                        
                        logger.info(f"Successfully processed: {file} -> {json_filename}")
                        os.remove(filename)
                        logger.info(f'file {file} was deleted') 
                    except Exception as e:
                        logger.error(f"Failed to process file {file}: {str(e)}")

        try:
            # Delete the temporary directory
            shutil.rmtree(temp_dir)
            logger.info("Temp directory deleted")

        except Exception as e:
            logger.error(f"Failed to delete temp directory: {str(e)}")

    print("All files extracted to the 'data' directory!")
    logger.info(f'All files extracted to {data_dir}')