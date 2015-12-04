# coding=utf-8
import constants
from common import logs
from db.models import AlertHistory
from datetime import datetime


class NotificationHandler(object):

    def __init__(self):
        self._alert_rule = None
        self.warn_original = {key: 0 for key in constants.NOTIFICATION_TYPES}
        self.error_original = {key: 0 for key in constants.NOTIFICATION_TYPES}
        self.warn_previous = {key: 0 for key in constants.NOTIFICATION_TYPES}
        self.error_previous = {key: 0 for key in constants.NOTIFICATION_TYPES}
        self.warn_notify = {key: 0 for key in constants.NOTIFICATION_TYPES}
        self.error_notify = {key: 0 for key in constants.NOTIFICATION_TYPES}

    def _get_all_counter(self, counters, key):
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
                print(total, warn, error)

            return okay, int(warn), int(error)

    def _get_usage_ratio(self, usage_space):
        """
        get space values - 0:free_bytes, 1:used_bytes, 2:capacity_bytes
        """
        if constants.SPACE_KEY in usage_space:
            space = tuple()
            for key in constants.USAGE_KEYS:
                space += (usage_space[constants.SPACE_KEY][key],)

            return (float(space[1]) / float(space[-1])) * 100

    def update_rule(self, rule):
        """
        Update alert rule from client response
        """
        self._alert_rule = rule

    def checking_normal(self, health_counters):
        """
        Check {osd, mon, pg} alert condition
        """
        for key in constants.NOTIFICATION_TYPES:
            if key is not constants.USAGE_TYPE_KEY:
                okay, warn, error = self._get_all_counter(health_counters, key)
                self._checking_threshold(key, True, warn)
                self._checking_threshold(key, False, error)
                logs.manager(logs.INFO, '{0} - okay: {1}, warn: {2}, error: {3}'
                             .format(key.upper(), okay, warn, error))

    def _checking_threshold(self, key, is_warn, count):
        """
        Check {osd, mon, pg} alert threshold,
        if event some scenarios will push message
        """
        new_notify_count = lambda x, y, z: x + (y - z)
        original = self.warn_original[key] if is_warn else self.error_original[key]
        previous = self.warn_previous[key] if is_warn else self.error_previous[key]
        notify_count = self.warn_notify[key] if is_warn else self.error_notify[key]
        type_key = 'warning' if is_warn else 'error'
        threshold = self._alert_rule.get_thresholds(key + '_' + type_key)

        logs.manager(logs.INFO, '{} - {} - original:{}, previous:{}, threshold:{}'
                     .format(key.upper(), type_key.upper(), original, previous, threshold))

        if count >= threshold:
            # Scenarios - New
            if original < threshold and original < count and previous < count:
                self._update_normal_original(key, is_warn, count)
                self._update_normal_previous(key, is_warn, count)
                self._up_normal_notify(key, is_warn, count)
                self._make_notification()
                logs.manager(logs.INFO, '{0} - ConditionNew{1}'
                             .format(key.upper(), type_key.title()))
            # Scenarios - More Than Original
            elif threshold <= original < count and count > previous:
                self._update_normal_original(key, is_warn, count)
                self._update_normal_previous(key, is_warn, count)
                self._up_normal_notify(key, is_warn, new_notify_count(notify_count, count, previous))
                logs.manager(logs.INFO, '{0} - Condition{1}MoreThanOriginal'
                             .format(key.upper(), type_key.title()))
            # Scenarios - Now Fix
            elif count < original and count < previous:
                self._update_normal_previous(key, is_warn, count)
            # Scenarios - More Then Done
            elif previous < count < original:
                self._update_normal_previous(key, is_warn, count)
                logs.manager(logs.INFO, '{0} - ConditionWarn{1}Then{1}'
                             .format(key.upper(), type_key.title()))
        else:
            # Scenarios - Done
            if count < original and count < previous:
                self._update_normal_original(key, is_warn, 0)
                self._update_normal_previous(key, is_warn, 0)
                self._up_normal_notify(key, is_warn, 0)
                logs.manager(logs.INFO, '{0} - Condition{1}Done'
                             .format(key.upper(), type_key.title()))

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

    def _up_normal_notify(self, key, is_warn, count):
        """
        Update notification count
        """
        if is_warn:
            self.warn_notify[key] = count
        else:
            self.error_notify[key] = count

    def checking_usage(self, usage_space):
        """
        Check usage alert condition,
        if more than the threshold will push some message
        """
        ration = self._get_usage_ratio(usage_space)
        logs.manager(logs.INFO, 'USAGE - ration: {0}'.format(ration))

        if self._alert_rule.usage_warning <= ration < self._alert_rule.usage_error:
            self._update_usage_previous(warn=1, error=0)
            logs.manager(logs.DEBUG, constants.USAGE_STATUS_MESSAGE['03']
                         .format(self._alert_rule.usage_warning))

        elif ration >= self._alert_rule.usage_error:
            self._update_usage_previous(warn=0, error=1)
            logs.manager(logs.DEBUG, constants.USAGE_STATUS_MESSAGE['02'])

        else:
            if self.warn_previous[constants.USAGE_TYPE_KEY] > 0 or self.error_previous[constants.USAGE_TYPE_KEY] > 0:
                self._update_usage_previous(warn=0, error=0)
                logs.manager(logs.DEBUG, constants.USAGE_STATUS_MESSAGE['04'])

    def _update_usage_previous(self, warn, error):
        """
        Update usage previous count
        """
        self.warn_previous[constants.USAGE_TYPE_KEY] = warn
        self.error_previous[constants.USAGE_TYPE_KEY] = error

    def _make_notification(self):
        alert_history = AlertHistory(
            '013001', constants.INFO,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            constants.PENDING, 'TEST......', self._alert_rule.user_id
        )
        print(alert_history)