__author__ = 'peter'


dic = { }

dic['a'] = 'alpha'
dic['o'] = 'omega'
dic['g'] = 'gamma'

dic['a']

dic.keys()

dic.values()


for x in sorted(dic.keys()):
    print 'key: ', x, '-->', dic[x]


dic.items()

for tuple in dic.items():
    print tuple



