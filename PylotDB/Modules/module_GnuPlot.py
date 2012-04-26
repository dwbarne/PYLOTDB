#! /usr/local/bin/python     # for *nix runs
# ===== Header =====
# Filename: module_codeinserts_Header.py
# Author: dwbarne
# Creation date: Thu, 10-10-2008

# Purpose:
"""
defs to insert text containing class statement and
constructor, as well as calling the Frame constructor, with all necessary statements

"""

from Tkinter import *
from numpy import *

# If the package has been installed correctly, this should work:
import Gnuplot, Gnuplot.funcutils

def gnuPlot(self,xwin,ywin,shell,colorbg):
    """
    main def called when button
    'Gnu Plot' is pressed
    """
    print '\n** In gnuPlot in module_gnuplot'

    try:
        if self.frameMainGnuPlot:
            print ' frame self.frameMainGnuPlot already exists.'
            print '   A new window will not be opened.'
            return
    except AttributeError:
        print '\n     frame self.frameMainGnuPlot will be created.'
        
    self.shell=shell

# first, construct frame of frames
    self.frame_ToplevelGnuPlot = Toplevel(
        borderwidth=5,
        bg=colorbg,
        )
    self.frame_ToplevelGnuPlot.grid()
    self.frame_ToplevelGnuPlot.title(
        'GnuPlot'
        )

# place the sub_window
    self.frame_ToplevelGnuPlot.geometry(
        '+%d+%d' % (
            xwin, 
            ywin
            )
        )
# insert sub_frames into main frame    
    frame0 = Frame(
        self.frame_ToplevelGnuPlot,
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
        self.frame_ToplevelGnuPlot,
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
        self.frame_ToplevelGnuPlot,
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
        self.frame_ToplevelGnuPlot,
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
        text='GNUPLOT',
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
        
    """
# FRAME 2        
# ... Purpose
    self.labelPurpose = Label(
        frame2,
        text='Purpose of code:',
        justify=LEFT,
        bg='tan',
        )
    self.labelPurpose.grid(
        row=0,
        column=0,
        padx=5,
        pady=5,
        sticky=W,
        )
#    self.varPurpose = StringVar()
#    self.varPurpose.set('')
# set scrollbars
    self.xScrollPurpose = Scrollbar(
        frame2,
        orient=HORIZONTAL,
        )
    self.xScrollPurpose.grid(
        row=2,
        column=0,
        sticky=EW,
        )
    self.yScrollPurpose = Scrollbar(
        frame2,
        orient=VERTICAL,
        )
    self.yScrollPurpose.grid(
        row=1,
        column=1,
        sticky=NS,
        )
        
    self.textHeader_Purpose = Text(
        frame2,
        wrap=NONE,
        height=5,
        width=40,
        xscrollcommand=self.xScrollPurpose.set,
        yscrollcommand=self.yScrollPurpose.set,
        )
    self.textHeader_Purpose.grid(
        row=1,
        column=0,
        padx=2,
        pady=2,
        )
    self.xScrollPurpose.configure(
        command=self.textHeader_Purpose.xview
        )
    self.yScrollPurpose.configure(
        command=self.textHeader_Purpose.yview
        )
    """

        
# FRAME 3:
    buttonInsertHeader = Button(
        frame3,
        text='Plot',
        justify=CENTER,
        bg='darkblue',
        fg='white',
        borderwidth=5,
        relief=RAISED,
        command=demo(self),
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
            self.frame_ToplevelGnuPlot.destroy()
            ),
        )
    buttonCloseInsertHeader.grid(
        row=0,
        column=1,
        padx=5,
        pady=5,
        )
        
# ===== end of handlerHeader =====

# ===== handlerGnuPlot=====

def handlerGnuPlot(self,):
    """
    Purpose:
        print the code necessary to create a header
    """
    print '\n** In handlerPrintCreateHeader'
    print '     you have clicked "Insert code" button'
    
    def insert():
# concatenate strings to form what is needed to insert into code 
# ... first, create empty list
        stringsHeader=[]
        
# ... append all other strings   
        stringsHeader.append(
            '#! /usr/local/bin/python     # for *nix runs\n'
            )            
        stringsHeader.append(
            '# ===== Header =====\n,comment'
            )
        stringsHeader.append(
            '# Filename: ' + self.varFileName.get() + '\n'
            )
        stringsHeader.append(
            '# Author: ' + self.varAuthor.get() + '\n'
            )
        
        stringsHeader.append(
            '# Creation date: ' + self.varCreationDate.get() + '\n'
            )
        stringsHeader.append(
            '\n'
            )
        stringsHeader.append(
            '# Purpose:\n,comment' 
            )
        stringsHeader.append(
            '"""\n'
            )
# lines in Purpose text box            
        linesPurpose = []
        linesPurpose = self.textHeader_Purpose.get(1.0,END).split('\n')
        print ' len(linesPurpose) =',len(linesPurpose)
        
        for lineNum in range(len(linesPurpose) - 1):
            stringsHeader.append(
                linesPurpose[lineNum] + '\n'
                )
        
