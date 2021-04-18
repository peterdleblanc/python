__author__ = 'Peter LeBlanc'

import feedparser
import random
import cx_Oracle
import math
import hashlib
import re
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

## Create a file handler
handler = logging.FileHandler('sql.log')
handler.setLevel(logging.INFO)
## create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
## Add the handler to the logger
logger.addHandler(handler)


from HTMLParser import HTMLParser

import itertools

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def set_global_variables():
    #Lists to be used for random fill values
    global iir_filters
    iir_filters = ['Butter', 'Chebys', 'Ellip', 'Bessel', 'Direct']
    global item_status
    item_status = ['a','b','c','d']
    global randFlag
    randFlag = ['Y', 'N']
    global securityCode
    securityCode = ['U', 'S','TS']
    global nbrg
    nbrg = ['LSAR', 'WORLDVIEW', 'WARFIGHTER', 'Terra','Other']
    global declass_text
    declass_text = ['COMMERCIAL', 'NTM', 'MCG','OTHER']
    global ro_type
    ro_type = ['RPF', 'ADR', 'ITD', 'TER','ELE', 'FEA']

def get_seq_value(table, seq):
    ### Setup Oracle Connection ####
    dsnStr = cx_Oracle.makedsn('oracle11.compusult.net','1521','devel11')
    con = cx_Oracle.connect(user="NES_Simulator", password="wes", dsn=dsnStr)

    ### Get report_seq value ###
    cursor = con.cursor()
    sql = "SELECT MAX(" + seq + ") FROM " + table
    cursor.execute(sql)
    results = cursor.fetchall()
    for i in results:
        seq_value = i[0]
    if seq_value == None:
        seq_value = 1

    cursor.close()
    con.close()

    return seq_value

def get_column_names(table):
    ### Setup Oracle Connection ####
    dsnStr = cx_Oracle.makedsn('oracle11.compusult.net','1521','devel11')
    con = cx_Oracle.connect(user="NES_Simulator", password="wes", dsn=dsnStr)
    cursor = con.cursor()

    #### Get all the column names ####
    sql = "SELECT * FROM " + table
    cursor.execute(sql)
    results = cursor.fetchall()
    cols = {}
    for i in cursor.description:
        k = i[0]
        cols[k] = 'null'

    cursor.close()
    con.close()

    return cols

def write_dict_to_database(table_name, table_dict):

    ### Setup Oracle Connection ####
    dsnStr = cx_Oracle.makedsn('oracle11.compusult.net','1521','devel11')
    con = cx_Oracle.connect(user="NES_Simulator", password="wes", dsn=dsnStr)
    cursor = con.cursor()

    sql = 'INSERT INTO ' + table_name + '('

    for k,v in table_dict.items():
        if v is not 'null':
            sql = sql + k + ','
    sql = sql[:-1]
    sql = sql + ') VALUES('

    for k,v in table_dict.items():
        if v is not 'null':
            #if v.isdigit() == True:
            if re.match(r"[-+]?\d+(\.0*)?$", str(v)) is not None:
                sql = sql +   str(v) + ","
            #if v.isdigit() == False:
            else:
                if k == 'IDC_LONGITUDE':
                    sql = sql +   str(v) + ","
                elif k == 'idc_longitude':
                    sql = sql +   str(v) + ","
                elif k == 'IDC_LATITUDE':
                    sql = sql +   str(v) + ","
                elif k == 'idc_latitude':
                    sql = sql +   str(v) + ","
                else:
                    sql = sql + "'" + str(v) + "'" + ","

    sql = sql[:-1]
    sql = sql + ')'

    logger.info(sql)
    cursor.execute(sql)
    sql = "commit"
    cursor.execute(sql)
    cursor.close()
    con.close()

def write_cable_report(table_name, table_dict):

    ### Setup Oracle Connection ####
    dsnStr = cx_Oracle.makedsn('oracle11.compusult.net','1521','devel11')
    con = cx_Oracle.connect(user="NES_Simulator", password="wes", dsn=dsnStr)
    cursor = con.cursor()

    sql = "INSERT INTO " + table_name + "("

    for k,v in table_dict.items():
        if v is not 'null':
            sql = sql + k + ","
    sql = sql[:-1]
    sql = sql + ") VALUES("

    for k,v in table_dict.items():
        if v is not 'null':
            if re.match(r"[-+]?\d+(\.0*)?$", str(v)) is not None:
                sql = sql +   str(v) + ","
            else:
                sql = sql + "'" + str(v) + "'" + ","

    sql = sql[:-1]
    sql = sql + ")"

    logger.info(sql)
    cursor.execute(sql)
    sql = "commit"
    cursor.execute(sql)
    cursor.close()
    con.close()

