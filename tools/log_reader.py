'''''''''''''''''
 * Author : Mao FENG
 * Email : maofeng.fr@gmail.com
 * Last modified : 2018-09-14 11:02
 * Filename : log_reader.py
 * Description : tools for reading specific logs, optimized by always remembering the file offset of last valid record that has been read 
'''''''''''''''''

import re
from tools.log_entities import LogRecord, LogInterval, LogWindow
from config import config
from datetime import datetime, timedelta
import logging

logger = logging.getLogger('root')
record_keys = ['ip', 'client_id', 'user_id', 'time', 'time_zone', 'req_line', 'status', 'size']

def read_record(record_line, offset):
    """
        read a record form a record line, if an exceprion occurs, return None

    """
    # ------------------ ['ip', 'client_id', 'user_id', 'time', 'time_zone', 'req_line', 'status', 'size']
    record_pattern = re.compile('^(.*?) (.*?) (.*?) \[(.*?) (.*?)\] "(.*?)" (.*?) (.*?)$')
    record_values = re.findall(record_pattern, record_line)
    if record_values:
        try:
            return LogRecord(offset, **dict(zip(record_keys, record_values[0])))
        except Exception as err:
            logger.exception(str(err))
    else:
        logger.debug('the record line can not be recognized: ' + record_line)
        


def read_interval(start_dt, end_dt, offset = 0):
    records = []
    try:
        with open(config.LOG_FILE, 'r') as f:
            if offset:
                f.seek(offset)
            for line in f:
                record = read_record(line, offset)
                if record:
                    if record.datetime < start_dt:
                        offset += len(line)
                        continue
                    elif record.datetime < end_dt:
                        records.append(record)
                        offset += len(line)
                    else:
                        break

    except Exception as err:
        logger.exception(str(err))

    finally:
        interval = LogInterval(records, start_dt, end_dt, offset)
        logger.debug('interval read: ' + str(interval))
        return interval

def read_last_window():
    logger.info('reading last window ...')
    curr_dt = datetime.now().astimezone()
    dts = [] 
    for i in range(config.WINDOW_SIZE, 0, -1):
        dts.append(curr_dt - timedelta(seconds=config.INTERVAL_SIZE) * i)
    dts.append(curr_dt)

    intervals = []
    offset = 0
    for i in range(config.WINDOW_SIZE):
        start_dt, end_dt = dts[i], dts[i+1]
        interval = read_interval(start_dt, end_dt, offset)
        offset = interval.offset
        intervals.append(interval)

    return LogWindow(intervals)
