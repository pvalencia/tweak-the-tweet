import unittest
import chile_mysql as cm
import mock
import tweepy

class TestStreamWatcherListener(unittest.TestCase):
	
	def setUp(self):
		self.saver=mock.Mock()
		
	def test_save_matched_tweet(self):
		primary_tags=["#primary1","primary2"]
		listener=cm.StreamWatcherListener(["#secondary1","#secondary2"],"TtTReadChile","TtT4Chile",[self.saver])
		
		status1=mock.Mock()
		status1.text="#primary1 este no se guarda"
		listener.on_status(status1)
		self.assertEquals(self.saver.save_raw_tweet.call_count,0)
		
		status2=mock.Mock()
		status2.text="#primary2 este se guarda #secondary1"
		listener.on_status(status2)
		self.assertEquals(self.saver.save_raw_tweet.call_count,1)
		
		status3=mock.Mock()
		status3.text="#secondary2 este deberia pasar"
		listener.on_status(status3)
		self.assertEquals(self.saver.save_raw_tweet.call_count,2)
		