def get_dmc_record(lat, long):
    ### Setup Oracle Connection ####
    dsnStr = cx_Oracle.makedsn('oracle12c.compusult.net','1521','demo')
    con = cx_Oracle.connect(user="ngds_demo_tactical_dmc", password="wes", dsn=dsnStr)
    cursor = con.cursor()

    ### List of required fields  ###
    requested_fields = ['mission_id', 'cloud_cover_percentage_rate', 'focus_plane_grazing_angle','ground_coverage_area_dim','image_collection_mode', 'image_id_text','image_sequence_id','image_type_code','internal_id','native_file_format_code','obliquity_angle','roll_angle','platform_code', 'scan_path_azimuth','security_class_code']
    cursor = con.cursor()
    sql = "SELECT "
    for i in requested_fields:
        sql = sql + i + ','
    sql = sql[:-1]
    sql = sql + " FROM PRODUCTS WHERE (MDSYS.SDO_WITHIN_DISTANCE(products.search_geometry, MDSYS.SDO_GEOMETRY(2001,8307,NULL,MDSYS.SDO_ELEM_INFO_ARRAY(1,1,1),MDSYS.SDO_ORDINATE_ARRAY("
    sql = sql + str(lat) + ',' + str(long)

    sql = sql + ")), 'distance=250000.0 unit=meter') = 'TRUE') and rownum = 1"

    logging.info(sql)
    cursor.execute(sql)
    results = cursor.fetchall()

    dmc_record = {}

    ### Building Dictonary ###
    for i in results:
        count = 0
        for x in requested_fields:
            dmc_record[x] = i[count]
            count = count + 1

    cursor.close()
    con.close()

    return dmc_record

def check_for_desc(desc):


    ### Setup Oracle Connection ####
    dsnStr = cx_Oracle.makedsn('oracle11.compusult.net','1521','devel11')
    con = cx_Oracle.connect(user="NES_Simulator", password="wes", dsn=dsnStr)
    cursor = con.cursor()

    cursor = con.cursor()
    sql = "SELECT DESC_HASH FROM EXPL_REPORT"
    cursor.execute(sql)
    results = cursor.fetchall()
    existing_flag = 'n'
    for i in results:
        if i[0] == desc:
            existing_flag = 'y'

    cursor.close()
    con.close()

    return existing_flag

def check_for_cable_record(desc):


    ### Setup Oracle Connection ####
    dsnStr = cx_Oracle.makedsn('oracle11.compusult.net','1521','devel11')
    con = cx_Oracle.connect(user="NES_Simulator", password="wes", dsn=dsnStr)
    cursor = con.cursor()

    cursor = con.cursor()
    sql = "SELECT DESC_HASH FROM cable_released"
    cursor.execute(sql)
    results = cursor.fetchall()
    existing_flag = 'n'
    logger.error('Checking for: ' + desc)
    for i in results:
        logger.error(i[0])
        if i[0] == desc:
            existing_flag = 'y'
            logger.error('Found Record')

    cursor.close()
    con.close()

    return existing_flag

def check_for_IP_record(desc):


    ### Setup Oracle Connection ####
    dsnStr = cx_Oracle.makedsn('oracle11.compusult.net','1521','devel11')
    con = cx_Oracle.connect(user="NES_Simulator", password="wes", dsn=dsnStr)
    cursor = con.cursor()

    cursor = con.cursor()
    sql = "SELECT DESC_HASH FROM ip_report"
    cursor.execute(sql)
    results = cursor.fetchall()
    existing_flag = 'n'
    for i in results:
        if i[0] == desc:
            existing_flag = 'y'
            logger.error('Found Record')

    cursor.close()
    con.close()

    return existing_flag

