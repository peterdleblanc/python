
__author__ = 'Peter LeBlanc'

import cherrypy
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

## Create a file handler
handler = logging.FileHandler('./logs/Home_webservice.log')
handler.setLevel(logging.INFO)
## create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
## Add the handler to the logger
logger.addHandler(handler)


import cherrypy
import json
import datetime
from dateutil import parser

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

## Create a file handler
handler = logging.FileHandler('./logs/MedTracker.log')
handler.setLevel(logging.INFO)
## create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
## Add the handler to the logger
logger.addHandler(handler)

def set_global_database_variables():
    pass

class Home(object):

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
                <h1>Welcome to Med Tracker</h1>
                <h2>Web Site Main Contents :</h2>

                <p>Doctors Interface (Python)</p>
                <p>Patients Interface</p>
                <p>Producers Interface</p>
                </div>
            <script src="./js/script.js"></script>
            </body>

        </html>"""

    @cherrypy.expose
    def about(self):
        return """
        <html>
            <head><title>About</title>
            <link href="./css/home.css" rel="stylesheet">
            </head>
            <nav id="nav01"></nav>
            <body>
                <div id="main">
                <h1>Developed by Peter LeBlanc</h1>
                <p>This is a Central Registery for medications</p>
                </div>
            <script src="./js/script.js"></script>
            </body>

        </html>"""

    @cherrypy.expose
    def DataSets(self):
        return """
        <html>
            <head>
                <title>Avaiable Data Sets</title>
                <link href="./css/home.css" rel="stylesheet">
            </head>
            <nav id="nav01"></nav>
            <body>
                <div id="main">
                <h1>Data Sets</h1>
                <table>
                    <tr>
                        <th><b>Data Set</b></th>
                        <th><b>Type</b></th>
                        <th><b>Source</b></th>
                        <th><b>Source Type</b></th>
                        <th><b>Real Time or Historical</b></th>
                        <th><b>Active</b></th>
                    </tr>
                    <tr>
                        <td><a href="doctors_home"></a></td>
                        <td>Earth Quake Data</td>
                        <td>USGS</td>
                        <td>JSON</td>
                        <td>Historical Data</td>
                        <td>Yes</td>
                    </tr>
                    <tr>
                        <td><a href="NaturalDisastersHome">Natural Disasters Data</a></td>
                        <td>Hurricane</td>
                        <td>GDACS</td>
                        <td>RSS Feeds</td>
                        <td>Real Time Data</td>
                        <td>Yes</td>
                    </tr>
                    <tr>
                        <td><a href="NaturalDisastersHome">Natural Disasters Data</a></td>
                        <td>Tsunami</td>
                        <td>GDACS</td>
                        <td>RSS Feeds</td>
                        <td>Real Time Data</td>
                        <td>Yes</td>
                    </tr>
                    <tr>
                        <td>Natural Disasters Data</td>
                        <td>Flood</td>
                        <td>GDACS</td>
                        <td>RSS Feeds</td>
                        <td>Real Time Data</td>
                        <td>No</td>
                    </tr>
                    <tr>
                        <td>Natural Disasters Data</td>
                        <td>Valcano</td>
                        <td>GDACS</td>
                        <td>RSS Feeds</td>
                        <td>Real Time Data</td>
                        <td>No</td>
                    </tr>
                    <tr>
                        <td>Natural Disasters Data</td>
                        <td>Tropical Cyclone</td>
                        <td>GDACS</td>
                        <td>RSS Feeds</td>
                        <td>Real Time Data</td>
                        <td>No</td>
                    </tr>
                    <tr>
                        <td><a href="DiseaseOutbreakHome">Disease Outbreak News</a></td>
                        <td>Disease Outbreak News</td>
                        <td>World Health Organization</td>
                        <td>RSS Feeds</td>
                        <td>Real Time Data</td>
                        <td>Yes</td>
                    </tr>
                    <tr>
                        <td><a href="DiseaseOutbreakHome">Disease Outbreak News</a></td>
                        <td>Ebola Outbreak New</td>
                        <td>World Health Organization</td>
                        <td>RSS Feeds</td>
                        <td>Real Time Data</td>
                        <td>Yes</td>
                    </tr>
                    <tr>
                        <td><a href="NewsSourcesHome">World News</a></td>
                        <td>National News</td>
                        <td>CBC National</td>
                        <td>RSS Feeds</td>
                        <td>Real Time Data</td>
                        <td>Yes</td>
                    </tr>
                    <tr>
                        <td><a href="NewsSourcesHome">World News</a></td>
                        <td>iReports on CNN</td>
                        <td>CNN</td>
                        <td>RSS Feeds</td>
                        <td>Real Time Data</td>
                        <td>Yes</td>
                    </tr>
                    <tr>
                        <td>SRTM Elevation Data</a></td>
                        <td>SRTM Elecation Data</td>
                        <td>SRTM3</td>
                        <td>Map Elevation Data</td>
                        <td>Satellite Data</td>
                        <td>No</td>
                    </tr>


                </table>
                </div>
            <script src="./js/script.js"></script>
            </body>

        </html>"""




    @cherrypy.expose
    def display(self):
        return cherrypy.session['mystring']

    @cherrypy.expose
    def doctors_home(self):
        return """<html>
          <head>
            <link href="./css/home.css" rel="stylesheet">
          </head>
          <nav id="nav01"></nav>
          <body>
          <div id="main">
              <br><h1><b>Doctors Interface:</b></h1></br>
              <form action="get_eq_by_place_date_sort">
                    Patients Name:<br>
                    <input type="text" name="patientsName" value="John"><br>
                    Patients ID:<br>
                    <input type="text" name="patientsName" value="12345"><br>
                    <br>
                    <input type="hidden" name="sort_by" value='mag'>
                    <br>
                    <input type="submit" value="Search">
              </form>
          </div>

          <script src="./js/script.js"></script>
          </body>
        </html>"""

    @cherrypy.expose
    def patients_home(self):
        return """<html>
          <head>
            <link href="./css/home.css" rel="stylesheet">
          </head>
          <nav id="nav01"></nav>
          <body>
          <div id="main">
              <br><h1><b>Patients Interface:</b></h1></br>
              <form action="get_eq_by_place_date_sort">
                    Patients Name:<br>
                    <input type="text" name="patientsName" value="John"><br>
                    Begin Date: <input type="date" name="begin_date">End Date: <input type="date" name="end_date">
                    <br>
                    <input type="hidden" name="sort_by" value='mag'>
                    <br>
                    <input type="submit" value="Get Earth Quake Data">
              </form>
          </div>

          <script src="./js/script.js"></script>
          </body>
        </html>"""

    @cherrypy.expose
    def display(self):
        return cherrypy.session['mystring']

    @cherrypy.expose
    def NaturalDisastersHome(self):
        return """<html>
          <head>
            <link href="./css/home.css" rel="stylesheet">
            <title>Natural Disasters Data</title>
          </head>
          <nav id="nav01"></nav>
          <body>
               <div id="main">
               <form action="get_event_by_type">
                    Type of Natural Disaster:<br>
                    <select name='event_type'>
                        <option value="HURRICANE">Hurricane</option>
                        <option value="TSUNAMI">Tsunami</option>
                    </select>
                    <br><br>
                    <input type="submit" value="get">
               </form>
               </div>
          <script src="./js/script.js"></script>
          </body>
        </html>"""

    @cherrypy.expose
    def DiseaseOutbreakHome(self):
        return """<html>
          <head>
            <link href="./css/home.css" rel="stylesheet">
            <title>Natural Disasters Data</title>
          </head>
          <nav id="nav01"></nav>
          <body>
               <div id="main">
               <form action="get_outbreak_by_type">
                    Type of Disease Outbreak:<br>
                    <select name='outbreak_type'>
                        <option value="Ebola Outbreak News">Ebola Outbreak News</option>
                        <option value="Disease Outbreak News">Disease Outbreak News</option>
                    </select>
                    <br><br>
                    <input type="submit" value="get">
               </form>
               </div>
          <script src="./js/script.js"></script>
          </body>
        </html>"""

    @cherrypy.expose
    def NewsSourcesHome(self):
        return """<html>
          <head>
            <link href="./css/home.css" rel="stylesheet">
            <title>National News Reports</title>
          </head>
          <nav id="nav01"></nav>
          <body>
               <div id="main">
               <form action="get_news_by_source">
                    News Sources:<br>
                    <select name='news_source'>
                        <option value="National News">National News</option>
                        <option value="iReports on CNN">iReports on CNN</option>
                    </select>
                    <br><br>
                    <input type="submit" value="get">
               </form>
               </div>
          <script src="./js/script.js"></script>
          </body>
        </html>"""

    @cherrypy.expose
    def get_eq_by_event_id_form(self, event_id):

        requested_fields = ['event_id', 'title','longitude','latitude','depth','mag','place','url','felt','cdi','mmi','alert','status','tsunami','sig','net','code','ids','sources','types','nst','dmin','rms','gap','magType','type','seq_id','event_time']

        #### Get Data ####
        sql ="SELECT "
        for x in requested_fields:
            sql = sql + x + ','
        sql = sql[:-1]
        sql = sql + " FROM USGS_EQ_DATA"
        sql = sql + " WHERE event_id = '" + event_id + "'"

        logger.info(sql)
        cursor.execute(sql)
        results = cursor.fetchall()

        response_dict = {}

        response_dict['keys'] = requested_fields


        for x in results:
            response_dict[x[0]] = (x[0], x[1], x[2], x[3], x[4], x[5],x[6], x[7], x[8], x[9], x[10], x[11],x[12], x[13], x[14], x[15], x[16], x[17],x[18], x[19], x[20], x[21], x[22], x[23],x[24], x[25], x[26], x[27].isoformat())

        form_response = '<html><head><link href="./css/home.css" rel="stylesheet"><b>Results for event id: </b>' + event_id + '<head><nav id="nav01"></nav><body><div id="main">'
        form_response = form_response + '<table style="width:90%">'
        form_response = form_response + '<br></br>'
        for k,v in response_dict.items():
            count = 0
            if k is not 'keys':
                for i in xrange(len(requested_fields)):
                    form_response = form_response + '<tr>'
                    if requested_fields[i] == 'url':
                        form_response = form_response + '<td><b>' + requested_fields[i] + ':</b></td>' + '<td><a href=' + str(v[i]) + '>' + str(v[i]) + '</a></td>'
                        pass
                    else:
                        form_response = form_response + '<td><b>' + requested_fields[i] + ':</b></td>' + '<td>' + str(v[i]) + '</td>'
                    form_response = form_response + '</tr>'
        form_response = form_response + '</table>'


        form_response = form_response + '</div><script src="./js/script.js"></script></body></html>'

        return form_response

        cursor.close()
        con.close()


    @cherrypy.expose
    def get_eq_by_place_date_sort(self, place, begin_date, end_date, sort_by):

        cursor.execute(
            "ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'"
            " NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF'")

        requested_fields = ['event_id', 'title','longitude','latitude','depth','mag','place','alert','status','tsunami','event_time']

        sql ="SELECT "
        for x in requested_fields:
            sql = sql + x + ','
        sql = sql[:-1]
        sql = sql + " FROM USGS_EQ_DATA"
        sql = sql + " WHERE Upper(place) like '%" + place.upper() + "%' AND event_time > '" + str(begin_date) + "' AND event_time < '" + str(end_date) + "' ORDER BY " + sort_by

        logger.info(sql)
        cursor.execute(sql)
        results = cursor.fetchall()

        response_dict = {}

        response_dict['keys'] = requested_fields

        for x in results:
            response_dict[x[0]] = (x[0], x[1], x[2], x[3], x[4], x[5],x[6], x[7], x[8], x[9], x[10].isoformat())

        table_response = '<html><link href="./css/home.css" rel="stylesheet"><head>Results for place name: ' + place + '<head><nav id="nav01"></nav><body><div id="main">'
        table_response =  table_response + '<table>'
        table_response = table_response + '<tr>'
        for x in requested_fields:
            table_response = table_response + '<th> <a href="get_eq_by_place_date_sort?place=' + place + '&begin_date=' + begin_date + '&end_date=' + end_date + '&sort_by=' + x + '">' + x.upper() + '</a></th>'
        for x in results:
            table_response = table_response + '<tr>'
            for i in range(len(requested_fields)):
                if requested_fields[i] == 'event_id':
                        table_response = table_response + '<td> <a href="get_eq_by_event_id_form?event_id='+ str(x[i]) + '">' + str(x[i]) + '</a></td>'
                elif requested_fields[i] == 'alert':
                    if x == 'green':
                        table_response = table_response + '<td bgcolor="#66ff33">' + str(x[i]) + '</td>'
                    elif x == 'yellow':
                        table_response = table_response + '<td bgcolor="#ffff00">' + str(x[i]) + '</td>'
                    elif x == 'orange':
                        table_response = table_response + '<td bgcolor="#ff9900">' + str(x[i]) + '</td>'
                    elif x == 'red':
                        table_response = table_response + '<td bgcolor="#ff0000">' + str(x[i]) + '</td>'
                    else:
                        table_response = table_response + '<td>' + str(x[i]) + '</td>'
                else:
                    table_response = table_response + '<td>' + str(x[i]) + '</td>'
            table_response = table_response + '</tr>'
        table_response = table_response + '</table>'
        table_response = table_response + '</div><script src="./js/script.js"></script></body></html>'


        return table_response

        cursor.close()
        con.close()


    @cherrypy.expose
    def get_event_by_type(self, event_type):


        requested_fields = ['EVENT_ID', 'EVENT_TYPE', 'TITLE','LATITUDE','LONGITUDE', 'EVENT_DESC']

        sql ="SELECT "
        for x in requested_fields:
            sql = sql + x + ','
        sql = sql[:-1]
        sql = sql + " FROM NATURAL_EVENTS"
        sql = sql + " WHERE EVENT_TYPE = '" + event_type + "'"

        logger.info(sql)
        cursor.execute(sql)
        results = cursor.fetchall()

        response_dict = {}

        response_dict['keys'] = requested_fields

        for x in results:
            response_dict[x[0]] = (x[0], x[1], x[2], x[3], x[4], x[5].read())

        table_response = '<html><link href="./css/home.css" rel="stylesheet"><head>Results for place name: ' + event_type + '<head><nav id="nav01"></nav><body><div id="main">'
        table_response =  table_response + '<table>'
        table_response = table_response + '<tr>'
        for x in requested_fields:
            table_response = table_response + '<th>' + x.upper() + '</th>'
        for x in results:
            table_response = table_response + '<tr>'
            for i in range(len(requested_fields)):
                if requested_fields[i] == 'event_id':
                        table_response = table_response + '<td> <a href="get_eq_by_event_id_form?event_id='+ str(x[i]) + '">' + str(x[i]) + '</a></td>'
                elif requested_fields[i] == 'alert':
                    if x == 'green':
                        table_response = table_response + '<td bgcolor="#66ff33">' + str(x[i]) + '</td>'
                    elif x == 'yellow':
                        table_response = table_response + '<td bgcolor="#ffff00">' + str(x[i]) + '</td>'
                    elif x == 'orange':
                        table_response = table_response + '<td bgcolor="#ff9900">' + str(x[i]) + '</td>'
                    elif x == 'red':
                        table_response = table_response + '<td bgcolor="#ff0000">' + str(x[i]) + '</td>'
                    else:
                        table_response = table_response + '<td>' + str(x[i]) + '</td>'
                else:
                    table_response = table_response + '<td>' + str(x[i]) + '</td>'
            table_response = table_response + '</tr>'
        table_response = table_response + '</table>'
        table_response = table_response + '</div><script src="./js/script.js"></script></body></html>'


        return table_response


        #response = json.dumps(response_dict, sort_keys=True, indent=4, separators=(',', ': '))
        #response = json.dumps(response_dict)
        #return response

        cursor.close()
        con.close()

    @cherrypy.expose
    def get_outbreak_by_type(self, outbreak_type):


        requested_fields = ['CABLE_RELEASED_SEQ', 'CABLE_TYPE', 'DECLASSIFICATION_TEXT', 'CABLE_TEXT']

        sql ="SELECT "
        for x in requested_fields:
            sql = sql + x + ','
        sql = sql[:-1]
        sql = sql + " FROM CABLE_RELEASED"
        sql = sql + " WHERE CABLE_TYPE = '" + outbreak_type + "'"

        logger.info(sql)
        nes_cursor = con_NES_sim.cursor()
        nes_cursor.execute(sql)
        #results = nes_cursor.fetchall()

        response_dict = {}

        response_dict['keys'] = requested_fields

        for x in nes_cursor:
            response_dict[x[0]] = (x[0], x[1], x[2], x[3].read())

        table_response = '<html><link href="./css/home.css" rel="stylesheet"><head>Results for place name: ' + outbreak_type + '<head><nav id="nav01"></nav><body><div id="main">'
        table_response =  table_response + '<table>'
        table_response = table_response + '<tr>'
        for x in requested_fields:
            table_response = table_response + '<th>' + x.upper() + '</th>'
        for x,v in response_dict.items():
            table_response = table_response + '<tr>'
            for i in range(len(requested_fields)):
                table_response = table_response + '<td>' + str(v[i]) + '</td>'
            table_response = table_response + '</tr>'
        table_response = table_response + '</table>'
        table_response = table_response + '</div><script src="./js/script.js"></script></body></html>'

        return table_response

        cursor_nes_sim.close()
        con_NES_sim_.close()

    @cherrypy.expose
    def get_news_by_source(self, news_source):


        requested_fields = ['IP_REPORT_SEQ', 'DECLASSIFICATION_TEXT', 'IP_RPT_TEXT']

        sql ="SELECT "
        for x in requested_fields:
            sql = sql + x + ','
        sql = sql[:-1]
        sql = sql + " FROM IP_REPORT"
        sql = sql + " WHERE DECLASSIFICATION_TEXT = '" + news_source + "'"

        logger.info(sql)
        nes_cursor = con_NES_sim.cursor()
        nes_cursor.execute(sql)
        #results = nes_cursor.fetchall()

        response_dict = {}

        response_dict['keys'] = requested_fields

        for x in nes_cursor:
            response_dict[x[0]] = (x[0], x[1], x[2].read())

        table_response = '<html><link href="./css/home.css" rel="stylesheet"><head>Results for place name: ' + news_source + '<head><nav id="nav01"></nav><body><div id="main">'
        table_response =  table_response + '<table>'
        table_response = table_response + '<tr>'
        for x in requested_fields:
            table_response = table_response + '<th>' + x.upper() + '</th>'
        for x,v in response_dict.items():
            table_response = table_response + '<tr>'
            for i in range(len(requested_fields)):
                table_response = table_response + '<td>' + str(v[i]) + '</td>'
            table_response = table_response + '</tr>'
        table_response = table_response + '</table>'
        table_response = table_response + '</div><script src="./js/script.js"></script></body></html>'

        return table_response

        cursor_nes_sim.close()
        con_NES_sim_.close()

if __name__ == '__main__':
    set_global_database_variables()
    cherrypy.config.update('/opt2/pythonDevelopment/projects/MedTracker/conf/global.conf')
    cherrypy.tree.mount(Home(), "/","/opt2/pythonDevelopment/projects/MedTracker/conf/config.conf")

    #css_handler = cherrypy.tools.staticdir.handler(section="/", dir='/opt2/pythonDevelopment/projects/Home/css')
    #cherrypy.tree.mount(css_handler, '/home.css')

    cherrypy.engine.start()
    cherrypy.engine.block()

