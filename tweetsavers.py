from __future__ import with_statement
from textwrap import TextWrapper
import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class TweetSaverLog(object):
    def __init__(self, log):
        self.log = log

    status_wrapper = TextWrapper(width=70,
                                 initial_indent=' ',
                                 subsequent_indent=' ')

    def save_raw_tweet( self, text, author, tweet_id, source, time ):
        self.log.info(self.status_wrapper.fill(text))
        self.log.info('%s %s via %s #%s\n' % (
                                       author,
                                       time,
                                       source,
                                       tweet_id))

import csv, os
class TweetSaverCSV(object):
    def __init__(self, filename):
        self.filename = filename
        if not os.path.isfile(self.filename):
            self.writerow(['text', 'author', 'tweet_id', 'source', 'time'])

    def writerow(self,row):
        with open(self.filename, 'a') as destfile:
            writer = csv.writer(destfile, delimiter=';', dialect='excel')
            writer.writerow(row)

    def save_raw_tweet(self, text, author, tweet_id, source, time ):
        self.writerow([text, author, tweet_id, source, time])

import MySQLdb
import traceback,sys
class TweetSaverMySQL(object):
    def __init__(self, host, db, user, passwd):
        self.db =  MySQLdb.connect(host = host, user = user ,passwd = passwd ,db = db)
        self.cursor = self.db.cursor()

    def save_raw_tweet(self, text, author, tweet_id, source, time ):
        sql = "INSERT INTO tweets (text, author, tweet_id, source, time) VALUES  ('%s', '%s', '%s', '%s', '%s' )" %  (text, author, tweet_id, source, time)
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Commit your changes in the database
            self.db.commit()
            log.info('MySQL Commit')

        except:
            # Rollback in case there is any error
            self.db.rollback()
            log.info('MySQL Rollback')
            traceback.print_exc(file=sys.stdout)




