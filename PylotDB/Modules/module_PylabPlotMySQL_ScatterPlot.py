#! /usr/local/bin/python    # for *nix runs

# filename: polynomial_curve_fit.py

# References:
#  - Matplotlib  User's Guide, p. 79
#  - Matplotlib for Python Developers, PACKT Press

# import following modules
#from pylab import *
import pylab
import matplotlib
from tkMessageBox import *      # dialogs such as askokcancel, showinfo, showerror, etc.
from Tkinter import *               # Tkinter widgets, like Tk()
import math                             # for logarithms and the value for 'e'

# import modules
import module_PlotUtilities

# Debug parameters
DEBUG = 0      # 1 for printout of various parameters and variables in this module

class ScatterPlot():
    def __init__(
        self,
        selfExternal,
        parent,
        keepPreviousPlot,
        xwin,
        ywin,
        colorbg,
        xxDataLists,
        yyDataLists,
        numberOfTableCurves,
        numberOfBufferCurves,
        numberPylabPlotFigure,
# **kwargs 
        showTitle,
        showYLabel,
        showXLabel,
        showLegend,
        showLegendShadow,
        showGrid,
        showReferenceCurve,
        showSlopedStraightLineReferenceCurve,
        showHorizontalStraightLineReferenceCurve,
        showVerticalStraightLineReferenceCurve,
        colorBackground,
        colorXYLabels,
        colorXTicks,
        colorYTicks,
        colorTitle,
        colorPlotBorder,
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
        lineWidthCurveFit,
        numPointsForCurveFit,
        markerSize,
        connectDataPoints,
        polyDegree,
        plotPolyDegree,
        plotAllLesserDegrees,
        numberDecimalPlacesInEqn,  # 0 for integers; otherwise, range is 1 to 10, editable
        formatPolyCoefs,
        ):
        
        selfExternal.MySQL_Output(
            1,
            '\n** In class ScatterPlot in module_PylabPlotMySQL_ScatterPlot'
            )
        
        if DEBUG:
            print('\nHorizontal xlist:')
            print(valuesHorizontalStraightLineRefCurvePlotXList)
            print('\nHorizontal ylist:')
            print(valuesHorizontalStraightLineRefCurvePlotYList)

# reset defaults
        pylab.rcdefaults()
        
# tell pylab which figue we are dealing with; otherwise, defaults to Figure 1, which conflicts with regular x-y plots        
        pylab.figure(
            numberPylabPlotFigure,
            facecolor=colorPlotBorder
            )
# color plot border
#        pylab.figure().patch.set_facecolor(colorPlotBorder)
            
# clear the figure
        if not keepPreviousPlot:
            pylab.clf()

# set plot background color            
        matplotlib.rc('axes', facecolor = colorBackground)
        matplotlib.rc('axes', labelsize = int(fontsizeXYLabels))
        matplotlib.rc('axes', labelcolor = colorXYLabels)
        matplotlib.rc('xtick', labelsize = int(fontsizeXTicks))
        matplotlib.rc('xtick', color = colorXTicks)
        matplotlib.rc('ytick', labelsize = int(fontsizeYTicks))
        matplotlib.rc('ytick', color = colorYTicks)
        
# scatter plot plotting options (4 colors, 4 line styles, and 7 markers = 112 unique plot possibilities);
#  however, since line styles are not used with scatterplots, there are 28 unique plot possibilities
# ... colors: b = blue, g = green, k = black, m = magenta
# ... NOTE: Don't use red here; red is used for polynomial curve fits
        plotOptions_Colors = ['b','g','k','m',]
        
#  ... line style: '-' solid line, '--' dashed line, ':' dotted line, '-.' dash-dot line
# ...  NOTE: these are not used for data plotted with scatterplots!
        plotOptions_LineStyles = ['-','--',':','-.']
        plotOptions_LineStyles = ['--']
        
# ... markers: s = square, o = filled circle, d = diamond, v = down triangle,
#                 ^ = up triangle, < = triangle left, > triangle right
        plotOptions_Markers = ['s','o','d','v','^','<','>']
        
