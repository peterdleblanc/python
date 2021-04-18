__author__ = 'peter'

lines = []
for line in open('./AnnexH_raw.txt', 'r'):
    if line[:-1]:
        lines.append(line)

description_location = []
description_ref = {}
component_ref= {}


line_count = 0
for line in lines:
    #print(line)
    if 'Description:' in line:
        description_location.append(line_count)
    if 'Component Ref #' in line:
        #print('*****************************')
        component = lines[line_count].lstrip('Component Ref #: ')
    else:
        pass
    line_count += 1
    print(line_count)

starts = []
ends = []
flag = True

for location in description_locations:
    if flag is True:
        starts.append(location)
        flag = False
    else:
        ends.append(location)
        flag = True

for x in starts:
    print(x)


for i in range(len(starts)):
    #:w
    # print(component_ref[i])
    filename = component_ref[i].lstrip('Component Ref #: ')
    filename = filename + '.txt'
    f = open(filename, 'w')

    for x in range(starts[i],ends[i]):
        f.write(lines[x])
    f.close()




