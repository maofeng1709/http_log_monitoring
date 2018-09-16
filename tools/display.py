'''''''''''''''''
 * Author : Mao FENG
 * Email : maofeng.fr@gmail.com
 * Last modified :	2018-09-15 19:35
 * Filename :		display.py
 * Description : 
'''''''''''''''''

import logging
import inspect

logger = logging.getLogger('root')

NO_COLOR = "\33[m"
RED, GREEN, ORANGE, BLUE, PURPLE, LBLUE, GREY = map("\33[%dm".__mod__, range(31, 38))

def display_stats(window):
    logger.info('displaying stats of current window ...')
    
    if window.stats.dict['n_records'] == 0:
        logger.info('no requests in current window')
        return

    stats = window.stats
    avg_records = stats.dict['n_records'] / (window.end_dt - window.start_dt).total_seconds()
    alert = ('no alert - average hits/seconds: {}' if window.alert_state == 0 else 'High traffic alert recovered - average hits/seconds: {}' if window.alert_state == 1 else 'High traffic generated an alert - average hits/seconds: {}').format(avg_records)

    for key, val in stats.dict.items():
        if isinstance(val, dict):
            # display top 3 of the dictionary-like stats
            msg = sorted(val.items(), key=lambda x: x[1], reverse=True)[:3]
        else:
            msg = val
        logger.info(key + ': ' + str(msg))
    
    if window.alert_state:
        logger.warn('alert_state' + ': ' + alert)
    else:
        logger.info('alert_state' + ': ' + alert)

def add_color(logger_method, _color):
    def wrapper(message, *args, **kwargs):
        color = kwargs.pop("color", _color)
        if isinstance(color, int):
            color = "\33[%dm" % color
        frame = inspect.stack()[1]
        filename = frame[0].f_code.co_filename
        real_module = filename.split('/')[-1].split('.')[0]
        if 'extra' in kwargs:
            kwargs['extra']['real_module'] = real_module 
        else:
            kwargs['extra'] = {'real_module': real_module}
        return logger_method(color+message+NO_COLOR, *args, **kwargs)
    return wrapper

def set_root_logger(level):
    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(real_module)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger('root')
    logger.setLevel(level)
    logger.addHandler(handler)

    for level, color in zip(("info", "warn", "error", "debug"), (GREEN, ORANGE, RED, LBLUE)):
        setattr(logger, level, add_color(getattr(logger, level), color))

    return logger

