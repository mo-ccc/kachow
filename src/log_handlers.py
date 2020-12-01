import os
import logging
import datetime

log_directory = os.path.join(os.getcwd(), 'log')

if not os.path.exists(log_dir):
    os.mkdir(log_dir)
    
now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")

file_handler = logging.handlers.TimedRotatingFileHandler(
    filename=os.path.join(log_directory, date),
    when='midnight'
)
file_handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)


