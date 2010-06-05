class TweetMatcher(object):
	
	def __init__(self, requests, responses):
		self.requests = requests
		self.responses = responses
		self.parsed_requests = []
		self.parsed_responses = []
		
	def parse(self, tweet):
		if self.is_request(tweet):
			pass
		for itera_tweet in self.parsed_requests:
			pass