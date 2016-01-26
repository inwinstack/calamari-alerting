
INFO = 4
WARNING = 3
ERROR = 2
CRITICAL = 1

WARN_KEY = 'warn'
CRITICAL_KEY = 'critical'
OK_KEY = 'ok'
COUNT_KEY = 'count'
SPACE_KEY = 'space'

OSD_TYPE_KEY = 'osd'
MON_TYPE_KEY = 'mon'
PG_TYPE_KEY = 'pg'
USAGE_TYPE_KEY = 'usage'

PENDING = 'pending'
RESOLVED = 'resolved'

MESSAGE_WARN_KEY = 'warning'
MESSAGE_ERROR_KEY = 'error'

USAGE_KEYS = [
    'free_bytes',
    'used_bytes',
    'capacity_bytes'
]

NOTIFICATION_TYPES = [
    OSD_TYPE_KEY,
    MON_TYPE_KEY,
    PG_TYPE_KEY,
    USAGE_TYPE_KEY
]

HISTORY_CODE = {
    OSD_TYPE_KEY: '01',
    MON_TYPE_KEY: '02',
    PG_TYPE_KEY: '03',
    USAGE_TYPE_KEY: '04'
}


ENGLISH_STATUS_MESSAGE = {
    OSD_TYPE_KEY: {
        MESSAGE_WARN_KEY: {
            '01': 'OSD is in abnormal status!',
            '02': 'OSD comes new abnormal status!',
            '03': 'OSD comes new abnormal status!',
            '04': 'OSD has been repaired!',
        },
        MESSAGE_ERROR_KEY: {
            '01': 'OSD is in severe status!',
            '02': 'OSD comes new severe status!',
            '03': 'OSD comes new severe status!',
            '04': 'OSD has been repaired!'
        }
    },
    MON_TYPE_KEY: {
        MESSAGE_WARN_KEY: {
            '01': 'Monitor is in abnormal status!',
            '02': 'Monitor comes new abnormal status!',
            '03': 'Monitor comes new abnormal status!',
            '04': 'Monitor has been repaired!'
        },
        MESSAGE_ERROR_KEY: {
            '01': 'Monitor is in severe status!',
            '02': 'Monitor comes new severe status!',
            '03': 'Monitor comes new severe status!',
            '04': 'Monitor has been repaired!',
        }
    },
    PG_TYPE_KEY: {
        MESSAGE_WARN_KEY: {
            '01': 'Some PGs are being modified by Ceph!',
            '02': 'Some other PGs are being modified by Ceph!',
            '03': 'Some other PGs are being modified by Ceph!',
            '04': 'PGs have been repaired!',
        },
        MESSAGE_ERROR_KEY: {
            '01': 'Some PGs stuck in abnormal states!',
            '02': 'Some other PGs are being modified by Ceph!',
            '03': 'Some other PGs are being modified by Ceph!',
            '04': 'PGs have been repaired!',
        }
    },
    USAGE_TYPE_KEY: {
        '01': 'Disk usage exceeds {0}%! Please expand the storage capacity!',
        '02': 'Not enough free space! Please expand the storage capacity immediately!',
        '04': 'Storage capacity has been expanded!'
    },
}


