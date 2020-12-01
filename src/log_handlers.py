import os
import logging
import logging.handlers as handlers
import datetime

log_directory = os.path.join(os.getcwd(), 'logs')

if not os.path.exists(log_directory):
    os.mkdir(log_directory)
    
now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")

file_handler = handlers.TimedRotatingFileHandler(
    filename=os.path.join(log_directory, date),
    when='midnight'
)
file_handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)


