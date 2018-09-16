'''''''''''''''''
 * Author : Mao FENG
 * Email : maofeng.fr@gmail.com
 * Last modified : 2018-09-15 19:34
 * Filename : test.py
 * Description : test the alert logic by simulating periodically a certain number of requests so that the alert message can be toggled and than recovered.
'''''''''''''''''

import logging
import time
import random
import sys
import urllib
import urllib.request
from config import config

logger = logging.getLogger('root')
sections = ['', 'ohlala', 'ohmygod', 'mondieu', 'wodemaya']

def test_alert_logic():
    logger.info('test function started, generating requests ...', color=35)
    for i in range(config.WINDOW_SIZE // 2):
        n = config.ALERT_THRESHOLD * config.INTERVAL_SIZE * 5
        simulate_requests(n) 
        logger.info('{} requests simulated'.format(n), color=35)
        time.sleep(config.INTERVAL_SIZE // 2)
    logger.info('test function sleeping ...', color=35)
    time.sleep(config.INTERVAL_SIZE * config.WINDOW_SIZE)

     

def simulate_requests(n):
    for i in range(int(n)):
        url = 'http://127.0.0.1:{}/'.format(config.SERVER_PORT) + random.choice(sections)
        try:
            response = urllib.request.urlopen(url)

        except Exception as err:
            if not isinstance(err, urllib.error.HTTPError):
                logger.error('can not reach {}, please check whether the server port is correct'.format(url))
                logger.error('test thread exit')
                sys.exit(2)




