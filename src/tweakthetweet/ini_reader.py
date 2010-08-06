
import ConfigParser

class IniReader(object):
    def __init__(self,file_path):
        config = ConfigParser.ConfigParser()
        config.read(file_path)
        self.username = config.get('CONFIG','twitter_user')
        self.password = config.get('CONFIG','twitter_pass')
        self.mysql_info = [config.get('MYSQL','host'),config.get('MYSQL','port'),config.get('MYSQL','user'),config.get('MYSQL','pass'),config.get('MYSQL','db_name')]
        self.csv_info = config.get('CSV','path').strip()
        self.primary_tag_list = config.get('TAGS','situation').split(' ')
        self.primary_tag_list = map(lambda x:x.strip(),self.primary_tag_list)
        self.infotags = dict([])
        self.infotags["name"] = self.__cleanlist(config.get('TAGS', 'name').split(' '))
        self.infotags["location"] = self.__cleanlist(config.get('TAGS', 'location').split(' '))
        self.infotags["contact"] = self.__cleanlist(config.get('TAGS', 'contact').split(' '))
        self.secondary_tag_list = dict([])
        self.primary_categories=config.get('TAGS','primary_categories')
        self.primary_categories=self.__cleanlist(self.primary_categories.split(' '))
        for category in self.primary_categories:
                category_request_list=config.get(category,'request_tags').split(' ')
                self.secondary_tag_list[(category,"request")]=self.__cleanlist(category_request_list)
                category_response_list=config.get(category,'response_tags').split(' ')
                self.secondary_tag_list[(category,"response")]=self.__cleanlist(category_response_list)
    
    def __cleanlist(self,l):
            ret=map(lambda x:x.strip(),l)
            ret=filter(lambda x:x!='',ret)
            return ret

    def get_username(self):
            return self.username
    
    def get_password(self):
            return self.password
    
    def get_primary_tag_list(self):
            return self.primary_tag_list
            
    def get_secondary_tag_list(self):
            return reduce(lambda x,y:x+y,self.secondary_tag_list.values())
    
    def get_categories_req_resp(self):
            return self.secondary_tag_list

    def get_categories(self):
            return self.primary_categories
    
    def get_mysql_info(self):
            return self.mysql_info

    def get_info_contact(self):
            return self.infotags["contact"]

    def get_info_location(self):
            return self.infotags["location"]

    def get_info_name(self):
            return self.infotags["name"]

    def get_csv_info(self):
        return self.csv_info
