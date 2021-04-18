__author__ = 'peter'

import sys
import os
import commands

def listFiles(dir):
    filenames = os.listdir(dir)
    for filename in filenames:
        path = os.path.join(dir,filename)
        print path
        print os.path.abspath(path)
        #os.path.exist('/tmp/')
        #os.path.makedir
        #import shutil

def customCommands(dir):
    cmd = 'ls -l ' + dir
    (status, output) = commands.getstatusoutput(cmd)
    if status:
        sys.stderr.write( "There was a error: " + output)
        sys.exit(1)

    print output

def part3():


def main():
    #listFiles(sys.argv[1])
    #customCommands(sys.argv[1])
    part3()


if __name__ == '__main__':
    main()