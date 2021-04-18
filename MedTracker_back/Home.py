__author__ = 'Peter LeBlanc'

import cherrypy
import logging

class Home(object):

    def __init__(self):
        self.name = 'MedTackerWebservice'

    @cherrypy.expose
    def index(self):
        return """
        <html>
            <head><title>Med Tracker</title>
            <link href="./css/home.css" rel="stylesheet">
            </head>
            <nav id="nav01"></nav>
            <body>
                <div id="main">
                <h1>Welcome Med Tracker</h1>
                <p>Doctors Interface</p>
                <p>Patients Interface</p>
                <p>Producers Interface</p>
                </div>
            <script src="./js/script.js"></script>

            </body>

        </html>"""



if __name__ == '__main__':
    cherrypy.config.update('/opt2/pythonDevelopment/projects/MedTracker/conf/global.conf')
    cherrypy.tree.mount(Home(), "/","./conf/config.conf")

    cherrypy.engine.start()
    cherrypy.engine.block()


