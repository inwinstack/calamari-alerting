import logging
import config


INFO = 1
DEBUG = 2
WARN = 3
ERROR = 4

log_file = config.CONF.DEFAULT.log_dir + '/calamari-alert.log'
logger = logging.getLogger('calamari_alert')
logger.setLevel(logging.DEBUG)
file_stream = logging.FileHandler(log_file)
file_stream.setLevel(logging.DEBUG)
stream = logging.StreamHandler()
stream.setLevel(logging.DEBUG)

formatter = logging.Formatter(config.CONF.DEFAULT.log_format,
                              datefmt='%Y-%m-%d %H:%M:%S')
file_stream.setFormatter(formatter)
stream.setFormatter(formatter)

logger.addHandler(file_stream)
logger.addHandler(stream)


def manager(level, message):
    if level == INFO:
        logger.info(message)
    elif level == DEBUG:
        logger.debug(message)
    elif level == WARN:
        logger.warning(message)
    else:
        logger.error(message)