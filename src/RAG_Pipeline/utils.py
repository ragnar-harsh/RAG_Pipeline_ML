import os
import sys
import pickle

import numpy as np

from dotenv import load_dotenv

from src.RAG_Pipeline.exception import CustomException
from src.RAG_Pipeline.logger import logging


load_dotenv()

host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
user = os.getenv('DB_USERNAME')
passwd = os.getenv('DB_PASSWORD')
db = os.getenv('DB_DATABASE')




def save_object(file_path, obj):
    '''
        Export Object with Pickle (Serialization)
    '''

    try:
        # pass
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)
        logging.info(f"Exporting Object to ===>> {dir_path}")

        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)


    except Exception as e:
        raise CustomException(e, sys)
