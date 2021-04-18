__author__ = 'Peter LeBlanc'

from itertools import *

def main():

    lines = []
    currentName = 'pass'
    for line in open('./mgcp-style.xml', 'r'):

        if 'MinScaleDenominator' in line:
            pass
        elif 'MaxScaleDenominator' in line:
            pass
        elif 'LineSymbolizer' in line:
            pass
        elif '<!-- Symbol Type:' in line:
            pass
        elif '<TextSymbolizer' in line:
            pass
        elif '<PointSymbolizer' in line:
            pass
        elif 'PolygonPatternSymbolizer' in line:
            pass
        elif '<Rule>' in line:
            pass
        elif '</Rule>' in line:
            pass
        elif '</Style>' in line:
            pass
        elif 'name=' in line:
            if currentName == line[35:41]:
                pass
            else:
                lines.append('<*********************************************************************************>\n')
                lines.append(line[35:41] + '\n')
                currentName = line[35:41]

        elif line[:-1]:
            lines.append(line)

    f = open('features.txt', 'w')

    for line in lines:
        f.write(line)

    f.write('<*********************************************************************************>\n')
    f.close()

    featuresList = []
    for line in open('./features.txt', 'r'):
        line = line.strip()
        line = line.strip('<Filter>')
        line = line.strip('!-- ')
        line = line.strip('</')
        featuresList.append(line)

    x = 0
    featureMap = {}
    tempList = []
    for x in range(len(featuresList)-1 ):
        if '****************' in featuresList[x]:
            x = x + 1
            f = open(featuresList[x] + '.dat', 'w')
            feature = featuresList[x]
            while '***********' not in featuresList[x]:
                tempList = featuresList[x]
                f.write(featuresList[x] + '\n')
                x = x + 1
            f.close()
            featureMap[feature] = tempList

    keysList = []

    for k,v in featureMap.items():
        print(k)


if __name__ == '__main__':
    main()