def get_gdacs_hurricane_data():
    ### RSS Feed to harvest ###
    d = feedparser.parse('http://www.gdacs.org/XML/RSS.xml')

    ### Get column names ###
    expl_report_cols = get_column_names('expl_report')
    target_cols = get_column_names('target')
    report_seq = get_seq_value('expl_report', 'report_seq')

    ### Create a record for each entry in the RSS Feed ###
    for post in d.entries:
        desc_text = post.description
        hashed_desc = hashlib.md5(desc_text)
        existing_flag = check_for_desc(hashed_desc.hexdigest())
        if existing_flag == 'n':
            report_seq = report_seq + 1
            expl_report_cols['mission_number'] = str(random.randint(500, 1000))
            expl_report_cols['correction_flag'] = 'N'
            expl_report_cols['iir_type'] = random.choice(iir_filters)
            expl_report_cols['iir_significance'] = 's' + str(random.randint(1, 99))
            expl_report_cols['item_type'] = post.gdacs_eventtype
            expl_report_cols['mission_nsc'] = 'miss' + str(random.randint(1, 99))
            expl_report_cols['ro_type'] = random.choice(ro_type)
            expl_report_cols['status_activity_code'] = 'ac' + str(random.randint(1,9))
            expl_report_cols['defense_security_text'] = post.gdacs_acknowledgements
            expl_report_cols['descr_text'] = post.title
            expl_report_cols['descr_more_text'] = post.summary
            expl_report_cols['nbrg'] = random.choice(nbrg)
            expl_report_cols['releasability'] =  post.gdacs_accesslevel
            expl_report_cols['declassification_text'] =random.choice(declass_text)
            expl_report_cols['precedence'] = random.choice(item_status)
            expl_report_cols['correction_flag'] = 'N'
            expl_report_cols['idc_latitude'] = post.geo_lat
            expl_report_cols['idc_longitude'] = post.geo_long
            expl_report_cols['r_flag'] = random.choice(randFlag)
            expl_report_cols['security_code'] = 'U'
            expl_report_cols['imcon_flag'] = random.choice(randFlag)
            expl_report_cols['source_flag'] =  random.choice(randFlag)
            expl_report_cols['REPORT_NUM'] = report_seq
            expl_report_cols['REPORT_SEQ'] = report_seq
            expl_report_cols['TARGET_ID'] = report_seq
            expl_report_cols['SERVICE_UUID'] = 'NESSim_GDACS'
            expl_report_cols['agency'] = 'GDACS'
            expl_report_cols['DESC_HASH'] = hashed_desc.hexdigest()
            #expl_report_cols['date_nsc'] = post.gdacs_todate
            #expl_report_cols['date_created'] = post.gdacs_todate
            #expl_report_cols['date_modified'] = post.gdacs_fromdate
            #expl_report_cols['date_mission'] = post.gdacs_fromdate

            write_dict_to_database('expl_report', expl_report_cols)
            create_target_record(target_cols, report_seq,post.geo_lat, post.geo_long)
            dmc_record = get_dmc_record(post.geo_lat,post.geo_long)

            if 'image_id_text' not in dmc_record:
                logger.info('No record found in DMC')
            else:
                create_photo_record(post.geo_lat, post.geo_long, dmc_record, report_seq)

            #report_seq = report_seq + 1
        else:
            logger.info("Found DMC record")

