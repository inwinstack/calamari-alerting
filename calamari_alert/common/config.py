from __future__ import print_function
from oslo_config import cfg


CONF = cfg.CONF

defaults_group = cfg.OptGroup(name='DEFAULT', title='a default conf group')
ssl_group = cfg.OptGroup(name='ssl', title='a ssl conf group')
calamari_group = cfg.OptGroup(name='calamari', title='a calamari conf group')
database_group = cfg.OptGroup(name='database', title='a database conf group')
email_group = cfg.OptGroup(name='email', title='a email conf group')

defaults_opts = [
    cfg.StrOpt('debug', default='True'),
    cfg.StrOpt('log_format', default='%(asctime)s %(levelname)8s [%(name)s] %(message)s'),
    cfg.StrOpt('log_date_format', default='%Y-%m-%d %H:%M:%S'),
    cfg.StrOpt('log_dir', default='/var/log/calamari_alert'),

    cfg.StrOpt('ca_file_dir', default=''),
    cfg.StrOpt('ca_files', default=''),
]

ssl_opts = [
    cfg.StrOpt('verify', default='True'),
    cfg.StrOpt('ca_file_dir', default='/var/lib/calamari-alert/ssl'),
    cfg.StrOpt('ca_files', default='server.pem'),
]

calamari_opts = [
    cfg.StrOpt('url', default='localhost', help='Calamari Server ip address'),
    cfg.StrOpt('port', default='80', help='Calamari Server port'),
    cfg.StrOpt('username', default='admin'),
    cfg.StrOpt('password', default='admin')
]

database_opts = [
    cfg.StrOpt('connection', default='')
]

email_opts = [
    cfg.StrOpt('address', default='smtp.gmail.com'),
    cfg.StrOpt('port', default=587),
    cfg.StrOpt('mode', default='None'),
    cfg.StrOpt('auth_account', default=True),
    cfg.StrOpt('username', default='localhost'),
    cfg.StrOpt('password', default='localhost')
]

CONF.register_group(defaults_group)
CONF.register_opts(defaults_opts, defaults_group)

CONF.register_group(ssl_group)
CONF.register_opts(ssl_opts, ssl_group)

CONF.register_group(calamari_group)
CONF.register_opts(calamari_opts, calamari_group)

CONF.register_group(database_group)
CONF.register_opts(database_opts, database_group)

CONF.register_group(email_group)
CONF.register_opts(email_opts, email_group)

CONFIG_FILE = '/etc/calamari-alert'
CONF(default_config_files=[CONFIG_FILE + '/calamari-alert.conf'])