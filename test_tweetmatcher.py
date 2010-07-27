import unittest
import tweetmatcher
from ini_reader import IniReader
import MySQLdb
class TestTweetMatcher(unittest.TestCase):
	
	def setUp(self):
		db=MySQLdb.connect("localhost","ttt","ttt","ttt_testing")
		db.query("truncate tweets;")
		db.query("truncate tweets_matched;")
		db.query("truncate tweets_parsed;")
		self.expected_requests = ["#busco", "#sebusca", "#ruok", "#need"]
		self.expected_responses = ["#encontre","#seencontro","#imok","#found"]
		self.expected_location = ["#sitio","#location","#en","#loc","#zona","#localidad","#gps"," #lugar"]
		self.expected_contact = ["#contacto","#contact","#contactar","#con","#cont","#avisar","#telefono","#fono","#tel","#cel"]
		self.expected_name = ["#name","#nombre"]
		ini = IniReader("testing.ini")
		mysql_info = ini.get_mysql_info()
		mysql_info = [mysql_info[0]]+mysql_info[2:]
		self.tweet_matcher = tweetmatcher.TweetMatcher("categoria",self.expected_requests, self.expected_responses,self.expected_location,self.expected_contact,self.expected_name,mysql_info)
	
	def test_creatematcher(self):
		self.assertEquals (self.expected_requests, self.tweet_matcher.requests)
		self.assertEquals (self.expected_responses, self.tweet_matcher.responses)
		self.assertEquals (self.expected_location, self.tweet_matcher.location)
		self.assertEquals (self.expected_contact, self.tweet_matcher.contact)
		self.assertEquals (self.expected_name, self.tweet_matcher.name)
		
	def test_succesful_storing(self):	
		test_tweet_request = [0, "#chile #sebusca Novia #contacto Pablo Cordella #location Martin Fierro 1234 #info buena presencia #status urgente","2010-01-01 00:00:00"]
		test_tweet_response = [1, "#chile #encontre Novia #contacto Felipe Garrido #location Principe de Gales","2010-01-01 00:00:00"]
		self.tweet_matcher.parse(test_tweet_request)
		self.tweet_matcher.parse(test_tweet_response)
		db=MySQLdb.connect("localhost","ttt","ttt","ttt_testing")
		db.query("SELECT info FROM tweets_parsed WHERE id_tweet=0 AND category='categoria';")
		info_req=db.store_result().fetch_row()[0][0]
		db.query("SELECT info FROM tweets_parsed WHERE id_tweet=1 AND category='categoria';")
		info_resp=db.store_result().fetch_row()[0][0]
		
		assert "novia"==info_req
		assert "novia"==info_resp

	def test_succesful_matching(self):	
		test_tweet_request = [0, "#chile #sebusca Novia #contacto Pablo Cordella #location Martin Fierro 1234 #info buena presencia #status urgente","2010-01-01 00:00:00"]
		test_tweet_response = [1, "#chile #encontre Novia #contacto Felipe Garrido #location Principe de Gales","2010-01-01 00:00:00"]
		assert self.tweet_matcher.parse(test_tweet_request) == [tweetmatcher.REQ,[]]
		assert self.tweet_matcher.parse(test_tweet_response) == [tweetmatcher.RESP,['0']]
		
	def test_succesful_secondary_storage(self):
	    #seria ideal que esta cosa haga un tweet con referencia a ambos respecto al match
		#ie: "@pcordell @fgarrido hay match de Novia 1313"""
		test_tweet_request = [0, "#chile #sebusca Novia #contacto Pablo Cordella #location Martin Fierro 1234 #info buena presencia #status urgente","2010-01-01 00:00:00"]
		test_tweet_response = [1, "#chile #encontre Novia #contacto Felipe Garrido #location Principe de Gales","2010-01-01 00:00:00"]
		
		self.tweet_matcher.parse(test_tweet_request)
		self.tweet_matcher.parse(test_tweet_response)
		db=MySQLdb.connect("localhost","ttt","ttt","ttt_testing")
		db.query("SELECT contact FROM tweets_parsed WHERE id_tweet=0 AND category='categoria';")
		cont_req=db.store_result().fetch_row()[0][0]
		db.query("SELECT contact FROM tweets_parsed WHERE id_tweet=1 AND category='categoria';")
		cont_resp=db.store_result().fetch_row()[0][0]
		
		assert "felipe garrido"==cont_resp
		assert "pablo cordella"==cont_req
