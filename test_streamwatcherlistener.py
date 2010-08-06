import unittest
import TTT_retriever as cm
import mock
import tweepy

class TestStreamWatcherListener(unittest.TestCase):
	
	def setUp(self):
		self.saver=mock.Mock()
		self.listener=cm.StreamWatcherListener(["#secondary1","#secondary2"],"TtTReadChile","TtT4Chile",[self.saver])
		
	def test_save_matched_tweet_succesful(self):
		status1=mock.Mock()
		status1.text="#primary2 este se guarda #secondary1"
		self.listener.on_status(status1)
		self.assertEquals(self.saver.save_raw_tweet.call_count,1)
		
		args = self.saver.save_raw_tweet.call_args[0]
		self.assertEquals(len(args), 5)
		self.assertEquals(args[0], status1.text)
		
		status2=mock.Mock()
		status2.text="#secondary2 este deberia pasar"
		self.listener.on_status(status2)
		self.assertEquals(self.saver.save_raw_tweet.call_count,2)

		args = self.saver.save_raw_tweet.call_args[0]
		self.assertEquals(len(args), 5)
		self.assertEquals(args[0], status2.text)

	def test_save_matched_tweet_failed(self):
		status1=mock.Mock()
		status1.text="#primary2 este no se guarda"
		self.listener.on_status(status1)
		self.assertEquals(self.saver.save_raw_tweet.call_count,0)
		
		status2=mock.Mock()
		status2.text="#primary1 tampoco se guarda"
		self.listener.on_status(status2)
		self.assertEquals(self.saver.save_raw_tweet.call_count,0)
