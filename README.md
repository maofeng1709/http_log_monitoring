## HTTP log monitoring console program by Mao FENG

### 1. Run and test the program in virtualenv with python3
The program is suggested to be run in virtualenv:

`source env/bin/activate`

To Run the script with default settings:

`python main.py`

Detailed usage:

```
python main.py --LOG_FILE=<log-file-path> --INTERVAL_SIZE=<INTERVAL_SIZE> --WINDOW_SIZE=<WINDOW_SIZE> --ALERT_THRESHOLD=<ALERT_THRESHOLD>
	--LOG_FILE: path to the log file, by default as /var/log/access.log
	--INTERVAL_SIZE: a float number of seconds, monitoring script is toggled every INTERVAL_SIZE seconds, by default 10s, at least 5s
	--WINDOW_SIZE: an integer number of intervals, stats and alerts are generated within a window, by default 12 intervals, at least 2
	--ALERT_THRESHOLD: an integer number requests, an alert will be generated if the average requests per sencond exceeds this threshold, by default 10 requests, at least 1
	--test to enter test mode
	--SERVER_PORT: required for test mode, by default 80
```
	
To Enter the test mode:

`python main.py --test --SERVER_PORT=<SERVER_PORT>`

In test mode, the program create a thread, simulating periodically a certain number of requests so that the alert message can be toggled and than recovered.

### 2. Configurations and specifications

General default settings are defined at `config.py`:

```
self.LOG_FILE = '/var/log/access.log'
self._INTERVAL_SIZE = 10
self._WINDOW_SIZE= 12
self._ALERT_THRESHOLD = 10
self.MIN_INTERVAL_SIZE = 5
self.MIN_WINDOW_SIZE = 2
self.MIN_ALERT_THRESHOLD = 1
self.LOGGING_LEVEL = logging.INFO
self.SERVER_PORT = 80
```

Three classes are defined for facilitate the reading and logging logic:

- LogRecord: each line in the http log file corresponds to a LogRecord
- LogInterval: containing list of LogRecords in a INTERVAL_SIZE period and related information
- LogWindow: WINDOW_SIZE of LogIntervals, maintained in a FIFO queue. A `slide` operation is used to pop the oldest LogInterval and push a new LogInterval, updating the stats of the window at the same time.

### 3. Perspectives

- Exception handling: Although I tried to cover all the exception cases, unhandled errors may occur that blocks the main process.
- Class refinement: Some class can be still refined, e.g. add property setters to check values... 
