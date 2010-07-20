import MySQLdb
import re

REQ=1
RESP=2

class TweetMatcher(object):

	def __init__(self, category,requests, responses, location, contact, name, db_conf):
		self.category=category
		self.requests = requests
		self.responses = responses
		self.location= location
		self.contact= contact
		self.name = name
		self.dbconf=db_conf
#		self.parsed_requests = []
#		self.parsed_responses = []
		
	def parse(self, tupla_tweet):
		tweet = tupla_tweet[1]
		result = self.get_value(tweet, self.requests) #si el tweet es un request, entonces result = novia
		if result:
			self.insert_bd('request',result,tupla_tweet) # insertar en bd
			matches = self.get_match_bd('response',result)
			matches = map(lambda x:x[0],matches.fetch_row(0))
			return [REQ,matches]
		result = self.get_value(tweet, self.responses)
		if result:					
			self.insert_bd('response',result,tupla_tweet)
			matches = self.get_match_bd('request',result)
			matches = map(lambda x:x[0],matches.fetch_row(0))
			return [RESP,matches]
		return [None,None]
			
	def get_value(self, tweet, type):
		result = re.search('('+ (' |').join(type) + ')([^#]*)', tweet)
		if result:
			return result.group(2).strip().lower()
		return ""
		
	
	def secondary_info(self, tweet, str):
		result = re.search('('+ ('|').join(str) + ')([^#]*)(.*)', tweet)
		if result:
			return result.group(3).strip().lower()
		return ""
		
	def insert_bd(self, type, info, tweet):
		categ=self.category
		loc=self.get_value(tweet[1],self.location)
		cont=self.get_value(tweet[1],self.contact)
		name=self.get_value(tweet[1],self.name)
		db =  MySQLdb.connect(self.dbconf[0], self.dbconf[1], self.dbconf[2], self.dbconf[3])
		sql = "INSERT INTO tweets_parsed(id_tweet,type,category,info,contact,location,name,time) VALUES(%s,'%s','%s','%s','%s','%s','%s','%s');" % (tweet[0],type,categ,info,cont,loc,name,tweet[2])
		db.query(sql)
		
	def get_match_bd(self,type,info):
		db =  MySQLdb.connect(self.dbconf[0], self.dbconf[1], self.dbconf[2], self.dbconf[3])
		info="%"+info+"%"
		sql = "SELECT id_tweet FROM tweets_parsed WHERE type='%s' AND info LIKE '%s';" % (type,info)
		db.query(sql)
		return db.store_result()

