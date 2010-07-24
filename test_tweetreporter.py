from tweetreporter import TweetReporter
import unittest

class TestTweetReporter(unittest.TestCase):
	
	def test_writecsv(self):
		tr=TweetReporter("testing.ini")
		line=['cero', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve', 'diez', 'once', 'doce', 'trece', 'catorce', 'quince']
		tr.write_csv("test.csv",[line])
		f=open("test.csv","r")
		header=f.readline().strip()
		first=f.readline().strip()
		assert header=="id_tweet;type;category;info;contact;location;name;time;id_tweet;type;category;info;contact;location;name;time"
		assert first==";".join(line)
		
