__author__ = 'peter'
import mido as myMidi

print(myMidi.get_output_names())
inport = myMidi.open_input()


from mido.ports import BaseIOPort

def _receive(self, block=True):
        # Non-blocking read like above.
        while True:
            data = device.read()
            if data:
                 parser.feed(data)


_receive()
