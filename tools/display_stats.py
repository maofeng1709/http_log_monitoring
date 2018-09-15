'''''''''''''''''
 * Author : Mao FENG
 * Email : maofeng.fr@gmail.com
 * Last modified : 2018-09-15 13:09
 * Filename : display_stats.py
 * Description : 
'''''''''''''''''

import logging

logger = logging.getLogger('root')

def display(stats):
    logger.info('displaying stats of last window ...')
    for key, val in stats.items():
        logger.info(key + ': ' + str(val))
