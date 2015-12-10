from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
import json

Base = declarative_base()


class AlertRule(Base):
    __tablename__ = 'alert_rule'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    osd_warning = Column(Integer, default=1)
    osd_error = Column(Integer, default=1)
    mon_warning = Column(Integer, default=1)
    mon_error = Column(Integer, default=1)
    pg_warning = Column(Integer, default=20)
    pg_error = Column(Integer, default=20)
    usage_warning = Column(Integer, default=70)
    usage_error = Column(Integer, default=85)
    general_polling = Column(Integer, default=30)
    abnormal_state_polling = Column(Integer, default=120)
    abnormal_server_state_polling = Column(Integer, default=3600)
    enable_email_notify = Column(Boolean, default=True)

    def __init__(self, data):
        self.update(data)

    def update(self, data):
        all_key = [
            'user_id', 'osd_warning', 'osd_error', 'mon_warning', 'mon_error',
            'pg_warning', 'pg_error', 'usage_warning', 'usage_error', 'general_polling',
            'abnormal_state_polling', 'abnormal_server_state_polling', 'enable_email_notify'
        ]
        for key in all_key:
            var = 'self.{0}'.format(key)
            if key is not 'enable_email_notify':
                exec("{0} = {1}".format(var, int(data[key])))
            else:
                exec("{0} = {1}".format(var, True if data[key] == '1' else False))

    def get_thresholds(self, name):
        thresholds = 0
        var = 'self.{0}'.format(name)
        exec("{0} = {1}".format('thresholds', var))
        return thresholds


class AlertHistory(Base):
    __tablename__ = 'alert_history'

    id = Column(Integer, primary_key=True)
    count = Column(Integer)
    code = Column(String(100))
    level = Column(Integer)
    triggered = Column(DateTime)
    resolved = Column(DateTime)
    status = Column(String(20))
    event_message = Column(String(100))
    user_id = Column(Integer)

    def __init__(self, user_id, status, event_message):
        self.code = '00000'
        self.level = 4
        self.triggered = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.resolved = None
        self.status = status
        self.event_message = event_message
        self.user_id = user_id
        self.count = 0

    def tag_resolved(self):
        self.resolved = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def tag_triggered(self):
        self.triggered = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class AlertCounter(Base):
    __tablename__ = 'alert_counter'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    warn_original = Column(String(200))
    error_original = Column(String(200))
    warn_previous = Column(String(200))
    error_previous = Column(String(200))
    warn_notify = Column(String(200))
    error_notify = Column(String(200))
    warn_id = Column(String(200))
    error_id = Column(String(200))

    def __init__(self, user_id, keys):
        self.user_id = user_id

        for key in self.all_key():
            var = 'self.{0}'.format(key)
            exec("{0} = {1}".format(var, '"{0}"'.format({key: 0 for key in keys})))

    def get(self, key):
        var = None
        exec("var = self.{0}".format(key))
        exec("self.count = {0}".format(var))
        return self.count

    def all_key(self):
        return [
            'warn_original', 'error_original', 'warn_previous', 'error_previous',
            'warn_notify', 'error_notify', 'warn_id', 'error_id'
        ]