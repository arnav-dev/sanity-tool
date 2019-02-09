'''
## Program: sanity_ui.py
## Authors: Arnav Sharma
##
## Date: 
'''

from Tkinter import *
import tkMessageBox
from ScrolledText import *
import sys

from serror import *
import sglobals
from scommands import run_cmd
from sbrowser import stage1, stage3

''' Declare global variables here'''
S1 = False
S2 = False
S3 = False
RID = ""
URL = ""
VERBOSE = True
HELP = False

class IORedirector(object):
    '''A general class for redirecting I/O to this Text widget.'''
    def __init__(self,text_area):
        self.text_area = text_area

class StdoutRedirector(IORedirector):
    '''A class for redirecting stdout to this Text widget.'''
    def write(self, raw_msg):
        msg = raw_msg
        self.text_area.config(state=NORMAL)
        self.text_area.insert(END, msg, 'STDOUT')  
        self.text_area.config(state=DISABLED)
        root.update_idletasks()

class StderrRedirector(IORedirector):
    '''A class for redirecting stderr to this Text widget.'''
    def write(self, raw_msg):
        msg = raw_msg + '\n'
        self.text_area.config(state=NORMAL)
        self.text_area.insert(END, msg, 'STDERR')  
        self.text_area.config(state=DISABLED)
        root.update_idletasks()

class App:

    def __init__(self, master):
        frame_in1 = Frame(master)
        frame_in1.grid(row=0, column=0, padx=5, pady=5, sticky=N+W+E+S)

        Label(frame_in1, text="URL: ").grid(row=0, column=0, sticky=E)
        self.url_entry = Entry(frame_in1, width=60)
        self.url_entry.grid(row=0, column=1, columnspan=3, sticky=N+W+E+S,
                            padx=5, pady=5)
        self.url_entry.insert(0, sglobals.BASE_URL)

        frame_in1.grid_columnconfigure(0, weight=0)
        frame_in1.grid_columnconfigure(1, weight=1)

        frame_in2 = Frame(master)
        frame_in2.grid(row=1, column=0, padx=5, pady=5, sticky=N+W+E+S)

        Label(frame_in2, text="RID: ").grid(row=0, column=0, sticky=E)
        self.rid_entry = Entry(frame_in2, width=10)
        self.rid_entry.grid(row=0, column=1, sticky=W, padx=5, pady=5)

        self.rid_msg = StringVar()
        self.status_label = Label(frame_in2, textvariable=self.rid_msg, fg="Red")
        self.status_label.grid(row=0, column=2, padx=5, pady=5)

        self.verbose_ck = BooleanVar()
        c = Checkbutton(frame_in2, text="Show Details", variable=self.verbose_ck,
                        onvalue=True, offvalue=False, command=self.verbose)
        c.select()
        c.grid(row=0, column=3, sticky=E)
        
        self.rid_entry.focus_set()

        frame_in2.grid_columnconfigure(2, weight=1)
        
        frame_but = Frame(master)
        frame_but.grid(row=2, column=0, padx=5, pady=5, sticky=N+E+W+S)
        
        self.button1 = Button(
            frame_but, padx=5, pady=5, text="Sanity", command=self.dosanity 
            )
        self.button1.grid(row=0, column=0)
        
        self.button2 = Button(
            frame_but, padx=5, pady=5, text="Stage 1", command=self.stage1
            )
        self.button2.grid(row=0, column=1)

        self.button3 = Button(
            frame_but, padx=5, pady=5, text="Stage 3", command=self.stage3
            )
        self.button3.grid(row=0, column=2)

        self.button4 = Button(
            frame_but, padx=5, pady=5, text="About", command=self.about
            )
        self.button4.grid(row=0, column=3, sticky=E)

        frame_but.grid_columnconfigure(0, weight=1)
        frame_but.grid_columnconfigure(1, weight=1)
        frame_but.grid_columnconfigure(2, weight=1)
        frame_but.grid_columnconfigure(3, weight=1)

        frame_out = Frame(master)
        frame_out.grid(row=3, column=0, padx=5, pady=5, sticky=N+E+W+S)

        self.output = ScrolledText(frame_out, width=60, height=12, state=NORMAL)
        self.output.grid(row=0, column=0, sticky=N+E+W+S)

        self.output.tag_configure('STDOUT',background='white',foreground='black')
        self.output.tag_configure('STDERR',background='white',foreground='red')
        sys.stdout = StdoutRedirector( self.output )
        sys.stderr = StderrRedirector( self.output )

        frame_out.grid_columnconfigure(0, weight=1)
        frame_out.grid_rowconfigure(0, weight=1)

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(3, weight=1)

    def dosanity(self):

        global S1, S2, S3

        S1 = False
        S2 = False
        S3 = False
        
        clear_out()
        main()
        
    def stage1(self):

        global S1, S2, S3

        S1 = False
        S2 = False
        S3 = False
        clear_out()
        if self.rid_correct():
            S1 = True
            self.set_url() 
            main()

    def stage3(self):

        global S3, S2, S3

        S1 = False
        S2 = False
        S3 = False
        clear_out()
        if self.rid_correct():
            S3 = True
            self.set_url()
            main()

    def about(self):
        tkMessageBox.showinfo("About", shelp.__doc__)

    def set_url(self):

        global URL
        url = self.url_entry.get()
        if sglobals.BASE_URL == url:
            URL = ""
        else:
            URL = url

    def verbose(self):

        global VERBOSE
        
        if self.verbose_ck.get():
            VERBOSE = True
        else:
            VERBOSE = False

    def rid_correct(self):

        global RID
        
        rid_var = self.rid_entry.get()
        if rid_var:
            if rid_var.isdigit():
                RID = rid_var
                show_status(app, "", "Black")
                return True
            else:
                show_status(app, "Invalid RID", "Red")
                return False
        else:
            show_status(app, "Enter RID", "Red")
            return False

