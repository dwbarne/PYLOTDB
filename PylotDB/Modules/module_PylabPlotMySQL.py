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
from Tkinter import *   # for widgets
import tkFont           # to specify various fonts
import pylab            # for plots
import time, sys        # for timestamps, sysem info


class PlotsForPylot(Frame):
    def __init__(
        self,
        parent,
        xwin,
        ywin,
        colorbg,
        label_X,
        label_Y,
        plot_X,
        plot_Y,
        showGrid,
        demo
        ):
        
        """
        main def called when button
        'Plot Y-X-Select Fields' is pressed
        
        Entry fields:
        x label:        self.varLabelX
        y label:        self.varLabelY
        plot title:     self.varPlotTitle
        
        Variables:
        x:  self.plot_X
        y:  self.plot_Y
        
        """
        print '\n** In class PlotsForPylot in module_PylabPlotMySQL'
        
        Frame.__init__(self)
        
# backgroung color
        self.colorbg=colorbg
# window location   
        self.xwin = xwin
        self.ywin = ywin
# parent frame
        self.frameParentPlots = parent
# labels
        self.label_X = label_X
        self.label_Y = label_Y
# reassign plot variables        
        self.plot_X = plot_X
        self.plot_Y = plot_Y

# tell pylab to plot grid       
        self.plotGrid = showGrid
       
# define data font BOLD
        self.dataFontBold = tkFont.Font(
            family='Arial',
            size="8",
            weight='bold'
            )
# define button font small
        self.buttonFontSmall = tkFont.Font(
            family='arial',
            size=7,
            )
# plotting options
# ... colors: b = blue, g = green, k = black
        plotOptions_Colors = ['b','g','k']
#  ... line style
        plotOptions_LineStyles = ['-','--',':']
# ... markers: s = square, o = filled circle, d = diamond
        plotOptions_Markers = ['s','o','d']
# form list of plot options
        self.plotOptions = []
        for style in plotOptions_LineStyles:
            for marker in plotOptions_Markers:
                for color in plotOptions_Colors:
                    self.plotOptions.append(color + style + marker)
        print 'self.plotOptions = \n',self.plotOptions

# plot
        if demo:
        self.demoPlotsForPylot()
        else:
            
        self.plot_OnePlotPerCurve()
        
        self.plot_SeveralCurvesOnOnePlot()
        

# ===== PlotsForPylot =====
    def plot_OnePlotPerCurve(self):
        '''
        Calls pylab.plot to do the actual plotting; data
        is specified.
        
        These are NOT demo plots.
        
        Max number of plots: 25
        
        Variables:
            self.plot_X[] (x list of length 1)
            self.plot_Y[] (y list of lists of variable length)
            
        Plot Options:
            self.plotOptions (list of third argument plot line
                                colors, line styles, line markers)
            plotOptions_SubPlot (number determining rows x columns x plot_number)
            
            
        Labels:
            x label:        self.varLabelX
            y label:        self.varLabelY[]
            plot title:     self.varPlotTitle
        '''
        print(
            '** In PlotsForPylotMySQL in module_PylabPlotMySQL'
            )

# create an array of floating point 
    
# destroy old popup
        try:
            self.frame_ToplevelPylabPlotMySQL.destroy()
        except:
            pass
    
# calculate min and max X values
# ... needed only for user-specified X limits; for now, let pylab set these automatically
        min_X = min(self.plot_X)
        max_X = max(self.plot_X)
        
# determine dimension of subplot, upto 25 plots max
        lenYList = len(self.plot_Y[0])
        if lenYList == 1: 
            plotOptions_SubPlot = 110
        elif lenYList <= 2: 
            plotOptions_SubPlot = 210
        elif lenYList <= 4:
            plotOptions_SubPlot = 220
        elif lenYList <= 6:
            plotOptions_SubPlot = 320
        elif lenYList <= 9:
            plotOptions_SubPlot = 330
        elif lenYList <= 12:
            plotOptions_SubPlot = 430
        elif lenYList <= 16:
            plotOptions_SubPlot = 440
        elif lenYList <= 20:
            plotOptions_SubPlot = 540
        elif lenYList <= 25:
            plotOptions_SubPlot = 550
        else:
            stringLenYList = (
                'Number of plots out of range:\n' +
                '   Number of plots attempted: ' + lenYList + '\n' +
                '   Number of plots allowed: 25\n\n' +
                'Please choose 25 or less plots and try again.\n'
                )
            print stringLenYList
            self.MySQL_Output(
                1,
                stringLenYList
                )
            showinfo(
                'Error: too many plots',
                '\n' + stringLenYList + '\n'
                )
            return  

# clear the figure
        pylab.clf()
# create plots
# ... subplot base number, which determines plot layout in plot window
        subplot = plotOptions_SubPlot
        for numberPlot in range(lenYList):
            subplot+=1
            pylab.subplot(subplot)
            pylab.grid(self.plotGrid)