# curve fit plotting options
# ... colors: r = red
        curveFitOptions_Colors = ['r']

# ... line style: '-' solid line, '--' dashed line, ':' dotted line, '-.' dash-dot line
        curveFitOptions_LineStyles = ['-','--',':','-.']
        
# markers: s = square, o = filled circle, d = diamond, v = down triangle,
#             ^ = up triangle, < = triangle left, > triangle right
# NOTE: do not use markers for curve fits, just use solid lines, dashed lines, etc.
        curveFitOptions_Markers = ['s','o','d','v','^','<','>']
        
# form list of plot options for data
        plotOptions = []
        if connectDataPoints:
            for style in plotOptions_LineStyles:
                for color in plotOptions_Colors:
                    for marker in plotOptions_Markers:
                        plotOptions.append(color + style + marker)
        else:
            for color in plotOptions_Colors:
                for marker in plotOptions_Markers:
                    plotOptions.append(color + marker)
# determine total number of options, so that when plotting, we can cycle thru the option using modulo function
        plotOptions_Total = len(plotOptions)
                    
# form list of plot options for curve fit
        curveFitOptions = []
        for style in curveFitOptions_LineStyles:
            for color in curveFitOptions_Colors:
#            for marker in curveFitOptions_Markers:
                curveFitOptions.append(color + style)
 #                   curveFitOptions.append(color + style + marker)
 # determine total number of options so that when plotting we can cycle thru the option using modulo funtion
        curveFitOptions_Total = len(curveFitOptions)

        if DEBUG:
            print('plotOptions = \n%s\n' % plotOptions)   
            print('curveFitOptions = \n%s\n' % curveFitOptions)
                       
# create plots
# ... only one plot
        subplot=111
        self.pylabSubplot = pylab.subplot(subplot)
        
        if DEBUG:
            print('\nxxDataLists from calling program:')
            print(xxDataLists)
            print('\nyyDataLists from calling program:')
            print(yyDataLists)
            print('')
            
# keep track of global values for xMin, yMin, xMax, yMax
        self.xMin_Global = []
        self.xMax_Global = []
        self.yMin_Global = []
        self.yMax_Global = []
    
# plot data; each list of data is plotted with separate markers
        for numberPlot in range(len(yyDataLists)):
# plot based on plotStyle
            plotOptionsIndex = numberPlot%plotOptions_Total
            
            module_PlotUtilities.plotStyleForCurve(
                self,
                pylab,
                plotStyle,
                xxDataLists[numberPlot],
                yyDataLists[numberPlot],
                plotOptions[plotOptionsIndex],
                lineWidthCurveFit,
                markerSize,
                plotBaseX,
                plotBaseY,
                )
                
            module_PlotUtilities.globalMinMaxValues(
                self,
                xxDataLists[numberPlot], 
                yyDataLists[numberPlot]
                )
            
# compute 1-D vectors for both x and y by joining all data together
# ... used for determining polynomial coefficients by calling pylab.polyfit()
        x = []
        y = []
        for i in range(len(xxDataLists)):
            x.extend(xxDataLists[i])
            y.extend(yyDataLists[i])
            
#        print('\n x scatter = %s' % x)
#        print('\n y scatter = %s' % y)
            
# find min and max values for both x and y
        xmax = max(x)
        xmin = min(x)
        
# ... 'bestX' values for later determining 'bestY'
        deltaX = (xmax - xmin)/float(numPointsForCurveFit)
        bestX = []
        for i in range(numPointsForCurveFit + 1):
            if i == 0:
                xtemp = xmin
            else:
                xtemp += deltaX
            bestX.append(xtemp)
            
        if DEBUG:
            print('\nx = %s\n' % x)
            print('\ny = %s\n' % y)
            print('\nlen(x) = %s\n' % len(x))
            print('\nlen(y) = %s\n' % len(y))
            print('\nxmin = %s\n' % xmin)
            print('\nxmax = %s\n' % xmax)
            print('\nbestX = %s\n' % bestX)

