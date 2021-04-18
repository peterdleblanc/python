__author__ = 'Peter LeBlanc'

#import cql
import datetime

from cqlengine import columns
from cqlengine.models import Model
from cqlengine import connection
from cqlengine.management import sync_table


#### Run this manually ###
# CREATE KEYSPACE usgs_eq_data WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };


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

def create_gdacs_model():
    # Connect to the demo keyspace on our cluster running at 127.0.0.1
    connection.setup(['127.0.0.1'], "usgs_eq_data")

    # Sync your model with your cql table
    sync_table(usgs_eq_data)


def main():
    create_gdacs_model()


if __name__ == '__main__':
    main()