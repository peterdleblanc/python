__author__ = 'peter'
import os
import subprocess
import logging

#logging.basicConfig(filename='output.log',level=logging.DEBUG)
logging.basicConfig(filename='output.log', format='%(levelname)s:%(message)s', level=logging.DEBUG)
from tkinter import *

def process_files():
    logging.info("Input Location:" + inputLocation.get())
    logging.info("Output Location:" + e2.get())
    files = []
    i = inputLocation.get()
    os.chdir(i)
    try:
        os.mkdir('./processing')
    except FileExistsError as e:
        pass

    for file in os.listdir('./'):
        if file.endswith(".tif"):
            files.append(file)

    for x in files:
        logging.info(x)
        if hillShade.get() == 1:
            modTiff=subprocess.Popen(['gdaldem','hillshade',x , './processing/hillshade_'+ x, '-z','5','-s','111120'])
            output = modTiff.communicate()
            logging.info(output)

        if colorRelief.get() == 1:
            modTiff=subprocess.Popen(['gdaldem', 'color-relief', x, 'ramp.txt', './processing/color_'+x])
            output = modTiff.communicate()

        print('process complete')


    Message(master, text='output').grid(row=6, column=0, columnspan=2, pady=4)


master = Tk()


Label(master, text="Input Location").grid(row=0)
Label(master, text="Output Location").grid(row=1)

inputLocation = Entry(master)
e2 = Entry(master)

inputLocation.grid(row=0, column=1)
e2.grid(row=1, column=1)

hillShade = IntVar()
Checkbutton(master, text="Hillshade", variable=hillShade).grid(row=3, column=0, sticky=W)

colorRelief = IntVar()
Checkbutton(master, text="Color Relief", variable=colorRelief).grid(row=3, column=1, sticky=W)

merge = IntVar()
Checkbutton(master, text="Merge", variable=merge).grid(row=4, column=0, sticky=W)

trans = IntVar()
Checkbutton(master, text="Transparency", variable=trans).grid(row=4, column=1, sticky=W)


Button(master, text='Quit', command=master.quit).grid(row=5, column=0, sticky=W, pady=4)
Button(master, text='Process', command=process_files).grid(row=5, column=1, sticky=W, pady=4)


mainloop()

