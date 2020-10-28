from db_sync.db_ops_handler import DbOpsHandler
from db_sync.posting import Posting
from db_sync.sync import DbSync

def test_db_ops_handler_creates_db():
    db = DbOpsHandler('test.db')
    session = db.get_session()
    posting = Posting(rooms="1br", posting_id=123, 
            url="/posting-1br-url", price="$750", last_updated=1234567)

    session.add(posting)
    session.commit()

def test_db_sync():
    db_sync = DbSync()
    posting_info = {
            'rooms' : '1br',
            'posting_id' : 123,
            'url' : "/posting-1br-url",
            'price' : "$750",
            'last_updated' : 1234567,
    }
    db_sync.add_posting(posting_info)
