# Filename: module_codeinserts_Header.py
# Author: dwbarne
# Creation date: Thu, 10-10-2008

# Purpose:
"""
plot utilities common to X-Y and Scatter plot modules
"""

import math

# Globals
DEBUG = 0       # set to 1 to print variables for debugging
 
def globalMinMaxValues(self, xList, yList):
    '''
    Purpose:
        to determine min and max values of lists passed in
    '''
    self.xMin_Global.append(min(xList))
    self.xMax_Global.append(max(xList))
    self.yMin_Global.append(min(yList))
    self.yMax_Global.append(max(yList))
    
    return
    
    
def plotStyleForCurve(
    self,pylab,plotStyle,dataX,dataY,option,lineWidth,markerSize,
    plotBaseX,plotBaseY
    ):
    '''
    Purpose:
    set plot style for curve
    '''
    if plotStyle == 'cartesian':
# set scales
        self.pylabSubplot.set_xscale("linear")
        self.pylabSubplot.set_yscale("linear")  
# form the plot
        pylab.plot(
            dataX,
            dataY,
            option,
            linewidth=lineWidth,
            markersize=markerSize,
            )
            
    elif plotStyle == 'semilogx':
# set y scale
        self.pylabSubplot.set_yscale("linear") 
        
        if plotBaseX == 'e':
            self.pylabSubplot.set_xscale("log", nonposx='clip')
            pylab.semilogx(
                dataX,
                dataY,
                option,
                basex=math.e,
                linewidth=lineWidth,
                markersize=markerSize,
                )
             
        elif plotBaseX == 'log_e':
            self.pylabSubplot.set_xscale("linear")
            pylab.plot(
                [math.log(x) for x in dataX],
                dataY,
                option,
                linewidth=lineWidth,
                markersize=markerSize,
                )
                    
        elif plotBaseX == 'log_10':
            self.pylabSubplot.set_xscale("linear")
            pylab.plot(
                [math.log10(x) for x in dataX],
                dataY,
                option,
                linewidth=lineWidth,
                markersize=markerSize,
                )
                
        else:
# ... basex = some power of 2
            self.pylabSubplot.set_xscale("log", nonposx='clip')
            pylab.semilogx(
                dataX,
                dataY,
                option,
                basex=plotBaseX,
                linewidth=lineWidth,
                markersize=markerSize,
                )

    elif plotStyle == 'semilogy':
# set scales
        self.pylabSubplot.set_xscale("linear")
    
        if plotBaseY == 'e':
# ... basey = 'e'
            self.pylabSubplot.set_yscale("log", nonposy='clip')
            pylab.semilogy(
                dataX,
                dataY,
                option,
                linewidth=lineWidth,
                markersize=markerSize,
                basey=math.e,
                )
            
        elif plotBaseY == 'log_e':
            self.pylabSubplot.set_yscale("linear")
            pylab.plot(
                dataX,
                [math.log(y) for y in dataY],
                option,
                linewidth=lineWidth,
                markersize=markerSize,
                )
                
        elif plotBaseY == 'log_10':
            self.pylabSubplot.set_yscale("linear")
            pylab.plot(
                dataX,
                [math.log10(y) for y in dataY],
                option,
                linewidth=lineWidth,
                markersize=markerSize,
                )
            
        else:
            self.pylabSubplot.set_yscale("log", nonposy='clip')
            pylab.semilogy(
                dataX,
                dataY,
                option,
                linewidth=lineWidth,
                markersize=markerSize,
                basey=plotBaseY,
                )

