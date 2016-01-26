# coding=utf-8
from calamari_alert import constants
from calamari_alert.common import logs
from calamari_alert.db.models import AlertHistory, AlertCounter


class NotificationHandler(object):

    def __init__(self, sql, mail_client, to_account):
        self._alert_rule = None
        self._sql = sql
        self._mail_client = mail_client
        self._to_account = to_account
        self._alert_counter = None
        self.warn_original = self.error_original = None
        self.warn_previous = self.error_previous = None
        self.warn_notify = self.error_notify = None
        self.warn_id = self.error_id = None

    def update(self, rule):
        """
        Update alert rule from client response
        """
        self._alert_rule = rule
        self._get_alert_counter(rule.user_id)

    def _get_alert_counter(self, user_id):
        try:
            query = self._sql.query(AlertCounter, AlertCounter.user_id).filter_by(user_id=user_id).first()
            if query:
                self._alert_counter = query
            else:
                raise AttributeError
        except AttributeError:
            self._alert_counter = AlertCounter(user_id, constants.NOTIFICATION_TYPES)
            self._sql.add(self._alert_counter)

        self._set_alert_counter()

    def _set_alert_counter(self):
        for key in self._alert_counter.all_key():
            var = 'self.{0}'.format(key)
            exec("{0} = {1}".format(var, self._alert_counter.get(key)))

    def update_alert_counter(self):
        for key in self._alert_counter.all_key():
            var = 'self._alert_counter.{0}'.format(key)
            assign_var = None
            exec("assign_var = {0}".format('self.{0}'.format(key)))
            exec("{0} = {1}".format(var, '"{0}"'.format(assign_var)))

        self._sql.add(self._alert_counter)

    def checking_normal(self, health_counters):
        """
        Check {osd, mon, pg} alert condition
        """
        for key in constants.NOTIFICATION_TYPES:
            if key is not constants.USAGE_TYPE_KEY:
                okay, warn, error = self._all_counter(health_counters, key)
                self._checking_normal_threshold(key, True, warn)
                self._checking_normal_threshold(key, False, error)
                # logs.manager(logs.INFO, '{0} - okay: {1}, warn: {2}, error: {3}'
                #              .format(key.upper(), okay, warn, error))

    def checking_usage(self, usage_space):
        """
        Check usage alert condition,
        if more than the threshold will push some message
        """
        warn = self.warn_previous[constants.USAGE_TYPE_KEY]
        error = self.error_previous[constants.USAGE_TYPE_KEY]

        ration = self._usage_ratio(usage_space)
        # Scenarios -  More Than Original
        if ration >= self._alert_rule.usage_error and warn == 1:
            self._update_usage_previous(warn=0, error=1)
            self._make_notification(constants.USAGE_TYPE_KEY, ration, '02')
        # Scenarios - New
        elif self._alert_rule.usage_warning <= ration < self._alert_rule.usage_error and warn == 0:
            self._update_usage_previous(warn=1, error=0)
            self._make_notification(constants.USAGE_TYPE_KEY, ration, '01')
        # Scenarios -  Now Fix
        elif self._alert_rule.usage_warning > ration or (self._alert_rule.usage_error > ration and error == 1):
            if self.warn_previous[constants.USAGE_TYPE_KEY] > 0 or self.error_previous[constants.USAGE_TYPE_KEY] > 0:
                self._update_usage_previous(warn=0, error=0)
                self._make_notification(constants.USAGE_TYPE_KEY, ration, '04')

    def _checking_normal_threshold(self, key, is_warn, count):
        """
        Check {osd, mon, pg} alert threshold,
        if event some scenarios will push message
        """
        new_notify_count = lambda x, y, z: x + (y - z)
        original = self.warn_original[key] if is_warn else self.error_original[key]
        previous = self.warn_previous[key] if is_warn else self.error_previous[key]
        notify_count = self.warn_notify[key] if is_warn else self.error_notify[key]
        message_type = constants.MESSAGE_WARN_KEY if is_warn else constants.MESSAGE_ERROR_KEY
        threshold = self._alert_rule.get_thresholds(key + '_' + message_type)

        # logs.manager(logs.INFO, '{} - {} - original:{}, previous:{}, threshold:{}'
        #              .format(key.upper(), message_type.upper(), original, previous, threshold))

        if count >= threshold:
            # Scenarios - New
            if original < threshold and original < count and previous < count:
                self._update_normal_original(key, is_warn, count)
                self._update_normal_previous(key, is_warn, count)
                self._update_normal_notify(key, is_warn, count)
                self._make_notification(key, message_type, level='01')
            # Scenarios - More Than Original
            elif threshold <= original < count and count > previous:
                self._update_normal_original(key, is_warn, count)
                self._update_normal_previous(key, is_warn, count)
                self._update_normal_notify(key, is_warn, new_notify_count(notify_count, count, previous))
                self._make_notification(key, message_type, level='02')
            # Scenarios - Now Fix
            elif count < original and count < previous:
                self._update_normal_previous(key, is_warn, count)
            # Scenarios - More Then Done
            elif previous < count < original:
                self._make_notification(key, message_type, level='03')
                self._update_normal_previous(key, is_warn, count)

        else:
            # Scenarios - Done
            if count < original and count < previous:
                self._update_normal_original(key, is_warn, 0)
                self._update_normal_previous(key, is_warn, 0)
                self._make_notification(key, message_type, level='04')
                self._update_normal_notify(key, is_warn, 0)

    def _all_counter(self, counters, key):
        """
        get counter values - 0:okay, 1:warn, 2:critical(error)
        """
        if key in counters:
            values = counters[key]
            okay = values[constants.OK_KEY][constants.COUNT_KEY]
            warn = values[constants.WARN_KEY][constants.COUNT_KEY]
            error = values[constants.CRITICAL_KEY][constants.COUNT_KEY]

            if key is constants.PG_TYPE_KEY:
                total = okay + warn + error
                warn = (float(warn) / float(total)) * 100
                error = (float(error) / float(total)) * 100

            return okay, int(warn), int(error)

    def _update_normal_previous(self, key, is_warn, count):
        """
        Update previous count
        """
        if is_warn:
            self.warn_previous[key] = count
        else:
            self.error_previous[key] = count

    def _update_normal_original(self, key, is_warn, count):
        """
        Update original count
        """
        if is_warn:
            self.warn_original[key] = count
        else:
            self.error_original[key] = count

    def _update_normal_notify(self, key, is_warn, count):
        """
        Update notification count
        """
        if is_warn:
            self.warn_notify[key] = count
        else:
            self.error_notify[key] = count

    def _usage_ratio(self, usage_space):
        """
        get space values - 0:free_bytes, 1:used_bytes, 2:capacity_bytes
        """
        if constants.SPACE_KEY in usage_space:
            space = tuple()
            for key in constants.USAGE_KEYS:
                space += (usage_space[constants.SPACE_KEY][key],)

            return (float(space[1]) / float(space[-1])) * 100

    def _update_usage_previous(self, warn, error):
        """
        Update usage previous count
        """
        self.warn_previous[constants.USAGE_TYPE_KEY] = warn
        self.error_previous[constants.USAGE_TYPE_KEY] = error

    def _make_notification(self, name_type, message_type, level):
        if name_type == constants.USAGE_TYPE_KEY:
            message = constants.ENGLISH_STATUS_MESSAGE[name_type][level]
            if level == '01':
                message = message.format(message_type)
        else:
            message = constants.ENGLISH_STATUS_MESSAGE[name_type][message_type][level]

        logs.manager(logs.INFO, '{0} - {1}'.format(name_type.upper(), message))
        self._mail_client.sent(self._to_account, message)

        if level == '01':
            alert_history = AlertHistory(self._alert_rule.user_id, constants.PENDING, message)
            self._sql.add(alert_history)
            # alert_history.code = '%s1%03d' % (constants.HISTORY_CODE[name_type], alert_history.id)
            alert_history.level = "2" if message_type == constants.MESSAGE_ERROR_KEY else "3"
            alert_history.code = '{0}{1}001'.format(
                constants.HISTORY_CODE[name_type],
                alert_history.level
            )
            self._sql.add(alert_history)

            if message_type == constants.MESSAGE_WARN_KEY:
                self.warn_id[name_type] = alert_history.id
            else:
                self.error_id[name_type] = alert_history.id
        else:
            id = self.warn_id[name_type] if message_type == constants.MESSAGE_WARN_KEY \
                else self.error_id[name_type]
            query = self._sql.query(AlertHistory, AlertHistory.user_id).filter_by(id=id)
            alert_history = query.first()
            alert_history.event_message = message
            alert_history.count = self.warn_notify[name_type] if message_type == constants.MESSAGE_WARN_KEY \
                else self.error_notify[name_type]
            alert_history.tag_resolved() if level == '04' else alert_history.tag_triggered()
            alert_history.status = constants.RESOLVED if level == '04' else constants.PENDING
            self._sql.add(alert_history)