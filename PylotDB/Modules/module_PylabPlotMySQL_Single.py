#! /usr/local/bin/python     # for *nix runs
# ===== Header =====
# Filename: module_codeinserts_Header.py
# Author: dwbarne
# Creation date: Thu, 10-10-2008

# Purpose:
"""
defs to generate plots; single curve per plot
"""

# for debugging; if True, prints many module variables
DEBUG = 0

# imports
from Tkinter import *       # for widgets
import tkFont               # to specify various fonts
import pylab                # for plots
import time, sys            # for timestamps, sysem info
from tkMessageBox import *  # dialogs such as showinfo
import math                 # for natural logarithms (base e)

# import modules
import module_PlotUtilities

# GLOBALS
numberCurvesMax = 25


class PlotsForPylotDB(Frame):
    def __init__(self,
        parent,
        keepPreviousPlot,
        xwin,
        ywin,
        label_X,
        label_Y,
        plot_X,
        plot_Y,
        numberOfTableCurves,
        numberOfBufferCurves,
        numberPylabPlotFigure,
        **plotParams
        ):
        
        '''
        main def called when button
        'Plot Y-X-Select Fields' is pressed
        
        Entry fields:
        x label:        self.varLabelX
        y label:        self.varLabelY
        plot title:     self.varPlotTitle
        
        Variables:
        x:  self.plot_X
        y:  self.plot_Y
        
        '''
        if DEBUG:
            print ('\n** In class PlotsForPylot in module_PylabPlotMySQL_Single')
        
        Frame.__init__(self)
        
# backgroung color
#        self.colorbg=colorbg
# figure number, if needed
        self.numberPylabPlotFigure = numberPylabPlotFigure
# erase previous plot
        self.keepPreviousPlot = keepPreviousPlot
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
        
# change self.plot_Y to log base e
        '''
        print('\n&&& Before changing to log: self.plot_Y = ')
        print(self.plot_Y)
        print('')
        
        for i in range(len(self.plot_Y)):
            for inum,element in enumerate(self.plot_Y[i]):
                self.plot_Y[i][inum] = math.log(self.plot_Y[i][inum])
        
        print('\n&&& After changing to log: self.plot_Y = ')
        print(self.plot_Y)
        print('')
        '''
                
# number of table and buffer curves
        self.numberOfTableCurves = numberOfTableCurves
        self.numberOfBufferCurves = numberOfBufferCurves

# tell pylab to plot grid       
#        self.plotGrids = showGrids
        
# tell pylab to show titles
#        self.showPlotTitles = showPlotTitles
       
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
        if DEBUG:
            print 'self.plotOptions = \n',self.plotOptions

# plot     
        self.plot_OnePlotPerCurve(**plotParams)
        

