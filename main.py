'''''''''''''''''
 * Author : Mao FENG
 * Email : maofeng.fr@gmail.com
 * Last modified :	2018-09-13 19:28
 * Filename :		main.py
 * Description : the entry of the monitoring program 
'''''''''''''''''

import time
import re
import sys, getopt
from config import config
from datetime import datetime
from tools import log_reader, display_stats
import logging

logger = None

def set_root_logger(level):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger('root')
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

def usage():
    print('usage: \tpython main.py --LOG_FILE=<log-file-path> --INTERVAL_SIZE=<INTERVAL_SIZE> --WINDOW_SIZE=<WINDOW_SIZE> --ALERT_THRESHOLD=<ALERT_THRESHOLD>')
    print('\t--LOG_FILE: path to the log file, by default as /var/log/access.log')
    print('\t--INTERVAL_SIZE: a float number of seconds, monitoring script is toggled every INTERVAL_SIZE seconds, by default 10s, at least {}s'.format(config.MIN_INTERVAL_SIZE))
    print('\t--WINDOW_SIZE: an integer number of intervals, stats and alerts are generated within a window, by default 12 intervals, at least {}'.format(config.MIN_WINDOW_SIZE))
    print('\t--ALERT_THRESHOLD: an integer number requests, an alert will be generated if the average requests per sencond exceeds this threshold, by default 10 requests, at least {}'.format(config.MIN_ALERT_THRESHOLD))
    print('\t--test to enter test mode')

def initializer(argv):
    test_mode = False
    try:
        opts, args = getopt.getopt(argv, 'h', ['LOG_FILE=', 'INTERVAL_SIZE=', 'WINDOW_SIZE=', 'ALERT_THRESHOLD=', 'test', 'help', 'debug'])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
        elif o == '--test':
            test_mode = True
        elif o == '--debug':
            config.LOGGING_LEVEL = logging.DEBUG
        elif o in ('--LOG_FILE', '--INTERVAL_SIZE', '--WINDOW_SIZE', '--ALERT_THRESHOLD'):
            setattr(config, o[2:], a)
        else:
            assert False, "unhandled option"

    global logger
    logger = set_root_logger(config.LOGGING_LEVEL)
    logger.info('The monitor is configured as: ' + str(config))

    window = log_reader.read_last_window()
    logger.debug(str(window))
    display_stats.display(window.get_stats())




if __name__ == "__main__":
    initializer(sys.argv[1:]) 


