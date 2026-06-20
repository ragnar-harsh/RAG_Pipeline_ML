import sys
from src.RAG_Pipeline.logger import logging

def error_message_details(error, err_details: sys):
    _, _, exc_tb = err_details.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(file_name, exc_tb.tb_lineno, str(error))
    logging.error(error_message)
    return error_message


class CustomException(Exception):
    # def __init__(self, *args):
    #     super().__init__(args[0])
    #     self.error_message = error_message_details(args[0], args[1])
    def __init__(self, err_message, err_details):
        super().__init__(err_message)
        self.error_message = error_message_details(err_message, err_details)
    
    def __name__(self):
        return self.error_message

