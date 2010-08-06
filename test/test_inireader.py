from ini_reader import IniReader
import unittest

class TestIniReader(unittest.TestCase):
    def setUp(self):
        self.ini=IniReader("testing.ini")

    def test_get_configs(self):
        self.assertEquals(self.ini.get_username(),"twitter_user")
        self.assertEquals(self.ini.get_password(),"twitter_pass")

    def test_get_primary_tags(self):
        self.assertEquals(self.ini.get_primary_tag_list(),["#chile","#terremoto","#fmarepoto"])

    def test_get_secondary_tag_list(self):
        expected=["#estaibien","#missing","#ruok","#sebusca","#estaibien","#buscapersona","#estasbien","#tavivo","#estabien","#tabien","#estoybien","#todobien","#toybien","#imok","#survivor","#encontr","#found","#necesita","#need","#necesidad","#donacion","#ofrece","#tenemos","#tengo","#have","#offer","#dono","#closed","#open","#damage","#evac","#edificiocolapso"]
        expected.sort()
        got=self.ini.get_secondary_tag_list()
        got.sort()
        self.assertEquals(got,expected)
    
    def test_get_categories_req_resp(self):
        expected=dict([])
        expected[('PEOPLE','request')]= ["#estaibien","#missing","#ruok","#sebusca","#estaibien","#buscapersona","#estasbien"]
        expected[('PEOPLE','response')]=["#tavivo","#estabien","#tabien","#estoybien","#todobien","#toybien","#imok","#survivor","#encontr","#found"]
        expected[('HELP','request')]=["#necesita","#need","#necesidad"]
        expected[('HELP','response')]=["#donacion","#ofrece","#tenemos","#tengo","#have","#offer","#dono"]
        expected[('INFO','request')]=[]
        expected[('INFO','response')]=["#closed","#open","#damage","#evac","#edificiocolapso"]
        self.assertEquals(self.ini.get_categories_req_resp(),expected)

    def test_get_categories(self):
        self.assertEquals(self.ini.get_categories(),["PEOPLE","HELP","INFO"])

    def test_get_mysqlinfo(self):
        self.assertEquals(self.ini.get_mysql_info(),["localhost","3306","ttt","ttt","ttt_testing"])
    
    def test_get_info_tags(self):
        self.assertEquals(self.ini.get_info_contact(), ["#contacto","#contact", "#contactar", "#con", "#cont", "#avisar", "#telefono", "#fono", "#tel", "#cel"])
        self.assertEquals(self.ini.get_info_location(), ["#sitio","#location","#en","#loc","#zona","#localidad","#gps","#lugar"])
        self.assertEquals(self.ini.get_info_name(),["#name","#nombre"])

