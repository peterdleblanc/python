__author__ = 'Peter LeBlanc'

import cherrypy
import pyfirmata
import midiMonitor

print('Setting up Serial connection to the Arduino')
try:
    port = '/dev/ttyACM0'
except Exception as e:
    print('No device found on ACM0')
finally:
    port = '/dev/ttyACM1'

board = pyfirmata.Arduino(port)

ledPin4 = board.get_pin('d:4:o')

class uno(object):
    '''Class to manage the arduino uno from a webpage'''

    Pin3 = board.get_pin('d:3:o')
    Pin5 = board.get_pin('d:5:o')

    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.pin = ''
        self.type = 'digital'
        self.mode = 'output'
        self.state = 'off'

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
        if self.state == 'on':
            self.state = 'off'
        return self.state

    def set_type(self, type):
        self.type = type

    def set_mode(self, mode):
        self.mode = mode



class Home(object):
    @cherrypy.expose
    def index(self):
        return """
        <html>
            <head><title>Demo Site</title>
            <link href="./css/home.css" rel="stylesheet">
            </head>
            <nav id="nav01"></nav>
            <body>
                <div id="main">
                <h1>Welcome to Peter's Demo Site</h1>
                <h2>Web Site Main Components :</h2>

                <form action="LoadArduinoAdmin" method="post">
                    <button onclick="LoadArduinoAdmin">Load Arduino Admin</button>
                </form>
            </body>

        </html>"""

    @cherrypy.expose
    def LoadArduinoAdmin(self):
        return """
        <html>
            <head><title>Demo Site</title>
            <link href="./css/home.css" rel="stylesheet">
            </head>
            <nav id="nav01"></nav>
            <body>
                <div id="main">
                <h1>Welcome to Peter's Demo Site</h1>
                <h2>Web Site Main Components :</h2>

                <form action="togglePIN?PIN=2&STATE=1">
                    <input type="hidden" name="PIN" value=2>
                    <input type="hidden" name="STATE" value=1>
                    <input type="submit" value="PIN 2">
                </form>
                <form action="togglePIN?PIN=3&STATE=1">
                    <input type="hidden" name="PIN" value=3>
                    <input type="hidden" name="STATE" value=1>
                    <input type="submit" value="PIN 3">
                </form>
                <form action="togglePIN?PIN=4&STATE=1">
                    <input type="hidden" name="PIN" value=4>
                    <input type="hidden" name="STATE" value=1>
                    <input type="submit" value="PIN 4">
                </form>
                <form action="togglePIN?PIN=5&STATE=1">
                    <input type="hidden" name="PIN" value=5>
                    <input type="hidden" name="STATE" value=1>
                    <input type="submit" value="PIN 5">
                </form>
            </body>

        </html>"""


    @cherrypy.expose
    def updatePinState(self,PIN, requested_state):

        if PIN == '4':
            print('Updating pin: ' + str(PIN) + ' to: ' + str(requested_state))
            ledPin4.write(int(requested_state))


    @cherrypy.expose
    def togglePIN(self, PIN, STATE):

        print('updating state to: ' + str(STATE))

        requested_state = int(STATE)
        self.updatePinState(PIN, requested_state,)



        if STATE == '1':
            print('state on')
            doc = """
            <html>
                <head><title>Demo Site</title>
                <link href="./css/home.css" rel="stylesheet">
                </head>
                <nav id="nav01"></nav>
                <body>
                    <div id="main">
                    <h1>Welcome to Peter's Demo Site</h1>
                    <h2>Web Site Main Components :</h2>

                    <form action="togglePIN?PIN=2&STATE=0">
                        <input type="hidden" name="PIN" value=2>
                        <input type="hidden" name="STATE" value=0>
                        <input type="submit" value="PIN 2">
                    </form>
                    <form action="togglePIN?PIN=3&STATE=0">
                        <input type="hidden" name="PIN" value=3>
                        <input type="hidden" name="STATE" value=0>
                        <input type="submit" value="PIN 3">
                    </form>
                    <form action="togglePIN?PIN=4&STATE=0">
                        <input type="hidden" name="PIN" value=4>
                        <input type="hidden" name="STATE" value=0>
                        <input type="submit" value="PIN 4" button style="background-color:lightgreen">
                    </form>
                    <form action="togglePIN?PIN=5&STATE=0">
                       <input type="hidden" name="PIN" value=5>
                        <input type="hidden" name="STATE" value=0>
                        <input type="submit" value="PIN 5">
                    </form>
                </body>

            </html>"""

        if STATE == '0':
            print('off')
            doc = """
            <html>
                <head><title>Demo Site</title>
                <link href="./css/home.css" rel="stylesheet">
                </head>
                <nav id="nav01"></nav>
                <body>
                    <div id="main">
                    <h1>Welcome to Peter's Demo Site</h1>
                    <h2>Web Site Main Components :</h2>
                    <form action="togglePIN?PIN=2&STATE=1">
                        <input type="hidden" name="PIN" value=2>
                        <input type="submit" value="PIN 2">
                    </form>
                    <form action="togglePIN?PIN=3&STATE=1">
                        <input type="hidden" name="PIN" value=3>
                        <input type="submit" value="PIN 3">
                    </form>
                    <form action="togglePIN?PIN=4&STATE=1">
                        <input type="hidden" name="PIN" value=4>
                        <input type="hidden" name="STATE" value=1>
                        <input type="submit" value="PIN 4">
                    </form>
                    <form action="togglePIN?PIN=5&STATE=1">
                        <input type="hidden" name="PIN" value=5>
                        <input type="submit" value="PIN 5">
                    </form>
                </body>

             </html>"""

        return doc