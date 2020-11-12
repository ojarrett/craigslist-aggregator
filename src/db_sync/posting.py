from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Posting(Base):
    __tablename__ = "postings"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    rooms = Column(String)
    posting_id = Column(Integer)
    url = Column(String)
    price = Column(Float)
    last_updated = Column(String)
    region = Column(String)
    repost_of = Column(Integer)

    def __repr__(self):
        return "<Posting(rooms='{0}', posting_id={1}, url='{2}', price={3})>".format(
                self.rooms, self.posting_id, self.url, self.price)
