import MySQLdb
from ini_reader import IniReader

class TweetReporter(object):
	def __init__(self, date, file_path):
		self.date = date
		ini = IniReader(file_path)
		mysql_info = ini.get_mysql_info()
		self.host = mysql_info[0]
		self.port = mysql_info[1]
		self.user = mysql_info[2]
		self.passwd = mysql_info[3]
		self.db_name = mysql_info[4]
		self.db =  MySQLdb.connect(host = self.host , user = self.user ,passwd = self.passwd ,db = self.db_name)
		self.cursor = self.db.cursor()
		

	def match_finder(self, min_date):
		sql = "SELECT request_id, response_id FROM tweets_matched WHERE date > '%s' %(min_date)";
		self.cursor.execute(sql)
        return self.fetchall()
		
	def tweet_finder(self, matrix):
		for row in matrix:
			sql =  "SELECT * FROM tweets_parsed WHERE id_tweet = '%s' %(row[0]) OR id_tweet = '%s' %(row[1])"
			self.cursor.execute(sql)
			data = self.fetchall()
			
