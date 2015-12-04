
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

OSD_STATUS_MESSAGE = {
    '01': 'OSD is in abnormal status!',
    '02': 'OSD comes new abnormal status!',
    '03': 'OSD has been repaired!',
    '04': 'OSD is in severe status!',
    '05': 'OSD comes new severe status!'
}

MON_STATUS_MESSAGE = {
    '01': 'Monitor comes new severe status!',
    '02': 'Monitor is in severe status!',
    '03': 'Monitor has been repaired!',
    '04': 'Monitor comes new abnormal status!',
    '05': 'Monitor is in abnormal status!'
}

PG_STATUS_MESSAGE = {
    '01': 'Some PGs are being modified by Ceph!',
    '02': 'Some other PGs are being modified by Ceph!',
    '03': 'PGs have been repaired!',
    '04': 'Some PGs stuck in abnormal states!',
    '05': 'Some other PGs stuck in abnormal states!'
}

USAGE_STATUS_MESSAGE = {
    '02': 'USAGE - Not enough free space! Please expand the storage capacity immediately!',
    '03': 'USAGE - Disk usage exceeds {0} %! Please expand the storage capacity!',
    '04': 'Storage capacity has been expanded!'
}