# determine bestY best fit for bestX; 
# ... also, string for polynomial equation to be listed in legend
        bestY, stringEqn, stringEqnForLegend = \
                self.dataFit(x,y,bestX,polyDegree,numberDecimalPlacesInEqn,formatPolyCoefs)  
                
# ... parameters stored for use in calling program to place in storage buffer
# ...    initialization
        selfExternal.curvefit_CurveFitEquations_Scatter = []
        selfExternal.curvefit_BestY_Scatter = []
        selfExternal.curvefit_YHeader_Scatter = []
# ...    define values for main curve fit equation
        selfExternal.curvefit_CurveFitEquations_Scatter.append(stringEqnForLegend.lstrip())
        selfExternal.curvefit_BestY_Scatter.append(bestY)
        selfExternal.curvefit_BestX_Scatter = bestX
#        selfExternal.curvefit_YHeader_Scatter.append(valueLabelY)
        selfExternal.curvefit_YHeader_Scatter.append(stringEqnForLegend.lstrip())
        selfExternal.curvefit_XHeader_Scatter = valueLabelX
        selfExternal.curvefit_Title_Scatter = valueTitle

        if DEBUG:
            print('\ncurveFitOptions = \n')
            print(curveFitOptions)
            print()
            
# plot polynomial curve fit
        if plotPolyDegree:
        
            valuesLegendLabels.append(stringEqnForLegend)
            
            module_PlotUtilities.plotStyleForCurve(
                self,
                pylab,
                plotStyle,
                bestX,
                bestY,
                curveFitOptions[0],
                lineWidthCurveFit,
                markerSize,
                plotBaseX,
                plotBaseY,
                )

            module_PlotUtilities.globalMinMaxValues(self,bestX,bestY)
                
# fit all lesser degrees
            if (plotAllLesserDegrees) and (polyDegree > 1):
                optionsIndex = 0
                for i in range(polyDegree - 1,0,-1):
                    bestY, stringEqn, stringEqnForLegend = \
                            self.dataFit(x,y,bestX,i,numberDecimalPlacesInEqn,formatPolyCoefs)
                    if DEBUG:
                        print('For polynomial of degree %s: %s' % (i,stringEqn))
# ... store for use in calling program; strip leading white space
                    selfExternal.curvefit_CurveFitEquations_Scatter.append(stringEqnForLegend.lstrip())
                    selfExternal.curvefit_BestY_Scatter.append(bestY)
                    selfExternal.curvefit_YHeader_Scatter.append(stringEqnForLegend.lstrip())
# ... define options index
                    optionsIndex += 1
# ... cycle thru the values using the modulo operator
                    curveFitOptionsIndex = optionsIndex%curveFitOptions_Total
                    valuesLegendLabels.append(stringEqnForLegend)
                    
                    module_PlotUtilities.plotStyleForCurve(
                        self,
                        pylab,
                        plotStyle,
                        bestX,
                        bestY,
                        curveFitOptions[curveFitOptionsIndex],
                        lineWidthCurveFit,
                        markerSize,
                        plotBaseX,
                        plotBaseY,
                        )
                        
                    module_PlotUtilities.globalMinMaxValues(self,bestX,bestY)                    
                    
# reference plot, if desired
        if showReferenceCurve:
            valuesLegendLabels.append(
                str(valueRefCurveMultiplier) + ' * (' + valueRefCurveLabel +
                ') [ref]'
                )
            stringInvalidMultiplier = (
                'Unable to plot reference curve:' + '\n'
                '  Invalid value for reference curve multiplier.\n' +
                '  Multiplier must be a string representing either\n' +
                '  an integer, float, or fraction (e.g., 1/5).\n' 
                )
# change multiplier to decimal
            tempMult = valueRefCurveMultiplier
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
# ... plot X and Y lists
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
                lineWidthCurveFit,
                markerSize,
                plotBaseX,
                plotBaseY,
                )
                
            module_PlotUtilities.globalMinMaxValues(
                self,
                plot_X_RefCurve,
                plot_Y_RefCurve
                )
                
