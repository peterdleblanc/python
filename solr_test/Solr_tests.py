
__author__ = 'Peter LeBlanc'

import feedparser
import hashlib
import json
import urllib2
from urllib2 import *
import itertools
import logging
import datetime
import time
from cqlengine import columns
from cqlengine.models import Model
from cqlengine import connection
from cqlengine.management import sync_table
import solr


from HTMLParser import HTMLParser


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

## Create a file handler
handler = logging.FileHandler('./logs/solr_tests.log')
handler.setLevel(logging.DEBUG)
## create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
## Add the handler to the logger
logger.addHandler(handler)

class usgs_eq_data(Model):

    event_id = columns.Text(primary_key=True)
    title = columns.Text()
    longitude = columns.Float()
    latitude = columns.Float()
    depth = columns.Float()
    mag = columns.Float()
    place = columns.Text()
    event_time = columns.DateTime()
    url = columns.Text()
    felt = columns.Integer()
    cdi = columns.Integer()
    mmi = columns.Text()
    alert = columns.Text()
    status = columns.Text()
    tsunami = columns.Integer()
    sig = columns.Integer()
    net = columns.Text()
    code = columns.Text()
    ids = columns.Text()
    sources = columns.Text()
    types = columns.Text()
    nst = columns.Text()
    dmin = columns.Float()
    rms = columns.Float()
    gap = columns.Text()
    magType = columns.Text()
    type = columns.Text()
    harvest_date = columns.DateTime(default=datetime.datetime.today())

    def __repr__(self):
        return  '%s %d %' (self.record_num, self.title)


def get_usgs_place_name():

    # create a connection to a solr server
    s = solr.SolrConnection('http://localhost:8983/solr/usgs_eq_data')

    # do a search
    print('getting list of events from solr')
    event_ids=[]
    response = s.query('place:*Nepal*')
    for hit in response.results:
        event_ids.append(hit['event_id'][0])

    # Connect to the demo keyspace on our cluster running at 127.0.0.1
    connection.setup(['127.0.0.1'], "usgs_eq_data")

    # Sync your model with your cql table
    sync_table(usgs_eq_data)

    print('querying cassandra')
    for x in event_ids:
        print(x)
        record=usgs_eq_data.get(event_id=x)
        print(record['event_id'])
        print(record['place'])
        print(record['mag'])
        print(record['alert'])

    print('done')

def check_solr():

    #connection = urlopen('http://localhost:8983/solr/gettingstarted/select?q=*plugin*&wt=python')
    connection = urlopen('http://localhost:8983/solr/gettingstarted_shard2_replica2/select?q=*plugin*&wt=python')
    response = eval(connection.read())
    for document in response['response']['docs']:
        print("  Name =", document['title'])

    print('json response')

    connection = urlopen('http://localhost:8983/solr/gettingstarted/select?q=*peter*&wt=json')
    response = json.load(connection)
    print(response['response']['numFound'], "documents found.")

    # Print the name of each document.

    for document in response['response']['docs']:
        print("  Name =", document['title'])

def create_solr_entry():
    # create a connection to a solr server
    s = solr.SolrConnection('http://localhost:8983/solr/usgs_eq_data')

    # add a document to the index
    s.add(id=1, title='my test entry', event_id=['peter'])
    s.commit()

    # do a search
    response = s.query('title:my test doc')
    for hit in response.results:
        print(hit['title'])


    #response = s.query('title:test', facet='true', facet_field='date')
    #for hit in response.results:
    #    print hit['title']

    #response = s.query('title:test', facet='true', facet_field=['date', 'id'])
    #for hit in response.results:
    #    print hit['title']


def do_solr_search():

    # create a connection to a solr server
    s = solr.SolrConnection('http://localhost:8983/solr/usgs_eq_data')

    # do a search
    response = s.query('place:*Nepal*')
    for hit in response.results:
        print(hit['event_id'])




def main():

    #check_solr()
    #create_solr_entry()
    #do_solr_search()
    get_usgs_place_name()






if __name__ == '__main__':
    main()
