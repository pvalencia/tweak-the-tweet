import re
class TweetMatcher(object):
	
	def __init__(self, requests, responses, location,contact,name):
		self.requests = requests
		self.responses = responses
		self.location= location
		self.contact= contact
		self.name = name
		self.parsed_requests = []
		self.parsed_responses = []
		
	def parse(self, tweet):
		result = self.get_value(tweet, self.requests)
		if result:
			result_listed_info = []
			
			result_listed_info.append(result)
			result_listed_info.append(self.get_value(tweet, self.location))
			result_listed_info.append(self.get_value(tweet, self.contact))
			result_listed_info.append(self.get_value(tweet, self.name))
			
			self.parsed_requests.append(result_listed_info)
			matches = []
			for itera_tweet in self.parsed_responses:
				if itera_tweet[0] == result:
					matches.append(itera_tweet)
			return matches
		result = self.get_value(tweet, self.responses)
		if result:
			result_listed_info = []
			
			result_listed_info.append(result)
			result_listed_info.append(self.get_value(tweet, self.location))
			result_listed_info.append(self.get_value(tweet, self.contact))
			result_listed_info.append(self.get_value(tweet, self.name))
			
			self.parsed_responses.append(result_listed_info)
			matches = []
			for itera_tweet in self.parsed_requests:
				if itera_tweet[0] == result:
					matches.append(itera_tweet)
			return matches
		return []
			
	def get_value(self, tweet, type):
		result = re.search('('+ (' |').join(type) + ')([^#]*)', tweet)
		if result:
			return result.group(2).strip().lower()
		return ""
		
	
	def secondary_info(self, tweet, str):
		result = re.search('('+ ('|').join(str) + ')([^#]*)(.*)', tweet)
		if result:
			return result.group(3).strip().lower()
		return ""