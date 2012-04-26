#! /usr/local/bin/python     # for *nix runs
# ===== Header =====
# Filename: module_codeinserts_Header.py
# Author: dwbarne
# Creation date: Thu, 10-10-2008

# Purpose:
"""
defs to generate pie charts
"""

# imports
from Tkinter import *   # for widgets
import tkFont           # to specify various fonts
import pylab            # for plots
import time, sys        # for timestamps, sysem info
from tkMessageBox import *    # dialogs such as askokcancel, showinfo, showerror, etc.
import numpy            # needed for numpy.arrange()
import math             # needed for math.ceil()


class PlotsForPylotDB(Frame):
    def __init__(
        self,
        selfExt,
        parent,
        xwin,
        ywin,
        colorbg,
        plot_X_PieChart,
        plot_Y_PieChart,
        headerNameX,
        tableName,
        totalCount,
        **plotParams
        ):
        
        '''
        main def called when button
        'Pie Chart' is pressed
        
        Variables:
        x:  self.plot_X_PieChart
        y:  self.plot_y_PieChart       
        '''
        
        selfExt.MySQL_Output(
            1,
            '** In class PlotsForPylot in module_PylabPlotMySQL_PieChart'
            )
        
        Frame.__init__(self)
        
# parent frame
        self.frameParentPlots = parent
# window location   
        self.xwin = xwin
        self.ywin = ywin
# backgroung color
        self.colorbg=colorbg
# reassign plot variables        
        self.plot_X_PieChart = plot_X_PieChart
        self.plot_Y_PieChart = plot_Y_PieChart
#        print '\nIn module:\nplot_X_PieChart:\n %s \nplot_Y_PieChart:\n %s' % (plot_X_PieChart, plot_Y_PieChart)
# reassign header name and table name
        self.headerNameX = headerNameX
        self.tableName = tableName
# total count       
        self.totalCount = float(totalCount)
       
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
# ... colors: b = blue, g = green, k = black, etc; will cycle thru color list
        self.plotOptions_Colors = ['b','g','r','c','m','y']
# want 25 in all; if more than 25, just plot 25, no more
        self.plotOptions_Colors = 4*self.plotOptions_Colors + ['b']
# plot    
        self.plot_PieChart(selfExt,**plotParams)
        

# ===== PlotsForPylot =====
    def plot_PieChart(self,
        selfExt,
# **plotParams
        showTitle,
        titlePieChart,
        colorTitle,
        fontsizeTitle,
#        showLegend,
#        fontsizeLegend,
        showExplodedView,
        factorExplodeWedges,
#        colorChartBackground,
        fontsizeLabels,
        colorLabels
        ):
        '''
        Calls pylab.plot to do the actual plotting; data
        is specified.
        
        Variables:
            self.plot_X_PieChart[] (x list of length 1)
            self.plot_Y_PieChart[] (y list of lists of variable length)
        '''
        selfExt.MySQL_Output(
            1,
            '** In PlotsForPylotMySQL in module_PylabPlotMySQL'
            )
    
# calculate min and max X values
        min_X = min(self.plot_X_PieChart)
        max_X = max(self.plot_X_PieChart)
        max_Y = max(self.plot_Y_PieChart)
        
        print (
            '\nself.plot_X_PieChart = \n%s\n\nself.plot_Y_PieChart = \n%s\n\n'
            % (self.plot_X_PieChart,self.plot_Y_PieChart)
            )
        
        lenYList = len(self.plot_Y_PieChart)
        
# clear the figure
#        pylab.clf()

# set defaults, before changes are made 
        pylab.rcdefaults()
        
# figure size
        widthChartFigure = 6.0
        heightChartFigure = 6.0
#        pylab.figure(2, figsize=(figWidth, figHeight))
        pylab.figure(
            2000, 
#            facecolor='blue',
            facecolor='white',
            figsize=(
                float(widthChartFigure),
                float(heightChartFigure),
                ), 
            )
            
        pylab.clf()
        
        print(
            '\nlen(self.plot_Y_PieChart) =\n%d' % len(self.plot_Y_PieChart)
            )
        print(
            '\nfactorExplodeWedges, type() =\n%s, %s' % 
            (factorExplodeWedges, type(factorExplodeWedges))
            )
            
# labels
        labels = []
        icount=0
 #       labels = tuple(self.plot_X_PieChart)
        for label in self.plot_X_PieChart:
            labels.append(
                str(label) + '\n' + 
                '(' + str(self.plot_Y_PieChart[icount]) + ')' 
                )
            icount += 1
        print '\nlabels = \n',labels
        
# rcParams
#        pylab.rcParams['axes.titlesize'] = fontsizeTitle
#        pylab.rcParams['axes.labelsize'] = fontsizeLabels
#        pylab.rcParams['axes.labelcolor'] = colorLabels
        fig_size = [widthChartFigure,heightChartFigure]
        params = {
            'axes.titlesize' : fontsizeTitle,  # for title
#           'axes.labelsize' : fontsizeLabels,
#            'axes.labelcolor' : colorLabels,
#            'axes.facecolor' : colorChartBackground,
            'figure.figsize' : fig_size,
            'font.size' : int(fontsizeLabels), # for labels
            'text.color' : colorLabels,
#            'axes_left' : 0.1,
#            'axes_bottom' : 0.1,
#            'axes_height' : 0.9,
#            'axes_width' : 0.9
            }
        pylab.rcParams.update(params)
#        pylab.rcParams['legend.fontsize'] = 12.0

# title 
        if showTitle:
            pylab.title(
                titlePieChart,
                color=colorTitle,
                size=fontsizeTitle
                )
        
# exploded view
        if showExplodedView:
            explode = tuple((len(self.plot_Y_PieChart))*[float(factorExplodeWedges)]) 
        else:
            explode = None
        
# compute percentages
        print '\nself.totalCount, type() = ',self.totalCount,type(self.totalCount)
        print 'self.plot_Y_PieChart, type[0] =',self.plot_Y_PieChart, type(self.plot_Y_PieChart[0])
#        print '\nexplode = ',explode

        fractions = [float(yval)/float(self.totalCount)*100. for yval in self.plot_Y_PieChart]
#        print '\nfractions:\n',fractions
#        print '\nlabels:\n',labels
#        print '\nexplode:\n',explode
#        print '\ncolors:\n',self.plotOptions_Colors

# ... plot pie chart
        pylab.pie(
            fractions,
            explode=explode,
            colors=self.plotOptions_Colors,
            labels=labels,
            autopct='%1.1f%%',
            shadow=True
            )
        
# force the display
#        pylab.show()
        try:
            pylab.show()
        except (ValueError):
#        except:
            errorParams = (
                'One of the input parameters for matplotlib\n' +
                '  is invalid. Check params.\n\n' + 
                'One possibility is that the user has specified\n' +
                '  a color that matplotlib does not recognize.\n\n' + 
                'Check all paramaters for validity and try again.\n\n'
                )
            showinfo(
                'Error: params',
                errorParams
                )
            return        
        
def pylabCloseAll():
    '''
    Purpose:
        close all plot windows; called externally
            
    Called by:
        
        
    Calls:
        
        
    '''
    pylab.close(1000)
    pylab.close(2000)
# ===== end of PlotsForPylot ===== 

        


