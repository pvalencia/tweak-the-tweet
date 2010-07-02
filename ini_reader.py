
import ConfigParser
class IniReader(object):
	def __init__(self,file_path):
		config = ConfigParser.ConfigParser()
		config.read(file_path)
		self.username = config.get('CONFIG','twitter_user')
		self.password = config.get('CONFIG','twitter_pass')
		self.primary_tag_list = config.get('TAGS','situation')
		self.secondary_tag_list = dict([])
		primary_categories=config.get('TAGS','primary_categories')
		primary_categories=primary_categories.split(' ')
		for category in primary_categories:
			category_request_list=config.get(category,'request_tags').strip()
			category_request_list=category_request_list.split(' ')
			self.secondary_tag_list[(category,"request")]=category_request_list
			category_response_list=config.get(category,'response_tags').strip()
			category_response_list=category_response_list.split(' ')
			self.secondary_tag_list[(category,"response")]=category_response_list
		
	def get_username(self):
		return self.username
	
	def get_password(self):
		return self.password
	
	def get_primary_tag_list(self):
		return self.primary_tag_list
		
	def get_secondary_tag_list(self):
		return reduce(lambda x,y:x+y,self.secondary_tag_list.values(),[])
	
	def get_categories_req_resp(self):
		return self.secondary_tag_list