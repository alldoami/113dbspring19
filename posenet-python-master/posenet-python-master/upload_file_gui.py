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
exercise = 0


def openFile():
  root.filename =  filedialog.askopenfilename(initialdir = "C:/Users/Allison/Downloads/",title = "Select file",filetypes = (("avi files","*.avi"),("all files","*.*")))
  returnOpenFile = root.filename
  print(returnOpenFile)
  return returnOpenFile
def setPullUp():
  exercise = 1
def setPushUp():
  exercise = 2
def setSquat():
  exercise = 3

def uploadFileGUI():
  root.title("WeightLiftHelper")
  label = ttk.Label(root, text = "In order to check your form, please upload a video of type *.api").pack()
  Title = root.title( "File Opener")
  btn = ttk.Button(root, text= "Upload File")
  btn_pull_up = ttk.Button(root, text = "Pull Up")
  btn_push_up = ttk.Button(root, text = "Push Up")
  btn_squat = ttk.Button(root, text = "Squat")
  btn.pack()
  btn_pull_up.pack()
  btn_push_up.pack()
  btn_squat.pack()
  #getFile = openFile()
  btn.config(command=openFile())
  btn_pull_up.config(command=setPullUp)
  btn_push_up.config(command=setPushUp)
  btn_squat.config(command=setSquat)
  if exercise != 0:
    return returnOpenFile, exercise
  
