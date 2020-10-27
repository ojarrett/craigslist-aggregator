from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DbOpsHandler:
    def __init__(self, db_name):
        self.db_name = db_name
        self.engine = None
        self.session = None
        self.sessionmaker = None

    def create_engine(self):
        if self.engine is None:
            self.engine = create_engine("sqlite:///{0}".format(self.db_name))
            self.sessionmaker = sessionmaker(bind=self.engine)

    def get_session(self):
        if self.session:
            return session
        else:
            if not self.engine:
                self.create_engine()

            self.session = self.sessionmaker()
            return self.session
