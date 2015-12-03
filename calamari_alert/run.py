from common import config
from common import logs
from db.base import SQLMapper
from db.models import AlertRule
from handler import NotificationHandler
from client import HTTPClient
import time

calamari_ip = config.CONF.calamari.ip
calamari_port = config.CONF.calamari.port
endpoint = calamari_ip + ':' + calamari_port + '/api/'

username = config.CONF.calamari.username
password = config.CONF.calamari.password

connection = config.CONF.database.connection


def main():
    sql = SQLMapper(connection=connection, enable_echo=False)
    sql.sync()

    client = HTTPClient(endpoint=endpoint, debug=False)
    client.login(username, password)

    client.cluster_list()
    client.first_cluster_detail()
    handler = NotificationHandler()

    while True:
        alert_rule = get_last_rule(sql, client.alert_rule())
        space = client.cluster_space(client.cluster_id)
        counter = client.health_counters(client.cluster_id)

        handler.update_rule(alert_rule)
        handler.checking_usage(space)
        handler.checking_normal(counter)

        time.sleep(10)


def get_last_rule(sql, rule):
    query_alert_rule = sql.query(AlertRule, AlertRule.user_id)

    if query_alert_rule is not None and rule is not None:
        alert_rule = query_alert_rule.first()
        alert_rule.update(rule)
    elif rule is None:
        alert_rule = query_alert_rule.first()
    else:
        alert_rule = AlertRule(rule)

    sql.add(alert_rule)
    return alert_rule


if __name__ == "__main__":
    main()
