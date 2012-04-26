#!/usr/local/bin/python         # for *nix runs
# ===== Header =====
# filename: radar_chart_dwb.py
#

# Purpose:
'''
Create Kiviat (spider web, or radar) charts, all curves on multiple plots
'''

import numpy as np                  # for calculations with Pi, linspace, etc.
import matplotlib.pyplot as plt     # for plots
import pylab                        # to set parameters
#from Tkinter import *               # for widgets
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection


# ===== main class =====
class Kiviat_All():
    def __init__(
        self,
#        parent,
#        selfExt,
        keepPreviousPlot,
        xwin,
        ywin,
        dataKiviatAll,
        numberOfTableCurves,
        numberPylabPlotFigure,
        plotTitle,
        legendLabels,
        plotData,
        spokeLabels,
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
        print('\n** in class Kiviat in module_KiviatMySQL_All')
        
# call constructor for Frame
#        Frame.__init__(self) 
# parent frame
#        self.frameParentKiviatPlots = parent

# erase previous plot
        self.keepPreviousPlot = keepPreviousPlot
# window location
        self.xwin = xwin
        self.ywin = ywin
# figure number, if needed
        self.numberPylabPlotFigure = numberPylabPlotFigure
# plot data     
        self.plotData = plotData
# plot title
        self.plotTitle = plotTitle
# legend labels
        self.legendLabels = legendLabels
# spoke labels
        self.spokeLabels = spokeLabels
# number of table and buffer curves
        self.numberOfTableCurves = numberOfTableCurves
# plot colors            
        self.plotOptions_Colors = [
            'b',    # blue
            'r',    # red
            'g',    # green
            'm',    # magenta
            'y',    # yellow
            'c',    # cyan
            ]
        
        self.createKiviatDiagrams(**plotParams)
    
    def createKiviatDiagrams(self,
# **plotParams as defined in calling module
        showTitle,
        showLegend,
        showGrid,
        colorBackground,
        colorTitle,
        fontsizeTitle,
        fontsizeLabels,
        fontsizeLegend,
        valueLegendLocation,
        valueLegendLabelSpacing,
        ):
        '''
        Purpose:
            define all data and call methods to create Kiviat diagrams
        Max data values are assumed to be 1, so all data must be normalized
        by max data value in dataset.
        '''

#        N = 9
# calculate number of spokes needed
        N = len(self.plotData[self.plotData.keys()[0]][0])
        theta = self.radar_factory(N)

        fig = plt.figure(
#            figsize=(9,9)
            figsize=(8,8)
            )
# adjust spacing around the subplots
        fig.subplots_adjust(
#            wspace=0.25,            
            wspace=0.50,            
#            hspace=0.20, 
            hspace=0.50, 
#            top=0.85, 
            top=0.85, 
#            bottom=0.05
            bottom=0.05
            )
        ''' original
        title_list = [
            'Basecase', 
            'With CO', 
            'With O3', 
            'CO & O3'
            ]
        '''
        
# colors available:
#   b (blue), g (green), r (red), c (cyan), m (magenta), y (yellow), k (black), 
# most of these colors come in light, e.g., lightred, lightblue
        
        params = {
            'font.size' : 12,                   # font size for title
            
            'axes.facecolor' : 'lightyellow',        # color for interior of plots
            'axes.background' : 'blue',        # color of plots background
            'axes.titlesize' : '20',
            
            'xtick.labelsize' : 14,             # font size for labels at ends of spokes
            'xtick.color' : 'black',            # color for radial grid labels
            
            'ytick.labelsize' : 10,             # font size for circular grid numbers
            'ytick.color' : 'magenta',          # color for radial grid numbers
            
            'grid.color' : 'red',               # color of radial grids
            'grid.linewidth' : 0.5,             # linewidth of radial grids
            'grid.linestyle' : ':',            # :=dodtted; '-', '--','|'

            
            'legend.fancybox' : True,   # rounded corners on legend box
            'legend.fontsize' : '10',    # small, medium, large, or use font sizes of 10, 12, etc.
            'legend.shadow' : True,     # shadows the legend box
            }
            
        pylab.rcParams.update(params)

        title_list = plotData.keys()
        title_list.sort()
 
        colors = self.plotOptions_Colors
        
# chemicals range from 0 to 1
        ''' original
        radial_grid = [0.2, 0.4, 0.6, 0.8]
        '''
# grid increments shown on diagram, using grid stepsize(0.1, 0.2,0.5)
        grid_stepsize = 0.1
        grid_stepsize = 0.2
        grid_count = int(1./grid_stepsize)
        radial_grid = []
        for grid in range(grid_count):
# radial_grid cannot contain a zero! All values must be > 0
            if grid == 0: continue
            radial_grid.append(grid * grid_stepsize)
            
        print('\nradial_grid = %s' % radial_grid)
        

# If you don't care about the order, you can loop over data_dict.items()
        for n, title in enumerate(title_list):
            ax = fig.add_subplot(
                2, 
                2, 
                n+1, 
                projection='radar',

                )
            if showGrid:
                plt.rgrids(radial_grid)
            if showTitle:
                ax.set_title(
                    title, 
                    weight='bold', 
#                    size='medium', 
                    size=12, 
#                    position=(0.5, 1.1),
# adjust height of each plot title above plot (1 -> 1.25)
                    position=(0.5, 1.15),
                    horizontalalignment='center', 
                    verticalalignment='center'
                    )
            for d, color in zip(self.plotData[title], colors):
                ax.plot(
                    theta, 
                    d, 
                    color=color,
                    )
                ax.fill(
                    theta, 
                    d, 
                    facecolor=color,
# opacity   (higher is more opaque) , values are from 0 to 1               
#                    alpha=0.25,
                    alpha=0.2,
                    )
# spoke labels
            ax.set_varlabels(
                self.spokeLabels
                )
# add legend relative to top-left plot

        plt.subplot(2,2,1)
        '''
        lenYList = len(title_list)
        if lenYList == 1: 
            plotOptions_SubPlot = 111
            plt.subplot(1,1,1)
            print('plt.subplot(1,1,1)')
        elif lenYList <= 2: 
            plotOptions_SubPlot = 211
            plt.subplot(2,1,1)
            print('plt.subplot(2,1,1)')
        elif lenYList <= 4:
            plotOptions_SubPlot = 221
            plt.subplot(2,2,1)
            print('plt.subplot(2,2,1)')
        elif lenYList <= 6:
            plotOptions_SubPlot = 321
            plt.subplot(3,2,1)
            print('plt.subplot(3,2,1)')
        elif lenYList <= 9:
            plotOptions_SubPlot = 331
            plt.subplot(3,3,1)
            print('plt.subplot(3,3,1)')
        elif lenYList <= 12:
            plotOptions_SubPlot = 431
            plt.subplot(4,3,1)
            print('plt.subplot(4,3,1)')
        elif lenYList <= 16:
            plotOptions_SubPlot = 441
            plt.subplot(4,4,1)
            print('plt.subplot(4,4,1)')
        elif lenYList <= 20:
            plotOptions_SubPlot = 541
            plt.subplot(5,4,1)
            print('plt.subplot(5,4,1)')
        elif lenYList <= 25:
            plotOptions_SubPlot = 551
            plt.subplot(5,5,1)
            print('plt.subplot(5,5,1)')
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
        '''
        
        
        
        labels = self.legendLabels
        print('self.legendLabels = %s' % self.legendLabels)
        '''
        labels = (
            'Factor 1', 
            'Factor 2', 
            'Factor 3', 
            'Factor 4', 
            'Factor 5'
            )
        '''
        
        print('valueLegendLocation = %s' % valueLegendLocation)
        print('valueLegendLabelSpacing = %s' % valueLegendLabelSpacing)
        if showLegend:
            labels = self.legendLabels
            legend = plt.legend(
                labels, 
#                loc=(0.9, .95), 
                loc=(valueLegendLocation[0],valueLegendLocation[1]), 
                labelspacing=valueLegendLabelSpacing,
                )
            plt.setp(
                legend.get_texts(), 
#                fontsize='small'
                )
        if showTitle:
            plt.figtext(
# as measured from lower left corner; all measurements between 0 and 1
                0.50, 
                0.95,  
#                '5-Factor Solution Profiles Across Four Scenarios',
                self.plotTitle,
                ha='center', 
#                color=colorTitle, 
                weight='bold', 
#            size='large'
                size=fontsizeTitle,
                )
        plt.show()
      
# factory function that returns class to the caller
# ... register class as handler for projections of type 'radar' ;
# ... class RadarAxes is implementing a protocol (interface) that is required by register_projection()
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
            return plt.Circle((x0, y0), r)

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
                    labels,
# label distance from plot; x value has no effect for radial plot label; use only the y value (weird!)
# ... good range: 0, 0.025, 0.05, 0.075,  0.10, 0.125, 0.150
                    position=(0.0,0.1)
#                    size=10,
#                    backgroundcolor='red',
                    
                    )

            def _gen_axes_patch(self):
                x0, y0 = (0.5, 0.5)
                r = 0.5
                return self.draw_frame(x0, y0, r)

        register_projection(RadarAxes)
        return theta


