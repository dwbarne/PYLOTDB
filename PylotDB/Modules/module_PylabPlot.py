#! /usr/local/bin/python     # for *nix runs
# ===== Header =====
# Filename: module_codeinserts_Header.py
# Author: dwbarne
# Creation date: Thu, 10-10-2008

# Purpose:
"""
defs to generate plots in the post-process tab
"""

# imports
from Tkinter import *
import pylab
import time, sys
#import numpy

def PlotsForPylot(self,parent,xwin,ywin,shell,colorbg,demo):
    """
    main def called when button
    'Plot' is pressed
    """
    print '\n** In PlotsForPylot in module_PylabPlot'

    """
    try:
        if self.frameMainGnuPlot:
            print ' frame self.frameMainGnuPlot already exists.'
            print '   A new window will not be opened.'
            return
    except AttributeError:
        print '\n     frame self.frameMainGnuPlot will be created.'
    """
        
    self.shell=shell
    self.frameParentPlots = parent

# first, construct frame of frames
    self.frame_ToplevelPylabPlot = Toplevel(
        borderwidth=5,
        bg=colorbg,
        )
#    self.frame_ToplevelPylabPlot.grid()
    self.frame_ToplevelPylabPlot.transient(self.frameParentPlots)
    self.frame_ToplevelPylabPlot.title(
        'Plot'
        )

# place the sub_window
    self.frame_ToplevelPylabPlot.geometry(
        '+%d+%d' % (
            xwin, 
            ywin
            )
        )
# insert sub_frames into main frame    
    frame0 = Frame(
        self.frame_ToplevelPylabPlot,
        bg=colorbg,
        borderwidth=2,
#        relief=RIDGE,
        )
    frame0.grid(
        row=0,
        column=0,
        padx=5,
        pady=2,
        )
        
    frame1 = Frame(
        self.frame_ToplevelPylabPlot,
        bg=colorbg,
        borderwidth=2,
#        relief=RIDGE,
        )
    frame1.grid(
        row=1,
        column=0,
        padx=5,
        pady=2,
        sticky=W
        )
        
    frame2 = Frame(
        self.frame_ToplevelPylabPlot,
        bg=colorbg,
        borderwidth=2,
#        relief=RIDGE,
        )
    frame2.grid(
        row=2,
        column=0,
        padx=5,
        pady=2,
        sticky=W,
        )
        
    frame3 = Frame(
        self.frame_ToplevelPylabPlot,
        bg=colorbg,
        )
    frame3.grid(
        row=3,
        column=0,
        padx=5,
        pady=5,
        )

# -----------------------------------------------------------------------------------

# FRAME 0:        
# label
    labelMyCode = Label(
        frame0,
        text='PLOTS USING PYLAB',
        justify=CENTER,
        font=self.dataFontBold,
        bg=colorbg,
        )
    labelMyCode.grid(
        row=0,
        column=0,
        padx=5,
        pady=5,
        )
        
# FRAME 1:
# ... X label
    self.labelFileName = Label(
        frame1,
        text='X label:',
        justify=LEFT,
        bg='tan',
        )
    self.labelFileName.grid(
        row=1,
        column=0,
        padx=5,
        pady=5,
        sticky=W,
        )
    self.varLabelX = StringVar()
    self.varLabelX.set('X')
    self.entryLabelX = Entry(
        frame1,
        justify=LEFT,
        textvariable=self.varLabelX,
        width=10
        )
    self.entryLabelX.grid(
        row=1,
        column=1,
        padx=5,
        pady=5,
        )

# Y label        
    self.labelFileName = Label(
        frame1,
        text='Y label:',
        justify=LEFT,
        bg='tan',
        )
    self.labelFileName.grid(
        row=2,
        column=0,
        padx=5,
        pady=5,
        sticky=W,
        )
    self.varLabelY = StringVar()
    self.varLabelY.set('Y')
    self.entryLabelY = Entry(
        frame1,
        justify=LEFT,
        textvariable=self.varLabelY,
        width=10,
        )
    self.entryLabelY.grid(
        row=2,
        column=1,
        padx=5,
        pady=5,
        )
        
        
# ... Legend Caption
    self.labelLegendCaption = Label(
        frame1,
        text='Legend Caption:',
        justify=LEFT,
        bg='tan',
        )
    self.labelLegendCaption.grid(
        row=3,
        column=0,
        padx=5,
        pady=5,
        sticky=W,
        )
    self.varLegendCaption = StringVar()
    self.varLegendCaption.set('Curve')
    self.entryLegendCaption = Entry(
        frame1,
        justify=LEFT,
        textvariable=self.varLegendCaption,
        width=10
        )
    self.entryLegendCaption.grid(
        row=3,
        column=1,
        padx=5,
        pady=5,
        )
        
