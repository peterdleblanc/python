__author__ = 'Peter LeBlanc'

from cqlengine import columns
from cqlengine.models import Model
from cqlengine import connection
from cqlengine.management import sync_table


class Gdacs(Model):
    record_num = columns.Integer(primary_key=True)
    title = columns.Text()
    published = columns.Text()
    #YEAR = columns.Text()
    #MONTH = columns.Text()
    #DAY = columns.Text()
    #DESCRIPTION = columns.Text()
    #HASHED DESC = columns.Text()
    #LINK = columns.Text()
    #Country = columns.Text()
    #lat = columns.Integer()
    #long = columns.Integer()
    #Event Type = columns.Text()
    #Alert Level = columns.Text()
    #Event ID = columns.Text()
    #Epsoide ID = columns.Text()
    #Severity = columns.Text()
    #Population = columns.Text()
    #gts link = columns.Text()
    def __repr__(self):
        return  '%s %d %' (self.record_num, self.title, self.published)

def read_record():



    # Connect to the demo keyspace on our cluster running at 127.0.0.1
    connection.setup(['127.0.0.1'], "rss_webservice")

    # Sync your model with your cql table
    sync_table(Gdacs)


    q=Gdacs.get(record_num=1)

    print(q['record_num'])
    print(q['title'])
    print(q['published'])

def main():
    read_record()

if __name__ == '__main__':
    main()
    