def get_earthquack_data():
    d = feedparser.parse('http://www.bgs.ac.uk/feeds/MhSeismology.xml')

    ### Get column names ###
    expl_report_cols = get_column_names('expl_report')
    target_cols = get_column_names('target')
    report_seq = get_seq_value('expl_report', 'report_seq')

    for post in d.entries:
        desc_text = post.description
        hashed_desc = hashlib.md5(desc_text)
        existing_flag = check_for_desc(hashed_desc.hexdigest())
        if existing_flag == 'n':
            report_seq = report_seq + 1
            expl_report_cols['REPORT_SEQ'] = report_seq
            expl_report_cols['REPORT_NUM'] = report_seq
            expl_report_cols['TARGET_ID'] = report_seq
            expl_report_cols['SERVICE_UUID'] = 'NESSim_BGS'
            expl_report_cols['iir_significance'] = 's' + str(random.randint(1, 99))
            expl_report_cols['mission_nsc'] = 'miss' + str(random.randint(1, 99))
            expl_report_cols['DESCR_TEXT'] = post.title
            expl_report_cols['DESCR_MORE_TEXT'] = post.description
            expl_report_cols['IDC_LATITUDE'] = post.geo_lat
            expl_report_cols['IDC_LONGITUDE'] = post.geo_long
            expl_report_cols['mission_number'] = str(random.randint(500, 1000))
            expl_report_cols['ro_type'] = random.choice(ro_type)
            expl_report_cols['declassification_text'] =random.choice(declass_text)
            expl_report_cols['correction_flag'] = 'N'
            expl_report_cols['iir_type'] = random.choice(iir_filters)
            expl_report_cols['nbrg'] = random.choice(nbrg)
            expl_report_cols['item_type'] = 'EQ'
            expl_report_cols['agency'] = 'BGS'
            expl_report_cols['security_code'] = 'U'
            expl_report_cols['DESC_HASH'] = hashed_desc.hexdigest()

            write_dict_to_database('expl_report', expl_report_cols)
            create_target_record(target_cols, report_seq,post.geo_lat, post.geo_long)
            dmc_record = get_dmc_record(post.geo_lat,post.geo_long)

            if 'image_id_text' not in dmc_record:
                logger.info('No record found in DMC')
            else:
                create_photo_record(post.geo_lat, post.geo_long, dmc_record, report_seq)
        else:
            logger.info('Record Exist')

def get_tsunami_data():

    d = feedparser.parse('http://ptwc.weather.gov/feeds/ptwc_rss_pacific.xml')

    ### Get column names ###
    expl_report_cols = get_column_names('expl_report')
    target_cols = get_column_names('target')
    report_seq = get_seq_value('expl_report', 'report_seq')

    for post in d.entries:
        desc_text = post.description
        hashed_desc = hashlib.md5(desc_text)
        existing_flag = check_for_desc(hashed_desc.hexdigest())
        if existing_flag == 'n':
            report_seq = report_seq + 1
            expl_report_cols['REPORT_SEQ'] = report_seq
            expl_report_cols['REPORT_NUM'] = report_seq
            expl_report_cols['TARGET_ID'] = report_seq
            expl_report_cols['SERVICE_UUID'] = 'NESSim_ptwc'
            expl_report_cols['iir_significance'] = 's' + str(random.randint(1, 99))
            expl_report_cols['mission_nsc'] = 'miss' + str(random.randint(1, 99))
            expl_report_cols['DESCR_TEXT'] = post.title
            expl_report_cols['DESCR_MORE_TEXT'] = post.description
            expl_report_cols['IDC_LATITUDE'] = post.geo_lat
            expl_report_cols['IDC_LONGITUDE'] = post.geo_long
            expl_report_cols['mission_number'] = str(random.randint(500, 1000))
            expl_report_cols['ro_type'] = random.choice(ro_type)
            expl_report_cols['correction_flag'] = 'N'
            expl_report_cols['iir_type'] = random.choice(iir_filters)
            expl_report_cols['nbrg'] = random.choice(nbrg)
            expl_report_cols['declassification_text'] =random.choice(declass_text)
            expl_report_cols['item_type'] = 'TS'
            expl_report_cols['agency'] = 'PTWC'
            expl_report_cols['security_code'] = 'U'
            expl_report_cols['DESC_HASH'] = hashed_desc.hexdigest()

            write_dict_to_database('expl_report', expl_report_cols)
            create_target_record(target_cols, report_seq,post.geo_lat, post.geo_long)
            dmc_record = get_dmc_record(post.geo_lat,post.geo_long)

            if 'image_id_text' not in dmc_record:
                logger.info('Record found in DMC')
            else:
                create_photo_record(post.geo_lat, post.geo_long, dmc_record, report_seq)
        else:
            logger.info('Record Exist')

