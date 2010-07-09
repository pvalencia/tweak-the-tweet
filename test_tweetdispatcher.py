import unittest
import tweetdispatcher
class TestTweetDispatcher(unittest.TestCase):

	def setUp(self):
		#self.path = "D:\Incoming\U\2010-1\eXtremeProgramming\dcc-cc6401-2010-tweakthetweet\config-chile.ini"
		self.tweet_dispatcher = tweetdispatcher.TweetDispatcher(".")

	def test_d(self):
		assert(1==1)
