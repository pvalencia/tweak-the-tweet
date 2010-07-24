import unittest
import tweetreporter
import MySQLdb

class TestTweetReporterIntegracionBD(unittest.TestCase):
	
	def setUp(self):
		db=MySQLdb.connect("localhost","ttt","ttt","ttt_testing")
		db.query("truncate tweets_matched;")
		db.query("truncate tweets_parsed;")
		sql1="INSERT INTO `ttt_testing`.`tweets_parsed` (`id_tweet` ,`type` ,`category` ,`info` ,`contact` ,`location` ,`name` ,`time`) VALUES ('1', 'request', 'PEOPLE', 'papelucho', 'la mama', 'Chile', '', '2010-07-01 00:00:0');"
		sql2="INSERT INTO `ttt_testing`.`tweets_parsed` (`id_tweet` ,`type` ,`category` ,`info` ,`contact` ,`location` ,`name` ,`time`) VALUES ('2', 'response', 'PEOPLE', 'papelucho', 'el viejo del saco', 'Valparaiso', '', '2010-07-02 00:00:0');"
		sql3="INSERT INTO `ttt_testing`.`tweets_matched` (`request_id`, `response_id`, `date`, `type`) VALUES ('1', '2', '2010-07-03 00:00:0', 'PEOPLE');"
		db.query(sql1)
		db.query(sql2)
		db.query(sql3)
		db.close()
		self.tr=tweetreporter.TweetReporter("testing.ini")
		
	def test_readpairs(self):
		pairs=self.tr.match_finder("2010-01-01 00:00:00")
		assert pairs[0]==('1','2','PEOPLE')

	def test_readtweets(self):
		tweets=self.tr.tweet_finder((('1','2','PEOPLE'),))
		assert map(lambda x:str(x),tweets[0])==['1', 'request', 'PEOPLE', 'papelucho', 'la mama', 'Chile', '', '2010-07-01 00:00:00', '2', 'response', 'PEOPLE', 'papelucho', 'el viejo del saco', 'Valparaiso', '', '2010-07-02 00:00:00']
		
