__author__ = 'peter'



from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement


def count(host, cf):
    keyspace = "identification"
    cluster = Cluster([host], port=9042, control_connection_timeout=600000000)
    session = cluster.connect(keyspace)
    session.default_timeout=600000000

    host = HostConnectionPool(['127.0.0..1'])
    session = host._connections('rss_webservice')

if __name__ == '__main__':
    main()