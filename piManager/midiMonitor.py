__author__ = 'peter'
import time
import os
import webserviceLauncher
import serialTesting
import logging
import mido
from mido import Message
import threading

logger = logging.getLogger(__name__)

class MidiMonitor():
    '''
    Class to monitor midi port to perform hotkey actions
    '''

    logging.basicConfig(level=logging.DEBUG)
    handler = logging.FileHandler('./logs/piManager.log')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(threadName)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


    def __init__(self):
        self.name = 'midi Monitor'
        self.msg = ''
        self.inputDevices = mido.get_input_names()

    def monitor_port(self):
        launcher = webserviceLauncher.Launcher()

        print(mido.get_output_names())
        print(mido.get_input_names())

        outport = mido.open_output('LPD8 MIDI 1')
        msg = Message(note=7, channel=10,type='note_on',velocity=17, time=0)
        msg = Message(note=7, channel=10,type='note_on',velocity=17, time=0)
        outport.send(msg)

        print(self.inputDevices)

        p = mido.Parser()
        controlKnobs = {}


        with mido.open_input('LPD8 MIDI 1') as inport:
            for msg in inport:
                print(msg)
                if hasattr(msg, 'note'):
                    if msg.note == 4 and msg.type =='note_on':
                        launcher.startHomeWebservice()
                    elif msg.note == 4 and msg.type =='note_off':
                        launcher.stopHomeWebservice()
                    elif msg.note == 0 and msg.type =='note_off':
                        serialTesting.toggleOffPIN4()
                    elif msg.note == 0 and msg.type =='note_on':
                        serialTesting.toggleOnPIN4()
                    elif msg.note == 7 and msg.type =='note_off':
                        raise SystemExit
                    elif msg.note == 2:
                        print(controlKnobs['cc8'])
                    elif msg.note == 1:
                        serialTesting.readPin9()
                    elif msg.note == 3:
                        print(threading.enumerate())

                if hasattr(msg, 'control'):
                    if msg.control == 8:
                        controlKnobs['cc8'] = msg.value
                    elif msg.control == 9:
                        controlKnobs['cc9'] = msg.value
                    elif msg.control == 10:
                        controlKnobs['cc10'] = msg.value
                    elif msg.control == 11:
                        controlKnobs['cc11'] = msg.value
                    elif msg.control == 12:
                        controlKnobs['cc12'] = msg.value
                    elif msg.control == 13:
                        controlKnobs['cc13'] = msg.value
                    elif msg.control == 14:
                        controlKnobs['cc14'] = msg.value
                    elif msg.control == 15:
                        controlKnobs['cc15'] = msg.value

