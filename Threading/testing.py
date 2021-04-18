__author__ = 'peter'

import threading
import random

def Splitter(words):
    mylist = words.split()
    newList = []
    while (mylist):
        newList.append(mylist.pop(random.randrange(0,len(mylist))))
    print(' '.join(newList))


def main():
    sentance = 'I am a handsome beast. Word.'
    numOfThreads = 5
    threadList = []

    print('starting...\n')
    for i in range(numOfThreads):
        t = threading.Thread(target=Splitter, args=(sentance,))
        t.start()
        threadList.append(t)

    print('\n Thread Count: ' + str(threading.activeCount()))
    print('Exiting')

if __name__ == '__main__':
    main()
