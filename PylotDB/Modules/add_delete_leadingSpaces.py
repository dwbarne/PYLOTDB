#! /usr/local/bin/python     # for *nix runs
# ===== Header =====
# Filename: leadingSpaces.py
# Author: dwbarne
# Creation date: Thu, 10-30-2008

# Purpose:
"""
program to add or subtract leading spaces from
all or portions of a file

"""


# >> INSERT: Global Imports <<
# ===== Global Imports =====
from Tkinter import *                    # Tkinter widgets
import tkFont                    # fonts
import string                    # process standard Python strings
import sys                  # to append module search path
sys.path.append('.\\Modules')
import module_leadingSpaces

# ===== Geometry =====
# Define global geometry values
# ... Text frame width and height
w_frameText = 80
h_frameText = 35
# ... Main-window placement relative to top left of screen
x_Windows = 75
y_Windows = 125
# ... Sub-window placement relative to top left of screen
x_subWindows = 10
y_subWindows = 20
# ... button width and height
buttonWidth = 10
buttonHeight = 1
# ... width and height of Pmw scrolled frame
globalHullWidth = 1100
globalHullWidth = 775


# ===== main class ===== # 
class LeadingSpaces(Frame):
    def __init__(self, parent):
        global x_Windows, y_Windows
        print '\n\n ***** Welcome to leadingSpaces **********'

        Frame.__init__(self)

        self.frameParent = parent

        self.frameParent.geometry(
            '+%d+%d' % (x_Windows, y_Windows) 
            )

# ============ Font Parameters =====================
        print '\nFonts used:'
# define font parameters
# ... data
        dataFontFamily = 'arial'
        dataFontSize = '8'
        dataFontWeight = 'bold'
# ... button
        buttonFontFamily = 'helvetica'
        buttonFontSize = '6'
# ... entry
        entryFontFamily = 'arial'
        entryFontSize = '10'
# ... small quit button
        quitFontFamily = 'helvetica'
        quitFontSize = '6'
# ... title family
        titleFontFamily = 'arial'
        titleFontSize = '8'
        titleFontWeight = 'bold'
        
#=========== end of Font Parameters ================

#=========== Data Fonts ===========================
        
# define data font
        self.dataFont = tkFont.Font(
            family=dataFontFamily,
            size=dataFontSize,
            )
        print '\n     self.dataFont: family=' + dataFontFamily + \
            ', size=' + dataFontSize
            
# define data font bold       
        self.dataFontBold = tkFont.Font(
            family=dataFontFamily,
            size=dataFontSize,
            weight=dataFontWeight,
            )
        print '     self.dataFontBold: family=' + dataFontFamily + \
            ', size=' + dataFontSize + ',  weight = ' + dataFontWeight
            
# define button font
        self.buttonFont = tkFont.Font(
            family=buttonFontFamily,
            size=buttonFontSize,
            )
        print '     self.buttonFont: family=' + buttonFontFamily + \
            ', size=' + buttonFontSize
            
# define entry font
        self.entryFont = tkFont.Font(
            family=entryFontFamily,
            size=entryFontSize,
            )
        print '     self.entryFont: family=' + entryFontFamily + \
            ', size=' + entryFontSize
            
# define 'quit' button font
        self.buttonQuitFont = tkFont.Font( 
            family=quitFontFamily,
            size=quitFontSize,
            )
        print '     self.buttonQuitFont: family=' + quitFontFamily + \
        ', size=' + quitFontSize
        

# define 'title' font
        self.titleFont = tkFont.Font(
            family=titleFontFamily,
            size=titleFontSize,
            weight=titleFontWeight
            )
        print (
            '     self.titleFont: family=' + titleFontFamily + \
            ', size=' + titleFontSize + 
            ', weight=' + titleFontWeight
            )
           
# ================ end of Data Fonts ========================


        self.spacesAddDelete()

    def spacesAddDelete(self):

        module_leadingSpaces.leadingSpaces(
            self,
            self.frameParent)


# ===== Handlers go below ===== #


# >> INSERT: If Name=Main <<

# ===== main ===== # 
if __name__ == '__main__':
    root = Tk()
    app = LeadingSpaces(root)
    app.master.title(
       'Main window'
        )
    app.master.configure(
        bg='lightgreen',
        )
    app.mainloop()







