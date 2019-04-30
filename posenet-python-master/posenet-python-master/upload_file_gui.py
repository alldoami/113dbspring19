#! Python 3.4
"""
Open a file dialog window in tkinter using the filedialog method.

Tkinter has a prebuilt dialog window to access files. 

This example is designed to show how you might use a file dialog askopenfilename
and use it in a program.
"""

from tkinter import filedialog
from tkinter import *
from tkinter import ttk

root = Tk()
returnOpenFile = ""

def openFile():
    root.filename =  filedialog.askopenfilename(initialdir = "C:/Users/Allison/Downloads/",title = "Select file",filetypes = (("avi files","*.avi"),("all files","*.*")))
    returnOpenFile = root.filename
    print(returnOpenFile)
    return returnOpenFile
def uploadFileGUI():
  root.title("WeightLiftHelper")
  label = ttk.Label(root, text = "In order to check your form, please upload a video of type *.api").pack()
  Title = root.title( "File Opener")
  btn = ttk.Button(root, text= "Upload File")
  btn.pack()
  getFile = openFile()
  btn.config(command=getFile)
  return getFile
  