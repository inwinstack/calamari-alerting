from __future__ import print_function
from oslo_config import cfg


CONF = cfg.CONF

defaults_group = cfg.OptGroup(name='DEFAULT', title='a default conf group')
calamari_group = cfg.OptGroup(name='calamari', title='a calamari conf group')
database_group = cfg.OptGroup(name='database', title='a database conf group')
email_group = cfg.OptGroup(name='email', title='a email conf group')

defaults_opts = [
    cfg.StrOpt('debug', default='True'),
    cfg.StrOpt('log_format', default='%(asctime)s %(levelname)8s [%(name)s] %(message)s'),
    cfg.StrOpt('log_date_format', default='%Y-%m-%d %H:%M:%S'),
    cfg.StrOpt('log_dir', default='/var/log/calamari_alert'),
]

calamari_opts = [
    cfg.StrOpt('ip', default='localhost', help='Calamari Server ip address'),
    cfg.StrOpt('port', default='80', help='Calamari Server port'),
    cfg.StrOpt('username', default='admin'),
    cfg.StrOpt('password', default='admin')
]

database_opts = [
    cfg.StrOpt('connection', default='')
]

email_opts = [
    cfg.StrOpt('email_type', default='gmail'),
    cfg.StrOpt('username', default='test'),
    cfg.StrOpt('password', default='test')
]

CONF.register_group(defaults_group)
CONF.register_opts(defaults_opts, defaults_group)

CONF.register_group(calamari_group)
CONF.register_opts(calamari_opts, calamari_group)

CONF.register_group(database_group)
CONF.register_opts(database_opts, database_group)

CONF.register_group(email_group)
CONF.register_opts(email_opts, email_group)

CONFIG_FILE = '/Users/kairenbai/Desktop/Python/Projects/calamari_alert/etc/calamari_alert'

CONF(default_config_files=[CONFIG_FILE + '/calamari_alert.conf'])