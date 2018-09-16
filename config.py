'''''''''''''''''
 * Author : Mao FENG
 * Email : maofeng.fr@gmail.com
 * Last modified : 2018-09-13 19:28
 * Filename : config.py
 * Description : the congifuration file for the monitoring program 
'''''''''''''''''

import logging

class Config():
    def __init__(self):
        self.LOG_FILE = '/var/log/access.log'
        self._INTERVAL_SIZE = 10
        self._WINDOW_SIZE= 12
        self._ALERT_THRESHOLD = 10
        self.MIN_INTERVAL_SIZE = 5
        self.MIN_WINDOW_SIZE = 2
        self.MIN_ALERT_THRESHOLD = 1
        self.LOGGING_LEVEL = logging.INFO

    @property
    def INTERVAL_SIZE(self):
        return self._INTERVAL_SIZE

    @INTERVAL_SIZE.setter
    def INTERVAL_SIZE(self, size):
        self._INTERVAL_SIZE = max(self.MIN_INTERVAL_SIZE, float(size))

    @property
    def WINDOW_SIZE(self):
        return self._WINDOW_SIZE

    @WINDOW_SIZE.setter
    def WINDOW_SIZE(self, size):
        self._WINDOW_SIZE = max(self.MIN_WINDOW_SIZE, int(size))

    @property
    def WINDOW_SIZE(self):
        return self._WINDOW_SIZE

    @WINDOW_SIZE.setter
    def WINDOW_SIZE(self, size):
        self._WINDOW_SIZE = max(self.MIN_WINDOW_SIZE, int(size))

    @property
    def ALERT_THRESHOLD(self):
        return self._ALERT_THRESHOLD

    @ALERT_THRESHOLD.setter
    def ALERT_THRESHOLD(self, threshold):
        self._ALERT_THRESHOLD = max(self.MIN_ALERT_THRESHOLD, int(threshold))



    def __str__(self):
        return 'LOG_FILE = {}, INTERVAL_SIZE = {} seconds, WINDOW_SIZE = {} intervals, ALERT_THRESHOLD = {} requests per second'.format(self.LOG_FILE, self.INTERVAL_SIZE, self.WINDOW_SIZE, self.ALERT_THRESHOLD)


config = Config()
