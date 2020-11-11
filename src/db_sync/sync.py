from db_sync.db_ops_handler import DbOpsHandler
from db_sync.posting import Posting

class DbSync:
    def __init__(self):
        self.db_ops_handler = DbOpsHandler('test.db')

    def add_posting(self, posting):
        rooms = posting['rooms']
        posting_id = posting['posting_id']
        url = posting['url']
        price = posting['price']
        last_updated = posting['last_updated']
        title = posting['title']
        region = posting['region']

        new_posting = Posting(rooms=rooms, posting_id=posting_id,
                url=url, price=price, last_updated=last_updated,
                title=title, region=region)

        session = self.db_ops_handler.get_session()
        session.add(new_posting)
        session.commit()

    def get_posting(self, posting_id, region):
        session = self.db_ops_handler.get_session()
        posting = session.query(Posting).filter(Posting.region == region).filter(Posting.posting_id == posting_id).first()

        if posting:
            return {
                    'rooms': posting.rooms,
                    'url': posting.url,
                    'price': posting.price,
                    'last_updated': posting.last_updated,
                    'posting_id': posting_id,
                    'region': region,
                    'title': posting.title,
            }

        return None