if __name__ == '__main__':
    #The following data is from the Denver Aerosol Sources and Health study.
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
    #  4)Inclusion of both gas-phase speciesis present...
    
    plotParams = {
        'showTitle' : True,
        'showLegend' : True,
        'showGrid' : True,
        'colorBackground' : 'lightgray',
        'colorTitle' : 'black',
        'fontsizeTitle' : 'large',
        'fontsizeLabels' : 'small',
        'fontsizeLegend' : 'small',
        'valueLegendLocation' : [1.0, 0.95],    # legend location
        'valueLegendLabelSpacing' : 0.1,        # vertical spacing between legend labels
        }
# plot title       
    plotTitle = '5-FactorSolution Profiles Across Four Scenarious'
# legend labels
    legendLabels = ['Factor 1','Factor 2', 'Factor 3', 'Factor 4', 'Factor 5']
# plot data
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
        'CO & O3': [f1_both, f2_both, f3_both, f4_both, f5_both]
        }
            
    spokeLabels = ['Sulfate', 'Nitrate', 'EC', 'OC1', 'OC2', 'OC3', 'OP', 'CO',
                    'O3']
                    
#    root=Tk()
    root=[]
    
    Kiviat_All(
        True,
        150,
        150,
        1,
        4,
        1,
        plotTitle,
        legendLabels,
        plotData,
        spokeLabels,
        **plotParams
        )
