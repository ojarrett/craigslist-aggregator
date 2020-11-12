from db_sync.db_ops_handler import DbOpsHandler
from db_sync.posting import Posting

class DbSync:
    def __init__(self, clean=False):
        self.db_ops_handler = DbOpsHandler('test.db')

        if clean:
            self.db_ops_handler.clean_tables()

    def add_posting(self, posting):
        rooms = posting['rooms']
        posting_id = posting['posting_id']
        url = posting['url']
        price = posting['price']
        last_updated = posting['last_updated']
        title = posting['title']
        region = posting['region']
        repost_of = posting['repost_of'] if 'repost_of' in posting else None

        new_posting = Posting(rooms=rooms, posting_id=posting_id,
                url=url, price=price, last_updated=last_updated,
                title=title, region=region, repost_of=repost_of)

        session = self.db_ops_handler.get_session()
        session.add(new_posting)
        session.commit()

    def get_posting(self, posting_id, region, repost_of=None):
        session = self.db_ops_handler.get_session()
        posting = session.query(Posting).filter(Posting.region == region).filter(Posting.posting_id == posting_id).first()

        # Case 1: Posting cannot be found but is a repost of a posting in the local DB
        if posting is None and repost_of is not None:
            posting = session.query(Posting).filter(Posting.region == region).filter(Posting.posting_id == repost_of).first()

        # Case 2: Posting cannot be found but shares the same repost ID as another posting in the local DB
        if posting is None and repost_of is not None:
            posting = session.query(Posting).filter(Posting.region == region).filter(Posting.repost == repost_of).first()

        if posting:
            return {
                    'rooms': posting.rooms,
                    'url': posting.url,
                    'price': posting.price,
                    'last_updated': posting.last_updated,
                    'posting_id': posting.posting_id,
                    'region': posting.region,
                    'title': posting.title,
                    'repost_of': posting.repost_of,
            }

        return None

