import os 
import sys

from src.RAG_Pipeline.exception import CustomException
from src.RAG_Pipeline.logger import logging
from src.RAG_Pipeline.utils import export_list_to_artifact
from src.RAG_Pipeline.components.data_ingestion import DataIngestion







if __name__ == "__main__":
    logging.info("---------------- Application Started -------------------")
    try:
        # pass


        file_path = "./Notebook/NIPS-2017-attention-is-all-you-need-Paper.pdf"
        project_name = "RAG_Pipeline_Project"
        file_id = "Ingestion_IG0023"

        data_ingestion = DataIngestion()

        elements = data_ingestion.partition_document(file_path)
        if len(elements) - 5 >= 0:
            print(data_ingestion.get_element_details(elements, len(elements) - 5))
        elif len(elements) >= 0:
            print(data_ingestion.get_element_details(elements, 0))

        f_path = export_list_to_artifact(project_name, file_id, elements)
        
        uni_type, t_count = data_ingestion.get_elements_metadata(elements)

        # print(t_count)
        images, table = data_ingestion.gather_media_data(elements)








        logging.info("---------------- Application Ended -------------------")


    except Exception as e:
        raise CustomException(e, sys)

