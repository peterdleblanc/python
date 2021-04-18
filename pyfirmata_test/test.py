__author__ = 'peter'
from time import sleep
from pyfirmata import Arduino, util

port = '/dev/ttyACM1'

def main():
    board = Arduino(port)
    sleep(2)
    #pin13 = board.get_pin('d:13:o')
    #pin13.write(1)
    while 1:
        board.digital[13].write(1)
        print(board.digital[13].read())
        sleep(4)
if __name__ == '__main__':
    main()