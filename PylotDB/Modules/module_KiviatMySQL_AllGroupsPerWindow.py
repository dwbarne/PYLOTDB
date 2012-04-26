#!/usr/local/bin/python         # for *nix runs
# ===== Header =====
# filename: radar_chart_dwb.py
#

# Purpose:
'''
Create Kiviat (spider web, or radar) charts
'''

# for debugging; if True, prints many module variables
DEBUG = False

# Module
MODULE = 'module_KiviatMySQL_AllGroupsPerWindow'

# import modules
from tkMessageBox import *      # dialogs such as askokcancel, showinfo, showerror, etc.
import Tkinter                  # to remove root.window()
import sys
import pylab                    # for closing plots
import time                     # to halt program for specific period using "time.sleep(secs)"
import matplotlib as mpl        # graphics package

stringImportsSuccess = ''
stringImportsFail = ''
flagImportsSuccess = False
flagImportsFail = False

# numpy
try:
    import numpy as np
    stringImportsSuccess += '\n  - numpy'
    flagImportsSuccess = True
except:
    stringImportsFail += '\n  - numpy'
    flagImportsFail = True
    
# matplotlib.pyplot
try:
    import matplotlib.pyplot as plt
    stringImportsSuccess += '\n  - matplotlib.pyplot'
    flagImportsSuccess = True
except:
    stringImportsFail += '\n  - matplotlib.pyplot'
    flagImportsFail = True
    
# matplotlib.patches as Circular
try:
    from matplotlib.patches import Circle
    stringImportsSuccess += '\n  - from matplotlib.patches import Circle'
except:
    stringImportsFail += '\n  - from matplotlib.patches import Circle'
    
# matplotlib.projections.polar
try:
    from matplotlib.projections.polar import PolarAxes
    stringImportsSuccess += '\n  - matplotlib.projections.polar'
    flagImportsSuccess = True
except:
    stringImportsFail += '\n  - matplotlib.projections.polar'
    flagImportsFail = True
    
# matplotlib.projections
try:
    from matplotlib.projections import register_projection
    stringImportsSuccess += '\n  - matplotlib.projections'
    flagImportsSuccess = True
except:   
    stringImportsFail += '\n  - matplotlib.projections'
    flagImportsFail = True

# show import result successes   
if DEBUG:
    if flagImportsSuccess:
        string = (
            '\nIn module: %s\nImported following modules:%s\n'
            ) % (stringImportsSuccess,MODULE)
        print(string)
        string=''
# show import result failures and exit if these exist
if flagImportsFail:
    string = (
        '\nIn module: %s\n' +
        'Cannot find following modules -- please install before continuing:%s\n'
        ) % (MODULE,stringImportsFail)
    print(string)
    showinfo(
        'Module import error',
        string
        )
    sys.exit()


# ===== main class =====
class Kiviat():
    def __init__(
        self,
        keepPreviousPlotWindow,
        xwin,
        ywin,
        numberPylabPlotFigure,
        **plotParams        
        ):
        '''
        Purpose:
            Create Kiviat diagrams
        '''
        '''
        selfExt.MySQL_Output(
            1,
            '** in class Kiviat in module_KiviaMySQL_All'
            )
        '''
        print '\n\n** in class Kiviat in module_KiviatMySQL_All'
        
# call constructor for Frame
#        Frame.__init__(self)
        
# parent frame
#        self.frameParentKiviatPlots = parent
# erase previous plot
        self.keepPreviousPlotWindow = keepPreviousPlotWindow
# window location
        self.xwin = xwin
        self.ywin = ywin
# figure number, if needed
        self.numberPylabPlotFigure = numberPylabPlotFigure
# plot data     
#        self.plotData = plotData
# legend labels
#        self.legendLabels = legendLabels
# spoke labels
#        self.spokeLabels = spokeLabels
# define empty list
        self.plotColorAndStyleOptions = []
# maximum number of plots allowed; 
#  hey, we have to draw the line somewhere.
        self.numPlotsMax = 25   # do NOT change!
# also, max number of curves/plot allowed;
# ... corresponds to number of combinations of [line colors] * [line styles]
        self.numCurvesPerPlotMax = 25 # do NOT change!
        
# plot curve colors and line styles; all combos result in max of 28 different types of lines
# ... plot colors            
        plotOptions_Colors = [
            'b',    # blue
            'r',    # red
            'g',    # green
            'm',    # magenta
            'y',    # yellow
            'c',    # cyan
            'lightgreen',
            ]
# ... line styles; matploblib has only 4 from which to choose
        plotOptions_Styles = [
            '-',    # solid line
            '--',   # dashed line
            '-.',   # dash-dot line
            ':',    # dotted line
            ]
# form all combinations of colors and styles; 28 total, which is
#   more than the max number of plots of 25; still do a check on this
#   farther below to see if user has changed max number of plots
        self.plotColorAndStyleOptions = []
        for style in plotOptions_Styles:
            for color in plotOptions_Colors:
                tempList=[]
# make a short list
                tempList.append(color)
                tempList.append(style)
