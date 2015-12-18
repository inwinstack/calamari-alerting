from calamari_alert.common import config
from calamari_alert.common import logs
from calamari_alert.db.base import SQLMapper
from calamari_alert.db.models import AlertRule
from calamari_alert.handler import NotificationHandler
from calamari_alert.client import HTTPClient
from calamari_alert.smtp import SMTPClient
import time
import traceback

calamari_ip = config.CONF.calamari.ip
calamari_port = config.CONF.calamari.port
endpoint = calamari_ip + ':' + calamari_port + '/api/'

username = config.CONF.calamari.username
password = config.CONF.calamari.password

connection = config.CONF.database.connection

mail_username = config.CONF.email.username
mail_password = config.CONF.email.password
mail_address = config.CONF.email.address
mail_port = config.CONF.email.port


def main():
    try:
        mail_client = SMTPClient(mail_username, mail_password, mail_address, mail_port)
        sql_connect = SQLMapper(connection=connection, enable_echo=False)
        sql_connect.sync()

        client = HTTPClient(endpoint=endpoint, debug=False)
        client.login(username, password)

        client.cluster_list()
        client.first_cluster_detail()
        user_info = client.user_info()
        user_id = user_info['id']
        user_email = user_info['email']
        handler = NotificationHandler(sql_connect, mail_client, user_email)

        while True:
            alert_rule = get_last_rule(sql_connect, client.alert_rule(), user_id)
            space = client.cluster_space(client.cluster_id)
            counter = client.health_counters(client.cluster_id)

            handler.update(alert_rule)
            handler.checking_usage(space)
            handler.checking_normal(counter)
            handler.update_alert_counter()

            time.sleep(10)
    except Exception:
        tb = traceback.format_exc()
        logs.manager(logs.ERROR, "SYSTEM - {0}".format(tb))
    finally:
        del tb


def get_last_rule(sql, rule, user_id):
    try:
        query = sql.query(AlertRule, AlertRule.user_id).filter_by(user_id=user_id).first()
        if query:
            query.update(rule)
    except AttributeError:
        query = AlertRule(rule)

    sql.add(query)
    return query


if __name__ == "__main__":
    main()