# ===== PlotsForPylot =====
    def plot_OnePlotPerCurve(self,
        showMainTitle,
        showPlotTitles,
        showGrids,
        mainTitle,
        colorMainTitle,
        fontsizeMainTitle,
        fontsizePlotTitles,
        fontsizeXYLabels,
        colorXYLabels,
        fontsizeXTicks,
        colorXTicks,
        fontsizeYTicks,
        colorYTicks,
        colorChartBackground,
        colorPlotBorder,
        plotStyle,
        plotBaseX,
        plotBaseY,
        lineWidth,
        markerSize,
        ):
        '''
        Calls pylab.plot to do the actual plotting; data
        is specified.
        
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

        if DEBUG:
            print('\n-- DEBUG --')
            print('showMainTitle: %s (%s)' % (showMainTitle, type(showMainTitle)))
            print('showPlotTitles: %s (%s)' % (showPlotTitles,type(showPlotTitles)))
            print('showGrids: %s (%s)' % (showGrids,type(showGrids)))
            print('mainTitle: %s (%s)' % (mainTitle,type(mainTitle)))
            print('fontsizeMainTitle: %s (%s)' % (fontsizeMainTitle,type(fontsizeMainTitle)))
            print('fontsizePlotTitles: %s (%s)' % (fontsizePlotTitles,type(fontsizePlotTitles)))
            print('fontsizeXYLabels: %s (%s)' % (fontsizeXYLabels,type(fontsizeXYLabels)))
            print('colorXYLabels: %s (%s)' % (colorXYLabels,type(colorXYLabels)))
            print('fontsizeXTicks: %s (%s)' % (fontsizeXTicks,type(fontsizeXTicks)))
            print('colorXTicks: %s (%s)' % (colorXTicks,type(colorXTicks)))
            print('fontsizeYTicks: %s (%s)' % (fontsizeYTicks,type(fontsizeYTicks)))
            print('colorYTicks: %s (%s)' % (colorYTicks,type(colorYTicks)))
            print('colorChartBackground: %s (%s)' % (colorChartBackground,type(colorChartBackground)))
            print('plotStyle: %s (%s)' % (plotStyle,type(plotStyle)))
            print('plotBaseX: %s (%s)' % (plotBaseX,type(plotBaseX)))
            print('plotBaseY: %s (%s)' % (plotBaseY,type(plotBaseY)))
            print('lineWidth: %s (%s)' % (lineWidth,type(lineWidth)))
            print('markerSize: %s (%s)' % (markerSize,type(markerSize)))
            print('-- END OF DEBUG --\n')
    
# destroy old popup
#        try:
#            self.frame_ToplevelPylabPlotMySQL.destroy()
#        except:
#            pass        
        
# determine dimension of subplot, upto 'numberCurvesMax' plots max
        lenYList = len(self.plot_Y)  # tells how many curves, and therefore how many plots, are to be drawn
# bounds check; no more than 'numberCurvesMax' plots in a 5x5 array allowed; 
        if lenYList > numberCurvesMax:
            stringLenYList = (
                'Number of plots out of range:\n\n' +
                '   Number of plots attempted: ' + str(lenYList) + '\n' +
                '   Max number of plots allowed: ' + str(numberCurvesMax) + '\n\n' +
                'To continue with plotting the first ' + str(numberCurvesMax) + '\n' +
                ' of ' + str(lenYList) + ' plots selected, click "OK".' + '\n\n' +
                'To halt plotting, click "CANCEL".' + '\n'
                )
            ans = askokcancel(
                'Max number of plots exceeded',
                stringLenYList
                )
            if not ans:
                return 
            else:
                lenYList = numberCurvesMax
         
        plotOptions_SubPlot = []
        if lenYList == 1: 
            plotOptions_SubPlot = [1,1,0]
        elif lenYList <= 2: 
            plotOptions_SubPlot = [2,1,0]
        elif lenYList <= 4:
            plotOptions_SubPlot = [2,2,0]
        elif lenYList <= 6:
            plotOptions_SubPlot = [3,2,0]
        elif lenYList <= 9:
            plotOptions_SubPlot = [3,3,0]
        elif lenYList <= 12:
            plotOptions_SubPlot = [4,3,0]
        elif lenYList <= 16:
            plotOptions_SubPlot = [4,4,0]
        elif lenYList <= 20:
            plotOptions_SubPlot = [5,4,0]
        elif lenYList <= 25:
            plotOptions_SubPlot = [5,5,0]
        else:
            stringLenYList = (
                'Number of plots out of range:\n' +
                '   Number of plots attempted: ' + str(lenYList) + '\n' +
                '   Max number of plots allowed: ' + str(lenYList_Max) + '\n\n' +
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
        
# reset defaults
        pylab.rcdefaults()

# tell pylab which figue we are dealing with; otherwise, defaults to Figure 1
        pylab.figure(
            self.numberPylabPlotFigure,
            facecolor=colorPlotBorder
            )
            
# color plot border
#        pylab.figure().patch.set_facecolor(colorPlotBorder)
        
# clear the figure
        if not self.keepPreviousPlot:         
            pylab.clf()

# set some plot params
        params = {
#                   'font.size' : int(fontsizePlotTitles), #fontsizeGeneral for title
              'axes.facecolor' : colorChartBackground,   #chart background color
              'axes.labelsize' : int(fontsizeXYLabels),   #fontsizeChartLabels,
             'axes.labelcolor' : colorXYLabels,  #chart x-y label colors
             'xtick.labelsize' : int(fontsizeXTicks),   #fontsizeXTickLabels,
                 'xtick.color' : colorXTicks,    #colorXTickLabels, 
             'ytick.labelsize' : int(fontsizeYTicks),  #fontsizeYTickLabels,
                 'ytick.color' : colorYTicks,  #colorYTickLabels,  
#             'lines.linewidth' : lineWidth, # width of data plot lines (0=thin, 5=thick)                 
            }
# update the params
        pylab.rcParams.update(params)
        
# create plots
# ... subplot base number, which determines plot layout in plot window
        numRowsTotal = plotOptions_SubPlot[0]
        numColumnsTotal = plotOptions_SubPlot[1]
        subplot = 0

# iterate over plots
        for numberPlot in range(lenYList):
        
# keep track of subplot number
            subplot+=1
            
# define subplot FIRST before defining other parameters
            self.pylabSubplot = pylab.subplot(numRowsTotal,numColumnsTotal,subplot)

# set plot sizes within frame; also set distance from each other vertically and horizontally
            pylab.subplots_adjust(
                left=0.125,
                right=0.9,
                bottom=0.1,
                top=0.9,
                wspace=0.30,
                hspace=0.5,
                )
            
            pylab.grid(showGrids)
            
# use following x and y label for multiplot labeling
# ... x label
            try:
                pylab.xlabel(self.label_X[numberPlot])
            except:
                stringErrorXLabel = (
                    'The value\n\n' +
                    '   self.label_X[numberPlot]\n\n' +
                    'is out of range in module_PylabPlotMySQL_Single.\n\n' + 
                    'This is a coding error. Please contact the\n' +
                    'code administrator.'
                    )
                print stringErrorXLabel
                showinfo(
                    'Error: out of range',
                    stringErrorXLabel
                    )
                return
# ... y label
            try:
                pylab.ylabel(self.label_Y[numberPlot])   
            except:
                stringErrorYLabel = (
                    'The value\n\n' +
                    '   self.label_Y[numberPlot]\n\n' +
                    'is out of range in module_PylabPlotMySQL_Single.\n\n' +
                    'This is a coding error. Please contact the\n' +
                    'code administrator.'
                    )
                print stringErrorYLabel
                showinfo(
                    'Error: out of range',
                    stringErrorYLabel
                    )
                return  
                
# ... use title for single plots only
#            pylab.title(self.varPlotTitle.get())
            if showPlotTitles:
                colorTitle = 'black'
                pylab.title(
                    self.label_Y[numberPlot],
                    color=colorTitle,
                    size=fontsizePlotTitles
                    )

            if DEBUG:
                print('self.plotOptions[0]: %s',self.plotOptions[0])
            
 #           self.plotStyleForCurve(
            module_PlotUtilities.plotStyleForCurve(
                self,
                pylab,
                plotStyle,
                self.plot_X[numberPlot],
                self.plot_Y[numberPlot],
                self.plotOptions[0],
                lineWidth,
                markerSize,
                plotBaseX,
                plotBaseY,
                )
                
# zero out global values for xMin, yMin, xMax, yMax for each plot
            self.xMin_Global = []
            self.xMax_Global = []
            self.yMin_Global = []
            self.yMax_Global = []
            
# determine min and max values for each plot
#            self.globalMinMaxValues(
            module_PlotUtilities.globalMinMaxValues(
                self,
                self.plot_X[numberPlot],
                self.plot_Y[numberPlot]
                )
                
# change labels to 'e' if needed
            if plotStyle == 'semilogx' or plotStyle == 'loglog':
                if plotBaseX == 'e':
                    xMin_Local = min(self.xMin_Global)
                    xMax_Local = max(self.xMax_Global)
#                    self.formNewXLabels(xMin_Local,xMax_Local,colorXTicks,fontsizeXTicks)
                    okXLabels = module_PlotUtilities.formNewXLabels(
                        self,pylab,xMin_Local,xMax_Local,colorXTicks,fontsizeXTicks
                        )
                    if not okXLabels:
                        return
            
            if plotStyle == 'semilogy' or plotStyle == 'loglog':
                if plotBaseY == 'e':
                    yMin_Local = min(self.yMin_Global)
                    yMax_Local = max(self.yMax_Global)
#                    self.formNewYLabels(yMin_Local,yMax_Local,colorYTicks,fontsizeYTicks) 
                    okYLabels = module_PlotUtilities.formNewYLabels(
                        self,pylab,yMin_Local,yMax_Local,colorYTicks,fontsizeYTicks
                        ) 
                    if not okYLabels:
                        return
        
# --- end of for loop ---

# show overall plot title
        if showMainTitle:
            pylab.suptitle(
                mainTitle,
                color=colorMainTitle,
                fontsize=fontsizeMainTitle
                )
                
# graph the plot
        pylab.show()
        
        return
        

# ===== end of PlotsForPylot ===== 

        
def pylabCloseAll(self):
    '''
    Purpose:
        close all plot windows; called externally
            
    Called by:
        
        
    Calls:
        
        
    '''
    pylab.close('all')
        

        
