import tkinter as tk
from tkinter import *


class InitialPage:
    def __init__(self, master):
        self.FinalPage = None
        self.frame = tk.Frame(master)
        self.frame.pack(padx=10, pady=10)

        disp_lbl = tk.Label(self.frame, text='displacement')
        disp_lbl.pack(padx=0, pady=10)
        self.neto = tk.IntVar()
        disp_entry = tk.Entry(self.frame, textvariable=self.neto)
        disp_entry.pack(padx=0, pady=10)

        button = tk.Button(self.frame, text='Open Settings', command=self.open)
        button.pack(padx=3, pady=10)

        button = tk.Button(
            self.frame, text='Update Settings', command=self.config)
        button.pack(padx=3, pady=10)

        self.label = tk.Label(self.frame, text='')
        self.label.pack(pady=10)

    def open(self):
        self.FinalPage = FinalPage(self.update)

    def config(self):
        self.FinalPage.entry_val.set(self.neto.get())

    def update(self, entry_val, option_choice):
        """
        here we want to call this function from the SettingsWidow
        class, so we put self.update in the function open, and in the
        FinalPage class, and in the submit function to be called
        by the submit button
        :return: None or what ever you want
        """
        print('Entry value is :', entry_val.get())
        print('Option Choice  is :', option_choice.get())
        self.label.configure(text=entry_val.get() +
                             ' ' + str(option_choice.get()))


class FinalPage:
    def __init__(self, update):
        top = tk.Toplevel()
        self.frame = tk.Frame(top)
        self.frame.pack(padx=10, pady=10)
        self.update = update

        self.entry_val = tk.StringVar()
        entry = tk.Entry(top, textvariable=self.entry_val)
        entry.pack(padx=60, pady=30)

        self.option_choice = tk.IntVar()
        option1 = tk.Radiobutton(
            top, value=1, text='Option1', variable=self.option_choice)
        option1.pack(padx=10, pady=20)
        option2 = tk.Radiobutton(
            top, value=2, text='Option2', variable=self.option_choice)
        option2.pack(padx=10, pady=20)

        button = tk.Button(top, text='Apply Settings', command=self.submit)
        button.pack(pady=10)

    def submit(self):
        self.update(self.entry_val, self.option_choice)


root = tk.Tk()
window = InitialPage(root)
root.geometry('400x300')
root.title('Passing Data between pages')
root.mainloop()
