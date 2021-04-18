
import logging
import logging.config
import cherrypy
import socket

logging.config.fileConfig('./conf/logging.conf')
# create logger
logger = logging.getLogger('./logs/launchWebService.log')
# 'application' code
logger.debug('Preparing CherryPy Web Server')


class Home(object):
    log = logging.getLogger('./logs/Home.log')
    log.debug(socket.getaddrinfo('localhost', '8080'))
    log.debug(socket.gethostbyname('localhost'))
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
                <h2>Web Site Main Contents :</h2>

                <p>Geospatial Map Hosting Service (Geoserver)</p>
                <p>Geospatial Client Service (Open Layers)</p>
                <p>RSS Feed Harvesting and Searching (Python / Solr / Cassandra)</p>
                <p>JSON Services (Python)</p>
                <p>REST Services (Python)</p>
                <p>Satellite Data Visualization </p>
                </div>
            <script src="./js/script.js"></script>
            </body>

        </html>"""

if __name__ == '__main__':
    cherrypy.config.update('./conf/cherrypy_global.conf')
    cherrypy.tree.mount(Home(), "/","./conf/cherrypy_Home.conf")

    #css_handler = cherrypy.tools.staticdir.handler(section="/", dir='/opt2/pythonDevelopment/projects/Home/css')
    #cherrypy.tree.mount(css_handler, '/home.css')

    cherrypy.engine.start()
    cherrypy.engine.block()


