__author__ = 'Peter LeBlanc'
import piManager as Manager
import ThreadManager
import midiMonitor
import cherrypy
import webserviceLauncher
import time



class PIManager():

    def startHomeWebservice(self):
        launcher = webserviceLauncher.Launcher()
        launcher.startHomeWebservice()

    def createThreadsTable(self):
        i = ThreadManager.ThreadManager()
        i.createThreadManagerTable()

    def startMidiMonitor(self):
        i = ThreadManager.ThreadManager()
        monitor=midiMonitor.MidiMonitor()
        monitor = i.createManagerThread(name='midiMonitor', threadType='monitor', status='active', flagged='no', target=monitor.monitor_port, args=())
        monitor.start()

    def send_status_report(self):

        x = Manager.PI_manager('piManager', 'pleblanc.python@gmail.com')
        i = ThreadManager.ThreadManager()
        waitForValid = 'no'
        t1=i.createManagerThread(name = 'getInternalIP', threadType='report', status='active', flagged='yes', target=x.get_internal_ip,args=(waitForValid,))
        t1.start()
        #t2=i.createManagerThread(name = 'getExternalIP', threadType='report', status='active', flagged='no', target=x.get_external_ip,args=())
        #t2.start()

        '''
        monitor= i.createManagerThread(name='ThreadStatus', threadType='monitor', status='active', flagged='no', target=i.checkForActiveThreads, args=())
        monitor.start()
        while monitor == 'yes':
            monitor= i.createManagerThread(name='ThreadStatus', threadType='monitor', status='active', flagged='no', target=i.checkForActiveThreads, args=())
            monitor.start()
            monitor.join()
        '''

        i.waitOnThreadType(threadType='report')

        #t3 = i.createManagerThread(name = 'sendStatusEmail', threadType='monitor',status='active',flagged='no',target=x.send_status_email,args=())
        #t3.start()
        #i.waitOnActiveThreads()
        print('complete generating report')



def main():
    tm = ThreadManager.ThreadManager()
    pi = PIManager()
    pi.createThreadsTable()
    pi.startMidiMonitor()
    #pi.startHomeWebservice()
    pi.send_status_report()
    tm.getThreadList()
    print('main complete')

if __name__ == '__main__':
    main()
