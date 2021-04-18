__author__ = 'Peter LeBlanc'

from cqlengine import columns
from cqlengine.models import Model
from cqlengine import connection
from cqlengine.management import sync_table

import feedparser
import datetime
import hashlib

class patients(Model):    patient_id = columns.Integer(primary_key=True)
    patient_name = columns.Text()
    doctors_id = columns.Integer()
    date_created = columns.DateTime()
    date_updated = columns.DateTime(default=datetime.datetime.today())
    prescription = columns.Text()
    amount_thc = columns.Integer()

    def __repr__(self):
        return  '%s %d %' (self.record_num, self.title)
    # Connect to the demo keyspace on our cluster running at 127.0.0.1
    connection.setup(['127.0.0.1'], "rss_webservice")

    # Sync your model with your cql table
    sync_table(patients)

def update_patient_record():
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