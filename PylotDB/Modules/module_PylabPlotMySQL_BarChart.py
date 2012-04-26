#! /usr/local/bin/python     # for *nix runs
# ===== Header =====
# Filename: module_codeinserts_Header.py
# Author: dwbarne
# Creation date: Thu, 10-10-2008

# Purpose:
"""
defs to generate bar charts
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
        plot_X_BarChart,
        plot_Y_BarChart,
        headerNameX,
        tableName,
        **plotParams
        ):
        
        """
        main def called when button
        'Bar Chart' is pressed
        
        Variables:
        x:  self.plot_X_BarChart
        y:  self.plot_y_BarChart
        
        """
        selfExt.MySQL_Output(
            1,
            '** In class PlotsForPylot in module_PylabPlotMySQL_BarChart'
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
        self.plot_X_BarChart = plot_X_BarChart
        self.plot_Y_BarChart = plot_Y_BarChart
#        print '\nIn module:\nplot_X_BarChart:\n %s \nplot_Y_BarChart:\n %s' % (plot_X_BarChart, plot_Y_BarChart)
# reassign header name and table name
        self.headerNameX = headerNameX
        self.tableName = tableName
       
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
            
# DWB: Delete this
        print (
            '\n In module_PylabPlotMySQL_BarChart.py,\n' + 
            '  before call to self.plot_BarChart:'
            )
        print ' plotParams.keys() = \n',plotParams.keys()
        print
        icount=0
        for key in plotParams.keys():
            value = plotParams[key]
            icount+=1
            print '%s. key, value = %s, %s' % (icount,key,value)
# --- end of delete ---

# method for plots    
        self.plot_BarChart(selfExt,**plotParams)
        

# ===== PlotsForPylot =====
    def plot_BarChart(self,
        selfExt,
# **plotParams 
        showTitle,
        showYLabel,
        showGrid,
        useLogScale,
        orientBarsHorizontal,
        titleBarChart,
        labelYBarChart,
        fontsizeChartTitle,
        fontsizeChartLabels,
        fontsizeGeneral,
        fontsizeXTickLabels,
        fontsizeYTickLabels,
        fontsizeLegend,
        colorChartTitle,
        colorChartBackground,
        colorChartBorder,
        colorChartLabels,
        colorXTickLabels,
        colorYTickLabels,
        widthChartFigure,
        heightChartFigure,
        widthBars,
        widthBarsEdge,
        colorBars,
        colorBarsEdge,
        alignBars,
        axesLeft,
        axesBottom,
        axesWidth,
        axesHeight
        ):
        '''
        Calls pylab.plot to do the actual plotting; data
        is specified.
        
        Variables:
            self.plot_X_BarChart[] (x list of length 1)
            self.plot_Y_BarChart[] (y list of lists of variable length)
        '''
        selfExt.MySQL_Output(
            1,
            '** In PlotsForPylotMySQL in module_PylabPlotMySQL'
            )
            
# DWB Delete this
        print 
        print '1. showTitle =',showTitle
        print '2. showYLabel =',showYLabel
        print '3. showGrid =',showGrid
        print '4. useLogScale =',useLogScale
        print '5. orientBarsHorizontal =',orientBarsHorizontal
        print '6. titleBarChart =',titleBarChart
        print '7. labelYBarChart =',labelYBarChart
        print '8. fontsizeChartTitle =',fontsizeChartTitle
        print '9. fontsizeChartLabels =',fontsizeChartLabels
        print '10. fontsizeGeneral =',fontsizeGeneral
        print '11. fontsizeXTickLabels =',fontsizeXTickLabels
        print '12. fontsizeYTickLabels =',fontsizeYTickLabels
        print '13. fontsizeLegend =',fontsizeLegend
        print '14. colorChartTitle =',colorChartTitle
        print '15. colorChartBackground =',colorChartBackground
        print '16. colorChartBorder =',colorChartBorder
        print '17. colorChartLabels =',colorChartLabels
        print '18. colorXTickLabels =',colorXTickLabels
        print '19. colorYTickLabels =',colorYTickLabels
        print '20. widthChartFigure =',widthChartFigure
        print '21. heightChartFigure =',heightChartFigure
        print '22. widthBars =',widthBars
        print '23. widthBarsEdge =',widthBarsEdge
        print '24. colorBars =',colorBars
        print '25. colorBarsEdge =',colorBarsEdge
        print '26. alignBars =',alignBars
        print '27. axesLeft =',axesLeft
        print '28. axesBottom =',axesBottom
        print '29. axesWidth =',axesWidth
        print '30. axesHeight =',axesHeight
# --- end of delete ---
    
# calculate min and max X values
        min_X = min(self.plot_X_BarChart)
        max_X = max(self.plot_X_BarChart)
        max_Y = max(self.plot_Y_BarChart)
        
        print (
            '\nself.plot_X_BarChart = \n%s\n\nself.plot_Y_BarChart = \n%s\n\n'
            % (self.plot_X_BarChart,self.plot_Y_BarChart)
            )
        
        lenYList = len(self.plot_Y_BarChart)
        lenXList = len(self.plot_X_BarChart)
        
# x index
        index_X = numpy.arange(len(self.plot_X_BarChart))
        print '\nindex_X from numpy.arange:\n',index_X
        print 
        print 'colorChartBorder, type() = ',colorChartBorder,type(colorChartBorder)

# set defaults, before changes are made 
        pylab.rcdefaults()

# tell pylab which figure we are dealing with; otherwise, defaults to Figure 1, which conflicts with regular x-y plots  
        pylab.figure(
            1000, 
            facecolor=colorChartBorder,     # does NOT work (must be a bug in matplotlib)
#            facecolor='white',
            figsize=(
                float(widthChartFigure), 
                float(heightChartFigure)
                ),
            )         
# clear the figure
        pylab.clf()
        
        
# rcParams 

        params = {
                      'font.size' : fontsizeGeneral,
                 'axes.facecolor' : colorChartBackground,
 #             'figure.figsize' : [float(widthChartFigure), float(heightChartFigure)],
                 'axes.titlesize' : fontsizeChartTitle,
                 'axes.labelsize' : fontsizeChartLabels,
                'axes.labelcolor' : colorChartLabels,
                'xtick.labelsize' : fontsizeXTickLabels,
                    'xtick.color' : colorXTickLabels,
                'ytick.labelsize' : fontsizeYTickLabels,
                    'ytick.color' : colorYTickLabels,
            }

# update the params
        pylab.rcParams.update(params)

# form bars        
        pylab.bar(
            index_X,
            self.plot_Y_BarChart,
            width=float(widthBars),
            color=colorBars,
            edgecolor=colorBarsEdge,
            linewidth=float(widthBarsEdge),
#            xerr=None,
#            yerr=None,
#            ecolor=None,
#            capsize=3,
#            align=alignBars,
#            orientation=orient,
#            log=useLogScale
            )
        
# ... show grid 
        pylab.grid(showGrid)
            
# ... convert x titles to numbers
        '''
        xrange=[]
        for i in range(len(self.plot_X_BarChart)):
            xrange.append(i)
        print '\nxrange =\n',xrange
        '''
          
# ... horizontal or vertical bars
        if orientBarsHorizontal:
            orient = 'horizontal'
        else:
            orient = 'vertical'
        orient = 'vertical'
# ... logscale
        if useLogScale:
            logScale = True
        else:
            logScale = False
        logScale = False
            
# in case labels are long, put a <CR> in every other label
# ... make strings out of every label
        plot_X_BarChart_Labels=[]
        if orient <> 'horizontal':  # orient == 'vertical'
            for i in range(len(self.plot_X_BarChart)):
                if i%2 == 1:
# odd
                    plot_X_BarChart_Labels.append('\n\n' + str(self.plot_X_BarChart[i]))
                else:
# even
                    plot_X_BarChart_Labels.append(str(self.plot_X_BarChart[i]))
# labels and numbers for tick marks                   
            pylab.xticks(index_X + float(widthBars)/2., plot_X_BarChart_Labels)
            values_Y = numpy.arange(0,math.ceil(1.05*max_Y)+1)
            pylab.yticks(values_Y)
            
        else: # orient == 'horizontal':
            for i in range(len(self.plot_X_BarChart)):
                if i%2 == 1:
# odd
                    plot_X_BarChart_Labels.append('  ' + str(self.plot_X_BarChart[i]))
                else:
# even
                    plot_X_BarChart_Labels.append(str(self.plot_X_BarChart[i]))
# title
        if showTitle:
            pylab.title(
                titleBarChart,
                color=colorChartTitle,
                size=fontsizeChartTitle
                )
# y label
        if showYLabel:
            pylab.ylabel(labelYBarChart)      
# force the display
#        pylab.show()
#        '''
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
#        '''
        
def pylabCloseBarAndPieCharts():
    '''
    Purpose:
        closes bar and pie charts plot windows; called externally
            
    Called by:
        
        
    Calls:
        
        
    '''
    pylab.close(1000)
    pylab.close(2000)
# ===== end of PlotsForPylot ===== 

        


