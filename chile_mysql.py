#!/usr/bin/env python
# A #Haiti Twitter stream listener for TweakTheTweet using Tweepy.
# Requires Python 2.6
# Requires Tweepy http://github.com/joshthecoder/tweepy
# http://creativecommons.org/licenses/by-nc-sa/3.0/us/
# Based on: http://github.com/joshthecoder/tweepy-examples
# Modifications by @ayman

from textwrap import TextWrapper
import tweepy
import re
import tweetsavers

# Primary Filter, can be a comma seperated list.
# PRIMARY_TRACK_LIST = "#chile, #earthquake, #tsunami, #terremotochile, #fuerzachile"

# Secondary filter, must be a regex.
# SECONDARY_REGEX_FILTER = '#(need|offer|have|closed|open|taybien|toybien|tavivo|necesidad|tengo|tenemos|imok|ruok|missing|evac|damage|estasbien|estabien|estoybien|todobien|survivor|sebusca)'

import logging
from ini_reader import IniReader
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class StreamWatcherListener(tweepy.StreamListener):
	

	def __init__(self, secondary_tag_list, u, p, savers):
		self.auth = tweepy.BasicAuthHandler(username = u,
											password = p)
		self.api = tweepy.API(auth_handler = self.auth,
							  secure=True,
							  retry_count=3)
		self.savers = savers
		secondary_tag_string='#('+'|'.join(map(lambda x: x[1:],secondary_tag_list))+')'
		self.prog = re.compile(secondary_tag_string,re.IGNORECASE)

	def on_status(self, status):
		log.debug(status.text)

		if self.prog.search(status.text):
			for saver in self.savers:
				saver.save_raw_tweet(status.text,
										status.author.screen_name,													  
										status.id,
										status.source,												   
										status.created_at)

	def on_limit(self, track):
		log.error('Limit hit! Track = %s' % track)

	def on_error(self, status_code):
		log.warn('An error has occured! Status code = %s' % status_code)
		return True # keep stream alive

	def on_timeout(self):
		log.error('Timeout: Snoozing Zzzzzz')



	
def main():
	try:
		#connectors = config.get('CONFIG','connectors')
		#connectors = connectors.split(' ')
		#log.debug(connectors)
		
		#savers = []
		
		ini = IniReader('config-chile.ini')
		
		log_saver = tweetsavers.TweetSaverLog(logging.getLogger('tweets'))
		csv_saver = tweetsavers.TweetSaverCSV('tweets.csv')
		mysql_saver = tweetsavers.TweetSaverMySQL('localhost', 'haiti_db', 'ttt', 'ttt')
		print ini.get_secondary_tag_list()
		listener = StreamWatcherListener(ini.get_secondary_tag_list(),ini.get_username(), ini.get_password(), [log_saver, csv_saver, mysql_saver])
		stream = tweepy.Stream(ini.get_username(),
							   ini.get_password(),
							   listener,
							   timeout = None)
#		track_list = [k.strip() for k in PRIMARY_TRACK_LIST.split(',')]
		track_list = [k.strip() for k in ini.get_primary_tag_list().split(' ')]

		stream.filter(track = track_list)
	except KeyboardInterrupt:
		print '\nCiao!'

if __name__ == '__main__':
	main()
