import MySQLdb
import unittest
from tweetdispatcher import TweetDispatcher

class TestIntegrationDB(unittest.TestCase):

	def setUp(self):
		db=MySQLdb.connect("localhost","ttt","ttt","ttt_testing")
		db.query("truncate tweets_matched;")
		db.query("truncate tweets;")
		db.query("truncate tweets_parsed;")
		db.close()

	def test_insertion(self):
		tweetdispatcher=TweetDispatcher("testing.ini")
		tweetdispatcher.tweet_match("localhost", "ttt", "ttt", "ttt_testing",1,2,"PEOPLE")
		db =  MySQLdb.connect("localhost", "ttt", "ttt", "ttt_testing")
		sql = "SELECT count(*) FROM  tweets_matched WHERE request_id=1 AND response_id=2 AND type='PEOPLE';"
		db.query(sql)
		result=db.store_result()
		result=result.fetch_row()
		assert(result[0][0]==1)

