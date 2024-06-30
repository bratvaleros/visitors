import os
import logging

LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')  # CRITICAL, ERROR, WARNING, INFO, DEBUG
LOG_DIR = os.getenv('LOG_DIR', '/var/log/spectacular')
LOG_DEVICE = f'{LOG_DIR}/visit_control.log'
LOG_DEVICE_DJANGO = f'{LOG_DIR}/visit_control_django.log'
LOG_MAXFILESIZE = int(os.getenv('LOG_MAXFILESIZE', '10000000'))
LOG_FILECOUNT = int(os.getenv('LOG_FILECOUNT', '10'))

if os.getenv('DEBUG', False):
    LOGGING_LEVEL = 'DEBUG'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': (u'%(asctime)s [%(levelname)-8s] (%(module)s.%(funcName)s) %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'rotated_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DEVICE,
            'maxBytes': LOG_MAXFILESIZE,
            'backupCount': LOG_FILECOUNT,
            'formatter': 'simple'
        },
        'rotated_file_django': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DEVICE_DJANGO,
            'maxBytes': LOG_MAXFILESIZE,
            'backupCount': LOG_FILECOUNT,
            'formatter': 'simple'
        },
    },
    'loggers': {
        '': {  # default logger
            'handlers': ['rotated_file'],
            'level': LOGGING_LEVEL,
            'propagate': False,
        },
        'django': {
            'handlers': ['rotated_file_django'],
            'level': LOGGING_LEVEL,
            'propagate': False,
        },
    },
}
