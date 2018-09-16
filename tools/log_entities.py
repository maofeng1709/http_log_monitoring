'''''''''''''''''
 * Author : Mao FENG
 * Email : maofeng.fr@gmail.com
 * Last modified : 2018-09-13 19:37
 * Filename : data_structures.py
 * Description : 
'''''''''''''''''
import logging
from copy import deepcopy
from config import config
from datetime import datetime
from collections import deque, defaultdict

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
    def __init__(self, records, start_dt, end_dt, offset):
        self.records = records
        self.start_dt = start_dt
        self.end_dt = end_dt

        self.offset = offset # attr offset is necessary since records could be empty
        self.n_records = len(records)

    def __str__(self):
        return 'LogInterval from {} to {} with {} records'.format(self.start_dt, self.end_dt, self.n_records)




class LogWindow():
    """ 
    A Window uses a deque to store intervals, every interval-time performe a sliding operation which contains a pop and a push operation with corresponding calcuations for the stats to avoid unnecessary computations.
    """
    def __init__(self, intervals):
        assert len(intervals) == config.WINDOW_SIZE, 'Initilizing LogWindow with incorrect number of intervals'
        self.dq = deque(intervals)

        self.alert_state = 0 # 0: normal state, 1: recover state, 2: alert state
        self.offset = intervals[-1].offset

        self.stats = sum([Stats(interval) for interval in intervals])


        self.start_dt, self.end_dt = self.dq[0].start_dt, self.dq[-1].end_dt
        self.update_alert_state()


    def slide(self, interval):
        popped_interval = self.dq.popleft()
        self.dq.append(interval)

        self.offset = interval.offset
        
        self.stats += Stats(interval) - Stats(popped_interval)
        
        self.start_dt, self.end_dt = self.dq[0].start_dt, self.dq[-1].end_dt
        self.update_alert_state()
        
    def update_alert_state(self):
        avg_records = self.stats.dict['n_records'] / (self.end_dt - self.start_dt).total_seconds()
        if avg_records >= config.ALERT_THRESHOLD:
            self.alert_state = 2
        else:
            if self.alert_state == 2:
                self.alert_state = 1
            else:
                self.alert_state = 0

    def __str__(self):
        return 'LogWindow with {} intervals, and totally {} records'.format(config.WINDOW_SIZE, self.stats.dict['n_records'])

class Stats():
    INCREMENT, ACCUMULATION, DICTIONARY = 1,2,3
    stats_type_ref = {
        'n_records': INCREMENT,
        'size': ACCUMULATION,
        'section': DICTIONARY,
        'req_method': DICTIONARY,
        'req_protocol': DICTIONARY,
        'status': DICTIONARY
    }
    
    def __init__(self, interval):
        self.dict = {key: defaultdict(lambda: 0) if t == self.DICTIONARY else 0 for key, t in self.stats_type_ref.items()}
        for record in interval.records:
            for key, t in self.stats_type_ref.items():
                if t == self.INCREMENT:
                    self.dict[key] += 1
                elif t == self.ACCUMULATION:
                    val = getattr(record, key)
                    if val == '-': # unknown property
                        val = 0
                    self.dict[key] += int(val) 
                else: # t == dict
                    self.dict[key][getattr(record, key)] += 1

    def __add__(self, s):
        res = deepcopy(self)
        for key, t in res.dict.items():
            if self.stats_type_ref[key] != self.DICTIONARY:
                res.dict[key] += s.dict[key]
            else: # t == dict
                for key_ in (set(res.dict[key]) | set(s.dict[key])):
                    res.dict[key][key_] += s.dict[key][key_]

        return res

    def __sub__(self, s):
        res = deepcopy(self)
        for key, t in res.dict.items():
            if self.stats_type_ref[key] != self.DICTIONARY:
                res.dict[key] -= s.dict[key]
            else: # t == dict
                for key_ in (set(res.dict[key]) | set(s.dict[key])):
                    res.dict[key][key_] -= s.dict[key][key_]
        return res

    def __radd__(self, s):
        if s == 0:
            return self
        elif not isinstance(s, Stats):
            raise TypeError(" + operation not allowed between Stats and {}".format(type(s)))
        else:
            return s + self



    



        