# ... X column
    self.labelColumnX = Label(
        frame1,
        text='X column',
        justify=LEFT,
        bg='tan',
        )
    self.labelColumnX.grid(
        row=4,
        column=0,
        padx=5,
        pady=5,
        sticky=W,
        )
    self.varColumnX = StringVar()
    self.varColumnX.set('1')
    self.entryColumnX = Entry(
        frame1,
        justify=LEFT,
        textvariable=self.varColumnX,
        width=10,
        )
    self.entryColumnX.grid(
        row=4,
        column=1,
        padx=5,
        pady=5,
        )
        
# ... Y columns
    self.labelColumnY = Label(
        frame1,
        text='Y columns\n(separated by commas)',
        justify=LEFT,
        bg='tan',
        )
    self.labelColumnY.grid(
        row=5,
        column=0,
        padx=5,
        pady=5,
        sticky=W,
        )
    self.varColumnY = StringVar()
    self.varColumnY.set('2')
    self.entryColumnY = Entry(
        frame1,
        justify=LEFT,
        textvariable=self.varColumnY,
        width=10,
        )
    self.entryColumnY.grid(
        row=5,
        column=1,
        padx=5,
        pady=5,
        )

# FRAME 3:
    if demo:
        buttonInsertHeader = Button(
            frame3,
            text='Plot',
            justify=CENTER,
            bg='darkblue',
            fg='white',
            borderwidth=5,
            relief=RAISED,
            command=DemoPlotsForPylot(self),
            )
    else:
        buttonInsertHeader = Button(
            frame3,
            text='Plot',
            justify=CENTER,
            bg='darkblue',
            fg='white',
            borderwidth=5,
            relief=RAISED,
            command=PlotsForPylot(self),
            )    
    buttonInsertHeader.grid(
        row=0,
        column=0,
        padx=5,
        pady=5,
        )
        
    buttonCloseInsertHeader = Button(
        frame3,
        text='Cancel',
        justify=CENTER,
        bg='darkblue',
        fg='white',
        borderwidth=5,
        relief=RAISED,
        command=(lambda:
            self.frame_ToplevelPylabPlot.destroy()
            ),
        )
    buttonCloseInsertHeader.grid(
        row=0,
        column=1,
        padx=5,
        pady=5,
        )
 

# ===== PlotsForPylot =====
# ===== DemoPlotsForPylot =====
def DemoPlotsForPylot(self,list_x, list_y):
    """
    calls pylab.plot to do the actual plotting; data
    is specified
    
    These are demo plots only.
    """

# create an array of floating point 

    def tempDef():
        start = 0.0
        stop  = 128.0
        step  = 1.0
        x = pylab.arange(start, stop, step, 'float')
# square it
        y = x*x
        lenx = len(x)
        print len(x),len(y)
        print x[lenx-1], y[lenx-1]

# create an empty "ndarray"
        xy = pylab.empty( (lenx,2)) #, typecode='f')
# fill the array with x and y
        xy[:,0] = x
        xy[:,1] = y

# clear the figure
        pylab.clf()
#create first of 2 sub plots
        pylab.subplot(211)
        pylab.xlabel('X')
        pylab.ylabel('X * X')
        pylab.plot(xy[:,0],xy[:,1])

# create second of 2 sub plots
        pylab.subplot(212)
        pylab.cla()
        pylab.xlabel('index')
        pylab.ylabel('X')
        pylab.plot(xy[:,0])
        
# create third sub plot
        """
        pylab.subplot(213)
        pylab.cla()
        pylab.xlabel('X')
        pylab.ylable('X * X')
        pylabl.plot(xy[:,0],xy[:,1])
        """
        

# force the display
        pylab.show()
    return tempDef
    
# ===== end of PlotsForPylot ===== 

# ===== DemoPlotsForPylot =====
def DemoPlotsForPylot(self):
    """
    calls pylab.plot to do the actual plotting
    
    These are demo plots
    """

# create an array of floating point 

    def tempDef():
        start = 0.0
        stop  = 128.0
        step  = 1.0
        x = pylab.arange(start, stop, step, 'float')
# square it
        y = x*x
        lenx = len(x)
        print len(x),len(y)
        print x[lenx-1], y[lenx-1]

# create an empty "ndarray"
        xy = pylab.empty( (lenx,2)) #, typecode='f')
# fill the array with x and y
        xy[:,0] = x
        xy[:,1] = y

# clear the figure
        pylab.clf()
#create first of 2 sub plots
        pylab.subplot(211)
        pylab.xlabel('X')
        pylab.ylabel('X * X')
        pylab.plot(xy[:,0],xy[:,1])

# create second of 2 sub plots
        pylab.subplot(212)
        pylab.cla()
        pylab.xlabel('index')
        pylab.ylabel('X')
        pylab.plot(xy[:,0])
        
# create third sub plot
        """
        pylab.subplot(213)
        pylab.cla()
        pylab.xlabel('X')
        pylab.ylable('X * X')
        pylabl.plot(xy[:,0],xy[:,1])
        """
        

# force the display
        pylab.show()
    return tempDef
    
# ===== end of DemoPlotsForPylot =====
    


