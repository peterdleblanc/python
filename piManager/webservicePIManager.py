
__author__ = 'Peter LeBlanc'

import cherrypy

class PIManagerWebservice(object):
    @cherrypy.expose
    def index(self):
        return """
        <html>
            <head><title>PI Manager Web Service</title>
            <link href="./css/home.css" rel="stylesheet">
            </head>
            <nav id="nav01"></nav>
            <body>
                <div id="main">
                <h1>PI Manager</h1>
                <p>Managment Section </p>
                <button type="button" formaction="helloWorld">Hello World</button>
                <button type="button" formaction="printHello">Print Hellow</button>
                </div>
            <script src="./js/script.js"></script>

            </body>

        </html>"""

    @cherrypy.expose
    def helloWorld(self):
        return """
        <html>
            <head><title>Hello World</title>
            <link href="./css/home.css" rel="stylesheet">
            </head>
            <nav id="nav01"></nav>
            <body>
                <div id="main">
                <h1>Hello World</h1>
                </div>
            <script src="./js/script.js"></script>

            </body>

        </html>"""

    def printHello(self):
        print('Hello')
