import MySQLdb
from ini_reader import IniReader
from mock import Mock
import tweetmatcher

class TweetDispatcher(object):

	def __init__(self, file_path):	
		dict = []
		dict.append("PEOPLE")
		for itera in dict:
			
			self.expected_requests = ["#busco", "#sebusca", "#ruok", "#need"]
			self.expected_responses = ["#encontre","#seencontro","#imok","#found"]
			self.expected_location = ["#sitio","#location","#en","#loc","#zona","#localidad","#gps"," #lugar"]
			self.expected_contact = ["#contacto","#contact","#contactar","#con","#cont","#avisar","#telefono","#fono","#tel","#cel"]
			self.expected_name = ["#name","#nombre"]
			self.tweet_matcher = tweetmatcher.TweetMatcher(self.expected_requests, self.expected_responses,self.expected_location,self.expected_contact,self.expected_name)
			
			tweets = self.tweet_reader('localhost', 'ttt', 'ttt', 'haiti_db')
			rows = tweets.fetch_row(0)
			for tweet in rows: #tweet[0] = id, #tweet[1] = text
				#print tweet
				tupla  = [tweet[0], tweet[1]]				
				text = self.tweet_matcher.parse(tupla)
				print text
				if ( text != [] ):
					#TODO: hacer update a los tweets con el id, que esta en text[0]
					#acutalizar el dispatcher para leer del diccionario
					#modificar el mysql para que lea los parametros de la bd del .ini
					#ponerse de acuerdo que hacer cuando se hace un match
					print text
					
				
	def tweet_reader(self, host, user, passwd, db):
		self.db =  MySQLdb.connect(host, user, passwd, db)		
		sql = "SELECT id, text FROM  tweets"
		self.db.query(sql)
		return self.db.store_result()					
			
#necesitamos del ini_reader
#lista con nombre de categoria
#los datos de la base de datos
#la lista de contactos, location y name
		