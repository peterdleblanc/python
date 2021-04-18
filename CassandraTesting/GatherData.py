
__author__ = 'Peter LeBlanc'

from cqlengine import columns
from cqlengine.models import Model
from cqlengine import connection
from cqlengine.management import sync_table

import feedparser
import datetime
import hashlib

class Gdacs(Model):
    title = columns.Text()
    published = columns.DateTime()
    harvested = columns.DateTime(default=datetime.datetime.today())
    description = columns.Text(primary_key=True)
    link = columns.Text()
    country = columns.Text()
    lat = columns.Text()
    long = columns.Text()
    event_type = columns.Text()
    alert_level = columns.Text()
    event_id = columns.Text()
    epsoide_id = columns.Text()
    severity = columns.Text()
    population = columns.Text()

    def __repr__(self):
        return  '%s %d %' (self.record_num, self.title)

def create_test_record():
    # Connect to the demo keyspace on our cluster running at 127.0.0.1
    connection.setup(['127.0.0.1'], "rss_webservice")

    # Sync your model with your cql table
    sync_table(Gdacs)

    Gdacs.create(record_num='1', title='Test Title', published='2015/05/04')

def get_gdacs_hurricane_data():
    ### RSS Feed to harvest ###
    d = feedparser.parse('http://www.gdacs.org/XML/RSS.xml')

    # Connect to the demo keyspace on our cluster running at 127.0.0.1
    connection.setup(['127.0.0.1'], "rss_webservice")

    # Sync your model with your cql table
    sync_table(Gdacs)


    for post in d.entries:
            publishedDate = str(post.published_parsed[0]) + '-' + str(post.published_parsed[1]) + '-' + str(post.published_parsed[2])
            Gdacs.create(
            title = post.title,
            published = dateof(publishedDate),
            description = post.description,
            link = post.link,
            country = post.gdacs_country,
            lat = post.geo_lat,
            long = post.geo_long,
            event_type = post.gdacs_eventtype,
            alert_level = post.gdacs_alertlevel,
            event_id = post.gdacs_eventid,
            epsoide_id = post.gdacs_episodeid,
            severity = post.gdacs_severity['value'],
            population = post.gdacs_population['value'])

def main():
    get_gdacs_hurricane_data()


if __name__ == '__main__':
    main()
    
