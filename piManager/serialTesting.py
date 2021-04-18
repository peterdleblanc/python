__author__ = 'Peter LeBlanc'

from time import sleep
from pyfirmata import util
import pyfirmata

try:
    port = '/dev/ttyACM0'
except Exception as e:
    print('Device not found on ttyACM0')
finally:
    port = '/dev/ttyACM1'

print('Setting up Serial connection to the Arduino')
board = pyfirmata.Arduino(port)
ledPin4 = board.get_pin('d:4:o')

def get_pin_state(pin):

    board = pyfirmata.Arduino(port)
    sleep(3)
    ledPin = board.get_pin('d:8:o')
    state = ledPin.read()
    return state


def toggleOffPIN4():
    print('Updating pin to off')
    ledPin4.write(0)


def toggleOnPIN4():
    print('Updating pin to on')
    ledPin4.write(1)

def readPin9():
    it = util.Iterator(board)
    it.start()
    board.analog[0].enable_reporting()
    print(board.analog[0].read())
    #it.start()

def readPin8():
    #state = ledPin4.read()
    state = board.digital[8].read()
    print(state)
    return state

def main():
    pass
    #toggleOffPIN4()
    #pin = 12
    #delay = 2
    #message = 'cycle complete'
    #blinkLED(pin, delay, message)

if __name__ == '__main__':
    main()

