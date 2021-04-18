__author__ = 'Peter LeBlanc'

import pycassa
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily

##https://pycassa.github.io/pycassa/tutorial.html

import feedparser
import datetime
import hashlib

def get_gdacs_hurricane_data():
    ### RSS Feed to harvest ###
    d = feedparser.parse('http://www.gdacs.org/XML/RSS.xml')

    # Connect to the demo keyspace on our cluster running at 127.0.0.1
    pool = ConnectionPool('RSS_Webservice', ['localhost:9160'])

    gdacs_fam = ColumnFamily(pool, 'gdacs')


    for post in d.entries:
            publishedDate = str(post.published_parsed[0]) + '-' + str(post.published_parsed[2]) + '-' + str(post.published_parsed[2])
            description = post.description
            title = post.title
            published = publishedDate
            link = post.link
            country = post.gdacs_country
            lat = post.geo_lat
            long = post.geo_long
            event_type = post.gdacs_eventtype
            alert_level = post.gdacs_alertlevel
            event_id = post.gdacs_eventid
            epsoide_id = post.gdacs_episodeid
            severity = post.gdacs_severity['value']
            population = post.gdacs_population['value']

            gdacs_fam.insert(str(datetime.datetime.now()),{'description':description})

def get_record():

    d = feedparser.parse('http://www.gdacs.org/XML/RSS.xml')
    # Connect to the demo keyspace on our cluster running at 127.0.0.1
    pool = ConnectionPool('RSS_Webservice', ['localhost:9160'])

    gdacs_fam = ColumnFamily(pool, 'gdacs')

    for post in d.entries:
        description = post.description
        results = gdacs_fam.get_range()
        count = 0
        for x in results:
            print(x)
            count = count + 1


        print(count)
        #print(gdacs_fam.get_range(start=''))

def main():
    #get_gdacs_hurricane_data()
    get_record()

if __name__ == '__main__':
    main()
