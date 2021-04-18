__author__ = 'peter'

import cherrypy
import pyfirmata


class UNO(object):
    '''Class to manage the arduino uno from a webpage'''

    pin_list = []
    print('Setting up Serial connection to the Arduino')
    port_found = 'no'
    try:
        port = '/dev/ttyACM0'
        port_found = 'yes'
    except Exception as e:
        print('No device found on ACM0')
        port_found = 'no'
    finally:
        port = '/dev/ttyACM1'
        port_found = 'yes'

    if port_found == 'yes':
        board = pyfirmata.Arduino(port)

    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.pin = ''
        self.type = ''
        self.mode = ''
        self.state = ''

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.data[self.index]

    def get_pin(self):
        if self.type == 'digital':
            pin_request = 'd:'
        elif self.type == 'analog':
            pin_request = 'a:'
        pin_request = pin_request + str(self.location) + ':'

    def toggle_state(self):
        if self.state == 'off':
            self.state = 'on'
        elif self.state == 'on':
            self.state = 'off'
        return self.state

    def set_state(self, state):
        self.state = state

    def set_type(self, type):
        self.type = type

    def set_mode(self, mode):
        self.mode = mode

    @cherrypy.expose
    def index(self):
        def __init__(self):
            self.name = 'ArdCtl'
        print('generating control page')
        control_page = '''
            <html>
                <head><title>Arduino's Control Page</title>
                <link href="./css/home.css" rel="stylesheet">
                </head>
                <nav id="nav01"></nav>
                <body>
                    <div id="main">
                    <h1>Welcome to Peter's Arduino Control page</h1>
                    <h2>board configuration one :</h2>
                '''
        print(control_page)
        for pin in self.pin_list:
            print('adding pin')
            control_page = control_page + '''
                <form action="togglePIN?">
                    <input type="hidden" name="PIN" value=''' + str(pin.pin) + '''>
                    <input type="hidden" name="STATE" value=''' + str(pin.state) + '''>
                    <input type="submit" value="PIN ">
                </form>'''
            print(control_page)
        control_page = control_page + '</body></html>'

        print('loading page')
        print(control_page)
        return control_page

def main():

    pin1 = UNO(name = 'pin4',location = 4)
    pin1.set_state('off')


if __name__ == '__main__':
    cherrypy.config.update('./global.conf')
    cherrypy.tree.mount(UNO(name = 'pin4', location = 4), "/","config.conf")

    cherrypy.engine.start()
    cherrypy.engine.block()
    main()
