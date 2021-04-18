__author__ = 'peter'
import time
import os
import sys
import socket
import smtplib
import logging
import pycurl

PY3 = sys.version_info[0] > 2
logger = logging.getLogger(__name__)

class ext_ip:
    def __init__(self):
        self.PY3 = sys.version_info[0] > 2
        self.contents = ''
        if self.PY3:
            self.contents = self.contents.encode('ascii')
    def body_callback(self,buf):
            self.contents = self.contents + buf

class PI_manager():
    '''
    A manager class to manage the running of python scripts running on raspberry pi
    '''
    manager_ext_ip = ext_ip
    logging.basicConfig(level=logging.DEBUG)
    handler = logging.FileHandler('./logs/piManager.log')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(threadName)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


    def __init__(self,name,adminEmail):
        '''
        standard init method
        :param name: self.name
        :param adminEmail: email address to send reports to
        :return:
        '''
        self.name = name
        self.adminEmail = adminEmail
        self.internal_ip = '0.0.0.0'
        self.external_ip = '0.0.0.0'
        self.web_server_status = 'down'
        self.status_string = ''
        self.threads = []

    def buildStatusString(self):
        '''
        Builds the status message to be send to email
        :return: updates self.status message
        '''
        self.status_string = '''\\
            PI Manger Class
            name: ''' + self.name + '''
            external_ip: ''' + self.internal_ip + '''
            internal_ip: ''' + self.external_ip + '''
            web_server_status: ''' + self.web_server_status + '''
            processes failed:0'''

    def printAttributes(self):
        self.buildStatusString()
        print(self.status_string)

    def get_internal_ip(self, waitForValid='no'):
        '''
        returns the internal IP
        :param waitForValid: does not return until a valid IP has been obtained
        :return:
        '''
        logger.debug('attempting to get internal IP')
        #time.sleep(30)
        try:
            valid_ip = 0
            while (valid_ip == 0):
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(('www.gmail.com', 0))
                self.internal_ip = s.getsockname()[0]
                if ('169' in self.internal_ip and waitForValid=='yes'):
                    time.sleep(60)
                elif (waitForValid == 'no'):
                    valid_ip = 1
            logger.debug('returning IP: ' + self.internal_ip)
            return self.internal_ip
        except Exception as e:
            logger.error("Failed to get internal IP",e)
            pass

    def get_external_ip(self, waitForValid='no'):
        '''
        returns external IP
        :param waitForValid:
        :return:
        '''
        try:
            logger.debug('attempting to get external IP')
            t = self.manager_ext_ip()
            c = pycurl.Curl()
            c.setopt(c.URL, 'http://bot.whatismyipaddress.com')
            c.setopt(c.WRITEFUNCTION, t.body_callback)
            c.perform()
            c.close()
            self.external_ip = t.contents.decode()
            logger.debug('returning: ' + self.external_ip)
            return self.external_ip
        except Exception as e:
            logger.debug('Failed to get external IP', e)
            pass

    def send_status_email(self):
        '''
        Sends a email to the administrator email address
        :return:
        '''
        try:
            from_addrs = self.adminEmail
            to_addrs = self.adminEmail
            subject = 'pi manager status'

            username = self.adminEmail
            password = os.getenv('MAILPASSWORD')
            self.buildStatusString()
            msg_body = self.status_string
            logger.debug('Sending: ' + msg_body)
            message = 'Subject: %s\n\n%s' % ('piManager Admin Status',msg_body)
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login(username,password)
            server.sendmail(from_addrs,to_addrs, message)
            server.quit()
        except Exception as e:
            logger.error('Failed to send status email', e)
            pass

    def start_web_server(self):
        pass
