import datetime
import logging
import os
import re
from logging.handlers import TimedRotatingFileHandler
import sys

FORMATTER = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s")

date = datetime.date.today().strftime('%Y%m%d')

FIRST = True
dirname = os.path.dirname(__file__)

cnt_of_req = 0

dirname = os.path.join(dirname, 'logs')

if not os.path.exists(dirname):
    os.mkdir(dirname)

LOG_FILE = os.path.join(dirname, 'my_app.'+date+'.log')


def getFirst():
    global FIRST
    return FIRST
def setFirst(state):
    global FIRST
    FIRST = state
def getDate():
    global date
    return date

def namer(name):

    a = name[-28:][-8:]
    date = datetime.datetime.strptime(a, '%Y%m%d').date()
    date = date + datetime.timedelta(days=1)
    str_date = datetime.datetime.strftime(date, '%Y%m%d')
    name = name.replace('.'+getDate()+'.log', '') + '.log'
    return name.replace(a, str_date)


def get_console_handler():
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setFormatter(FORMATTER)
   return console_handler
def get_file_handler():
   file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight', backupCount=10, encoding='utf-8')
   file_handler.suffix = '%Y%m%d'
   file_handler.namer =namer
   file_handler.extMatch = re.compile(r"^\d{8}$")


   file_handler.setFormatter(FORMATTER)
   return file_handler
def get_logger(logger_name):
   logger = logging.getLogger(logger_name)
   logger.setLevel(logging.DEBUG)
   logger.addHandler(get_console_handler())
   logger.addHandler(get_file_handler())
   logger.propagate = False
   return logger

LOGGER = get_logger('Adil')