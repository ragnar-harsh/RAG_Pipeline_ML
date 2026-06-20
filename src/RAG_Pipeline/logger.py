import os
import logging
from datetime import datetime


LOG_FILE = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"

# log_dir = os.path.join(os.getcwd(), "logs", LOG_FILE)
log_dir = os.path.join(os.getcwd(), "logs")

os.makedirs(log_dir, exist_ok=True)

LOG_FILE_PATH = os.path.join(log_dir, LOG_FILE)

# logging.basicConfig(
#     filename=LOG_FILE_PATH,
#     format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
#     level=logging.INFO
# )

# Create Logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Add Formatting
formatter = logging.Formatter(
    "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s"
)

# File Handler
file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setFormatter(formatter)

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Add Both Handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)




# def get_project_logger(project_name: str) -> logging.Logger:
#     """
#     Creates or retrieves a logger specific to a project, 
#     saving logs into a dedicated folder for that project.
#     """
#     # 1. Clean the project name to ensure it's safe for folder naming
#     project_folder_name = project_name.replace(" ", "_").lower()
    
#     # 2. Define the path: logs/project_name/DD_MM_YYYY_HH_MM_SS.log
#     LOG_FILE = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"
#     log_dir = os.path.join(os.getcwd(), "logs", project_folder_name)
#     os.makedirs(log_dir, exist_ok=True)
#     log_file_path = os.path.join(log_dir, LOG_FILE)

#     # 3. Get a unique logger instance for this project
#     logger = logging.getLogger(project_name)
#     logger.setLevel(logging.INFO)

#     # 4. Prevent duplicate handlers if the logger is fetched multiple times
#     if not logger.handlers:
#         # Create file handler
#         file_handler = logging.FileHandler(log_file_path)
#         file_handler.setLevel(logging.INFO)

#         # Create and set the format
#         formatter = logging.Formatter("[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s")
#         file_handler.setFormatter(formatter)

#         # Add the handler to the logger
#         logger.addHandler(file_handler)

#     return logger


# # User A works on Project Alpha
# logger_alpha = get_project_logger("Project Alpha")
# logger_alpha.info("User A started processing the dataset.")

# # User B works on Project Beta
# logger_beta = get_project_logger("Project Beta")
# logger_beta.info("User B generated the final report.")