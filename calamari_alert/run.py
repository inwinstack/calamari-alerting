from calamari_alert.common import config
from calamari_alert.common import logs
from calamari_alert.db.base import SQLMapper
from calamari_alert.db.models import AlertRule
from calamari_alert.handler import NotificationHandler
from calamari_alert.client import HTTPClient
from calamari_alert.smtp import SMTPClient
import time
import traceback

calamari_url = config.CONF.calamari.url
calamari_port = config.CONF.calamari.port

if 'https' in calamari_url and calamari_port == '80':
    endpoint = calamari_url + '/api/'
else:
    endpoint = calamari_url + ':' + calamari_port + '/api/'

ca_verify = config.CONF.ssl.verify
ca_file_dir = config.CONF.ssl.ca_file_dir
ca_files = config.CONF.ssl.ca_files.split(',')

if len(ca_files) > 1:
    for i in range(0, len(ca_files)):
        if ca_files[i]:
            ca_files[i] = "{0}/{1}".format(ca_file_dir, ca_files[i].strip())
else:
    ca_files = ca_file_dir + '/' + config.CONF.ssl.ca_files

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
        mail_client.set_mode(config.CONF.email.mode)
        mail_client.set_auth_account(config.CONF.email.auth_account)

        sql_connect = SQLMapper(connection=connection, enable_echo=False)
        sql_connect.sync()

        client = HTTPClient(
            endpoint=endpoint,
            ca_verify=ca_verify,
            ca_files=ca_files
        )
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

            time.sleep(alert_rule.general_polling)
    except:
        tb = traceback.format_exc()
        logs.manager(logs.ERROR, "SYSTEM - {0}".format(tb))
    finally:
        del tb


def get_last_rule(sql, rule, user_id):
    try:
        query = sql.query(AlertRule, AlertRule.user_id).filter_by(user_id=user_id).first()
        if query:
            query.update(rule)
        else:
            raise AttributeError
    except AttributeError:
        query = AlertRule(rule)

    sql.add(query)
    return query


if __name__ == "__main__":
    main()