# add short list to 'list of lists'
                self.plotColorAndStyleOptions.append(tempList)
                
        if DEBUG:
            print('self.plotColorAndStyleOptions = %s\n' % self.plotColorAndStyleOptions)            
            
        self.createKiviatDiagrams(**plotParams)
    
    def createKiviatDiagrams(self,
# **plotParams as defined in calling module
# ... title
        plotTitle,
        showTitle,
        fontsizeTitle,
        colorTitle,
        weightTitle,
        xTitleLocation,
        yTitleLocation,
# ... figure
        figureSize,
# ... subtitles 
        showSubTitles,
        showSubTitleContent,
        subtitleSize,
        subtitleColor,
        subtitleWeight,
        xSubTitleLocation,
        ySubTitleLocation,
# ... legend
        titleLegend,
        showLegend,
        valueLegendLocation,
        valueLegendLabelSpacing,
        fontsizeLegend,
        numberOfColumnsLegend,
        paddingBorderLegend,
        modeLegend,
        locationBBoxLegend,
        legendLabels,
# ... spoke labels
        showSpokeLabels,
        fontsizeSpokeLabels,
        colorSpokeLabels,
        spokeLabels,
# ... background color
        colorBackground,
# ... interior color
        colorPlot,
# ... lines
        plotLineWidth,
# ... grid  
        showGrid,
        gridColor,
        gridYTickColor,
        gridYTickFontSize,
        gridLineWidth,
        gridLineStyle,
        gridStepSize,
# ... opacity of filled regions
        alphaFactor,
# ... absolute or relative radius
        absoluteRadius,
# ... max radius value if 'absoluteRadius' is True
        absoluteRadiusMax,
# ... plot data
        plotData,
        ):
        '''
        Purpose:
            define all data and call methods to create Kiviat diagrams
        Max data values are assumed to be 1, so all data must be normalized
        by max data value in dataset.
        '''
        
# set plot parameters
# ... set params before calling plt.figure(...)
# ... reset defaults first
        plt.rcdefaults() 
        mpl.rcdefaults()

# create figure instance; tell pylab which figure we are dealing with; 
#  otherwise, defaults to Figure 1 as printed at top left of plot
#        fig = plt.figure(
#            self.numberPylabPlotFigure,
#            )        
            
# use if plotting in the same window and don't want to keep
#   previous plot

        if self.keepPreviousPlotWindow:
            try:
#                plt.clf()
                if DEBUG:
                    print('\n***** PLOT: clear current plot figure, plot in same')
            except:
                if DEBUG:
                    print('\n***** PLOT: error in advancing plot figure number')
        else:
            if DEBUG:
                print('\n***** PLOT: will advance plot figure')

           
        params = {
#              'figure.figsize' : figureSize,            # plot WxH in inches (9,9) for 4 plots total,
#            'figure.facecolor' : colorBackground,       # plot background color, exterior to kiviat plots

              'axes.facecolor' : colorPlot,             # interior color of kiviat plots
             'lines.linewidth' : plotLineWidth,         # width of data plot lines, legend labels (0=thin, 5=thick)

             'xtick.labelsize' : fontsizeSpokeLabels,   # font size for labels at ends of spokes (14)
                 'xtick.color' : colorSpokeLabels,      # color for radial grid labels
            
             'ytick.labelsize' : gridYTickFontSize,     # font size for radial stepsizes
                 'ytick.color' : gridYTickColor,        # color for radial grid numbers
            
                  'grid.color' : gridColor,             # color of radial grids
              'grid.linewidth' : gridLineWidth,         # linewidth of radial grids; default 0.5
              'grid.linestyle' : gridLineStyle,         # :=dotted; '-', '--','|'
            
             'legend.fancybox' : True,                  # rounded corners on legend box
             'legend.fontsize' : fontsizeLegend,        # small, medium, large, or use font sizes of 10, 12, ..., 36.
               'legend.shadow' : True,                  # shadows the legend box
                 'legend.mode' : modeLegend,            # allows legend to expand horizontally
                 'legend.ncol' : numberOfColumnsLegend, # number of columns in legend; default is 1
            'legend.borderpad' : paddingBorderLegend,   # white space just inside legend; default is 1
                 }
        plt.rcParams.update(params)
#        mpl.rcParams['figure.figsize'] = figureSize # **
#        mpl.rcParams['figure.facecolor'] = colorBackground # **
        
# create figure instance; tell pylab which figure we are dealing with; 
#  otherwise, defaults to Figure 1 as printed at top left of plot
        
        fig = plt.figure(
            self.numberPylabPlotFigure,
            facecolor=colorBackground,
            figsize=figureSize,
            ) 
            
# use if plotting in the same window and don't want to keep
#   previous plot
        if self.keepPreviousPlotWindow:
            try:
                plt.clf()
                if DEBUG:
                    print('\n***** PLOT: clear current plot figure, plot in same')
            except:
                if DEBUG:
                    print('\n***** PLOT: error in advancing plot figure number')
        else:
            if DEBUG:
                print('\n***** PLOT: will advance plot figure')
                
        if DEBUG:
            print("\nself.numberPylabPlotFigure = %s" % self.numberPylabPlotFigure)
                
#        time.sleep(3)
                


# calculate number of spokes needed
        N = len(plotData[plotData.keys()[0]][0])

# angle between spokes
        theta = self.radar_factory(N)
        
# list of plot titles:
        title_list = plotData.keys() 
        
# number of plots
        numberOfPlots = len(title_list)
                
        if DEBUG:
            print('\nN = %s (number of spokes needed)' % N)
            print('\ntitle_list: %s (list of plot titles)' % title_list)
            print('\nnumberOfPlots = %s (number of plots to be shown)' % numberOfPlots)

