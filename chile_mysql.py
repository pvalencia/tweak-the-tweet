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
PRIMARY_TRACK_LIST = "#chile, #earthquake, #tsunami, #terremotochile, #fuerzachile"

# Secondary filter, must be a regex.
SECONDARY_REGEX_FILTER = '#(need|offer|have|closed|open|taybien|toybien|tavivo|necesidad|tengo|tenemos|imok|ruok|missing|evac|damage|estasbien|estabien|estoybien|todobien|survivor|sebusca)'

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class StreamWatcherListener(tweepy.StreamListener):
    prog = re.compile(SECONDARY_REGEX_FILTER,
                      re.IGNORECASE)

    def __init__(self, u, p, savers):
        self.auth = tweepy.BasicAuthHandler(username = u,
                                            password = p)
        self.api = tweepy.API(auth_handler = self.auth,
                              secure=True,
                              retry_count=3)
        self.savers = savers

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

import ConfigParser

def main():
    try:
        config = ConfigParser.ConfigParser()
        config.read('config-chile.ini')
        username = config.get('CONFIG','twitter_user')
        password = config.get('CONFIG','twitter_pass')
        
        #connectors = config.get('CONFIG','connectors')
        #connectors = connectors.split(' ')
        #log.debug(connectors)
        
        #savers = []
        
        log_saver = tweetsavers.TweetSaverLog(logging.getLogger('tweets'))
        csv_saver = tweetsavers.TweetSaverCSV('tweets.csv')
        mysql_saver = tweetsavers.TweetSaverMySQL('localhost', 'test', 'tweakthetweet', 'tweakthetweet')
        listener = StreamWatcherListener(username, password, [log_saver, csv_saver, mysql_saver])
        stream = tweepy.Stream(username,
                               password,
                               listener,
                               timeout = None)
        track_list = [k.strip() for k in PRIMARY_TRACK_LIST.split(',')]

        stream.filter(track = track_list)
    except KeyboardInterrupt:
        print '\nCiao!'

if __name__ == '__main__':
    main()