def get_disease_outbreak_news():
    d = feedparser.parse('http://www.who.int/feeds/entity/csr/don/en/rss.xml')

    ### Get column names ###
    cable_cols = get_column_names('cable_released')
    cable_seq = get_seq_value('cable_released', 'cable_released_seq')

    for post in d.entries:
        desc_text = post.description
        desc_notags = strip_tags(desc_text)
        hashed_desc = hashlib.md5(desc_notags.encode("utf-8"))
        existing_flag = check_for_cable_record(hashed_desc.hexdigest())
        if existing_flag == 'n':
            cable_seq = cable_seq + 1
            cable_cols['cable_released_seq'] = cable_seq
            cable_cols['cable_number'] = cable_seq
            cable_cols['SERVICE_UUID'] = 'NESSim_DOB'
            cable_cols['cable_type'] = 'Disease Outbreak News'
            cable_cols['cable_text'] = desc_text.encode('utf-8')
            cable_cols['declassification_text'] = 'World Health Organization'
            cable_cols['security_code'] = 'U'
            #cable_cols['date_created'] = post.published
            cable_cols['DESC_HASH'] = hashed_desc.hexdigest()

            write_cable_report('cable_released', cable_cols)
        else:
            logger.info("Record Exist")

def create_photo_record(lat, long, dmc_record, target_id):
    ### Setup Oracle Connection ####
    dsnStr = cx_Oracle.makedsn('oracle11.compusult.net','1521','devel11')
    con = cx_Oracle.connect(user="nes_simulator", password="wes", dsn=dsnStr)
    cursor = con.cursor()

    expl_phot_seq = get_seq_value('expl_phot','expl_phot_seq')
    expl_photo_cols = get_column_names('expl_phot')

    ###Rounding off focus_plane_grazing_angle ###
    angle_of_coverage = dmc_record['focus_plane_grazing_angle']
    if angle_of_coverage is None:
        angle_of_coverage = 0
    else:
        angle_of_coverage = math.ceil(angle_of_coverage*100)/100

    percent_coverage = dmc_record['cloud_cover_percentage_rate']
    if percent_coverage is None:
        percent_coverage = 0


    expl_phot_seq = expl_phot_seq + 1
    expl_photo_cols['IMAGE_ID'] = dmc_record['image_id_text']
    expl_photo_cols['TARGET_ID'] = target_id
    expl_photo_cols['REPORT_NUM'] = target_id
    expl_photo_cols['MISSION_NUMBER'] = str(random.randint(500, 1000))
    expl_photo_cols['ANGLE_OF_COVERAGE'] = angle_of_coverage
    expl_photo_cols['PERCENT_COVERAGE'] = percent_coverage
    expl_photo_cols['SECURITY_CODE'] = dmc_record['security_class_code']
    expl_photo_cols['PLATFORM_TYPE'] = dmc_record['platform_code']
    expl_photo_cols['EXPL_PHOT_SEQ'] = expl_phot_seq
    expl_photo_cols['Y_COORD'] = long
    expl_photo_cols['X_COORD'] = lat

    sql = 'INSERT INTO EXPL_PHOT('
    for k,v in expl_photo_cols.items():
        if v is not 'null':
            sql = sql + k + ','
    sql = sql[:-1]
    sql = sql + ') VALUES('

    for k,v in expl_photo_cols.items():
        v = str(v)
        if v is not 'null':
            if v.isdigit() == True:
                sql = sql +   v + ","
            if v.isdigit() == False:
                if k == 'IDC_LONGITUDE':
                    sql = sql +   v + ","
                elif k == 'idc_longitude':
                    sql = sql +   v + ","
                elif k == 'IDC_LATITUDE':
                    sql = sql +   v + ","
                elif k == 'idc_latitude':
                    sql = sql +   v + ","
                else:
                    sql = sql + "'" + v + "'" + ","

    sql = sql[:-1]
    sql = sql + ')'

    logger.info(sql)
    cursor.execute(sql)
    sql = "commit"
    cursor.execute(sql)
    cursor.close()
    con.close()

def generate_geom():
    ### Setup Oracle Connection ####
    dsnStr = cx_Oracle.makedsn('oracle11.compusult.net','1521','devel11')
    con = cx_Oracle.connect(user="nes_simulator", password="wes", dsn=dsnStr)
    cursor = con.cursor()
    ### Get report_seq value ###
    cursor = con.cursor()
    sql = "update expl_report set geom = MDSYS.SDO_GEOMETRY(2001, 8307, MDSYS.SDO_POINT_TYPE (idc_longitude, idc_latitude,NULL),NULL,NULL)"
    cursor.execute(sql)
    sql = "update target set geom = MDSYS.SDO_GEOMETRY(2001, 8307, MDSYS.SDO_POINT_TYPE (longitude, latitude,NULL),NULL,NULL)"
    cursor.execute(sql)
    sql = "commit"
    cursor.execute(sql)

    cursor.close()
    con.close()