# set plot window format (keep this local to module)
# ... numbers correspond to plot params: left, bottom, right, top wspace, hspace
        if showLegend:
            if numberOfPlots == 1:
                listPlotParams = (.13,.05,.90,.70,.20,.20)
            elif numberOfPlots == 2:
                listPlotParams = (.13,.05,.90,.95,.30,.20)
            elif numberOfPlots <= 4:
                listPlotParams = (.13,.05,.90,.80,.20,.35)
            elif numberOfPlots <= 6:
                listPlotParams = (.13,.05,.90,.80,.30,.10)
            elif numberOfPlots <= 9:
                listPlotParams = (.13,.05,.90,.77,.05,.45)
            elif numberOfPlots <= 12:
                listPlotParams = (.13,.05,.90,.78,.50,.45)
            elif numberOfPlots <= 16:
                listPlotParams = (.13,.05,.90,.78,.10,.50)
            elif numberOfPlots <= 20:
                listPlotParams = (.13,.05,.90,.80,.30,.50)
            elif numberOfPlots <= 25:
                listPlotParams = (.13,.05,.90,.80,.20,.50)
        else:
            if numberOfPlots == 1:
                listPlotParams = (.13,.10,.90,.80,.20,.20)
            elif numberOfPlots == 2:
                listPlotParams = (.13,.15,.90,.90,.30,.20)
            elif numberOfPlots <= 4:
                listPlotParams = (.13,.05,.90,.85,.20,.40)
            elif numberOfPlots <= 6:
                listPlotParams = (.13,.05,.90,.90,.35,.03)
            elif numberOfPlots <= 9:
                listPlotParams = (.13,.05,.90,.85,.20,.45)
            elif numberOfPlots <= 12:
                listPlotParams = (.13,.05,.90,.90,.50,.10)
            elif numberOfPlots <= 16:
                listPlotParams = (.13,.05,.90,.88,.42,.50)
            elif numberOfPlots <= 20:
                listPlotParams = (.13,.05,.90,.90,.50,.14)
            elif numberOfPlots <= 25:
                listPlotParams = (.13,.05,.90,.87,.34,.61)
            
# ----- ERROR CHECKING -----

# error check on number of plots max
# inform user if numberOfPlots exceeds self.numPlotsMax; give option to user to either quit
#   this plot routine or have number of plots reduced to self.numPlotsMax
        if numberOfPlots > self.numPlotsMax:
            stringErrorPlotsMax = (
                'Number of plots: %s\n\n' +
                'Maximum number of plots allowed: %s\n\n' +
                'If you choose to continue, the number of plots will\n' +
                'be reduced to the max number allowed.\n\n' +
                'Do you wish to continue?'
                ) % (numberOfPlots, self.numPlotsMax)
            print('\n' + stringErrorPlotsMax)
            ans = askyesno(
                'continue??',
                stringErrorPlotsMax
                )
            if not ans:
                return
            else:
                title_list = title_list[0:self.numPlotsMax]
                numberOfPlots = len(title_list)

# error check on number of Color/Styles corresponding to max curves/plot
        self.tooManyCurves = False
        if len(self.plotColorAndStyleOptions) < self.numCurvesPerPlotMax:
            stringTooFewOptions = (
                'There are too few Color/CurveStyle combinations for\n' +
                'the max-allowed number of curves that can be plotted.\n\n' +
                'Max number of allowed curves/plot that can be plotted: %s\n\n' +
                'Number of Color/CurveStyle combos: %s\n\n' +
                'Choose "OK" to continue on with max number of curves\n' +
                'reset to max number of Color/CurveStyle combos, or\n' +
                'choose "Cancel" to cancel this operation.\n'
                ) % (self.numCurvesPerPlotMax, len(self.plotColorAndStyleOptions))
            ans = askokcancel(
                'Too many curves',
                stringTooFewOptions
                )
            if ans:
                self.tooManyCurves = True
                self.numCurvesPerPlotMax = len(self.plotColorAndStyleOptions)
            else:
                return
                
# ----- END OF ERROR CHECKING -----
                
# set initial value of subplot
        if numberOfPlots == 1: 
            plotOptions_SubPlot = 110   # row, column, plotNumber; rows fill first
        elif numberOfPlots <= 2: 
            plotOptions_SubPlot = 120
        elif numberOfPlots <= 4:
            plotOptions_SubPlot = 220
        elif numberOfPlots <= 6:
            plotOptions_SubPlot = 230
        elif numberOfPlots <= 9:
            plotOptions_SubPlot = 330
        elif numberOfPlots <= 12:
            plotOptions_SubPlot = 340
        elif numberOfPlots <= 16:
            plotOptions_SubPlot = 440
        elif numberOfPlots <= 20:
            plotOptions_SubPlot = 450
        elif numberOfPlots <= 25:
            plotOptions_SubPlot = 550
        else:
            stringNumPlots = (
                'Number of plots out of range:\n' +
                '   Number of plots attempted: ' + str(numberOfPlots) + '\n' +
                '   Max number of plots allowed: ' + str(self.numPlotsMax) + '\n\n' +
                'This message represents a coding error. Please contact\n' +
                'the code administrator to correct this error.'
                )
            print stringNumPlots
            self.MySQL_Output(
                1,
                stringNumPlots
                )
