
__author__ = 'Peter LeBlanc'

from cqlengine import columns
from cqlengine.models import Model
from cqlengine import connection
from cqlengine.management import sync_table

import feedparser
import datetime
import logging
import hashlib
import json
import urllib2


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

## Create a file handler
handler = logging.FileHandler('usgs_eq_harvester.log')
handler.setLevel(logging.DEBUG)
## create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
## Add the handler to the logger
logger.addHandler(handler)


#create index on RSS_Webservice.usgs_eq_data (place);

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

def get_usgs_eq_data():

    response = urllib2.urlopen('http://earthquake.usgs.gov/fdsnws/event/1/query.geojson?starttime=2015-01-01%2000:00:00&minmagnitude=3&endtime=2015-02-01%2023:59:59&orderby=time')

    logger.info('###############Query Range: 2015-01-01 to  2015-02-01######################################')
    data = json.load(response)
    logger.info('starting json request')
    list_of_events = []
    for x in data['features']:
        for k,v in x['properties'].items():
            if k == 'detail':
                list_of_events.append(v)


    logger.info('################Getting Event Count#######################')
    count = 0
    for x in list_of_events:
        count = count + 1
    logger.info('Total event count: ' + str(count))

    logger.info('getting details')
    event_record = {}

    # Connect to the demo keyspace on our cluster running at 127.0.0.1
    connection.setup(['127.0.0.1'], "rss_webservice")

    # Sync your model with your cql table
    sync_table(usgs_eq_data)

    for event in list_of_events:
        logger.info('#####' + event + '#####')
        response = urllib2.urlopen(event)
        data = json.load(response)
        event_time = data['properties']['time']
        event_time_conv = datetime.datetime.fromtimestamp(event_time/1000)
        logger.info(event_time_conv)
        usgs_eq_data.create(
        event_id = (data['id']),
        title = (data['properties']['title'].encode('utf-8').replace("'","''")),
        longitude = (data['geometry']['coordinates'][0]),
        latitude = (data['geometry']['coordinates'][1]),
        depth = (data['geometry']['coordinates'][2]),
        mag = (data['properties']['mag']),
        place = (data['properties']['place'].replace("'", "''")),
        event_time = event_time_conv,
        url = (data['properties']['url']),
        felt = (data['properties']['felt']),
        cdi = (data['properties']['cdi']),
        mmi = str((data['properties']['mmi'])),
        alert = (data['properties']['alert']),
        status = (data['properties']['status']),
        tsunami = (data['properties']['tsunami']),
        sig = (data['properties']['sig']),
        net = (data['properties']['net']),
        code = (data['properties']['code']),
        ids = (data['properties']['ids']),
        sources = (data['properties']['sources']),
        types = (data['properties']['types']),
        nst = str((data['properties']['nst'])),
        dmin = (data['properties']['dmin']),
        rms = (data['properties']['rms']),
        gap = str((data['properties']['gap'])),
        magType = (data['properties']['magType']),
        type = (data['properties']['type']))


    # Connect to the demo keyspace on our cluster running at 127.0.0.1
    connection.setup(['127.0.0.1'], "rss_webservice")

    # Sync your model with your cql table
    sync_table(usgs_eq_data)


    logger.info('Inserted: ' + str(len(list_of_events)))

    logger.info('json Population Complete')


def main():
    get_usgs_eq_data()

if __name__ == '__main__':
    main()