#        stringsHeader.append(
#            self.textHeader_Purpose.get(1.0,END) + '\n'
#            )

        stringsHeader.append(
            '"""\n' 
            )
        stringsHeader.append(
            '\n'
            )
        stringsHeader.append(
            '\n'
            )
        stringsHeader.append(
            '# >> INSERT: Global Imports <<\n,comment'
            )
        stringsHeader.append(
            '\n'
            )
        stringsHeader.append(
            '\n'
            )
        stringsHeader.append(
            '# >> INSERT: Geometry <<\n,comment'
            )
        stringsHeader.append(
            '\n'
            )
        stringsHeader.append(
            '\n'
            )
        stringsHeader.append(
            '# >> INSERT: Windows or Unix? <<\n,comment'
            )
        stringsHeader.append(
            '\n'
            )
        stringsHeader.append(
            '\n'
            )
            
        self.insertStringsIntoTextBox(
            '1.0',
            stringsHeader
            )
            
    return insert
    
    
    
def demo(self):
    """Demonstrate the Gnuplot package."""

# A straightforward use of gnuplot.  The `debug=1' switch is used
# in these examples so that the commands that are sent to gnuplot
# are also output on stderr.
    def tempDef():
        if self.shell == 'cmd':
            g = Gnuplot.Gnuplot(debug=1)  # ,persist=1)   is not supported under Windows
            g.title('A simple example') # (optional)
            g('set data style linespoints') # give gnuplot an arbitrary command
# Plot a list of (x, y) pairs (tuples or a numpy array would
# also be OK):
            g.plot([[0,1.1], [1,5.8], [2,3.3], [3,4.2]])    
            raw_input('Please press return to continue...\n')
            
        else:
            g = Gnuplot.Gnuplot(debug=1,persist=1)
            g.title('A simple example') # (optional)
            g('set data style linespoints') # give gnuplot an arbitrary command
# Plot a list of (x, y) pairs (tuples or a numpy array would
# also be OK):
            g.plot([[0,1.1], [1,5.8], [2,3.3], [3,4.2]])    
            
    return tempDef

    g.reset()
    # Plot one dataset from an array and one via a gnuplot function;
    # also demonstrate the use of item-specific options:
    x = arange(10, dtype='float_')
    y1 = x**2
    # Notice how this plotitem is created here but used later?  This
    # is convenient if the same dataset has to be plotted multiple
    # times.  It is also more efficient because the data need only be
    # written to a temporary file once.
    d = Gnuplot.Data(x, y1,
                     title='calculated by python',
                     with_='points 3 3')
    g.title('Data can be computed by python or gnuplot')
    g.xlabel('x')
    g.ylabel('x squared')
    # Plot a function alongside the Data PlotItem defined above:
    g.plot(Gnuplot.Func('x**2', title='calculated by gnuplot'), d)
    raw_input('Please press return to continue...\n')

    # Save what we just plotted as a color postscript file.

    # With the enhanced postscript option, it is possible to show `x
    # squared' with a superscript (plus much, much more; see `help set
    # term postscript' in the gnuplot docs).  If your gnuplot doesn't
    # support enhanced mode, set `enhanced=0' below.
    g.ylabel('x^2') # take advantage of enhanced postscript mode
    g.hardcopy('gp_test.ps', enhanced=1, color=1)
    print ('\n******** Saved plot to postscript file "gp_test.ps" ********\n')
    raw_input('Please press return to continue...\n')

    g.reset()
    # Demonstrate a 3-d plot:
    # set up x and y values at which the function will be tabulated:
    x = arange(35)/2.0
    y = arange(30)/10.0 - 1.5
    # Make a 2-d array containing a function of x and y.  First create
    # xm and ym which contain the x and y values in a matrix form that
    # can be `broadcast' into a matrix of the appropriate shape:
    xm = x[:,newaxis]
    ym = y[newaxis,:]
    m = (sin(xm) + 0.1*xm) - ym**2
    g('set parametric')
    g('set data style lines')
    g('set hidden')
    g('set contour base')
    g.title('An example of a surface plot')
    g.xlabel('x')
    g.ylabel('y')
    # The `binary=1' option would cause communication with gnuplot to
    # be in binary format, which is considerably faster and uses less
    # disk space.  (This only works with the splot command due to
    # limitations of gnuplot.)  `binary=1' is the default, but here we
    # disable binary because older versions of gnuplot don't allow
    # binary data.  Change this to `binary=1' (or omit the binary
    # option) to get the advantage of binary format.
    g.splot(Gnuplot.GridData(m,x,y, binary=0))
    raw_input('Please press return to continue...\n')

    # plot another function, but letting GridFunc tabulate its values
    # automatically.  f could also be a lambda or a global function:
    def f(x,y):
        return 1.0 / (1 + 0.01 * x**2 + 0.5 * y**2)

    g.splot(Gnuplot.funcutils.compute_GridData(x,y, f, binary=0))
    raw_input('Please press return to continue...\n')

    # Explicit delete shouldn't be necessary, but if you are having
    # trouble with temporary files being left behind, try uncommenting
    # the following:
    #del g, d


# when executed, just run demo():
if __name__ == '__main__':
    demo()

