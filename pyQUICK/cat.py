__author__ = 'peter'

import sys

def cat(filename):
    f = open(filename, 'rU')
    for line in f:
        print line,

    f.close()

def cat2(filename):
    f = open(filename, 'rU')
    lines = f.readlines()
    print lines

def cat3(filename):
    f = open(filename, 'rU')
    text = f.read()
    print text

def main():
    cat(sys.argv[1])
    #cat2(sys.argv[1])
    #cat3(sys.argv[1])

if __name__ == '__main__':
    main()
