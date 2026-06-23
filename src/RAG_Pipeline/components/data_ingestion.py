import os
import sys
from dataclasses import dataclass
from collections import Counter

from src.RAG_Pipeline.exception import CustomException
from src.RAG_Pipeline.logger import logging


# import pandas as pd


from unstructured.partition.pdf import partition_pdf


@dataclass
class DataIngestionConfig:
    pass


class DataIngestion:
    def __init__(self):
        pass
        # self.ingestion_config = DataIngestionConfig()


    def partition_document(self, file_path: str):
        """Extract elements from pdf using Unstructured"""
        try:
            # pass
            logging.info(f'Extracting elements from pdf using Unstructured - {file_path}')

            print(f"Partitioning Document {file_path}")

            elements = partition_pdf(
                filename=file_path,
                strategy="hi_res", # use the most accurate (but slower) processing method for extraction
                infer_table_structure=True, # Keep Tables as structured HTML not jumbled text
                extract_image_block_types=["Image"], # Grab Images found in the PDF
                extract_image_block_to_payload=True # Store Image as base64 data you can actually use
            )

            print(f"Extracted {len(elements)} elements")
            logging.info(f'Extracted Elements -- {len(elements)}')
            return elements


        except Exception as ex:
            logging.error(f"Error Occured while document partitioning {ex}")
            raise CustomException(ex, sys)
        
    
    def get_element_details(self, elements, idx: int):
        '''Find Element details through Index'''
        try:
            # pass
            return elements[idx].to_dict()

        except IndexError as e:
            logging.error(e)
        except Exception as e:
            raise CustomException(e, sys)



    def get_elements_metadata(self, elements):
        '''Extract the raw type names, split by 'elements.', and take the last part'''

        try:

            cleaned_types = [str(type(el)).split("elements.")[-1].replace("'>", "") for el in elements]

            # 2. Get the exact types along with their counts
            type_counts = Counter(cleaned_types)


            # First requirement: Just the unique short names (like your original set)
            unique_types = set(type_counts.keys())
            # print("Unique Types:", unique_types)

            # Second requirement: The types with their exact counts
            # print("\nType Counts:")
            # for element_type, count in type_counts.items():
            #     print(f"{element_type}: {count}")

            logging.info(type_counts)
            
            return (
                unique_types, 
                type_counts
            )
        except Exception as ex:
            logging.error(f"Error during finding Meta Data")
            raise CustomException(ex, sys)


    def gather_media_data(self, elements):
        '''Gather Images & Tables from the Elements'''

        try:
            # pass
            images = [el for el in elements if el.category == 'Image']
            tables = [el for el in elements if el.category == 'Table']

            logging.info(f"Found: {len(images)} Images")
            logging.info(f"Found: {len(tables)} Tables")

            return (
                images,
                tables
            )

        except Exception as ex:
            # logging.error(f'Error Occured during collecting Images & Tables - {ex}')
            raise CustomException(ex, sys)


