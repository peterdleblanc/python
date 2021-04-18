
__author__ = 'peter'

#####  External Imports ######

import xml.etree.ElementTree as ET
from collections import OrderedDict
import shapefile


def main():
    #### Opening xml file #####
    tree = ET.parse('mgcp-style-trd4.xml')
    root = tree.getroot()

    #### Getting list of all the features ####
    features = []
    f = open('featuresList.txt', 'w')
    for feature in root.findall('Style'):
        features.append(feature.get('name'))
        f.write(feature.get('name') + '\n')
    f.close()

    #### Getting list of all the rules ###
    rulesList=[]
    for rule in root.findall('Style/Rule/Filter'):
        rulesList.append(rule.text)

    #### Starting Creation of the shape files ###
    genLog = open('GeneratedFiles.txt', 'w')
    w = shapefile.Writer(shapefile.POINT)
    w.autoBalance = 1

    #### Starting list of features
    for feature in features:
        #### Get all the rules for a feature ####
        rules = []
        searchString = ".//*[@name='" + feature + "']/Rule/Filter"
        for rule in root.findall(searchString):
            rules.append(rule.text)

        #### Get a list PSNUM's for a feature ####
        comments =[]
        searchString = ".//*[@name='" + feature + "']/Rule/comments"
        for comment in root.findall(searchString):
            flag = comment.text
            if flag.startswith('PL'):
                comments.append(comment.text)
            elif flag.startswith('PS'):
                comments.append(comment.text)
            else:
                pass

        #### Removing duplicates rules for multiple scales #####
        rules = list(OrderedDict.fromkeys(rules))

        #### Creating dictonary of all attributes to get all required attributes referenced in the rules ####
        filters = {'BAC':0,'BAL':0,'BOC':0,'BOT':0,'BST':0,'CAT':0,'CNS':0,'CSP':0,'DMT':0,'EET':0,'ESC':0,'FFN':0,'FFP':0,'FIC':0,'FMM':0,'FUN':0,'GEC':0,'HAF':0,'HCT':0,'HGT':0,'HQC':0,'HWT':0,'HYP':0,'LOC':0,'LSP':0,'LTN':0,'LUN':0,'MCC':0,'MZN':0,'NAM':0,'ORD':0,'PPO':0,'RGC':0,'RIR':0,'RRA':0,'RRC':0,'RST':0,'SCC':0,'SDT':0,'SEP':0,'SLT':0,'SMC':0,'SSC':0,'STA':0,'SUY':0,'TRE':0,'TRS':0,'TTC':0,'TXT':0,'VSP':0,'WID':0,'WLE':0,'WST':0,'WTC':0,'ZVH':0}

        #Starting location for point geom
        plon = 50
        plat = 60
        #Starting location for line geom
        llat = 70
        llon = 80
        #Starting location for area geom
        alat = 100
        alon = 110

        count = 0
        #### Generate Shape File
        for rule in rules:
            #### Check all the rules for a feature and generate a list of attributes ####
            for k,v in filters.items():
                if k in rule:
                    filters[k] = 1
            requiredFilters = []
            for k,v in filters.items():
                if v == 1:
                    requiredFilters.append(k)

            #### Generate geom for point features ####
            if feature.startswith('P'):
                if plat <= 60:
                    plon = plon - 2
                    plat = 80
                else:
                    plat = plat - 2
                w = shapefile.Writer(shapefile.POINT)
                w.autoBalance = 1
                w.point(plon,plat)

            #### Generate geom for line features ####
            if feature.startswith('L'):
                if llon <= 50:
                    llat = llat - 2
                    llon = 60
                else:
                    llon = llon - 2
                w = shapefile.Writer(shapefile.POLYLINE)
                w.autoBalance = 1
                p1 = (llat,llon + 0.3)
                p2 = (llat,llon + 0.6)
                p3 = (llat,llon + 0.9)
                w.line(parts=[[p1,p2,p3]])
                w.poly(parts=[[p1,p2,p3]], shapeType=shapefile.POLYLINE)

            #### Generate geom for area features ####
            if feature.startswith('A'):
                if alon <= 100:
                    alat = alat - 2
                    alon = 110
                else:
                    alon = alon - 2
                tl = (alat, alon)
                tr = (alat-0.3, alon)
                br = (alat,alon - 0.3)
                bl = (alat -0.3, alon - 0.3)
                w = shapefile.Writer(shapefile.POLYGON)
                w.autoBalance = 1
                w.poly(parts=[[tl,tr,bl,br]])

            #### Creating base fields for shape file ####
            w.field('PSNUM')
            w.field('FILTER')
            #### Creating fields for attributes ####
            for x in requiredFilters:
                w.field(x)

            #### Making a list of values to write to shape file ####
            writeValues= []
            writeValues.append(comments[count])  #PSNUM
            writeValues.append(rule)    #Rule
            for x in requiredFilters:
                writeValues.append(0)  # Empty values for each attribute

            w.record(*writeValues)   # Write values to shape file
            genLog.write(feature + ':' + comments[count] + '\n')    #Log name of psnum reference to text file
            count = count + 1  ### Advance in list of psnum

        w.save(feature)   #### Save shape file to disk
        print(feature + ' Saved')

        # create the PRJ file
        prj = open("%s.prj" % feature, "w")
        epsg = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
        prj.write(epsg)
        prj.close()

    f.close()  ### Close logs
    genLog.close()  ### Close logs

    print('Shape File Generation Complete')

if __name__ == '__main__':
    main()