#            root = Tkinter.Tk() 
#            root.withdraw() 
            showinfo(
                'Error: too many plots',
                '\n' + stringNumPlots + '\n'
                )
            return

        rowSubPlot = int(str(plotOptions_SubPlot)[0:1]) # first digit; defines number of rows
        colSubPlot = int(str(plotOptions_SubPlot)[1:2]) # second digit; defines number of columns
        numSubPlot = int(str(plotOptions_SubPlot)[2:3]) # third digit; defines plot number - first is zero

        if DEBUG:
            print('\nInitial subplot #: %s' % (str(rowSubPlot) + str(colSubPlot) + str(numSubPlot)))
        
# print some checks
        if DEBUG:
            print('\n*** In module module_KiviatMySQL_AllGroupsPerWindow')
            print('\n   Grid background color: %s\n' % colorBackground)
                  
# sort title list to display alphabetically; 
# ... MAY WANT TO MAKE THIS USER-SELECTABLE IN THE FUTURE <<<<<<<<<<<<<<<<<<<<<<<
        title_list.sort()

# define colors to cycle through        
#        colors = self.plotColorAndStyleOptions_Colors
        
# adjust spacing around the subplots; can be further
#   adjusted directly on plot
        fig.subplots_adjust(
            left=listPlotParams[0],      # orig value: 0.125
            bottom=listPlotParams[1],    # orig value: 0.05
            right=listPlotParams[2],     # orig value: 0.9
            top=listPlotParams[3],       # orig value: 0.85
            wspace=listPlotParams[4],    # orig value: 0.25
            hspace=listPlotParams[5],    # orig value: 0.20
            )
        
# grid increments shown on diagram, using grid stepsize(0.1, 0.2, or 0.5)
        if showGrid:
            if absoluteRadius:
                grid_count = int(absoluteRadiusMax/gridStepSize)
            else:
                grid_count = int(1./gridStepSize)
            radial_grid = []
            for grid in range(grid_count + 1):
# radial_grid cannot contain a zero! All values must be > 0
                if grid == 0: continue
                radial_grid.append(grid * gridStepSize)
            
        if DEBUG:
            if showGrid:
                print('\nradial_grid: %s' % radial_grid)
            else:
                print('\nradial grid not used for this run')

# If you don't care about the order, you can loop over data_dict.items()
# Note: n begins with number zero, so add 1 to n to get proper numbers
        subplot = plotOptions_SubPlot
        
        if DEBUG:
            print('\nshowLegend = %s' % showLegend)
            print('valueLegendLocation = %s' % str(valueLegendLocation))
            print('valueLegendLabelSpacing = %s' % str(valueLegendLabelSpacing))
            
# add 'ref' values to end if desired, to make sure circle radius is = 'absoluteRadiusMax'
        if absoluteRadius:
# include list 'ref' to make sure outer diameter of plots goes all way to 'absoluteRadiusMax';
#   otherwise, the plot diameter will be equal to max plotted value, which makes 
#   all plots have a different scale but same visual size. This is no good for visual comparisons.   
# form a list of reference values; list is same length as data list
            ref = [absoluteRadiusMax for x in range(len(plotData.values()[0][0]))]
            for key in plotData.keys():
                plotData[key].append(ref)

# list for tracking which plots has too many lines/plot                
        numberPlotHasTooManyCurves = []
        
# loop over data dictionary keys
        for title in title_list:
            numSubPlot += 1
            if DEBUG:
                print
                print('rowSubPlot, colSubPlot, numSubPlot = %s, %s, %s' %
                    (rowSubPlot, colSubPlot, numSubPlot))
            ax = fig.add_subplot(
#                2, 
#                2, 
#                n+1, 
#                subplot,
# must list subplot dimensions separately since numSubPlot can be greater than 9 
#  (see MatPlotLib manual)
                rowSubPlot,
                colSubPlot,
                numSubPlot,
                projection='radar',
                )
                
            if showGrid:
                if DEBUG:
                    print('\n Plotting grid...')
                    print('     calling plt.rgrids')
                    print
                plt.rgrids(radial_grid,labels=None)

            if showSubTitles:
                ax.set_title(
                    showSubTitleContent, 
                    weight=subtitleWeight, 
                    size=subtitleSize, 
#                    position=(0.5, 1.1),    # sub-titles for each plot; orig position (0.5, 1.1)
                    position=(xSubTitleLocation, ySubTitleLocation),    # sub-titles for each plot; orig position (0.5, 1.1)
                    horizontalalignment='center', 
                    verticalalignment='center',
                    color=subtitleColor,
                    )
                    
# this is where the plotting and filling is done
# check to see if too many curves per plot; if so, store plot number and print at end;
#   goal here is to present plots at all costs, but at least let user know
            lenPlotData = len(plotData[title]) # number of curves to plot
            if lenPlotData > self.numCurvesPerPlotMax:  
# reduce number of curves to max allowed            
                lenPlotData = self.numCurvesPerPlotMax
# store plot number in a list; if empty at end of loop, then no plot has too many curves
                numberPlotHasTooManyCurves.append(numSubPlot)
#            maxNumberOfStyles = len(self.plotColorAndStyleOptions_Styles)
#            maxNumberOfColors = len(self.plotColorAndStyleOptions_Colors)
            icount=0
#            for d, color in zip(self.plotData[title], colors):
            for numLine in range(lenPlotData):
