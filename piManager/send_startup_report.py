__author__ = 'Peter LeBlanc'
import piManager as Manager
import ThreadManager
import Home as homeWebservice

import time
def createThreadsTable():
    i = ThreadManager.ThreadManager()
    i.createThreadManagerTable()

def send_status_report():

    x = Manager.PI_manager('piManager', 'pleblanc.python@gmail.com')
    i = ThreadManager.ThreadManager()
    home = homeWebservice.Home


    waitForValid = 'no'
    t1=i.createManagerThread(name = 'getInternalIP', threadType='report', status='active', flagged='yes', target=x.get_internal_ip,args=(waitForValid,))
    t1.start()
    t2=i.createManagerThread(name = 'getExternalIP', threadType='report', status='active', flagged='no', target=x.get_external_ip,args=())
    t2.start()
    #t3=i.createManagerThread(name = 'Home_webservice', threadType='webservice', status='active', flagged='no', target=home.index ,args=())
    #t3.start()

    '''
    monitor= i.createManagerThread(name='ThreadStatus', threadType='monitor', status='active', flagged='no', target=i.checkForActiveThreads, args=())
    monitor.start()
    while monitor == 'yes':
        monitor= i.createManagerThread(name='ThreadStatus', threadType='monitor', status='active', flagged='no', target=i.checkForActiveThreads, args=())
        monitor.start()
        monitor.join()
    '''
    #i.checkThreadShutdownRequest()
    i.waitOnThreadType(threadType='report')

    t4 = i.createManagerThread(name = 'sendStatusEmail', threadType='monitor',status='active',flagged='no',target=x.send_status_email,args=())
    t4.start()

    #i.waitOnActiveThreads()

def main():
    createThreadsTable()
    send_status_report()
    print('main complete')
    raise SystemExit

if __name__ == '__main__':
    main()
