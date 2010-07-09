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

	
def main(ini_filename):
    try:
        #connectors = config.get('CONFIG','connectors')
        #connectors = connectors.split(' ')
        #log.debug(connectors)

        #savers = []

        ini = IniReader(ini_filename)
		
        mysql_info = ini.get_mysql_info()
        mysql_host = mysql_info[0]
        mysql_port = mysql_info[1]
        mysql_user = mysql_info[2]
        mysql_pass = mysql_info[3]
        mysql_db_name = mysql_info[4]

        csv_info_path = ini.get_csv_info()

        log_saver = tweetsavers.TweetSaverLog(logging.getLogger('tweets'))
        csv_saver = tweetsavers.TweetSaverCSV(csv_info_path)
        mysql_saver = tweetsavers.TweetSaverMySQL(mysql_host, mysql_db_name, mysql_user, mysql_pass)
#        print ini.get_secondary_tag_list()
        listener = StreamWatcherListener(ini.get_secondary_tag_list(),ini.get_username(), ini.get_password(), [log_saver, csv_saver, mysql_saver])
        stream = tweepy.Stream(ini.get_username(),
                                ini.get_password(),
                                listener,
                                timeout = None)
#		track_list = [k.strip() for k in PRIMARY_TRACK_LIST.split(',')]
#		track_list = [k.strip() for k in ini.get_primary_tag_list().split(' ')]
        track_list = [k.strip() for k in ini.get_primary_tag_list()]

        stream.filter(track = track_list)
    except KeyboardInterrupt:
        print '\nCiao!'

import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "USO: TTT_retriever [archivo ini]"
    else:
	    main(sys.argv[1])