# -----
# determine line color (red, blue, etc.) and line style (dash, dot, solid, etc.)
#                for numStyle in range(maxNumberOfStyles):
#                    for numColor in range(maxNumberOfColors):
#                        if numLine < (numStyle * numColor):
#                            lineColor = self.plotColorAndStyleOptions_Colors[numColor]
#                            lineStyle = self.plotColorAndStyleOptions_Styles[numStyle]
#                            break
# -----
                icount += 1
                if DEBUG:
                    print('lenPlotData, numLine, icount = %s, %s, %s' % 
                        (lenPlotData,numLine,icount)
                        )
                if absoluteRadius:
# each plot diameter will be equal to 'absoluteRadiusMax'
                    if icount < lenPlotData:
                        ax.plot(
                            theta, 
#                            d,
                            plotData[title][numLine],
#                            color=lineColor,
#                            linestyle=lineStyle,
                             color=self.plotColorAndStyleOptions[numLine][0],
                             linestyle=self.plotColorAndStyleOptions[numLine][1],
#                            linestyle='dashed',
#                            color=color,
                            )
                        ax.fill(
                            theta, 
#                            d, 
                            plotData[title][numLine],
#                            facecolor=color, 
                            facecolor=self.plotColorAndStyleOptions[numLine][0], 
                            alpha=alphaFactor,
                            )
# 'ref' data is plotted but is invisible; forces circle diameter equal 1 
#   if specified by 'absoluteRadius'; otherwise, will max diameter will default
#   to max value of data and will be different for each plot.
                    else:
                        ax.plot(
                            theta, 
#                            d,
                            plotData[title][numLine],
                            color='k', 
                            linestyle='solid',
                            alpha=0,   # set to 0.5 to see 'ref' lines
                            )
                        ax.fill(
                            theta, 
#                            d, 
                            plotData[title][numLine], 
                            facecolor='lightgreen', 
                            alpha=0,   # set to 0.5 to fill in 'ref' region
                            )
                else:
# each plot diameter will simply be equal to max data value rather than absolute value
                    ax.plot(
                        theta, 
                        plotData[title][numLine],
#                        color=lineColor
                        color=self.plotColorAndStyleOptions[numLine][0],
                        linestyle=self.plotColorAndStyleOptions[numLine][1],
                        )
                    ax.fill(
                        theta, 
                        plotData[title][numLine], 
                        facecolor=self.plotColorAndStyleOptions[numLine][0], 
                        alpha=alphaFactor
                        )
# if spokeLabels are not specified, display will default to angles in degrees
            if showSpokeLabels:
                ax.set_varlabels(
                    spokeLabels
                    ) 

        if showTitle:
            title_params = {
                'x' : xTitleLocation,   # x location of text in figure coords; practical range 0.1 -> 0.9
                'y' : yTitleLocation,  # y location; practical range is 0.1 -> 0.98
                'horizontalalignment' : 'center', # leave this as is
                'verticalalignment' : 'top',    # leave this as is
                }
            fig.suptitle(
                plotTitle,
                weight=weightTitle,
                size=fontsizeTitle,
                color=colorTitle,
                **title_params
                )
                
# not valid for positioning window
#        fig.figimage({'xo':self.xwin,'yo':self.ywin})

# specify which plot will get legend   
#        plt.subplot(rowSubPlot,colSubPlot,2)

        if showLegend:
#            if rowSubPlot == 1:
#                if colSubPlot == 2:
# legend appears to be placed relative to the last plot drawn
            labels = legendLabels
            if DEBUG:
                print('\nlegend labels = %s\n' % labels)
            legend = plt.legend(
                labels, 
                loc=valueLegendLocation,
                labelspacing=valueLegendLabelSpacing,
                bbox_to_anchor=locationBBoxLegend,
                bbox_transform=plt.gcf().transFigure,
                ncol=numberOfColumnsLegend,
                title=titleLegend,
                )       

        plt.show()
        
# print which plots had to be truncated;
# ... plots are numbered from left to right and top to bottom
        if len(numberPlotHasTooManyCurves) > 0:
            stringPlotHasTooManyCurves = (
                'The following plots were truncated, the number of lines\n' +
                'in each plot having exceeded the max allowed of %s\n\n' +
                '%s'
                ) % (numberPlotHasTooManyCurves)
            print(stringPlotHasTooManyCurves)
            showinfo(
                'Following plots truncated',
                stringPlotHasTooManyCurves
                )
            
      
# factory function that returns class to the caller
# ... register class as handler for projections of type 'radar' ;
# ... class RadarAxes is implementing a protocol (interface) that is 
#       required by register_projection()
    def radar_factory(self, num_vars, frame='circle'):
        '''
        Create a radar chart with `num_vars` axes.
        '''
# calculate evenly-spaced axis angles
        theta = 2*np.pi * np.linspace(0, 1-1./num_vars, num_vars)
# rotate theta such that the first axis is at the top
        theta += np.pi/2

        def draw_poly_frame(self, x0, y0, r):
