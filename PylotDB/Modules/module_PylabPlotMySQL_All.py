#! /usr/local/bin/python     # for *nix runs
# ===== Header =====
# Filename: module_codeinserts_Header.py
# Author: dwbarne
# Creation date: Thu, 10-10-2008

# Purpose:
"""
defs to generate plots; all curves on one plot
"""

# for debugging; if True, prints many module variables
DEBUG = 0

# imports
from Tkinter import *           # for widgets
import tkFont                   # to specify various fonts
import pylab                    # for plots
import time, sys                # for timestamps, sysem info
from tkMessageBox import *      # dialogs such as askokcancel, showinfo, showerror, etc.
import math                     # to handle math.e and math.log and math.log10 bases for plots

# import modules
import module_PlotUtilities

# Globals
numberCurvesMax = 25

class PlotsForPylotDB(Frame):
    def __init__(
        self,
        selfExt,
        parent,
        keepPreviousPlot,
        xwin,
        ywin,
        colorbg,
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
        y:  self.plotY
        
        '''
        selfExt.MySQL_Output(
            1,
            '\n** In class PlotsForPylotDB in module_PylabPlotMySQL_All'
            )
        
        Frame.__init__(self)
        
# parent frame
        self.frameParentPlots = parent
# erase previous plot
        self.keepPreviousPlot = keepPreviousPlot
# window location   
        self.xwin = xwin
        self.ywin = ywin
# backgroung color
        self.colorbg=colorbg
# figure number, if needed
        self.numberPylabPlotFigure = numberPylabPlotFigure
# reassign plot variables        
        self.plot_X = plot_X
        self.plot_Y = plot_Y
        if DEBUG:
            print '===== in module_PylabPlotMySQL_All ====='
            print '\nplot_X = ',plot_X
            print '\nplot_Y = ',plot_Y

# number of table and buffer curves
        self.numberOfTableCurves = numberOfTableCurves
        self.numberOfBufferCurves = numberOfBufferCurves
#        print '\nIn module:\nplot_X:\n %s \nplot_Y:\n %s' % (plot_X, plot_Y)
       
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
        self.plot_SeveralCurvesOnOnePlot(selfExt,**plotParams)
        

# ===== PlotsForPylotDB =====
    def plot_SeveralCurvesOnOnePlot(self,
        selfExt,
        showTitle,
        showYLabel,
        showXLabel,
        showLegend,
        showGrid,
        showReferenceCurve,
        showSlopedStraightLineReferenceCurve,
        showHorizontalStraightLineReferenceCurve,
        showVerticalStraightLineReferenceCurve,
        colorBackground,
        colorPlotBorder,
        colorXYLabels,
        colorXTicks,
        colorYTicks,
        colorTitle,
        fontsizeTitle,
        fontsizeXYLabels,
        fontsizeXTicks,
        fontsizeYTicks,
        fontsizeLegend,
        valueTitle,
        valueLabelY,
        valueLabelX,
        valueLegendLocation,
        valuesLegendLabels,
        valueRefCurveMultiplier,
        valueRefCurveLabel,
        valueSlopedStraightLineRefCurveLabel,
        valueHorizontalStraightLineRefCurveLabel,
        valueVerticalStraightLineRefCurveLabel,
        valuesRefCurvePlotYList,
        valuesRefCurvePlotXList,
        valuesSlopedStraightLineRefCurvePlotYList,
        valuesSlopedStraightLineRefCurvePlotXList,
        valuesHorizontalStraightLineRefCurvePlotYList,
        valuesHorizontalStraightLineRefCurvePlotXList,
        valuesVerticalStraightLineRefCurvePlotYList,
        valuesVerticalStraightLineRefCurvePlotXList,
        plotStyle,
        plotBaseX,
        plotBaseY,
        lineWidth,
        markerSize
        ):
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
        
        if DEBUG:
            print('\n-- DEBUG --')
            print('showTitle: %s (%s)' % (showTitle, type(showTitle)))
            print('showYLabel: %s (%s)' % (showYLabel,type(showYLabel)))
            print('showXLabel: %s (%s)' % (showXLabel,type(showXLabel)))
            print('showLegend: %s (%s)' % (showLegend,type(showLegend)))
            print('showGrid: %s (%s)' % (showGrid,type(showGrid)))
            print('showReferenceCurve: %s (%s)' % (showReferenceCurve,type(showReferenceCurve)))
            print('showSlopedStraightLineReferenceCurve: %s (%s)' % (
                showSlopedStraightLineReferenceCurve,
                type(showSlopedStraightLineReferenceCurve))
                )
            print('showHorizontalStraightLineReferenceCurve: %s (%s)' % (
                showHorizontalStraightLineReferenceCurve,
                type(showHorizontalStraightLineReferenceCurve))
                )
            print('showVerticalStraightLineReferenceCurve: %s (%s)' % (
                showVerticalStraightLineReferenceCurve,
                type(showVerticalStraightLineReferenceCurve))
                )
            print('colorBackground: %s (%s)' % (colorBackground,type(colorBackground)))
            print('colorXYLabels: %s (%s)' % (colorXYLabels,type(colorXYLabels)))
            print('colorXTicks: %s (%s)' % (colorXTicks,type(colorXTicks)))
            print('colorYTicks: %s (%s)' % (colorYTicks,type(colorYTicks)))
            print('colorTitle: %s (%s)' % (colorTitle,type(colorTitle)))
            print('fontsizeTitle: %s (%s)' % (fontsizeTitle,type(fontsizeTitle)))
            print('fontsizeXYLabels: %s (%s)' % (fontsizeXYLabels,type(fontsizeXYLabels)))
            print('fontsizeXTicks: %s (%s)' % (fontsizeXTicks,type(fontsizeXTicks)))
            print('fontsizeYTicks: %s (%s)' % (fontsizeYTicks,type(fontsizeYTicks)))
            print('fontsizeLegend: %s (%s)' % (fontsizeLegend,type(fontsizeLegend)))
            print('valueTitle: %s (%s)' % (valueTitle,type(valueTitle)))
            print('valueLabelY: %s (%s)' % (valueLabelY,type(valueLabelY)))
            print('valueLabelX: %s (%s)' % (valueLabelX,type(valueLabelX)))
            print('valueLegendLocation: %s (%s)' % (valueLegendLocation,type(valueLegendLocation)))
            print('valuesLegendLabels: %s (%s)' % (valuesLegendLabels,type(valuesLegendLabels)))
            print('valueRefCurveMultiplier: %s (%s)' % (valueRefCurveMultiplier,type(valueRefCurveMultiplier)))
            print('valueRefCurveLabel: %s (%s)' % (valueRefCurveLabel,type(valueRefCurveLabel)))
            print('valueSlopedStraightLineRefCurveLabel: %s (%s)' % (
                valueSlopedStraightLineRefCurveLabel,
                type(valueSlopedStraightLineRefCurveLabel))
                )
            print('valueHorizontalStraightLineRefCurveLabel: %s (%s)' % (
                valueHorizontalStraightLineRefCurveLabel,
                type(valueHorizontalStraightLineRefCurveLabel))
                )
            print('valueVerticalStraightLineRefCurveLabel: %s (%s)' % (
                valueVerticalStraightLineRefCurveLabel,
                type(valueVerticalStraightLineRefCurveLabel))
                )
            print('valuesRefCurvePlotYList: %s (%s)' % (
                valuesRefCurvePlotYList,
                type(valuesRefCurvePlotYList))
                )
            print('valuesRefCurvePlotXList: %s (%s)' % (
                valuesRefCurvePlotXList,
                type(valuesRefCurvePlotXList))
                )
            print('valuesSlopedStraightLineRefCurvePlotYList: %s (%s)' % (
                valuesSlopedStraightLineRefCurvePlotYList,
                type(valuesSlopedStraightLineRefCurvePlotYList))
                )
            print('valuesSlopedStraightLineRefCurvePlotXList: %s (%s)' % (
                valuesSlopedStraightLineRefCurvePlotXList,
                type(valuesSlopedStraightLineRefCurvePlotXList))
                )
            print('valuesHorizontalStraightLineRefCurvePlotYList: %s (%s)' % (
                valuesHorizontalStraightLineRefCurvePlotYList,
                type(valuesHorizontalStraightLineRefCurvePlotYList))
                )
            print('valuesHorizontalStraightLineRefCurvePlotXList: %s (%s)' % (
                valuesHorizontalStraightLineRefCurvePlotXList,
                type(valuesHorizontalStraightLineRefCurvePlotXList))
                )
            print('valuesVerticalStraightLineRefCurvePlotYList: %s (%s)' % (
                valuesVerticalStraightLineRefCurvePlotYList,
                type(valuesVerticalStraightLineRefCurvePlotYList))
                )
            print('valuesVerticalStraightLineRefCurvePlotXList: %s (%s)' % (
                valuesVerticalStraightLineRefCurvePlotXList,
                type(valuesVerticalStraightLineRefCurvePlotXList))
                )
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
                'Number of curves to plot is out of range:\n\n' +
                '   Number of curves attempted: ' + str(lenYList) + '\n' +
                '   Max number of curves allowed: ' + str(numberCurvesMax) + '\n\n' +
                'To continue with plotting the first ' + str(numberCurvesMax) + '\n' +
                ' of ' + str(lenYList) + ' curves selected, click "OK".' + '\n\n' +
                'To halt plotting, click "CANCEL".' + '\n'
                )
            ans = askokcancel(
                'Max number of curves exceeded',
                stringLenYList
                )
            if not ans:
                return 
            else:
                lenYList = numberCurvesMax
   
# print figure number:
        if DEBUG:
            print(
                '\n------------------\n' + 
                'In module_PylabPlotMySQL_All\n' +
                '    self.numberPylabPlotFigure = %s' 
                ) % self.numberPylabPlotFigure
                
        
# reset defaults
        pylab.rcdefaults()
        
# tell pylab which figue we are dealing with; otherwise, defaults to Figure 1, which conflicts with regular x-y plots        
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
              'axes.facecolor' : colorBackground,   #colorChartBackground, # plot bg USE THIS!
              'axes.labelsize' : int(fontsizeXYLabels),   #fontsizeChartLabels,
             'axes.labelcolor' : colorXYLabels,  #colorChartLabels,    # x-y labels
             'xtick.labelsize' : int(fontsizeXTicks),   #fontsizeXTickLabels,
                 'xtick.color' : colorXTicks,    #colorXTickLabels, 
             'ytick.labelsize' : int(fontsizeYTicks),  #fontsizeYTickLabels,
                 'ytick.color' : colorYTicks,  #colorYTickLabels,
             'legend.fontsize' : int(fontsizeLegend),
#             'lines.linewidth' : lineWidth, # width of data plot lines and legend labels (0=thin, 5=thick)
#                 'figure.titlesize': 24,
#                 'figure.facecolor' : 'darkgray',
#                 'figure.edgecolor' : 'cyan',
#                 'figure.figsize' : [float(widthChartFigure), float(heightChartFigure)],
#                 'axes.titlesize' :  8,   #fontsizeChartTitle,
            }
            
# update the params   
        pylab.rcParams.update(params)
        
# create plots
# ... only one plot; all curves on one plot
        subplot=111
        
# ... define subplot FIRST before defining other parameters
        self.pylabSubplot = pylab.subplot(subplot)

# ... apply grid 
        pylab.grid(showGrid)
# ... x and y labels
        if showXLabel:
            pylab.xlabel(valueLabelX)
        if showYLabel:
            pylab.ylabel(valueLabelY)
# ... plot title
        if showTitle:
            pylab.title(
                valueTitle,
                color=colorTitle,
                size=fontsizeTitle
                )
            
        if DEBUG:
            print(
                '\nmodule_PylabPlotMySQL_All self.plot_X = '
                )
            print(self.plot_X)
            print(
                '\nmodule_PylabPlotMySQL_All self.plot_Y = '
                )
            print(self.plot_Y)
            
            if lenYList > numberCurvesMax:
                stringErrorNumberPlot = (
                    'Number of curves requested for plotting is over\n' +
                    'the maximum:\n\n' +
                    '  number of curves requested: %s\n' +
                    '  number of curves allowed: %s\n\n' +
                    'Reduce the number of curves to be plotted and try again.'
                    ) % (
                    lenYList,
                    numberCurvesMax
                    )
                print stringErrorNumberPlot
                showinfo(
                    'Error: too many curves',
                    stringErrorNumberPlot
                    )
                return      
            
# keep track of global values for xMin, yMin, xMax, yMax
        self.xMin_Global = []
        self.xMax_Global = []
        self.yMin_Global = []
        self.yMax_Global = []
        
# ... plot x-y
        for numberPlot in range(lenYList):
        
            module_PlotUtilities.plotStyleForCurve(
                self,
                pylab,
                plotStyle,
                self.plot_X[numberPlot],
                self.plot_Y[numberPlot],
                self.plotOptions[numberPlot],
                lineWidth,
                markerSize,
                plotBaseX,
                plotBaseY,
                )
                
            module_PlotUtilities.globalMinMaxValues(
                self,self.plot_X[numberPlot], self.plot_Y[numberPlot]
                )
      
# reference plot, if desired
        if showReferenceCurve:
            stringInvalidMultiplier = (
                'Unable to plot reference curve:' + '\n'
                '  Invalid value for reference curve multiplier.\n' +
                '  Multiplier must be a string representing either\n' +
                '  an integer, float, or fraction (e.g., 1/5).\n' 
                )
# change multiplier to decimal
            tempMult = valueRefCurveMultiplier
#            print 'tempMult, type = ',tempMult,type(tempMult)
            if tempMult == '1/10':
                multiplier = 1./10.
            elif tempMult == '1/9':
                multiplier = 1./9.
            elif tempMult == '1/8':
                multiplier = 1./8.
            elif tempMult == '1/7':
                multiplier = 1./7.
            elif tempMult == '1/6':
                multiplier = 1./6.
            elif tempMult == '1/5':
                multiplier = 1./5.
            elif tempMult == '1/4':
                multiplier = 1./4.
            elif tempMult == '1/3':
                multiplier = 1./3.
            elif tempMult == '1/2':
                multiplier = 1./2.
            elif tempMult == '2':
                multiplier = 2.
            elif tempMult == '3':
                multiplier = 3.
            elif tempMult == '4':
                multiplier = 4.
            elif tempMult == '5':
                multiplier = 5.
            elif tempMult == '6':
                multiplier = 6.
            elif tempMult == '7':
                multiplier = 7.
            elif tempMult == '8':
                multiplier = 8.
            elif tempMult == '9':
                multiplier = 9.
            elif tempMult == '10':
                multiplier = 10.
            elif tempMult.count('/') == 1:
# just one division sign is present in string, so try arbitrary fraction; if fails, nothing left to try
                tempMult_New = tempMult.split('/')
                try:
                    multiplier = float(tempMult_New[0]) / float(tempMult_New[1])
                except:
                # form error string
                    selfExt.MySQL_Output(
                        1,
                        stringInvalidMultiplier
                        )
                    showinfo(
                        'Error: invalid value',
                        '\n' + stringInvalidMultiplier + '\n'
                        )
                    return               
            else:
# last ditch chance to just float the string representing a number; if fails, nothing left to try
                try:
                    multiplier = float(valueRefCurveMultiplier)
                except:                   
                    selfExt.MySQL_Output(
                        1,
                        stringInvalidMultiplier
                        )
                    showinfo(
                        'Error: invalid value',
                        '\n' + stringInvalidMultiplier + '\n'
                        )
                    return
                    
# choose correct X-values for reference curve
            plot_X_RefCurve = valuesRefCurvePlotXList
            plot_Y_RefCurve = [float(y)*float(multiplier) for y in valuesRefCurvePlotYList]
            
# ... set up plots   
            module_PlotUtilities.plotStyleForCurve(
                self,
                pylab,
                plotStyle,
                plot_X_RefCurve,
                plot_Y_RefCurve,
                'r--d',
                lineWidth,
                markerSize,
                plotBaseX,
                plotBaseY,
                )    

            module_PlotUtilities.globalMinMaxValues(
                self,plot_X_RefCurve,plot_Y_RefCurve
                )
            
# sloped straight-line reference curve, if desired
        if showSlopedStraightLineReferenceCurve:
        
            module_PlotUtilities.plotStyleForCurve(
                self,
                pylab,
                plotStyle,
                valuesSlopedStraightLineRefCurvePlotXList,
                valuesSlopedStraightLineRefCurvePlotYList,
                'r--s',
                lineWidth,
                markerSize,
                plotBaseX,
                plotBaseY,
                )
                
            module_PlotUtilities.globalMinMaxValues(
                self,
                valuesSlopedStraightLineRefCurvePlotXList,
                valuesSlopedStraightLineRefCurvePlotYList
                )
                
# horizontal straight-line reference curve, if desired
        if showHorizontalStraightLineReferenceCurve:
# ... no need to error check; validation done in "X-Y PLOTTING SPECS" window 
       
            module_PlotUtilities.plotStyleForCurve(
                self,
                pylab,
                plotStyle,
                valuesHorizontalStraightLineRefCurvePlotXList,
                valuesHorizontalStraightLineRefCurvePlotYList,
                'r--s',
                lineWidth,
                markerSize,
                plotBaseX,
                plotBaseY,
                )
                
            module_PlotUtilities.globalMinMaxValues(
                self,
                valuesHorizontalStraightLineRefCurvePlotXList,
                valuesHorizontalStraightLineRefCurvePlotYList
                )
                
# vertical straight-line reference curve, if desired
        if showVerticalStraightLineReferenceCurve:
        
            module_PlotUtilities.plotStyleForCurve(
                self,
                pylab,
                plotStyle,
                valuesVerticalStraightLineRefCurvePlotXList,
                valuesVerticalStraightLineRefCurvePlotYList,
                'r--s',
                lineWidth,
                markerSize,
                plotBaseX,
                plotBaseY,
                )
                
            module_PlotUtilities.globalMinMaxValues(
                self,
                valuesVerticalStraightLineRefCurvePlotXList,
                valuesVerticalStraightLineRefCurvePlotYList
                ) 
                    
# display legend
#        print '\nself.legend_buttonStatus = %s\n' % self.legend_buttonStatus
        if showLegend:
            if DEBUG:
                print '\n====\nvaluesLegendLabels:\n',valuesLegendLabels
# set legend shadow
            stringLegendShadow = 'True'
# legend labels
            stringLegendLabels = []
#            lenLabels = len(self.plot_Labels)
            lenLabels = len(valuesLegendLabels)
#            for label in self.plot_Labels:
            for label in valuesLegendLabels:
                stringLegendLabels.append(label)
                
            if showReferenceCurve:
# include reference curve in legend
#                stringLegendLabels.append(str(multiplier) + ' * ' + self.refCurveLabel)
                stringLegendLabels.append(
                    str(valueRefCurveMultiplier) + ' * (' + valueRefCurveLabel +
                    ') [ref]'
                    )
                    
            if showSlopedStraightLineReferenceCurve:
# include horizontal straight-line reference curve in legend
                stringLegendLabels.append(
#                    'straight line [ref]'
                    valueSlopedStraightLineRefCurveLabel
                    )

            if showHorizontalStraightLineReferenceCurve:
# include horizontal straight-line reference curve in legend
                stringLegendLabels.append(
#                    'straight line [ref]'
                    valueHorizontalStraightLineRefCurveLabel
                    )
                    
            if showVerticalStraightLineReferenceCurve:
# include vertical straight-line reference curve in legend
                stringLegendLabels.append(
#                    'straight line [ref]'
                    valueVerticalStraightLineRefCurveLabel
                    )

# form legend
            pylab.legend(
                tuple(stringLegendLabels), 
                loc=valueLegendLocation, 
                shadow=stringLegendShadow
                )
                
        if plotStyle == 'semilogx' or plotStyle == 'loglog':
            if plotBaseX == 'e':
                xMin_Local = min(self.xMin_Global)
                xMax_Local = max(self.xMax_Global)
                okXLabels = module_PlotUtilities.formNewXLabels(
                    self,pylab,xMin_Local,xMax_Local,colorXTicks,fontsizeXTicks
                    )
                if not okXLabels:
                        return
            
        if plotStyle == 'semilogy' or plotStyle == 'loglog':
            if plotBaseY == 'e':
                yMin_Local = min(self.yMin_Global)
                yMax_Local = max(self.yMax_Global)
                okYLabels = module_PlotUtilities.formNewYLabels(
                    self,pylab,yMin_Local,yMax_Local,colorYTicks,fontsizeYTicks
                    )  
                if not okYLabels:
                        return
                        
# graph the plot
        pylab.show()
        
        return
 
        
def pylabCloseAll():
    '''
    Purpose:
        close all plot windows; called externally
            
    Called by:
        
        
    Calls:
        
        
    '''
    stringCloseAll = (
        '            -- WARNING! --\n\n' +
        'You are about to close ANY AND ALL open plots!\n\n' + 
        'Do you wish to continue?'
        )
    ans = askyesno(
        'WARNING!',
        stringCloseAll
        )
    if ans:
        exitProgram = True
        pylab.close('all')
    else:
        exitProgram = False
            
    return exitProgram
# ===== end of PlotsForPylotDB ===== 

        


