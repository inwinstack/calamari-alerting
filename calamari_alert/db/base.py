from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from common import logs
import models


class SQLMapper(object):

    def __init__(self, connection, enable_echo):
        self.engine = create_engine(connection, echo=enable_echo)
        logs.manager(logs.INFO, 'SQL - Connected {0}'.format(connection))

        if not database_exists(self.engine.url):
            create_database(self.engine.url)
            logs.manager(logs.INFO, 'SQL - Created database {0}'
                         .format(self.engine.url.split('/')[-1]))

        session_maker = sessionmaker()
        session_maker.configure(bind=self.engine)
        self.session = session_maker()

    def set_connection(self, connection, enable_echo):
        self.engine = create_engine(connection, echo=enable_echo)

    def sync(self):
        models.Base.metadata.create_all(self.engine)
        logs.manager(logs.INFO, 'SQL - Synced all table ....')

    def add(self, model):
        self.session.add(model)
        self.session.commit()
        logs.manager(logs.INFO, 'SQL - Add {0} to database'.format(model))

    def query(self, model_class, args):
        query = self.session.query(model_class).order_by(args)
        logs.manager(logs.INFO, 'SQL - Query {0} with {1}'.format(model_class, args))
        if query.count() == 0:
            return None
        else:
            return query