# ... loglog                    
    elif plotStyle == 'loglog':
    
        if plotBaseX == 'e':
        
            self.pylabSubplot.set_xscale("log", nonposx='clip')
            
            if plotBaseY == 'e':
                self.pylabSubplot.set_yscale("log", nonposy='clip')
                pylab.loglog(
                    dataX,
                    dataY,
                    option,
                    linewidth=lineWidth,
                    markersize=markerSize,
                    basex=math.e,
                    basey=math.e,
                    )
            
            elif plotBaseY == 'log_e':
                self.pylabSubplot.set_yscale("linear")
                pylab.semilogx(
                    dataX,
                    [math.log(y) for y in dataY],
                    option,
                    linewidth=lineWidth,
                    markersize=markerSize,
                    basex=math.e,
                    )
            
            elif plotBaseY == 'log_10':
                self.pylabSubplot.set_yscale("linear")
                pylab.semilogx(
                    dataX,
                    [math.log10(y) for y in dataY],
                    option,
                    linewidth=lineWidth,
                    markersize=markerSize,
                    basex=math.e
                    )
            
            else:
                self.pylabSubplot.set_yscale("log", nonposy='clip')
                pylab.loglog(
                    dataX,
                    dataY,
                    option,
                    linewidth=lineWidth,
                    markersize=markerSize,
                    basex=math.e,
                    basey=plotBaseY,
                    )

        elif plotBaseX == 'log_e':
        
            self.pylabSubplot.set_xscale("linear")
            
            if plotBaseY == 'e':
                self.pylabSubplot.set_yscale("log", nonposy='clip')
                pylab.semilogy(
                    [math.log(x) for x in dataX],
                    dataY,
                    option,
                    linewidth=lineWidth,
                    markersize=markerSize,
                    basey=math.e,
                    )
        
            elif plotBaseY == 'log_e':
                self.pylabSubplot.set_yscale("linear")
                pylab.plot(
                    [math.log(x) for x in dataX],
                    [math.log(y) for y in dataY],
                    option,
                    linewidth=lineWidth,
                    markersize=markerSize,
                    )
            
            elif plotBaseY == 'log_10':
                self.pylabSubplot.set_yscale("linear")
                pylab.plot(
                    [math.log(x) for x in dataX],
                    [math.log10(y) for y in dataY],
                    option,
                    linewidth=lineWidth,
                    markersize=markerSize,
                    )
            
            else:
                self.pylabSubplot.set_yscale("log", nonposy='clip')
                pylab.semilogy(
                    [math.log(x) for x in dataX],
                    dataY,
                    option,
                    linewidth=lineWidth,
                    markersize=markerSize,
                    basey=plotBaseY,
                    )
                                            
        elif plotBaseX == 'log_10':
        
            self.pylabSubplot.set_xscale("linear")
            
            if plotBaseY == 'e':
                self.pylabSubplot.set_yscale("log", nonposy='clip')
                pylab.semilogy(
                    [math.log10(x) for x in dataX],
                    dataY,
                    option,
                    linewidth=lineWidth,
                    markersize=markerSize,
                    basey=math.e,
                    )
            
            elif plotBaseY == 'log_e':
                self.pylabSubplot.set_yscale("linear")
                pylab.plot(
                    [math.log10(x) for x in dataX],
                    [math.log(y) for y in dataY],
                    option,
                    linewidth=lineWidth,
                    markersize=markerSize,
                    )
            
            elif plotBaseY == 'log_10':
                self.pylabSubplot.set_yscale("linear")
                pylab.plot(
                    [math.log10(x) for x in dataX],
                    [math.log10(y) for y in dataY],
                    option,
                    linewidth=lineWidth,
                    markersize=markerSize,
                    )
            
            else:
                self.pylabSubplot.set_yscale("log", nonposy='clip')
                pylab.semilogy(
                    [math.log10(x) for x in dataX],
                    dataY,
                    option,
                    linewidth=lineWidth,
                    markersize=markerSize,
                    basey=plotBaseY,
                    )  

        else:
        
# at this point, all x values will be in terms of some power of 2
            
            self.pylabSubplot.set_xscale("log",nonposy='clip')
            
            if plotBaseY == 'e':
                self.pylabSubplot.set_yscale("log", nonposy='clip')
                pylab.loglog(
                    dataX,
                    dataY,
                    option,
                    linewidth=lineWidth,
                    markersize=markerSize,
                    basex=plotBaseX,
                    basey=math.e,
                    )
        
            elif plotBaseY == 'log_e':
                self.pylabSubplot.set_yscale("linear")
                pylab.semilogx(
                    dataX,
                    [math.log(y) for y in dataY],
                    option,
                    linewidth=lineWidth,
                    markersize=markerSize,
                    basex=plotBaseX
                    )
            
            elif plotBaseY == 'log_10':
                self.pylabSubplot.set_yscale("linear")
                pylab.semilogx(
                    dataX,
                    [math.log10(y) for y in dataY],
                    option,
                    linewidth=lineWidth,
                    markersize=markerSize,
                    basex=plotBaseX
                    )
            
            else:
                pylab.loglog(
                    dataX,
                    dataY,
                    option,
                    linewidth=lineWidth,
                    markersize=markerSize,
                    basex=plotBaseX,
                    basey=plotBaseY,
                    )                     
                
    return
    
    
def formNewXLabels(self,pylab,xMin,xMax,colorXTicks,fontsizeXTicks):
    '''
    Purpose:
        replace default axis labels with new ones
    '''
            
    if DEBUG:
        print('\nxMin = %s' % xMin)
        print('xMax = %s' % xMax)
                
    flagError = 0
    if xMin <=0.:
        flagError = 1
        stringMinError = (
            'Minimum X value is\n\n' +
            '  Xmin = %s\n\n' +
            'It is not possible to plot this value as an exponential.\n\n' +
            'Plotting cannot continue.'
            )
        print('\n' + stringMinError)
        showerror(
            'Error: x value out of range',
            stringMinError,
            )
        return 0
                
