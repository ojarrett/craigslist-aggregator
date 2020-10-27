from db_sync.db_ops_handler import DbOpsHandler
from db_sync.posting import Posting

def test_db_ops_handler_creates_db():
    db = DbOpsHandler('test.db')
    session = db.get_session()
    posting = Posting(rooms="1br", posting_id=123, url="/posting-1br-url", price="$750")

    session.add(posting)
    session.commit()
