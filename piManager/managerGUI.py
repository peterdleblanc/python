__author__ = 'Peter LeBlanc'

#from tkinter import *
import tkinter as tk


class App():

    def __init__(self, master):


        self.status_message = tk.StringVar()
        self.status_message.set('Unknowen')
        self.rec_status = self.status_message.get()

        self.status_label = tk.Label(root, text="No status updated", textvariable=self.status_message)
        self.user = tk.Entry(root)
        self.password = tk.Entry(root)

        self.login_button = tk.Button(text="Login", command=self.login_managerGUI)
        self.quit_button = tk.Button(text="Quit", command=self.quit_managerGUI)


        tk._default_root.grid_location(0,0)
        self.status_label.grid(row=0, column=1,columnspan=2)
        self.user.grid(row=1, column=1)
        self.password.grid(row=1, column=2)

        self.quit_button.grid(row=3, column=1)
        self.login_button.grid(row=3, column=2)


    def quit_managerGUI(self):
        raise SystemExit

    def login_managerGUI(self):
        print('Login button pressed')
        self.status_message.set('Status is stale please request a status update')


root = tk.Tk()

app = App(root)

root.mainloop()
#root.destroy() # optional; see description below
