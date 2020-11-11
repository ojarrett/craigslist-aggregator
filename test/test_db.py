from db_sync.db_ops_handler import DbOpsHandler
from db_sync.posting import Posting
from db_sync.sync import DbSync

def test_db_ops_handler_creates_db():
    db = DbOpsHandler('test.db')
    session = db.get_session()
    posting = Posting(rooms="1br", posting_id=123, region="test_city", 
            url="/posting-1br-url", price=750.0, last_updated=1234567, title="title")

    session.add(posting)
    session.commit()

def test_db_sync():
    db_sync = DbSync()
    posting_info = {
            'rooms' : '1br',
            'posting_id' : 123,
            'url' : "/posting-1br-url",
            'price' : 750.0,
            'last_updated' : 1234567,
            'title': 'title',
            'region': 'test_city',
    }
    db_sync.add_posting(posting_info)
    new_posting = db_sync.get_posting(posting_id=123, region="test_city")

    assert new_posting
    assert new_posting['price'] == 750.0

def test_db_sync_query_nonexistent_item():
    db_sync = DbSync()
    posting = db_sync.get_posting(posting_id=456, region="test_city")

    assert posting is None