def create_target_record(table_dict, report_seq, lat, long):
    ### Setup Oracle Connection ####
    dsnStr = cx_Oracle.makedsn('oracle11.compusult.net','1521','devel11')
    con = cx_Oracle.connect(user="NES_Simulator", password="wes", dsn=dsnStr)
    cursor = con.cursor()

    table_dict['TARGET_SEQ'] = report_seq
    table_dict['REPORT_NUM'] = report_seq
    table_dict['TARGET_ID'] = report_seq
    table_dict['LATITUDE'] = lat
    table_dict['LONGITUDE'] = long

    sql = 'INSERT INTO TARGET('
    for k,v in table_dict.items():
        if v is not 'null':
            sql = sql + k + ','
    sql = sql[:-1]
    sql = sql + ') VALUES('

    for k,v in table_dict.items():
        if v is not 'null':
            v = str(v)
            if v.isdigit() == True:
                sql = sql +   v + ","
            if v.isdigit() == False:
                if k == 'IDC_LONGITUDE':
                    sql = sql +   v + ","
                elif k == 'idc_longitude':
                    sql = sql +   v + ","
                elif k == 'IDC_LATITUDE':
                    sql = sql +   v + ","
                elif k == 'idc_latitude':
                    sql = sql +   v + ","
                else:
                    sql = sql + "'" + v + "'" + ","
    sql = sql[:-1]
    sql = sql + ')'

    logger.info(sql)
    cursor.execute(sql)
    sql = "commit"
    cursor.execute(sql)
    cursor.close()
    con.close()

def get_world_news():
    d = feedparser.parse('http://rss.ireport.com/feeds/oncnn.rss')

    ### Get column names ###
    ip_report_cols = get_column_names('IP_REPORT')
    ip_report_seq = get_seq_value('ip_report', 'ip_report_seq')

    for post in d.entries:
        desc_text = post.description
        desc_notags = strip_tags(desc_text)
        desc_notags = desc_notags.replace("'", "''")
        hashed_desc = hashlib.md5(desc_notags.encode("utf-8"))
        existing_flag = check_for_IP_record(hashed_desc.hexdigest())
        if existing_flag == 'n':
            ip_report_seq = ip_report_seq + 1
            ip_report_cols['ip_report_seq'] = ip_report_seq
            ip_report_cols['report_num'] = ip_report_seq
            ip_report_cols['SERVICE_UUID'] = 'NESSim_CNN'
            ip_report_cols['IP_RPT_TEXT'] = desc_notags
            ip_report_cols['declassification_text'] = 'iReports on CNN'
            ip_report_cols['security_code'] = 'U'
            ip_report_cols['DESC_HASH'] = hashed_desc.hexdigest()

            write_cable_report('ip_report', ip_report_cols)
        else:
            logger.info('Record Exist')

def get_national_news():
    d = feedparser.parse('http://www.cbc.ca/thenational/blog/atom.xml')


    for post in d.entries:
        desc_text = post.description
        desc_notags = strip_tags(desc_text)
        desc_notags = desc_notags.replace("'", "''")
        hashed_desc = hashlib.md5(desc_notags.encode("utf-8"))
        existing_flag = check_for_cable_record(hashed_desc.hexdigest())
        print('***************************************')
        print('title: ' + post.title)
        print('description: ' + post.description)
        print('published: ' + post.published)
        print('summary: ' + post.summary)
        print(post.content[0].value)


def main():

    set_global_variables()
    try:
        get_tsunami_data()
    except:
        logger.error('Failed to get Tsunami data')

    try:
        get_gdacs_hurricane_data()
    except:
        logger.error('Failed to get Hurricane data')

    try:
        get_earthquack_data()
    except:
        logger.error('Failed to get Earthquack')

    generate_geom()

    try:
        get_disease_outbreak_news()
    except:
        logger.error('Failed to get disease outbreak news')

    try:
        get_world_news()
    except:
        logger.error('Failed to get world news')


    #get_national_news()


    logger.info('Finished Population')


if __name__ == '__main__':
    main()
    
