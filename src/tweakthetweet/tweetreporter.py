import MySQLdb, csv
from ini_reader import IniReader

class TweetReporter(object):
	def __init__(self, file_path):
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
		sql = "SELECT request_id, response_id, type FROM tweets_matched WHERE date > '%s';" % min_date
		self.cursor.execute(sql)
		return self.cursor.fetchall()
		
	def tweet_finder(self, matrix):
		result=[]
		for row in matrix:
			match=[]
			sql1 =  "SELECT * FROM tweets_parsed WHERE id_tweet = '%s' AND category = '%s';" % (row[0],row[2])
			self.cursor.execute(sql1)
			match = list(self.cursor.fetchall()[0])
			sql2 =  "SELECT * FROM tweets_parsed WHERE id_tweet = '%s' AND category = '%s';" % (row[1],row[2])
			self.cursor.execute(sql2)
			match += list(self.cursor.fetchall()[0])
			result.append(match)
		return result
			
	def __call__(self,output_path):
		pares=self.match_finder(self.date)
		matches=self.tweet_finder(pares)
		self.write_csv(output_path,matches)
		
	def write_csv(self,path_file,tweets_list):
		writer = csv.writer(open(path_file,'w'), delimiter=';', dialect='excel')
		writer.writerow(['id_tweet','type','category','info','contact','location','name','time','id_tweet','type','category','info','contact','location','name','time'])
		for tweets in tweets_list:
			writer.writerow(tweets)
			
if __name__=="__main__":
	t=TweetReporter("2010-01-01 0:00:00","config-chile.ini")
	t("asdf.csv")

