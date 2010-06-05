import unittest
import tweetmatcher
class TestTweetMatcher(unittest.TestCase):
	
	def setUp(self):
		self.expected_requests = ["#busco", "#sebusca", "#ruok", "#need"]
		self.expected_responses = ["#encontre","#seencontro","#imok","#found"]
		self.tweet_matcher = tweetmatcher.TweetMatcher(self.expected_requests, self.expected_responses)
	
	def test_creatematcher(self):
		self.assertEquals (self.expected_requests, self.tweet_matcher.requests)
		self.assertEquals (self.expected_responses, self.tweet_matcher.responses)
		
	def test_succesful_storing(self):	
		test_tweet_request = "#chile #sebusca Novia #contacto Pablo Cordella #location Martin Fierro 1234 #info buena presencia #status urgente"
		test_tweet_response = "#chile #encontre Novia #contacto Felipe Garrido #location Principe de Gales"
		#seria ideal que esta cosa haga un tweet con referencia a ambos respecto al match
		#ie: "@pcordell @fgarrido hay match de Novia 1313"
		self.tweet_matcher.parse(test_tweet_request)
		self.tweet_matcher.parse(test_tweet_response)
		assert test_tweet_request in self.tweet_matcher.parsed_requests
		assert test_tweet_response in self.tweet_matcher.parsed_responses

	def test_succesful_matching(self):	
		test_tweet_request = "#chile #sebusca Novia #contacto Pablo Cordella #location Martin Fierro 1234 #info buena presencia #status urgente"
		test_tweet_response = "#chile #encontre Novia #contacto Felipe Garrido #location Principe de Gales"
		
		assert not self.tweet_matcher.parse(test_tweet_request)
		assert self.tweet_matcher.parse(test_tweet_response)
		
		