# TODO: use transforms to convert (x, y) to (r, theta)
            verts = [
                (r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta
                ]
            return plt.Polygon(verts, closed=True, edgecolor='k')

        def draw_circle_frame(self, x0, y0, r):
#            return plt.Circle((x0, y0), r)
#            return Circle((x0, y0), r, facecolor='none', edgecolor='green', alpha=0.2)
            if DEBUG:
                print('x0, y0, r: %s, %s, %s' % (x0, y0, r))
            params_circle = {
#                'facecolor' : 'blue',  # no effect
                'alpha' : 1,  # opacity; 0 = none, 1 = 100% opaque to background color;
                              #   leave at 1
#               'edgecolor' : 'red',    # no effect
                }
            return Circle((x0, y0), r, **params_circle)
            '''
                'edgecolor' : 'red', 
                'alpha' : 1.0}       
                )  
            '''

        frame_dict = {
            'polygon': draw_poly_frame, 
            'circle': draw_circle_frame
            }
        if frame not in frame_dict:
            raise ValueError, 'unknown value for `frame`: %s' % frame

        class RadarAxes(PolarAxes):
            '''
            Class for creating a radar chart (a.k.a. a spider, kiviat, or star chart)
            http://en.wikipedia.org/wiki/Radar_chart
            '''
            name = 'radar'
# use 1 line segment to connect specified points
            RESOLUTION = 1
# define draw_frame method
            draw_frame = frame_dict[frame]

            def fill(self, *args, **kwargs):
                '''
                Override fill so that line is closed by default
                '''
                closed = kwargs.pop('closed', True)
                return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

            def plot(self, *args, **kwargs):
                '''
                Override plot so that line is closed by default
                '''
                lines = super(RadarAxes, self).plot(*args, **kwargs)
                for line in lines:
                    self._close_line(line)

            def _close_line(self, line):
                x, y = line.get_data()
# FIXME: markers at x[0], y[0] get doubled-up
                if x[0] != x[-1]:
                    x = np.concatenate((x, [x[0]]))
                    y = np.concatenate((y, [y[0]]))
                    line.set_data(x, y)

            def set_varlabels(self, labels):
                self.set_thetagrids(
                    theta * 180/np.pi, 
                    labels
                    )

            def _gen_axes_patch(self):
                x0, y0 = (0.5, 0.5)
                r = 0.5
                return self.draw_frame(x0, y0, r)

        register_projection(RadarAxes)
        return theta
        
# close all plots
def pylabCloseAll():
    '''
    Purpose:
        close all plot windows; called externally
            
    Called by:
        module_accessMySQL
        
    Calls:
        pylab.close        
        
    '''
    plt.close('all')
        
# ===== end of Kiviat ===== 


if __name__ == '__main__':
    #The following example data is from the Denver Aerosol Sources and Health study.
    #See  doi:10.1016/j.atmosenv.2008.12.017
    #
    #The data are pollution source profile estimates for five modeled pollution
    #sources (e.g., cars, wood-burning, etc) that emit 7-9 chemical species.
    #The radar charts are experimented with here to see if we can nicely
    #visualize how the modeled source profiles change across four scenarios:
    #  1) No gas-phase species present, just seven particulate counts on
    #     Sulfate
    #     Nitrate
    #     Elemental Carbon (EC)
    #     Organic Carbon fraction 1 (OC)
    #     Organic Carbon fraction 2 (OC2)
    #     Organic Carbon fraction 3 (OC3)
    #     Pyrolized Organic Carbon (OP)
    #  2)Inclusion of gas-phase specie carbon monoxide (CO)
    #  3)Inclusion of gas-phase specie ozone (O3).
    #  4)Inclusion of both gas-phase species is present...
    
    # NOTE: For this program, the data has been duplicated enough times to produce
    #  a maximum of up to 25 plots depending on what number the user selects.
    
# standard technique to remove the root window that always pops up when
#  a full-blown gui is not implemented
# NOTE: makes process hard to stop. Sometimes CTRL-C works, sometimes not.
#    root = Tkinter.Tk() 
#    root.withdraw()
        
    numberOfPlots = 0
    while numberOfPlots < 1 or numberOfPlots > 28:
        numberOfPlots = eval(raw_input('\nEnter number of plots desired for demo (1-28): '))
        if numberOfPlots < 1 or numberOfPlots > 28:
            print('... plot range must be 1 <= number of plots <= 28\nTry again.\n')

# define plot parameters using a dictionary; these values will be selectable when
#   called from a gui            
    plotParams = {
    # title     
        'plotTitle' : '5-Factor Solution Profiles Across Four Scenarios', # main plot title
        'showTitle' : True, # main title (True/False)
        'fontsizeTitle' : int(24),       # sets font for title only (8-32; default 20)
        'colorTitle' : 'black',
        'weightTitle' : 'bold', # title weight: normal, bold
        'xTitleLocation' : float(0.5), # practical range 0.1 -> 0.9
        'yTitleLocation' : float(0.98), # practical range 0.1 -> 0.98
    # figure
        'figureSize' : (float(16),float(12)), # size of figure window relative to screen (default: (16,12))
    # subtitles
        'showSubTitles' : True, # individual plot titles (True/False)
        'showSubTitleContent' : 'Normalized values', # plot subtitle, "Normalization factor: "
        'subtitleSize' : int(16),    # subtitle font size (8->24; default 16)
        'subtitleColor' : 'black',    # subtitle color; default 'black'
        'subtitleWeight' : 'bold',    # subtitle weight (normal, bold; default bold)
        'xSubTitleLocation' : float(0.5),
        'ySubTitleLocation' : float(1.15), # practical range: 1.10 -> 1.25; default 1.15; increment by .01
    # legend
        'titleLegend' : 'Factor Number',
        'showLegend' : True, # should be True,
        'valueLegendLocation' : 'best',  # use 'bottom center'; orig values [0.9, 0.95]; seems relative (can be 'upper right')                                             to square drawn around plots only
        'valueLegendLabelSpacing' : float(0.2),    # can vary between 0 and 1; default 0.2; space between legend lines
        'fontsizeLegend' : int(14),    # can vary from 10 -> 32; default 14
        'numberOfColumnsLegend' : int(1), # number of columns in legend; 1 -> 3; default 1
        'paddingBorderLegend' : float(0.5), # padding between outer part of legend box and text; default 0.8; 0 -> 1
        'modeLegend' : 'expand',    # either 'expand' across figure, or None (no quotes)
        'locationBBoxLegend' : (float(0.55), float(0.95)), # will depend on how many plots are presented; 
                                             # in gui, set this depending on number of plots as shown below,
                                             # but give user opportunity to manually change legend_location;
                                             # subplot_params can always be changed directly in graph;
                                # if 'showLegend' is True:
                                    # plotnum   legend_location     subplot_params
                                    #                               left,bottom,right,top,wspace,hspace
                                    # -------   ---------------     ------------------------------------------
                                    #   1       (0.55, 0.95)        (.13,.05,.90,.70,.20,.20)
                                    #   2       (0.55, 0.95)        (.13,.05,.90,.95,.30,.20)
                                    #   3-4     (0.55, 0.95)        (.13,.05,.90,.80,.20,.35)
                                    #   5-6     (0.55, 0.95)        (.13,.05,.90,.80,.30,.10)
                                    #   7-9     (0.55, 0.95)        (.13,.05,.90,.77,.05,.45)
                                    #   10-12   (0.55, 0.95)        (.13,.05,.90,.78,.50,.45)
                                    #   13-16   (0.55, 0.95)        (.13,.05,.90,.78,.10,.50)
                                    #   17-20   (0.55, 0.95)        (.13,.05,.90,.80,.30,.50)
                                    #   21-25   (0.55, 0.95)        (.13,.05,.90,.80,.20,.50)
                                # if 'showLegend' is False:
                                    #   1       (0.55, 0.95)        (.13,.10,.90,.80,.20,.20)
                                    #   2       (0.55, 0.95)        (.13,.15,.90,.90,.30,.20)
                                    #   3-4     (0.55, 0.95)        (.13,.05,.90,.85,.20,.40)
                                    #   5-6     (0.55, 0.95)        (.13,.05,.90,.90,.35,.03)
                                    #   7-9     (0.55, 0.95)        (.13,.05,.90,.85,.20,.45)
                                    #   10-12   (0.55, 0.95)        (.13,.05,.90,.90,.50,.10)
                                    #   13-16   (0.55, 0.95)        (.13,.05,.90,.88,.42,.50)
                                    #   17-20   (0.55, 0.95)        (.13,.05,.90,.90,.50,.14)
                                    #   21-25   (0.55, 0.95)        (.13,.05,.90,.87,.34,.61)
        'legendLabels' : [],
    # spoke labels
        'showSpokeLabels' : True, # if False, angles in degrees will be displayed; not helpful
        'fontsizeSpokeLabels' : int(14), # font for spoke labels; 8-32; default 14
        'colorSpokeLabels' : 'black', # color for spoke labels
        'spokeLabels' : [], # list of spoke labels
    # background color
        'colorBackground' : 'lightblue',    # plot background color; default 'lightblue'
    # interior color
        'colorPlot' : 'white',     # interior color of plot; default 'white'
    # lines      
        'plotLineWidth' : float(2),    # vary between 1 and 10; default 2
    # grid
        'showGrid' : True,  # show grid
        'gridColor' : 'black',      # color of radial and circumferential grids lines
        'gridYTickColor' : 'blue',   # color of numbers delineating gridStepSize
        'gridYTickFontSize' : int(12),   # font size for grid increment numbers
        'gridLineWidth' : float(0.5),      # width of radial and circumferential grid lines
        'gridLineStyle' : ':',      # style of grid; can be ':'=dotted, '-'=solid, '--'=dashed, '|'=, '-.'=dash-dot
        'gridStepSize' : float(0.5),       # radial grid increments: 0.1, 0.2, or 0.5 only; default 0.5(no user input)
    # opacity of filled regions in Kiviat diagram
        'alphaFactor' : float(0.2), # range of 0 (clear) to 1 (opaque); default 0.2
    # specify if radius should always be 1, or max radial value <= 1  
        'absoluteRadius' : True,    # if True, sets normalized circle radius to 'absoluteRadiusMax'
                                    #  if False, sets normalized radius to max value of data for each plot (floating radius)
    # specify max radius value, used when 'absoluteRadius' is True
        'absoluteRadiusMax' : float(1),    # used when 'absoluteRadius' is True
    # plot data
        'plotData' : [],
        }

# legend labels
    plotParams['legendLabels'] = ['Factor 1','Factor 2', 'Factor 3', 'Factor 4', 'Factor 5']
# plot data; must be a list
    f1_base = [0.88, 0.01, 0.03, 0.03, 0.00, 0.06, 0.01, 0.00, 0.00]
    f1_CO =   [0.88, 0.02, 0.02, 0.02, 0.00, 0.05, 0.00, 0.05, 0.00]
    f1_O3 =   [0.89, 0.01, 0.07, 0.00, 0.00, 0.05, 0.00, 0.00, 0.03]
    f1_both = [0.87, 0.01, 0.08, 0.00, 0.00, 0.04, 0.00, 0.00, 0.01]

    f2_base = [0.07, 0.95, 0.04, 0.05, 0.00, 0.02, 0.01, 0.00, 0.00]
    f2_CO =   [0.08, 0.94, 0.04, 0.02, 0.00, 0.01, 0.12, 0.04, 0.00]
    f2_O3 =   [0.07, 0.95, 0.05, 0.04, 0.00, 0.02, 0.12, 0.00, 0.00]
    f2_both = [0.09, 0.95, 0.02, 0.03, 0.00, 0.01, 0.13, 0.06, 0.00]

    f3_base = [0.01, 0.02, 0.85, 0.19, 0.05, 0.10, 0.00, 0.00, 0.00]
    f3_CO =   [0.01, 0.01, 0.79, 0.10, 0.00, 0.05, 0.00, 0.31, 0.00]
    f3_O3 =   [0.01, 0.02, 0.86, 0.27, 0.16, 0.19, 0.00, 0.00, 0.00]
    f3_both = [0.01, 0.02, 0.71, 0.24, 0.13, 0.16, 0.00, 0.50, 0.00]

    f4_base = [0.02, 0.01, 0.07, 0.01, 0.21, 0.12, 0.98, 0.00, 0.00]
    f4_CO =   [0.00, 0.02, 0.03, 0.38, 0.31, 0.31, 0.00, 0.59, 0.00]
    f4_O3 =   [0.01, 0.03, 0.00, 0.32, 0.29, 0.27, 0.00, 0.00, 0.95]
    f4_both = [0.01, 0.03, 0.00, 0.28, 0.24, 0.23, 0.00, 0.44, 0.88]

    f5_base = [0.01, 0.01, 0.02, 0.71, 0.74, 0.70, 0.00, 0.00, 0.00]
    f5_CO =   [0.02, 0.02, 0.11, 0.47, 0.69, 0.58, 0.88, 0.00, 0.00]
    f5_O3 =   [0.02, 0.00, 0.03, 0.37, 0.56, 0.47, 0.87, 0.00, 0.00]
    f5_both = [0.02, 0.00, 0.18, 0.45, 0.64, 0.55, 0.86, 0.00, 0.16]
        
    plotData = {
        'Basecase': [f1_base, f2_base, f3_base, f4_base, f5_base],
        'With CO': [f1_CO, f2_CO, f3_CO, f4_CO, f5_CO],
        'With O3': [f1_O3, f2_O3, f3_O3, f4_O3, f5_O3],
        'CO & O3': [f1_both, f2_both, f3_both, f4_both, f5_both],
        'Basecase_2': [f1_base, f2_base, f3_base, f4_base, f5_base],
        'With CO_2': [f1_CO, f2_CO, f3_CO, f4_CO, f5_CO],
        'With O3_2': [f1_O3, f2_O3, f3_O3, f4_O3, f5_O3],
        'CO & O3_2': [f1_both, f2_both, f3_both, f4_both, f5_both],
        'Basecase_3': [f1_base, f2_base, f3_base, f4_base, f5_base],
        'With CO_3': [f1_CO, f2_CO, f3_CO, f4_CO, f5_CO],
        'With O3_3': [f1_O3, f2_O3, f3_O3, f4_O3, f5_O3],
        'CO & O3_3': [f1_both, f2_both, f3_both, f4_both, f5_both],
        'Basecase_4': [f1_base, f2_base, f3_base, f4_base, f5_base],
        'With CO_4': [f1_CO, f2_CO, f3_CO, f4_CO, f5_CO],
        'With O3_4': [f1_O3, f2_O3, f3_O3, f4_O3, f5_O3],
        'CO & O3_4': [f1_both, f2_both, f3_both, f4_both, f5_both],
        'Basecase_5': [f1_base, f2_base, f3_base, f4_base, f5_base],
        'With CO_5': [f1_CO, f2_CO, f3_CO, f4_CO, f5_CO],
        'With O3_5': [f1_O3, f2_O3, f3_O3, f4_O3, f5_O3],
        'CO & O3_5': [f1_both, f2_both, f3_both, f4_both, f5_both],
        'Basecase_6': [f1_base, f2_base, f3_base, f4_base, f5_base],
        'With CO_6': [f1_CO, f2_CO, f3_CO, f4_CO, f5_CO],
        'With O3_6': [f1_O3, f2_O3, f3_O3, f4_O3, f5_O3],
        'CO & O3_6': [f1_both, f2_both, f3_both, f4_both, f5_both],
        'Basecase_7': [f1_base, f2_base, f3_base, f4_base, f5_base],
        'With CO_7': [f1_CO, f2_CO, f3_CO, f4_CO, f5_CO],
        'With O3_7': [f1_O3, f2_O3, f3_O3, f4_O3, f5_O3],
        'CO & O3_7': [f1_both, f2_both, f3_both, f4_both, f5_both],
        }
            
    plotParams['spokeLabels'] = ['Sulfate', 'Nitrate', 'EC', 'OC1', 'OC2', 'OC3', 'OP', 'CO',
                    'O3']
                    
# plotData reduced to numberOfPlots
    tempDict = {}
    icount = 0
    for key,value in plotData.iteritems():
        icount += 1
        tempDict[key] = value
        if icount == numberOfPlots:
            break
                
    plotParams['plotData'] = tempDict
    

    
    Kiviat(
        True,   # keep previous plot
        150,    # xwin
        150,    # ywin
        1,      # numberPylabPlotFigure
        **plotParams
        )
