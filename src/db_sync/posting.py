from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Posting(Base):
    __tablename__ = "postings"

    id = Column(Integer, primary_key=True)
    rooms = Column(String)
    posting_id = Column(Integer)
    url = Column(String)
    price = Column(String)

    def __repr__(self):
        return "<Posting(rooms='{0}', posting_id={1}, url='{2}', price={3})>".format(
                self.rooms, self.posting_id, self.url, self.price)
