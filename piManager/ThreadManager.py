__author__ = 'peter'

import threading
import os
import sqlite3
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

class ThreadManager(ThreadManagerTable):
    '''
    ThreadManager class is a class that manages a list of threads and attributes
        in a sqlite database so that threads can be maintain by either a internal or external client
    '''
    logging.basicConfig(level=logging.DEBUG)
    handler = logging.FileHandler('./logs/ThreadManager.log')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(threadName)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    def __init__(self):
        self.sql = ''
        self.engine = create_engine('sqlite:///ThreadManager.db')
        self.DBSession = sessionmaker(bind=self.engine)
        self.threads=[]

    def createThreadManagerTable(self):
        '''Create thread manager table'''
        if os.path.isfile('ThreadManager.db'):
            os.remove('ThreadManager.db')
        Base.metadata.create_all(self.engine)

    def checkForActiveThreads(self):
        '''Check for active threads'''
        logger.debug('Checking for active threads')
        activeThreads = 'no'
        for t in threading.enumerate():
            logger.debug(t.name)
            if t.name != 'MainThread':
                activeThreads = 'yes'
        return activeThreads

    def waitOnActiveThreads(self):
        '''wait on all active threads'''
        try:
            logger.debug('waiting for active threads')
            for t in threading.enumerate():
                if t.name != 'MainThread':
                        threadName = t.name
                        session = self.DBSession()
                        results = session.query(ThreadManagerTable).all()
                        if results != None:
                            for row in results:
                                logger.debug('removing thread: %s', row.name)
                                session.query(ThreadManagerTable).filter(ThreadManagerTable.id == row.id).delete()
                            session.commit
                            logger.debug('joining thread: ' + t.name)
                            if t.name != 'ServerThread':
                                t.join()
                        else:
                            logger.debug('No Threads Found')
            logger.debug('All threads joined')

        except Exception as e:
            logger.debug('Failed to wait on threads' + str(e))

    def waitOnThreadType(self, threadType):
        '''
        wait on all active threads of a certain type
        :param threadType:(report,monitor,service)
        :return:
        '''
        logger.debug('waiting on thread type: ' + threadType)
        try:
            for t in threading.enumerate():
                main_thread = threading.currentThread()
                if t is main_thread:
                    logger.info('Skipping processing main thread')
                else:
                    session = self.DBSession()
                    results = []
                    results.append(session.query(ThreadManagerTable).filter(ThreadManagerTable.threadType == threadType).all())
                    if results != []:
                        for row in results:
                            logger.debug('Found Thread: ' + t.name)
                            logger.debug('Returning Thread: ' + t.name)
                            if t.name != 'ServerThread':
                                t.join()
                    else:
                        logger.debug('Thread not found in table')

            logger.debug('All threads in threadType joined')

        except Exception as e:
            logger.debug('Failed to wait on thread type: ' + str(e))

    def removeThreadFromManagerTable(self, threadName):
        '''
        remove thread the thread manager table
        :param threadName:
        :return: returns a 1 for of thread was removed
        '''
        try:
            session = self.DBSession()
            results = session.query(ThreadManagerTable).filter(ThreadManagerTable.name == threadName).all()
            for row in results:
                logger.debug('removing thread: ' + row.name)
                session.query(ThreadManagerTable).filter(ThreadManagerTable.id == row.id).delete()
            session.commit
            return 1

        except Exception as e:
            logger.debug('Failed to remove thread from thread manager table', e)

    def createManagerThread(self, name, threadType, status, flagged, target, args):
        '''
        Create Manager thread and add entry to thread manager database
        :param name: name of thread
        :param threadType: type of thread (report, monitor, thread)
        :param status: Status of string (active / idle / stuck)
        :param flagged: A flag to indicate that a thread should be shutdown
        :param target: The target method for the thread to run
        :param args: Arguments to be passed to the target method
        :return: returns the thread object
        '''
        try:
            logger.debug('adding thread ' + name + ' to database')
            Base.metadata.bind = self.engine
            session = self.DBSession()
            session.autocommit = True
            newThread = ThreadManagerTable(name=name, threadType=threadType, status=status, flagged=flagged)
            session.add(newThread)
            t = threading.Thread(name=name,target=target, args=args)
            self.threads.append(t)
            t.setDaemon(False)
            return t

        except Exception as e:
            logger.debug('Failed to create manager thread', e)

    def getThreadList(self):
        '''
        Get a list of all threads in manager table
        :return: A list of threads
        '''
        logger.debug('Getting Thread list')
        try:
            session = self.DBSession()
            session.autocommit = True
            results = session.query(ThreadManagerTable).all()
            threadList = []
            for row in results:
                logger.debug('row:' + row)
                threadList.append(row)
            return threadList
        except Exception as e:
            logger.debug('Failed to get thread list', e)

    def checkThreadShutdownRequest(self):
        '''
        Check thread table to see if any threads have been flagged to be stopped
        :return:
        '''
        logger.debug('checking for any threads marked to be stooped')
        try:
            session = self.DBSession()
            flagged = 'yes'
            #results = session.query(ThreadManagerTable).filter(ThreadManagerTable.flagged == 'yes').all()
            #results = session.query(ThreadManagerTable).filter(ThreadManagerTable.flagged == flagged).all()
            results = session.query(ThreadManagerTable).filter(ThreadManagerTable.flagged == flagged).all()
            shutdownList = []
            if results != []:
                logger.debug(results)
                for row in results:
                    logger.debug(row.name)
                    shutdownList.append(row.name)  ##need to call thread.signal = False on shutdown list
            else:
                logger.debug('No threads found that were marked to be stopped')
            return shutdownList

        except Exception as e:
            logger.debug('Failed to check thread shutdown request', e)
            return 1