import re
class TweetMatcher(object):
	
	def __init__(self, requests, responses):
		self.requests = requests
		self.responses = responses
		self.parsed_requests = []
		self.parsed_responses = []
		
	def parse(self, tweet):
		result = self.is_request(tweet)
		if result:			
			self.parsed_requests.append(result)
			matches = []
			for itera_tweet in self.parsed_responses:
				if itera_tweet == result:
					matches.append(itera_tweet)
			return matches
		result = self.is_response(tweet)
		if result:
			self.parsed_responses.append(result)			
			matches = []
			for itera_tweet in self.parsed_requests:
				if itera_tweet == result:
					matches.append(itera_tweet)
			return matches
		return []
			
	def is_request(self, tweet):
		result = re.search('('+ ('|').join(self.requests) + ')([^#]*)', tweet)
		if result:
			return result.group(2).strip().lower()
		return ""
		
	def is_response(self, tweet):
		result = re.search('('+ ('|').join(self.responses) + ')([^#]*)', tweet)
		if result:
			return result.group(2).strip().lower()
		return ""