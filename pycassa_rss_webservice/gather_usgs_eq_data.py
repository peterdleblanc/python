__author__ = 'Peter LeBlanc'

import pycassa
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily
from pycassa.index import *

##https://pycassa.github.io/pycassa/tutorial.html

import feedparser
import datetime
import logging
import hashlib


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

## Create a file handler
handler = logging.FileHandler('sql.log')
handler.setLevel(logging.INFO)
## create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
## Add the handler to the logger
logger.addHandler(handler)


def get_gdacs_hurricane_data():

def get_usgs_earthQuake_geoJSON_Feed():

    # Connect to the demo keyspace on our cluster running at 127.0.0.1
    pool = ConnectionPool('RSS_Webservice', ['localhost:9160'])

    response = urllib2.urlopen('http://earthquake.usgs.gov/fdsnws/event/1/query.geojson?starttime=2015-01-01%2000:00:00&minmagnitude=3&endtime=2015-02-01%2023:59:59&orderby=time')


    logger.info('###############Query Range: 2015-01-01 to  2015-05-01######################################')
    data = json.load(response)
    logger.info('starting json request')
    list_of_events = []
    for x in data['features']:
        for k,v in x['properties'].items():
            #logger.info(k + ': ' + str(v))
            if k == 'detail':
                list_of_events.append(v)
        #eq_record = dict(u.split(':') for u in x.split(','))
    ## reducing list of events

    logger.info('################Getting Event Count#######################')
    count = 0
    for x in list_of_events:
        count = count + 1
    logger.info('Total event count: ' + str(count))

    logger.info('getting details')
    event_record = {}

    seq_id = get_seq_value('USGS_EQ_DATA', 'seq_id')

    for event in list_of_events:
        seq_id = seq_id + 1
        logger.info('')
        logger.info('##################################' + event + '####################################')
        response = urllib2.urlopen(event)
        data = json.load(response)
        event_time = data['properties']['time']
        logger.info(event_time)
        event_time_conv = datetime.datetime.fromtimestamp(event_time/1000)

        logger.info(event_time_conv)
        event_record['event_id'] = (data['id'])
        event_record['title'] = (data['properties']['title'].encode('utf-8').replace("'","''"))
        event_record['longitude'] = (data['geometry']['coordinates'][0])
        event_record['latitude'] = (data['geometry']['coordinates'][1])
        event_record['depth'] = (data['geometry']['coordinates'][2])
        event_record['mag'] = (data['properties']['mag'])
        event_record['place'] = (data['properties']['place'].replace("'", "''"))
        event_record['event_time'] = event_time_conv
        event_record['url'] = (data['properties']['url'])
        event_record['felt'] = (data['properties']['felt'])
        event_record['cdi'] = (data['properties']['cdi'])
        event_record['mmi'] = (data['properties']['mmi'])
        event_record['alert'] = (data['properties']['alert'])
        event_record['status'] = (data['properties']['status'])
        event_record['tsunami'] = (data['properties']['tsunami'])
        event_record['sig'] = (data['properties']['sig'])
        event_record['net'] = (data['properties']['net'])
        event_record['code'] = (data['properties']['code'])
        event_record['ids'] = (data['properties']['ids'])
        event_record['sources'] = (data['properties']['sources'])
        event_record['types'] = (data['properties']['types'])
        event_record['nst'] = (data['properties']['nst'])
        event_record['dmin'] = (data['properties']['dmin'])
        event_record['rms'] = (data['properties']['rms'])
        event_record['gap'] = (data['properties']['gap'])
        event_record['magType'] = (data['properties']['magType'])
        event_record['type'] = (data['properties']['type'])
        event_record['seq_id'] = seq_id




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
