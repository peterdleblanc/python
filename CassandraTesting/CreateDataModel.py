__author__ = 'Peter LeBlanc'

#import cql
import datetime

from cqlengine import columns
from cqlengine.models import Model
from cqlengine import connection
from cqlengine.management import sync_table


#### Run this manually ###
# CREATE KEYSPACE RSS_Webservice WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };


class Gdacs(Model):
    record_num = columns.Integer()
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

def create_gdacs_model():
    # Connect to the demo keyspace on our cluster running at 127.0.0.1
    connection.setup(['127.0.0.1'], "rss_webservice")

    # Sync your model with your cql table
    sync_table(Gdacs)


def main():
    create_gdacs_model()


if __name__ == '__main__':
    main()
