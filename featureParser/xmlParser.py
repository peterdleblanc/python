__author__ = 'peter'

import xml.etree.ElementTree as ET
from collections import OrderedDict
import shapefile


def main():
    tree = ET.parse('mgcp-style-trd4.xml')
    root = tree.getroot()

    features = []
    f = open('featuresList.txt', 'w')
    for feature in root.findall('Style'):
        features.append(feature.get('name'))
        f.write(feature.get('name') + '\n')

    f.close()


    rulesList=[]
    for rule in root.findall('Style/Rule/Filter'):
        rulesList.append(rule.text)


    f = open('removedComments.txt', 'w')
    genLog = open('GeneratedFiles.txt', 'w')
    for feature in features:
        rules = []

        searchString = ".//*[@name='" + feature + "']/Rule/Filter"
        for rule in root.findall(searchString):
            rules.append(rule.text)

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

        #***********************  Removed Dups  **************************
        #comments = list(OrderedDict.fromkeys(comments))

        rules = list(OrderedDict.fromkeys(rules))


        filters = {'BAC':0,'BAL':0,'BOC':0,'BOT':0,'BST':0,'CAT':0,'CNS':0,'CSP':0,'DMT':0,'EET':0,'ESC':0,'FFN':0,'FFP':0,'FIC':0,'FMM':0,'FUN':0,'GEC':0,'HAF':0,'HCT':0,'HGT':0,'HQC':0,'HWT':0,'HYP':0,'LOC':0,'LSP':0,'LTN':0,'LUN':0,'MCC':0,'MZN':0,'NAM':0,'ORD':0,'PPO':0,'RGC':0,'RIR':0,'RRA':0,'RRC':0,'RST':0,'SCC':0,'SDT':0,'SEP':0,'SLT':0,'SMC':0,'SSC':0,'STA':0,'SUY':0,'TRE':0,'TRS':0,'TTC':0,'TXT':0,'VSP':0,'WID':0,'WLE':0,'WST':0,'WTC':0,'ZVH':0}
        count = 0
        lat = 50
        lon = 60
        for rule in rules:
            for k,v in filters.items():
                if k in rule:
                    filters[k] = 1
            requiredFilters = []
            for k,v in filters.items():
                if v == 1:
                    requiredFilters.append(k)


            w = shapefile.Writer(shapefile.POINT)
            w.autoBalance = 1

            if feature.startswith('P'):
                if lon <= 50:
                    lat = lat - 2
                    lon = 60
                else:
                    lon = lon - 2
                w.point(lat,lon)

            if feature.startswith('L'):
                if lon <= 50:
                    lat = lat - 2
                    lon = 60
                else:
                    lon = lon - 2
                for i in range(1,4):
                    lon = lon + 0.3
                    w.point(lat,lon)

            if feature.startswith('A'):
                if lon <= 50:
                    lat = lat - 2
                    lon = 60
                else:
                    lon = lon - 2
                tl = (lat, lon)
                tr = (lat, lon - 0.3)
                bl = (lat - 0.3,lon + 0.3)
                br = (lat, lon - 0.3)
                w.poly(parts=[[tl,tr,bl,br]])
            w.field('PSNUM')
            w.field('FILTER')
            for x in requiredFilters:
                w.field(x)

            writeValues= []
            writeValues.append(comments[count])
            writeValues.append(rule)
            for x in requiredFilters:
                writeValues.append(0)

            w.record(*writeValues)
            print('Saving ' + comments[count])
            genLog.write(comments[count] + '\n')
            w.save(comments[count])
            count = count + 1

    f.close()
    genLog.close()



if __name__ == '__main__':
    main()



