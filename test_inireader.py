from chile_mysql import IniReader
import unittest

class TestIniReader(unittest.TestCase):
	def setUp(self):
		self.ini=IniReader("config-chile.ini")

	def test_get_configs(self):
		self.assertEquals(self.ini.get_username(),"TtTReadChile")
		self.assertEquals(self.ini.get_password(),"TtT4Chile")
		
	def test_get_primary_tags(self):
		self.assertEquals(self.ini.get_primary_tag_list(),["#chile","#terremoto","#fmarepoto"])

