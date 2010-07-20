import MySQLdb
from ini_reader import IniReader
import tweetmatcher
import pdb

class TweetDispatcher(object):

	def __init__(self, file_path):

		ini = IniReader(file_path)
		mysql_info = ini.get_mysql_info()
		mysql_host = mysql_info[0]
		mysql_port = mysql_info[1]
		mysql_user = mysql_info[2]
		mysql_pass = mysql_info[3]
		mysql_db_name = mysql_info[4]



		categorias = ini.get_categories()
		diccionario = ini.get_categories_req_resp()

		location = ini.get_info_location()
		contact = ini.get_info_contact()
		name = ini.get_info_name()

		for categoria in categorias:

			requests = diccionario[(categoria, 'request')]
			responses = diccionario[(categoria, 'response')]

			tweet_matcher = tweetmatcher.TweetMatcher(categoria, requests, responses,location,contact,name,[mysql_host,mysql_user,mysql_pass,mysql_db_name])

			tweets = self.tweet_reader(mysql_host, mysql_user, mysql_pass, mysql_db_name)
			rows = tweets.fetch_row(0)
			for tweet in rows: #tweet[0] = id, #tweet[1] = text
				tupla  = [tweet[0], tweet[1], tweet[2]]
				[type,text] = tweet_matcher.parse(tupla)
				if text:
					#TODO: hacer update a los tweets con el id, que esta en text[0]
					#acutalizar el dispatcher para leer del diccionario
					#modificar el mysql para que lea los parametros de la bd del .ini
					#ponerse de acuerdo que hacer cuando se hace un match
					if type==tweetmatcher.REQ:
						map(lambda x:self.tweet_match(mysql_host,mysql_user,mysql_pass,mysql_db_name,x,tweet[0]),text)
					elif type==tweetmatcher.RESP:
						map(lambda x:self.tweet_match(mysql_host,mysql_user,mysql_pass,mysql_db_name,tweet[0],x),text)


	def tweet_reader(self, host, user, passwd, db):
		self.db =  MySQLdb.connect(host, user, passwd, db)
		sql = "SELECT tweet_id, text, time FROM tweets"
		self.db.query(sql)
		return self.db.store_result()

	def tweet_match(self, host, user, passwd, db, request_id, response_id):
		self.db =  MySQLdb.connect(host, user, passwd, db)
		sql = "INSERT INTO tweets_matched(request_id, response_id,date) VALUES(%s, %s,NOW());" % (request_id, response_id)
		self.db.query(sql)

if __name__ == '__main__':
	asdf=TweetDispatcher("config-chile.ini")
