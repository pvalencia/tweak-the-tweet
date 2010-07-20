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
		sql = "SELECT request_id, response_id, type FROM tweets_matched WHERE date > '%s' %(min_date)";
		self.cursor.execute(sql)
        return self.fetchall()
		
	def tweet_finder(self, matrix):
		result=[]
		for row in matrix:
			match=[]
			sql1 =  "SELECT * FROM tweets_parsed WHERE id_tweet = '%s';" % (row[0],row[2])
			self.cursor.execute(sql1)
			match = list(self.fetchall()[0])
			sql2 =  "SELECT * FROM tweets_parsed WHERE id_tweet = '%s';" % (row[1],row[2])
			self.cursor.execute(sql2)
			match += list(self.fetchall()[0])
			result.append(match)
		result
			
	def __call__(self,output_path):
		pares=match_finder(self.date)
		writer = csv.writer(open(output_path,'w'), delimiter=';', dialect='excel')
		for match in tweet_finder(pares):
			writer.writerow(match)
			
if __name__=="__main__":
	t=TweetDispatcher("config-chile.ini")
	t("asdf.csv")