# sloped straight-line reference curve, if desired
        if showSlopedStraightLineReferenceCurve:
            valuesLegendLabels.append(
                valueSlopedStraightLineRefCurveLabel
                )
                
# ... no need to error check; validation done in "SCATTER PLOT SPECS" window     
            module_PlotUtilities.plotStyleForCurve(
                self,
                pylab,
                plotStyle,
                valuesSlopedStraightLineRefCurvePlotXList,
                valuesSlopedStraightLineRefCurvePlotYList,
                'r--s',
                lineWidthCurveFit,
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
            valuesLegendLabels.append(
                valueHorizontalStraightLineRefCurveLabel
                )
                
# ... no need to error check; validation done in "SCATTER PLOT SPECS" window   
            module_PlotUtilities.plotStyleForCurve(
                self,
                pylab,
                plotStyle,
                valuesHorizontalStraightLineRefCurvePlotXList,
                valuesHorizontalStraightLineRefCurvePlotYList,
                'r--s',
                lineWidthCurveFit,
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
            valuesLegendLabels.append(
                valueVerticalStraightLineRefCurveLabel
                )

# ... no need to error check; validation done in "SCATTER PLOT SPECS" window  
            module_PlotUtilities.plotStyleForCurve(
                self,
                pylab,
                plotStyle,
                valuesVerticalStraightLineRefCurvePlotXList,
                valuesVerticalStraightLineRefCurvePlotYList,
                'r--s',
                lineWidthCurveFit,
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
        if showLegend:
            if DEBUG:
                print '\n====\nvaluesLegendLabels:\n',valuesLegendLabels
                
# legend labels
            stringLegendLabels = []
#            lenLabels = len(self.plot_Labels)
            lenLabels = len(valuesLegendLabels)
#            for label in self.plot_Labels:
            for label in valuesLegendLabels:
                stringLegendLabels.append(label)
                    
# title (fontsize specified in rcparams)
        if showTitle:
            pylab.title(
                valueTitle, 
                color=colorTitle,
                size=fontsizeTitle,
                )

# y label (fontsize specified in rcparams)
        if showYLabel:
            pylab.ylabel(
                valueLabelY,
                color=colorXYLabels,
                size=fontsizeXYLabels,
                )
 
# x label (fontsize specified in rcparams)
        if showXLabel:
            pylab.xlabel(
                valueLabelX,
                color=colorXYLabels,
                size=fontsizeXYLabels,
                )

# legend
        if showLegend:
            pylab.legend(
                stringLegendLabels,
                prop={'size':fontsizeLegend},
                loc=valueLegendLocation,
                shadow=showLegendShadow,
                )
                
# if any plots have base 'e', form new labels; 
# ... pass in all min-max data
        if DEBUG:
            print('\nself.xMin_Global:')
            print(self.xMin_Global)
            print('\nself.xMax_Global:')
            print(self.xMax_Global)
            print('\nself.yMin_Global:')
            print(self.yMin_Global)
            print('\nself.yMax_Global:')
            print(self.yMax_Global)
            print('')
            
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
                        
# grid
        if showGrid:
            pylab.grid(showGrid)
        
# finally, plot it
        pylab.show()
     
        return
        

    def dataFit(self,x,y,bestX,polyDegree,numberDecimalPlacesInEqn,formatPolyCoefs):
        '''
        Purpose:
            1. determine coefficients for fitting polynomial of degree 'polyDegree'
            2. determine format string for listing resulting polynomial equation in legend
                
        Input:
            bestX - x values determined by user
            polyDegree - highest degree of desired polynomial to be determined
            numberDecimalPlacesInEqn - number of decimal places for coefficients to be displayed in legend
            formatPolyCoefs - format of coefficients in legend, whether floating point, fixed decimal, etc
                
        Output:
            stringEqn - string of polynomial equation as it will be shown in legend
            bestY - y values corresponding to bestX x values as determined by polynomial equation determined here
        '''
# determine coefficients for polynomial that fits y vs x
# ... coeffs is a list of polynomial coefficents from highest power to lowest 
        coeffs = pylab.polyfit(x,y,polyDegree)
        lenCoeffs = len(coeffs)
            
        if DEBUG:
            print('coeffs = %s' % coeffs)
# define output as:
# ... formatPolyCoefs =
# ... f - floating_decimal
# ... g - floating_decimal/exponent_decimal (depends on magnitude of number)
# ... e - floating-point exponent
# ... i  - integer (won't be used in this module)

# format output string for polynomial equation that goes in legend
# ... if first power is greater than 1, no exponent; 
# ... same for last power before constant
# ... constant has no power associated with it
# ... so 3 formats are required for a proper polynomial equation to be expressed
        stringOutputFormatWithExponent= '%.' + str(numberDecimalPlacesInEqn) + formatPolyCoefs + '*X**%d '
        stringOutputFormatWithExponentForFirstPower = '%.' + str(numberDecimalPlacesInEqn) + formatPolyCoefs + '*X '
        stringOutputFormatConstant = '%.' + str(numberDecimalPlacesInEqn) + formatPolyCoefs
        stringEqn = ''
# ... if highest power has a positive coefficient, no + sign is used before it
        for exponent in range(lenCoeffs -1,-1,-1):      
            if exponent >= 2: 
# will need different format statement than that for other exponents
                coeff = coeffs[len(coeffs) - exponent - 1]
#        if len(coeffs) > 2:
                if exponent < lenCoeffs - 1:
# strings generated here are concatenated to previous string
                    if coeff < 0:
                        stringEqn += ('- ' + stringOutputFormatWithExponent % (abs(coeff), exponent))
                    else:
                        stringEqn += ('+ ' + stringOutputFormatWithExponent % (abs(coeff), exponent))               
                elif exponent == lenCoeffs -1:
# first number of the equation, so '+' sign not needed, '-' sign needs a space in front
                    coeff = coeffs[0]
                    if coeff < 0:
                        stringEqn += (' - ' + stringOutputFormatWithExponent % (abs(coeff), exponent))
                    else:
                        stringEqn += (stringOutputFormatWithExponent % (abs(coeff), exponent))
                
            if exponent == 1: 
# will need different format statement than that for the higher exponents or the last exponent == 0
                coeff = coeffs[len(coeffs) - exponent - 1]
#        if len(coeffs) > 2:
                if exponent < lenCoeffs - 1:
# strings generated here are concatenated to previous string
                    if coeff < 0:
                        stringEqn += ('- ' + stringOutputFormatWithExponentForFirstPower % abs(coeff))
                    else:
                        stringEqn += ('+ ' + stringOutputFormatWithExponentForFirstPower % abs(coeff))               
                elif exponent == lenCoeffs -1:
# first number of the equation, so '+' sign not needed, '-' sign needs a space in front
                    coeff = coeffs[0]
                    if coeff < 0:
                        stringEqn += (' - ' + stringOutputFormatWithExponentForFirstPower % abs(coeff))
                    else:
                        stringEqn += (stringOutputFormatWithExponentForFirstPower % abs(coeff))
            
            elif exponent == 0:
                coeff0 = coeffs[len(coeffs) - 1]
                if exponent < lenCoeffs - 1:
# strings generated here are concatenated to previous string
                    if coeff0 < 0:
#               stringEqn += '- ' + str(abs(coeff0))
#            stringEqn += ('- %.3f' % abs(coeff0))
                        stringEqn += ('- ' + stringOutputFormatConstant % abs(coeff0))
                    else:
#            stringEqn += '+ ' + str(coeff0)
                        stringEqn += ('+ ' + stringOutputFormatConstant % coeff0)
                else:
# first number of the equation, so '+' sign not needed, '-' sign needs a space in front
                    if coeff0 < 0:
                        stringEqn += (' - ' + stringOutputFormatConstant % abs(coeff0))
                    else:
                        stringEqn += (stringOutputFormatConstant % abs(coeff0))

# determine if equation needs to be split into two lines
            numberOfTerms = stringEqn.count('+ ') + stringEqn.count('- ')
            firstTermIsPositive = False
            if stringEqn[0:2] <> ' -':
# if positive, first term will not have a '+' sign
                firstTermIsPositive = True
                numberOfTerms += 1
                
            if DEBUG:
                print('Eqn: "%s"' % stringEqn)
                print('Number of terms in equation = %s' % numberOfTerms)
                
                
# OPTION - SHORTEN EQUATION FOR LEGEND USE
# ... optional logic -- change as desired
            stringChange1 = stringEqn.replace('**','^')
            stringChange2 = stringChange1.replace('*','')
            stringEqnShortForm = stringChange2
            
                
# OPTION - SPLIT LONG EQUATION INTO LINES
# ... logic left here, but not used at present
                
# if more than 3 terms, split equation into two lines to make legend smaller in width
# ... if 3 or less terms, leave as is     
            stringEqnForLegend = ''
            if numberOfTerms <= 3:
                stringEqnForLegend = stringEqn
            elif numberOfTerms == 4:
# 3rd order polynomial
# layout: 1 + 2
#              + 3 + 4
                stringEqnSplit = stringEqn.split(' ')
                if firstTermIsPositive:
                    stringEqnForLegend = ' '.join(stringEqnSplit[0:3]) + '\n' + '    ' + ' '.join(stringEqnSplit[3:7])
                else:
                    stringEqnForLegend = ' '.join(stringEqnSplit[0:4]) + '\n' + '    ' + ' '.join(stringEqnSplit[4:8])
            elif numberOfTerms == 5:
# 4th order polynomial
# layout: 1 + 2 + 3
#              + 4 + 5
                stringEqnSplit = stringEqn.split(' ')
                if firstTermIsPositive:
                    stringEqnForLegend = ' '.join(stringEqnSplit[0:5]) + '\n' + '    ' + ' '.join(stringEqnSplit[5:9])
                else:
                    stringEqnForLegend = ' '.join(stringEqnSplit[0:6]) + '\n' + '    ' + ' '.join(stringEqnSplit[6:10])
            elif numberOfTerms == 6:
# 5th order polynomial
# layout: 1 + 2 + 3
#              + 4 + 5 + 6
                stringEqnSplit = stringEqn.split(' ')
                if firstTermIsPositive:
                    stringEqnForLegend = ' '.join(stringEqnSplit[0:5]) + '\n' + '    ' + ' '.join(stringEqnSplit[5:11]) 
                else:
                    stringEqnForLegend = ' '.join(stringEqnSplit[0:6]) + '\n' + '    ' + ' '.join(stringEqnSplit[6:12]) 
            else:
                stringWrongPolynomialOrder = (
                    'Degree of polynomial is outside the range expected.\n\n' +
                    'Range expected: 1st to 5th order \n' +
                    'Current order: %s\n\n' +
                    'This is a coding error.\n\n' +
                    'Please inform code administrator of this error.'
                    ) % (numberOfTerms -1 )
                print(stringWrongPolynomialOrder)
                showerror(
                    'Error: wrong polynomial order',
                    stringWrongPolynomialOrder
                    )
                return
                
# determine coefficients of polynomial for curve fit            
# ... use coefficients and bestX to determine bestY         
        bestY = pylab.polyval(coeffs, bestX)

# using multi-line stringEqnForLegend messes up legend -- too bad;
#     would be nice to have multi-line legend descriptions;
#     leave here in case situation improves in the future
#        return (bestY, stringEqn, stringEqnForLegend)
# ... if want to use same string for legend 
#        return (bestY, stringEqn, stringEqn)
# ... if want to use short form of equation for legend
        return(bestY,stringEqn,stringEqnShortForm)
        

def pylabCloseAll():
    '''
    Purpose:
        close all plot windows; called externally
            
    Called by:
        
        
    Calls:
        
        
    '''
    stringCloseAll = (
        '-- WARNING! --\n\n' +
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
            