def clear_out():
    app.output.config(state=NORMAL)
    app.output.delete(1.0, END)
    app.output.config(state=DISABLED)
    root.update_idletasks()

def shelp():
    '''Do sanity tests of a device and update on SCM portal.

Sanity:  Do sanity tests for a device.
Stage 1: Do Sanity tests and update Stage 1 results on SCM portal.
Stage 3: Do Sanity tests and update Stage 3 results on SCM portal.
About:   Show this information.

------------------------------
Program developed by: Parishkrit Jain, Sanchit Kwatra
for File Systems team at SRI-Noida.
    '''
    pass

def show_status(obj, msg, color):
    obj.status_label.config(fg=color)
    obj.rid_msg.set(msg)

def main():

    global S1, S2, S3, VERBOSE, RID, URL

    show_status(app, "Running...", "Black")
    root.update_idletasks()

    if not (S1 or S2):
        if VERBOSE:
            print("--- Running sanity tests...")   
        flag_error, flag_issue = run_cmd(VERBOSE)
        
        if flag_error:
            print("--- Program terminated due to errors.")
            show_status(app, "Error", "Red")
            return
        
        if flag_issue:
            print("--- Issues were found. Results not posted.")
            show_status(app, "Issue Found", "Red")
            return
            
        if VERBOSE:
            print("--- Tests were successful.")    

    if S1:
        if VERBOSE:
            print("--- Updating Stage 1 results on portal...")
        flag_error, flag_warn = stage1(RID, URL)
        if VERBOSE:
            if flag_warn:
                print_error()
        if flag_error:
            print("--- Program will terminate due to errors.")
            show_status(app, "Error", "Red")
            return

    if S3:
        if VERBOSE:
            print("--- Updating Stage 3 results on portal...")
        flag_error, flag_warn = stage3(RID, URL)
        if VERBOSE:
            if flag_warn:
                print_error()
        if flag_error:
            print("--- Program will terminate due to errors.")
            show_status(app, "Error", "Red")
            return

    show_status(app, "Success", "Green")
    
root = Tk()
app = App(root)
root.title(sglobals.APP_TITLE)

root.mainloop()
