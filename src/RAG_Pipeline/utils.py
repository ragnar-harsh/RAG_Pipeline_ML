import os
import sys
import pickle

import numpy as np
import json
from pathlib import Path
from typing import List, Any

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





def export_list_to_artifact(project_name: str, unique_file_id: str, data_list: List[Any]) -> str:
    """
    Exports a list of items to a JSON file under /artifacts/{project_name}/{unique_file_id}.
    Creates the directory path if it does not exist.
    
    :param project_name: Name of the project (used for folder naming)
    :param unique_file_id: Unique identifier for the file (e.g., 'users_v1.json' or 'run_42')
    :param data_list: The list of items to save
    :return: The string path of the saved file
    """

    logging.info(f"Exporting to File - {unique_file_id}")
    try:

        # Ensure the file has a .json extension if not already provided
        if not unique_file_id.endswith('.json'):
            unique_file_id += '.json'
            
        # Define the target directory and file path
        # (Using Path.cwd() / 'artifacts' for local safety, or change to Path('/artifacts') if absolute root is required)
        target_dir = Path.cwd() / 'artifacts' / project_name
        # target_dir = Path("./artifacts") / project_name
        file_path = target_dir / unique_file_id
        
        # Create directory and any missing parent directories safely (parents=True, exist_ok=True)
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Write the list to the filecls
        with open(file_path, 'w', encoding='utf-8') as f:
            # json.dump(data_list, f, ensure_ascii=False, indent=4)
            json.dump(data_list, f, ensure_ascii=False, indent=4, default=str)
            
        logging.info(f"Successfully exported data to: {file_path}")
        return str(file_path)
    
    except Exception as e:
        raise CustomException(e, sys)


def import_list_from_artifact(project_name: str, unique_file_id: str) -> List[Any]:
    """
    Reads a JSON file from /artifacts/{project_name}/{unique_file_id} and converts it back to a list.
    
    :param project_name: Name of the project
    :param unique_file_id: Unique identifier for the file
    :return: The original list of items
    """

    logging.info(f"Importing from File - {unique_file_id}")

    try:

        if not unique_file_id.endswith('.json'):
            unique_file_id += '.json'
            
        # file_path = Path("./artifacts") / project_name / unique_file_id
        file_path = Path.cwd() / 'artifacts' / project_name
        
        # Check if file exists before trying to read it
        if not file_path.exists():
            logging.error(f"No artifact found at {file_path}")
            raise FileNotFoundError(f"No artifact found at {file_path}")
            
        with open(file_path, 'r', encoding='utf-8') as f:
            data_list = json.load(f)
            
        if not isinstance(data_list, list):
            logging.error(f"The data inside {unique_file_id} is not a list object.")
            raise TypeError(f"The data inside {unique_file_id} is not a list object.")
        
        logging.info(f"Successfully imported data from: {file_path}")
            
        return data_list

    except Exception as e:
        raise CustomException(e, sys)