# use following labels for multi-curves on single plot
#        pylab.xlabel(self.varLabelX.get())
#        pylab.ylabel(self.varLabelY.get())
# use following x and y label for multiplot labeling
            pylab.xlabel(self.label_X)
            pylab.ylabel(self.label_Y[numberPlot])
# ... use title for single plots only
#            pylab.title(self.varPlotTitle.get())
            pylab.title(self.label_Y[numberPlot])
            option = self.plotOptions[0]    # vary this for multi-curves on single plot
            print 'option:',option
            plot_y=[]
            for rowNum in range(len(self.plot_Y)):
                plot_y.append(self.plot_Y[rowNum][numberPlot])
            pylab.plot(
                self.plot_X,
                plot_y,
                option
                )
                
# example of bar plot                
#        pylab.plot(self.plot_Y,self.plot_X,'b-d')
#        pylab.subplot(212)
#        pylab.bar(self.plot_X,self.plot_Y,width=10,color='r')
        
# force the display
        pylab.show()
        
    def plot_SeveralCurvesOnOnePlot(self):
        '''
        Calls pylab.plot to do the actual plotting; data
        is specified.
        
        These are NOT demo plots.
        
        Max number of plots: 25 + 1 reference curve
        
        Variables:
            self.plot_X[] (x list of length 1)
            self.plot_Y[] (y list of lists of variable length)
            
        Plot Options:
            self.plotOptions (list of third argument plot line
                                colors, line styles, line markers)
            plotOptions_SubPlot (number determining rows x columns x plot_number)
            
            
        Labels and such from handlerPlotPreprocess:
           plot title:
                button status   self.varCheckbuttonShowTitle_AllCurvesOnePlot.get()
                value           self.varShowTitle_AllCurvesOnePlot.get()
            y label:
                button status   self.varCheckbuttonShowLabelY_AllCurvesOnePlot.get()
                value           self.varShowLabelY_AllCurvesOnePlot.get()
            x label:
                button status   self.varCheckbuttonShowLabelX_AllCurvesOnePlot.get()
                value           self.varShowLabelX_AllCurvesOnePlot.get()
            show grid:
                button status   self.varCheckbuttonShowGrid_AllCurvesOnePlot.get()
            reference curve: 
                button status   self.varCheckbuttonShowReferenceCurve_AllCurvesOnePlot.get()
                scale           self.comboboxShowReferenceCurveMultiplier_AllCurvesOnePlot.get()
                curve           self.comboboxShowReferenceCurveLabeled_AllCurvesOnePlot.get()
        '''
        print(
            '** In PlotsForPylotMySQL in module_PylabPlotMySQL'
            )

# get plot specs
        label_X = self.varShowLabelX_AllCurvesOnePlot.get()
        label_Y = self.varShowLabelY_AllCurvesOnePlot.get()
        label_Title = self.varShowTitle_AllCurvesOnePlot.get()
    
# destroy old popup
        try:
            self.frame_ToplevelPylabPlotMySQL.destroy()
        except:
            pass
    
# calculate min and max X values
        min_X = min(self.plot_X)
        max_X = max(self.plot_X)
        
        lenx = len(self.plot_X)

# determine dimension of subplot, upto 25 plots max on one plot
        lenYList = len(self.plot_Y)   
        print (
            'lenYList = %s, plotOptions_Subplot = %s' %
            (lenYList, plotOptions_Subplot)
            )   
# clear the figure
        pylab.clf()
# create plots
# ... only one plot
        pylab.subplot(111)
# ... apply grid 
        pylab.grid(self.plotGrid)
# ... x and y labels
        pylab.xlabel(label_X)
        pylab.ylabel(label_Y)
# ... plot title
        pylab.title(label_Title)
        for numberCurve in range(lenYList):
            pylab.plot(
                self.plot_X,
                self.plot_Y[numberCurve],
                self.plotOptions[numberCurve]
                )                
# reference plot, if desired
        self.plot_ReferenceY = [y*8 for y in self.plot_Y[0]]
        pylab.plot(
            self.plot_X,
            self.plot_ReferenceY,
            'r--d'
            )
#        pylab.plot(self.plot_Y,self.plot_X,'b-d')
#        pylab.subplot(212)
#        pylab.bar(self.plot_X,self.plot_Y,width=10,color='r')
        
# force the display
        pylab.show()
        
# ===== end of PlotsForPylot ===== 

# ===== DemoPlotsForPylot =====
    def demoPlotsForPylot(self):
        """
        calls pylab.plot to do the actual plotting
        
        These are demo plots only.
        """
        print(
            '** In DemoPlotsForPylot in module_PylabPlotMySQL'
            )

# create an array of floating point 
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
        '''
        pylab.subplot(213)
        pylab.cla()
        pylab.xlabel('X')
        pylab.ylable('X * X')
        pylabl.plot(xy[:,0],xy[:,1])
        '''
        

# force the display
        pylab.show()

# ===== end of DemoPlotsForPylot =====
        


