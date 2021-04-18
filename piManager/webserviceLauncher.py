__author__ = 'Peter LeBlanc'

import cherrypy
import threading
import webserviceHome
import startpiManager
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(__name__)
Base = declarative_base()

class ThreadManagerTable(Base):
    '''
   ThreadManagerTable class is a ORM for the managerThreads table
    '''
    __tablename__ = 'managerThreads'

    id = Column(Integer, primary_key=True)
    name = Column(String(250),nullable=False)
    threadType = Column(String(40),nullable=False)
    status = Column(String(40),nullable=False)
    flagged = Column(String(10),nullable=False)


class Launcher(object):
    logging.basicConfig(level=logging.DEBUG)
    handler = logging.FileHandler('./logs/webservice_launcher.log')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(threadName)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    def __init__(self):
        threading.Thread.__init__(self, name='homeWebservice')
        self.sync = threading.Condition()
        self.engine = create_engine('sqlite:///ThreadManager.db')
        self.DBSession = sessionmaker(bind=self.engine)


    def startHomeWebservice(self):
        pi = startpiManager.PIManager()
        with self.sync:
            cherrypy.server.socket_port = 8080
            cherrypy.server.socket_host = '0.0.0.0'
            cherrypy.tree.mount(webserviceHome.Home(), "/", './conf/config.conf')
            cherrypy.engine.start()

        #cherrypy.engine.block()

        Base.metadata.bind = self.engine
        session = self.DBSession()
        session.autocommit = True
        newThread = ThreadManagerTable(name='homeWebservice', threadType='webservice', status='active', flagged='no')
        session.add(newThread)
        #pi.startMidiMonitor()

    def stopHomeWebservice(self):
        with self.sync:
            cherrypy.engine.exit()
            cherrypy.server.stop()