# get minimum exponent
    exponentXMin = 0
    if xMin > 0.0 and xMin < 1.0:
        while math.exp(exponentXMin) > xMin:
            if DEBUG:
                print('exponentXMin, xMin = %s, %s' % (exponentXMin, xMin))
            exponentXMin -= 1
    else:
        while math.exp(exponentXMin) <= xMin:
            if DEBUG:
                print('exponentXMin, xMin = %s, %s' % (exponentXMin, xMin))
            exponentXMin += 1
        exponentXMin -= 1
                
# get maximum exponent
    exponentXMax = 0
    if xMax > 0.0 and xMax < 1.0:
        while math.exp(exponentXMax) > xMax:
            if DEBUG:
                print('exponentXMax, xMax = %s, %s' % (exponentXMax, xMax))
            exponentXMax -= 1
    else:
        while math.exp(exponentXMax) <= xMax:
            if DEBUG:
                print('exponentXMax, xMax = %s, %s' % (exponentXMax, xMax))
            exponentXMax += 1
            
# add one more to max value
    exponentXMax += 1
                    
    if DEBUG:
        print('\nFinal:')
        print('  exponentXMin = %s' % exponentXMin)
        print('  exponentXMax = %s' % exponentXMax)
                    
    xticklabels = pylab.getp(pylab.gca(), 'xticklabels')
    pylab.setp(xticklabels,'color',colorXTicks)
    pylab.setp(xticklabels,'fontsize',int(fontsizeXTicks))
    pylab.setp(xticklabels,'fontweight','bold') # does not appear to be functional
            
    if DEBUG:
        print('\nAfter: xticklabels = ')                
        print('*'*50)
        print('')
        for label in xticklabels:
            print('pylab.getp(label) = ')
            print(pylab.getp(label))
            print('\n\n')
        print('\n--end of labels--\n')
            
# form list of labels along x axis
    xtl_temp = []
    for exponent in range(exponentXMin, exponentXMax + 1,1):
        xtl_temp.append('$e^{%s}$' % exponent)
    pylab.setp(pylab.gca(),xticklabels=xtl_temp)
        
    return 1
        
        
def formNewYLabels(self,pylab,yMin,yMax,colorYTicks,fontsizeYTicks):
    '''
    Purpose:
        replace default axis labels with new ones
    '''           
            
    if DEBUG:
        print('\nyMin = %s' % yMin)
        print('yMax = %s' % yMax)
                
    flagError = 0
    if yMin <=0.:
        flagError = 1
        stringMinError = (
            'Minimum Y value is\n\n' +
            '  Ymin = %s\n\n' +
            'It is not possible to plot this value as an exponential.\n\n' +
            'Plotting cannot continue.'
            )
        print('\n' + stringMinError)
        showerror(
        'Error: y value out of range',
            stringMinError,
            )
        return 0
                
# get minimum exponent
    exponentYMin = 0
    if yMin > 0.0 and yMin < 1.0:
        while math.exp(exponentYMin) > yMin:
            if DEBUG:
                print('exponent, yMin = %s, %s' % (exponentYMin, yMin))
            exponentYMin -= 1
    else:
        while math.exp(exponentYMin) <= yMin:
            if DEBUG:
                print('exponentYMin, yMin = %s, %s' % (exponentYMin, yMin))
            exponentYMin += 1
        exponentYMin -= 1
                
# get maximum exponent
    exponentYMax = 0
    if yMax > 0.0 and yMax < 1.0:
        while math.exp(exponentYMax) > yMax:
            if DEBUG:
                print('exponent, yMax = %s, %s' % (exponentYMax, yMax))
            exponentYMax -= 1
    else:
        while math.exp(exponentYMax) <= yMax:
            if DEBUG:
                print('exponentYMax, yMax = %s, %s' % (exponentYMax, yMax))
            exponentYMax += 1
            
# add one more to max value
    exponentYMax += 1
                    
    if DEBUG:
        print('\nFinal:')
        print('  exponentYMin = %s' % exponentYMin)
        print('  exponentYMax = %s' % exponentYMax)
                    
    yticklabels = pylab.getp(pylab.gca(), 'yticklabels')
    pylab.setp(yticklabels,'color',colorYTicks)
    pylab.setp(yticklabels,'fontsize',int(fontsizeYTicks))
    pylab.setp(yticklabels,'fontweight','bold') # does not appear to be functional
            
    if DEBUG:
        print('\nAfter: yticklabels = ')                
        print('*'*50)
        print('')
        for label in yticklabels:
            print('pylab.getp(label) = ')
            print(pylab.getp(label))
            print('\n\n')
        print('\n--end of labels--\n')
            
# form list of labels along x axis
    ytl_temp = []
    for exponent in range(exponentYMin, exponentYMax + 1,1):
        ytl_temp.append('$e^{%s}$' % exponent)
    pylab.setp(pylab.gca(),yticklabels=ytl_temp)
        
    return 1