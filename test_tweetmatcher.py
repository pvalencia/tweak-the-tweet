import unittest
import tweetmatcher
class TestTweetMatcher(unittest.TestCase):
	
	def setUp(self):
		self.expected_requests = ["#busco", "#sebusca", "#ruok", "#need"]
		self.expected_responses = ["#encontre","#seencontro","#imok","#found"]
		self.expected_location = ["#sitio","#location","#en","#loc","#zona","#localidad","#gps"," #lugar"]
		self.expected_contact = ["#contacto","#contact","#contactar","#con","#cont","#avisar","#telefono","#fono","#tel","#cel"]
		self.expected_name = ["#name","#nombre"]
		self.tweet_matcher = tweetmatcher.TweetMatcher(self.expected_requests, self.expected_responses,self.expected_location,self.expected_contact,self.expected_name)
	
	def test_creatematcher(self):
		self.assertEquals (self.expected_requests, self.tweet_matcher.requests)
		self.assertEquals (self.expected_responses, self.tweet_matcher.responses)
		self.assertEquals (self.expected_location, self.tweet_matcher.location)
		self.assertEquals (self.expected_contact, self.tweet_matcher.contact)
		self.assertEquals (self.expected_name, self.tweet_matcher.name)
		
	def test_succesful_storing(self):	
		test_tweet_request = [0, "#chile #sebusca Novia #contacto Pablo Cordella #location Martin Fierro 1234 #info buena presencia #status urgente"]
		test_tweet_response = [1, "#chile #encontre Novia #contacto Felipe Garrido #location Principe de Gales"]
		self.tweet_matcher.parse(test_tweet_request)
		self.tweet_matcher.parse(test_tweet_response)
		assert "novia" in self.tweet_matcher.parsed_responses[0]
		assert "novia" in self.tweet_matcher.parsed_requests[0]

	def test_succesful_matching(self):	
		test_tweet_request = [0, "#chile #sebusca Novia #contacto Pablo Cordella #location Martin Fierro 1234 #info buena presencia #status urgente"]
		test_tweet_response = [1, "#chile #encontre Novia #contacto Felipe Garrido #location Principe de Gales"]
		
		assert not self.tweet_matcher.parse(test_tweet_request)
		assert self.tweet_matcher.parse(test_tweet_response)
		
	def test_succesful_secondary_storage(self):
	    #seria ideal que esta cosa haga un tweet con referencia a ambos respecto al match
		#ie: "@pcordell @fgarrido hay match de Novia 1313"""
		test_tweet_request = [0, "#chile #sebusca Novia #contacto Pablo Cordella #location Martin Fierro 1234 #info buena presencia #status urgente"]
		test_tweet_response = [1, "#chile #encontre Novia #contacto Felipe Garrido #location Principe de Gales"]
		
		self.tweet_matcher.parse(test_tweet_request)
		self.tweet_matcher.parse(test_tweet_response)
		print self.tweet_matcher.parsed_responses
		print self.tweet_matcher.parsed_requests
		assert "felipe garrido" in self.tweet_matcher.parsed_responses[0][3]
		assert "pablo cordella" in self.tweet_matcher.parsed_requests[0][3]