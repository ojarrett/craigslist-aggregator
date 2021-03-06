from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_sync.posting import Base

class DbOpsHandler:
    def __init__(self, db_name):
        self.db_name = db_name
        self.engine = None
        self.session = None
        self.sessionmaker = None

    def create_engine(self):
        if self.engine is None:
            self.engine = create_engine("sqlite:///{0}".format(self.db_name))

            Base.metadata.create_all(self.engine)

            self.sessionmaker = sessionmaker(bind=self.engine)

    # Mainly used for unit tests
    def clean_tables(self):
        if self.engine is None:
            self.create_engine()

        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def get_session(self):
        if self.session:
            return self.session
        else:
            if not self.engine:
                self.create_engine()

            self.session = self.sessionmaker()
            return self.session
