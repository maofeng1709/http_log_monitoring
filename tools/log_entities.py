'''''''''''''''''
 * Author : Mao FENG
 * Email : maofeng.fr@gmail.com
 * Last modified : 2018-09-13 19:37
 * Filename : data_structures.py
 * Description : 
'''''''''''''''''
import logging
from config import config
from datetime import datetime
from collections import deque

logger = logging.getLogger('root')


class LogRecord():
    def __init__(self, offset, **kwargs):

        self.offset = offset

        prop_defaults = {
            'ip': '0.0.0.0',
            'client_id': '-',
            'user_id': '-', 
            'time': '',
            'time_zone': '',
            'req_line': '-',
            'status': 'UNK',
            'size': 0
        }
        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        self.req_method, self.req_resource, self.req_protocol = ('UNK', 'UNK', 'UNK') if self.req_line == '-' else self.req_line.split()
        
        self.datetime = datetime.strptime(self.time + ' ' + self.time_zone, '%d/%b/%Y:%H:%M:%S %z')

        self.section = '/'.join(self.req_resource.split('/')[:4]) if self.req_resource.startswith('http') else '/'.join(self.req_resource.split('/')[:2])

            
    def __str__(self):
        return ' '.join([self.ip, self.client_id, self.user_id, '[{} {}]'.format(self.datetime, self.time_zone),
                '"{} {} {}"'.format(self.req_method, self.req_resource, self.req_protocol), self.status, self.size])


class LogInterval():
    def __init__(self, records, start_dt, end_dt):
        self.records = records
        self.start_dt = start_dt
        self.end_dt = end_dt

        self.offset = records[-1].offset if records else 0
        self.n_records = len(records)
        self.section_dict = dict()
        for record in records:
            if record.section not in self.section_dict:
                self.section_dict[record.section] = 1
            else:
                self.section_dict[record.section] += 1

    def __str__(self):
        return 'LogInterval from {} to {} with {} records'.format(self.start_dt, self.end_dt, self.n_records)




class LogWindow():
    """ 
    A Window uses a deque to store intervals, every interval-time performe a sliding operation which contains a pop and a push operation with corresponding calcuations for the stats to avoid unnecessary computations.
    """
    def __init__(self, intervals):
        assert len(intervals) == config.WINDOW_SIZE, 'Initilizing LogWindow with incorrect number of intervals'
        self.dq = deque(intervals)

        self.alert_state = 0
        self.n_records = 0

        self.section_dict = dict()
        for interval in intervals:
            self.n_records += interval.n_records
            for section, n_hits in interval.section_dict.items():
                if section not in self.section_dict:
                    self.section_dict[section] = n_hits
                else:
                    self.section_dict[section] += n_hits

        self.start_dt, self.end_dt = intervals[0].start_dt, intervals[-1].end_dt
        self.update_alert_state()

    def slide(self, interval):
        popped_interval = self.dq.popleft()
        self.dq.append(interval)

        self.n_records += interval.n_records - popped_interval.n_records

        for section, n_hits in popped_interval.section_dict.items():
            self.section_dict[section] -= n_hits
        for section, n_hits in interval.section_dict.items():
            if section not in self.section_dict:
                self.section_dict[section] = n_hits
            else:
                self.section_dict[section] += n_hits
        
        self.start_dt, self.end_dt = intervals[0].start_dt, intervals[-1].end_dt
        self.update_alert_state()

        
    def update_alert_state(self):
        avg_records = self.n_records / (self.end_dt - self.start_dt).total_seconds()
        if avg_records >= config.ALERT_THRESHOLD:
            self.alert_state = 2
        else:
            if self.alert_state == 2:
                self.alert_state = 1
            else:
                self.alert_state = 0

    def get_stats(self):
        avg_records = self.n_records / (self.end_dt - self.start_dt).total_seconds()
        stats = dict() 
        stats['max_section'] = max(self.section_dict.items(), key=lambda x: x[1]) if self.section_dict else 'no section visited'
        stats['n_hits'] = self.n_records + ' ' + 'High traffic alert recovered - average hits -{}'.foramt(avg_records) if self.alert_state == 1 else 'High traffic generated an alert - average hits: {}'.format(avg_records)
        return stats

    def __str__(self):
        return 'LogWindow with {} intervals, and totally {} records'.format(config.WINDOW_SIZE, self.n_records)

    



        


