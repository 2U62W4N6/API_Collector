import logging

# Set custom Log message format
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

class LogHandler:

    COUNT = {
        10:0,
        20:0,
        30:0,
        40:0,
        50:0
    }
    
    def __init__(self, name :str, log_file :str, level :int=logging.DEBUG):
        handler = logging.FileHandler(log_file)        
        handler.setFormatter(formatter)
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.addHandler(handler)
        self.level = level

    def log(self, message):
        log_type = {
            10 : self.logger.debug,
            20 : self.logger.info,
            30 : self.logger.warning,
            40 : self.logger.error,
            50 : self.logger.critical,
        }
        LogHandler.COUNT[self.level] += 1
        log_type[self.level](message)
    

LOGGER_DEBUG = LogHandler('debug', 'logs/debug.log', 10)
LOGGER_INFO = LogHandler('info', 'logs/info.log', 20)
LOGGER_WARNING = LogHandler('warning', 'logs/warning.log', 30)
LOGGER_ERROR = LogHandler('error', 'logs/error.log', 40)
LOGGER_CRITICAL = LogHandler('critical', 'logs/critical.log', 50)
