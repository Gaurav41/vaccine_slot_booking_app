import logging

logger=logging.getLogger()

logger.setLevel(logging.ERROR)

formatter = logging.Formatter("%(asctime)s:%(name)s:%(message)s")
file_handler = logging.FileHandler("error_logs.log") 
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.ERROR)

logger.addHandler(file_handler)
