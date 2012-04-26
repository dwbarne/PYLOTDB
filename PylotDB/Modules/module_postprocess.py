#!/usr/local/bin/python     # for *nix runs
# ===== Header =====
# Filename: module_postprocess.py
# author: dwbarne
# creation date: Thu, 11-06-2008

# Purpose:
"""
creates frames for the Post-Process tab, then
fills them with desired widgets

"""

from Tkinter import *
from tkMessageBox import *
import Pmw
#import module_spawnprogram
from tkMessageBox import *
import tkFont
import os
from tkFileDialog import *
import module_Editor
#import module_GnuPlot
import module_Editor2
import module_PylabPlot

# Define globals
# ... Text frame width and height
w_frameText = 75        # default: 75
h_frameText = 30        # default: 30

#  ... main Window placement relative to top left of screen
x_Windows = 75
y_Windows = 200

# ... subwindows
xwin=75
ywin=300

# width of frame for line numbers in text box
widthLineNumbersFrame = 6
widthLineNumbers = widthLineNumbersFrame - 0
# put together format string used in handlerTextLineNumbers; numbers are right justified
stringLineNumberFormat = '%' + str(widthLineNumbers) + 'd'

#   ... current directory
currentDirectory = os.getcwd().split('\\').pop()
currentDirectoryFullPath = os.getcwd()

colorbg1='lightgreen'

colorbg2='tan'

def main_postprocess(self,parentFrame,shell,bgcolor):
    """
    setup frames and widgets in parentFrame
    """
    self.shell=shell
    self.parentFramePostProcess=parentFrame
    
    self.parentFrame00 = Frame(
        parentFrame,
        bg=bgcolor,
        )
    self.parentFrame00.grid(
        row=0,
        column=0,
        padx=5,
        pady=5,
        sticky=N
        )
        
    self.parentFrame00_0 = Frame(
        self.parentFrame00,
        bg=bgcolor,
        )
    self.parentFrame00_0.grid(
        row=0,
        column=0,
        padx=5,
        pady=5,
        sticky=N,
        ) 

    self.parentFrame00_1 = Frame(
        self.parentFrame00,
        bg=bgcolor,
        )
    self.parentFrame00_1.grid(
        row=1,
        column=0,
        padx=5,
        pady=5,
        sticky=N,
        )
        
    self.parentFrame01 = Frame(
        parentFrame,
        bg=bgcolor,
        )
    self.parentFrame01.grid(
        row=0,
        column=1,
        padx=5,
        pady=5,
        )
        
#----------------------

# setup editor in frames 00 and 10        
#    module_Editor.my_Editor(
#        self,
#        self.parentFrame00,
#        self.parentFrame01,
#        bgcolor,
#        'PLOT FILE',
#        )
        
    instance_EditorPostProcess = module_Editor2.Editor(
        self.parentFrame00_0,   # frame for buttons
        self.parentFrame01,     # frame for editor
        bgcolor,
        'PLOT FILE',
        self.titleFont,
        self.dataFont,
        )

# GNU PLOT button in frame 10
    buttonPylabPlot = Button(
        self.parentFrame00_1,
        text='Plot...',
        borderwidth=5,
        relief=RAISED,
        width=15,
#        command=handlerButtonGnuPlot(self),
        command=handlerPylabPlot(self),
        )
    buttonPylabPlot.grid(
        row=0,
        column=0,
        padx=5,
        pady=15,
        )
        

def handlerButtonGnuPlot(self):
    """
    calls module_GnuPlot for plots in a separate frame
    """
    global xwin, ywin
    print '\n In handlerButtonGnuPlot'
    
    def tempDef():
        global xwin, ywin
    
        module_GnuPlot.gnuPlot(
            self,
            xwin,
            ywin,
            self.shell,
            colorbg2
            )
            
    return tempDef
    
    
def handlerPylabPlot(self):
    """
    calls module_PylabPlot for plots in separate frame
    """
    
    def tempDef():
        module_PylabPlot.PlotsForPylot(
            self,
            self.parentFramePostProcess,
            xwin,
            ywin,
            self.shell,
            colorbg2,
            1   # 1 for demo plots, 0 for regular plots
            )
        
    return tempDef
    
    
