from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime


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
        all_keys = [
            'user', 'osd_warning', 'osd_error', 'mon_warning', 'mon_error',
            'pg_warning', 'pg_error', 'usage_warning', 'usage_error', 'general_polling',
            'abnormal_state_polling', 'abnormal_server_state_polling', 'enable_email_notify'
        ]
        for key in all_keys:
            var = 'self.{0}'.format(key)
            if key is 'user':
                var += '_id'

            if key is not 'enable_email_notify':
                exec("{0} = {1}".format(var, int(data[key])))
            else:
                exec("{0} = {1}".format(var, True if data[key] == '1' else False))

    def get_thresholds(self, name):
        thresholds = 0
        var = 'self.{0}'.format(name)
        exec("{0} = {1}".format('thresholds', var))
        return thresholds

    def __repr__(self):
        return "AlertRule('%s'," \
               "'%s', '%s', " \
               "'%s', '%s', " \
               "'%s', '%s'," \
               "'%s', '%s', " \
               "'%s', '%s', " \
               "'%s', '%s')" \
               % (self.user_id,
                  self.osd_warning, self.osd_error,
                  self.mon_warning, self.mon_error,
                  self.pg_warning, self.pg_error,
                  self.usage_warning, self.usage_error,
                  self.general_polling, self.abnormal_state_polling,
                  self.abnormal_server_state_polling, self.enable_email_notify)


class AlertHistory(Base):
    __tablename__ = 'alert_history'

    id = Column(Integer, primary_key=True)
    code = Column(String(100))
    level = Column(String(10))
    triggered = Column(DateTime)
    resolved = Column(DateTime)
    status = Column(String(20))
    event_message = Column(String(100))
    user_id = Column(Integer)

    def __init__(self, code, level, triggered, resolved, status, event_message, user_id):
        self.code = code
        self.level = level
        self.triggered = triggered
        self.resolved = resolved
        self.status = status
        self.event_message = event_message
        self.user_id = user_id

    def __repr__(self):
        return "AlertHistory('%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
               % (self.id, self.level, self.triggered, self.resolved,
                  self.status, self.event_message, self.user_id)