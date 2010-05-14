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

# Primary Filter, can be a comma seperated list.
PRIMARY_TRACK_LIST = "#chile, #earthquake, #tsunami, #terremotochile, #fuerzachile"

# Secondary filter, must be a regex.
SECONDARY_REGEX_FILTER = '#(need|offer|have|closed|open|taybien|toybien|tavivo|necesidad|tengo|tenemos|imok|ruok|missing|evac|damage|estasbien|estabien|estoybien|todobien|survivor|sebusca)'

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

class TweetSaverLog(object):
    status_wrapper = TextWrapper(width=70,
                                 initial_indent=' ',
                                 subsequent_indent=' ')

    def save_raw_tweet( self, text, author, tweet_id, source, time ):
        log.info(self.status_wrapper.fill(text))                            
        log.info('%s %s via %s #%s\n' % ( 
                                       author,
                                       time,
                                       source,
                                       tweet_id))


class StreamWatcherListener(tweepy.StreamListener):
    prog = re.compile(SECONDARY_REGEX_FILTER,
                      re.IGNORECASE)

    def __init__(self, u, p, saver):
        self.auth = tweepy.BasicAuthHandler(username = u,
                                            password = p)
        self.api = tweepy.API(auth_handler = self.auth,
                              secure=True,
                              retry_count=3)
        self.saver = saver

    def on_status(self, status):
        log.debug(status.text)

        if self.prog.search(status.text):

            self.saver.save_raw_tweet(status.text,
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
        username = 'TtTReadChile'
        password = 'TtT4Chile'
        
        saver = TweetSaverLog()
        listener = StreamWatcherListener(username, password, saver)
        stream = tweepy.Stream(username,
                               password,
                               listener,
                               timeout = None)
        track_list = [k for k in PRIMARY_TRACK_LIST.split(',')]

        stream.filter(track = track_list)
    except KeyboardInterrupt:
        print '\nCiao!'

if __name__ == '__main__':
    main()
