import MySQLdb
import unittest
from tweetdispatcher import TweetDispatcher

class TestIntegrationDB(unittest.TestCase):

    def test_insertion(self):
        tweetdispatcher=TweetDispatcher("config-chile.ini")
        tweetdispatcher.insert_match("localhost", "tweakthetweet", "ttt", "haiti_db",1,2)
        db =  MySQLdb.connect("localhost", "tweakthetweet", "ttt", "haiti_db")
        sql = "SELECT count(*) FROM  tweet_matches WHERE request_id=1 AND response_id=2;"
        db.query(sql)
        result=db.store_result()
        result=result.fetch_row()
        assert(result[0][0]==1)

