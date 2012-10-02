# PylotDB - Job Submission and Analysis Tool
#   author:
#       Daniel W. Barnette, Sandia Labs, Albuquerque, NM, USA
#           email: dwbarne@sandia.gov
#   mentor:
#       John Shipman, New Mexico Tech, Socorro, NM, USA
#           email: john@nmt.edu

# Sandia National Laboratories software license with Open-Source software license
licenseSandia = (
    ' '*25 + 'COPYRIGHT NOTICE AND OPEN SOURCE LICENSE\n' +
    '\n' +
    'Copyright 2012 Sandia Corporation. Under the terms of Contract DE-AC04-94AL85000\n' +
    'with Sandia Corporation, the U.S. Government retains certain rights in this software.\n' +
    '\n' +
    'Redistribution and use in source and binary forms, with or without modification, are permitted\n' +
    'provided that the following conditions are met:\n' +
    '\n' +
    '   * Redistributions of source code must retain the above copyright\n' +
    '     copyright notice, this list of conditions and the following\n' +
    '     disclaimer.\n' +
    '\n' +
    '   * Redistributions in binary form must reproduce the above\n' +
    '     copyright notice, this list of conditions, and the following\n' +
    '     disclaimer in the documentation and/or other materials provided\n' +
    '     with the distribution.\n' +
    '\n' +
    '   * Neither the name of Sandia Corporation nor the names of its\n' +
    '     contributors may be used to endorse or promote products\n' +
    '     derived from this software without specific prior written\n' +
    '     permission.\n' +
    '\n' +
    'THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS\n' +
    '"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT\n' +
    'LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR\n' +
    'A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT\n' +
    'OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,\n' +
    'SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT\n' +
    'LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,\n' +
    'DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY\n' +
    'THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT\n' +
    '(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE\n' +
    'OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n' +
    '\n' +
    'Suggested reference wording for articles:\n' +
    '\n' +
    'D. W. Barnette, "PYLOTDB: A Python-MySQL Framework for Database Management and\n' +
    'Data Analysis," Sandia National Laboratories, Albuquerque, New Mexico, 2012.'
    )

# Globals
# ... DEBUG
DEBUG_FILES_IN_RUNTIME_DIRECTORY = 0    # = 1 print all files in runtime directory
DEBUG_MODULE_PATH = 0                           # = 1 print module path
DEBUG_PRINT_METHOD = 0                          # = 1 print method name PylotDB is in
DEBUG_YOUCLICKEDON = 0                          # = 1 print which widget was clicked

# ... stats
DEBUG_THREAD = 0                                    # = 1 print variables related to tracking thread
THREAD_STATS_PYLOTDB = 1                      # = 1 start thread for PylotDB usage stats info to database

# ... MODULE
MODULE = 'pylotdb.py'

# import standard python modules
import os               # to get environment variables, including username
import subprocess       # to determine if running on windows or unix os
import errno            # for error handling
import time             # for putting date & time on emails; also, current time/date
import sys              # for manipulating Python's runtime environment
import smtplib          # for sending emails
import string           # to cleanup emailTo list
import socket           # for error msg if email server cannot connect
import tkFont           # to specify various fonts
import webbrowser       # for accessing web (pylotdb home page, help page)
import urllib           # for accessing web (pylotdb home page)
import array            # for 'big-endian' or 'little-endian' of platform
import platform         # portable interface to platform information
import time             # for date calculations

# determine python version
versionPython = platform.python_version()

# module search path
if os.name == 'posix':
# NOTE: works for Mac where home directory starts with '/Users/', as well
#      as *nix machines where home directory starts with '/home/'; 
# ... get home dir
    homeDir = os.path.expanduser('~') 	
#    pylotdbHOME = '/home/' + os.environ['USER'] + '/PylotDB'
    pylotdbHOME = os.path.expanduser('~') + '/PylotDB'
    sys.path.append(pylotdbHOME + '/Modules')
    if DEBUG_MODULE_PATH:
        print('...appended ' + pylotdbHOME +'/Modules to path')
elif os.name == 'nt':
    sys.path.append('.\\Modules')
    if DEBUG_MODULE_PATH:
        print('...appended .\\Modules to path')
else:
    showerror(
        'Error: module path',
        'Unable to specify path name to Modules.\n\n' +
        'This is critical for running PylotDB.\n\n' +
        'Contact code administrator for help.',
        )
    sys.exit()
    
# define dictionary of key:paths to modules imported below; if one does
#   not import, ask to install it. 
# NOTE: MySQLdb is only good for Python 2.6 as it now stands, so if another
#   version of Python is installed, user must go look for the appropriate version
    self.dictInstalls = {}
    self.dictInstalls = {
        'pylab' : 'http://matplotlib.sourceforge.net',
        'Tkinter' : 'http://tkinter.unpythonic.net/wiki/How_to_install_Tkinter',
        'Pmw' : 'http://pmw.sourceforge.net',
        'yaml' : 'http://pyyaml.org',
        'MySQLdb' : 'http://sourceforge.net/projects/mysql-python'
        }
    
if DEBUG_MODULE_PATH:
    print('...sys.path = %s,' % sys.path)

# import from my modules
#from checkbutton_2 import CheckButton_2 # called by email_dialog
from email_dialog import *              # module for emailing

# ---------- imports from external modules ----------
stringCannotImport = ''
stringModulesNotImported = []
# Tkinter
try:
    from Tkinter import *       # for widgets
    from tkFileDialog import *  # for 'askopenfilename()', etc related to files
    from tkMessageBox import *  # askokcancel, showinfo, showerror, etc related to general dialog boxes
except:
    stringModulesNotImported.append('Tkinter')
    stringCannotImport += (
        ' - Your Python configuration needs to be changed\n' +
        '   to include the directory that contains Tkinter.py\n' +
        '   in its default module search path. You have probably\n' +
        '   forgotten to define TKPATH in the Modules/Setup file.\n' +
        '   A temporary workaround would be to find that directory\n' +
        '   and add it to your PYTHONPATH environment variable. It\n' +
        '   is the subdirectory named "lib-tk" of the Python library\n' +
        '   directory. (Taken from http://wiki.python.org/moin/TkInter.)\n' +
        '   If this does not work, take a look at "How_to_install_Tkiner" at\n' +
        '     http://tkinter.unpythonic.net/wiki/How_to_install_Tkinter\n\n'
        )
        
# pylab
try:
    import pylab
    print('\nSUCCESS: import pylab\n')
except:
    stringModulesNotImported.append('pylab')
    stringCannotImport += (
        '- Cannot import pylab.\n' +
        '  Check installation of Matplotlib with\n' +
        '  pylab module.\n' +
        '  http://matplotlib.sourceforge.net\n\n'
        )
        
# Pmw
try:
    import Pmw          # for Python Megawidgets
    print('SUCCESS: import Pmw\n')
except:
    stringModulesNotImported.append('Pmw')
    stringCannotImport += (
        '- Cannot import Pmw for Python Megawidgets:\n' + 
        '  http://pmw.sourceforge.net\n\n'
        )
        
# YAML
try:   
    import yaml         # for reading YAML objects
    print ('SUCCESS: import yaml\n')
except:
    stringModulesNotImported.append('yaml')
    stringCannotImport += (
        '- Cannot import yaml for YAML objects:\n' +
        '  http://pyyaml.org\n\n'
        )
        
# MySQLdb
try:
    import MySQLdb      # Python api module for accessing MySQL databases
    print ('SUCCESS: import MySQLdb\n')
except:
    stringCannotImport += (
        '- Cannot import MySQLdb for accessing MySQL databases:\n' +
        '  MySQLdb software is python-version specific, so make sure\n' +
        '  the MySQLdb version you install is compatible with the\n' +
        '  version of Python installed. For Python 2.6 on Windows, go to\n' +
#        '  http://sourceforge.net/projects/mysql-python\n\n'
        '  http://home.netimperia.com/files/misc/MySQL-python-1.2.2.win32-py2.6.exe\n'
        )
    
if stringCannotImport <> '':
    if os.name == 'posix':
        showerror(
            'Error: import problem',
            stringCannotImport +
            'Install missing module(s).',
            )
        sys.exit()
    elif os.name == 'nt':
        if versionPython[0:3] <> '2.6':
            stringCannotImport += (
                '\nIf you have or will install Python2.6 on Windows, and you\n' +
                'have the complete PYLOTDB source code, the missing modules you\n' +
                'need may be located in the directory\n' +
                '  <pylotdb_home_directory>\Installation software for Python 2.6\n' +
                'Note that MySQLdb software is specifically Python dependent.\n' +
                'MySQLdb version for Python releases other than 2.6 can be found\n' +
                'on the internet. It is recommended that you install Python 2.6' +
                'and all the included libraries.\n\n' +
                'If you do not wish to install Python 2.6, look in the following\n' +
                'locations for the correct modules to download:\n' 
                )
        else:
            stringCannotImport += (
                '\nYou are running Python version 2.6.X in Windows. If you have\n' +
                'the complete source code, the missing modules can be found in\n' +
                'the directory\n' +
                '  <pylotdb_home_directory>\Installation software for Python 2.6\n\n' +
                'If not, look in the following locations for missing modules:\n' 
                )
    else:
# os is something other than posix or windows
        stringCannotImport += (
            '\nYou are running Python version %s in *nix. Missing modules may be\n' +
            'found at the following locations:\n'
            ) % (
            versionPython
            )
            
    for keyValue in stringModulesNotImported:
        stringCannotImport += (
            ' %s : %s\n'
            ) % (
            keyValue,
            self.dictInstalls[keyValue]
            )
            
    showerror(
        'Error: import problem',
        stringCannotImport + 
        '\n\n' +
        'PylotDB must exit.'
        )
    sys.exit()
    
# ------- end of external module imports -----

# ===== For HostInfo_Output
prefix = '>$ '

# Define globals

# hide tabs that are not yet used
HIDE_OTHER_TABS = 1     # = 1, hide other tabs not yet used; 
                                    # = 0, show all tabs whether functional or not

# define minimum screen resolution (resolution of 1280 x 960 or higher)
minScreenResolution_Width = 1280
minScreenResolution_Height = 960

# set to 1 for more printout in various parts of the code
DEBUG = 0

#   width and height of main tabbed windows
globalHullWidth = 930
globalHullHeight = 650

#   width and height of external Windows_IO frames
externalFrameHeight = 550
externalFrameWidth = 800

#   main Window placement relative to top left of screen
x_Windows = 325
y_Windows = 40

#   external Windows_IO placement relative to top left of screen
x_Windows_IO = 30
y_Windows_IO = 10

#   background color of each main tabbed window
commonColor = 'tan'
backgroundInfoTab = commonColor
backgroundCvsSvnAccessTab = commonColor

# next line to be  DELETED
backgroundCheckOutTab = commonColor
backgroundCompileTab = commonColor
backgroundSetupTab = commonColor
backgroundRunTab = commonColor
backgroundStatusTab = commonColor
backgroundPostProcessTab = commonColor
backgroundMySQLTab = commonColor

#   background color of the top frame in each main tabbed window
commonColor = 'lightgreen'
backgroundTopFrameInfoTab = commonColor
backgroundTopFrameCvsSvnAccessTab = commonColor
# next line to be DELETED
backgroundTopFrameCheckOutTab = commonColor
backgroundTopFrameCompileTab = commonColor
backgroundTopFrameSetupTab = commonColor
backgroundTopFrameRunTab = commonColor
backgroundTopFrameStatusTab = commonColor
backgroundTopFramePostProcessTab = commonColor
backgroundTopFrameMySQLTab = commonColor

#   background color of the bottom frame in each main tabbed window
commonColor = 'maroon'
backgroundBottomFrameInfoTab = commonColor
backgroundBottomFrameCvsSvnAccessTab = commonColor
# next line to be DELETED
backgroundBottomFrameCheckOutTab = commonColor
backgroundBottomFrameCompileTab = commonColor
backgroundBottomFrameSetupTab = commonColor
backgroundBottomFrameRunTab = commonColor
backgroundBottomFrameStatusTab = commonColor
backgroundBottomFramePostProcessTab = commonColor
backgroundBottomFrameMySQLTab = commonColor

#   background color of COMMANDS window in external Windows_IO
commonColor = 'lightgreen'
backgroundCommandsInfoTabWindows_IO = commonColor
backgroundCommandsCvsSvnAccessTabWindows_IO = commonColor
# next line to be DELETED
backgroundCommandsCheckOutTabWindows_IO = commonColor
backgroundCommandsCompileTabWindows_IO = commonColor
backgroundCommandsSetupTabWindows_IO = commonColor
backgroundCommandsRunTabWindows_IO = commonColor
backgroundCommandsStatusTabWindows_IO = commonColor
backgroundCommandsPostProcessTabWindows_IO = commonColor
backgroundCommandsMySQLTabWindows_IO = commonColor

#   foreground color of COMMANDS window in external Windows_IO
commonColor = 'black'
foregroundCommandsInfoTabWindows_IO = commonColor
foregroundCommandsCvsSvnAccessTabWindows_IO = commonColor
foregroundCommandsCompileTabWindows_IO = commonColor
foregroundCommandsSetupTabWindows_IO = commonColor
foregroundCommandsRunTabWindows_IO = commonColor
foregroundCommandsStatusTabWindows_IO = commonColor
foregroundCommandsPostProcessTabWindows_IO = commonColor
foregroundCommandsMySQLTabWindows_IO = commonColor

#   background color of OUTPUT window in external Windows_IO
commonColor = 'black'
backgroundOutputInfoTabWindows_IO = commonColor
backgroundOutputCvsSvnAccessTabWindows_IO = commonColor
backgroundOutputCompileTabWindows_IO = commonColor
backgroundOutputSetupTabWindows_IO = commonColor
backgroundOutputRunTabWindows_IO = commonColor
backgroundOutputStatusTabWindows_IO = commonColor
backgroundOutputPostProcessTabWindows_IO = commonColor
backgroundOutputMySQLTabWindows_IO = commonColor

#   foreground color of OUTPUT window in external Windows_IO
commonColor = 'green'
foregroundOutputInfoTabWindows_IO = commonColor
foregroundOutputCvsSvnAccessTabWindows_IO = commonColor
foregroundOutputCompileTabWindows_IO = commonColor
foregroundOutputSetupTabWindows_IO = commonColor
foregroundOutputRunTabWindows_IO = commonColor
foregroundOutputStatusTabWindows_IO = commonColor
foregroundOutputPostProcessTabWindows_IO = commonColor
foregroundOutputMySQLTabWindows_IO = commonColor

#   insert background color of OUTPUT window in external Windows_IO
commonColor = 'green'
insertbackgroundOutputInfoTabWindows_IO = commonColor
insertbackgroundOutputCvsSvnAccessTabWindows_IO = commonColor
insertbackgroundOutputCompileTabWindows_IO = commonColor
insertbackgroundOutputSetupTabWindows_IO = commonColor
insertbackgroundOutputRunTabWindows_IO = commonColor
insertbackgroundOutputStatusTabWindows_IO = commonColor
insertbackgroundOutputPostProcessTabWindows_IO = commonColor
insertbackgroundOutputMySQLTabWindows_IO = commonColor

#   background color of Windows_IO frames containing text boxes
commonColor = 'darkgray'
backgroundInfoTabWindows_IO = commonColor
backgroundCvsSvnAccessTabWindows_IO = commonColor
backgroundCompileTabWindows_IO = commonColor
backgroundSetupTabWindows_IO = commonColor
backgroundRunTabWindows_IO = commonColor
backgroundStatusTabWindows_IO = commonColor
backgroundPostProcessTabWindows_IO = commonColor
backgroundMySQLTabWindows_IO = commonColor

# ----- end of Define globals -----


# import pylotdb_commands module for issuing commands from within pylotdb
#from pylotdb_commands import *

    
class PylotDB(Frame):        
    def __init__(self, master=None,parent=None):
    
        self.msgPylotDBVersion='1.0'
        
# print Welcome msg
        print '\n\n **** Welcome to PylotDB ****'
        
        stringErrorNoDisplay = (
            '\n>> NOTE FOR THOSE RUNNING PylotDB FROM A REMOTE MACHINE <<\n' +
            '\nIf an error occurs just after this message during PylotDB startup\n' +
            'on a remote machine, it is probably due to the fact that\n' + 
            ' 1. the DISPLAY environment variable on the local machine has not\n' +
            '    been set (see below for fix),\n' +
            ' 2. and/or a local X server is not running (see below for fix)\n\n' +
            '  For Windows, the display variable is set by entering the following\n\n' +
            'command in the command/terminal window before logging in to the\n' +
            'remote machine:\n' +
            '   C:\\....> set DISPLAY=localhost:0.0\n' +
            'For *nix:\n' +
            '   ...$ export DISPLAY=localhost:0.0\n' +
            'Also, for Windows an X server must be running. Xming, for example, is\n' +
            'known to run well on Windows and is easy to install and launch. Go to\n' +
            '   http://sourceforge.net/projects/xming/\n' +
            'to download.\n' +
            '  Once the DISPLAY variable is set and an X server is running, try again.\n\n'
            )
        print(stringErrorNoDisplay)
        
# call Frame constructor; we will need it
        Frame.__init__(self, parent)
            
        if subprocess.mswindows:
#    Requires install of Python windows extensions from
#        https://sourceforge.net/project/platformdownload.php?group_id=78018
#    which includes win32file and win32pipe    
            self.shell = 'cmd'
            self.newLine = '\n'
            self.os_message='(Windows)'
        else:  
            self.shell = 'sh'
            self.newLine = '\n'
            self.os_message='(Unix/Linux/Other)'
# define rows and columns
        self.colMin=0
#        self.colMax=12
        self.colMax=5
        self.rowMin=0
#        self.rowMax=19
        self.rowMax=2
        self.colHalf=(self.colMax - self.colMin)/2
        if self.colHalf < 1:
            self.colHalf = 1
# define main Frame
        self.grid(
            row=0,
            column=0,
            sticky=N+S+E+W, 
            padx=10,
            pady=10,
            ipadx=5,
            ipady=5,
            )

# get system info for this machine
        self.infoSystem_PylotDB()

# define data font
        self.dataFont = tkFont.Font(
            family="Arial",
            size="8"
            )
# define data font BOLD
        self.dataFontBold = tkFont.Font(
            family='Arial',
            size="8",
            weight='bold'
            )
# define button font
        self.buttonFont = tkFont.Font( 
            family="Helvetica",
#            size="6" 
            size="8" 
            )
# define entry font			
        self.entryFont = tkFont.Font( 
#                           family="lucidatypewriter",
            family="arial",
            size="12" 
            )
# define title font 
        self.titleFont = tkFont.Font(
            family='arial',
            size='8',
            weight='bold'
            )
# define title font big
        self.titleFontBig = tkFont.Font(
            family='arial',
            size='10',
            )
# define title font big bold
        self.titleFontBigBold = tkFont.Font(
            family='arial',
            size='10',
            weight='bold'
            )
# define 'quit' button font
        self.buttonQuitFont = tkFont.Font( 
            family='helvetica',
            size='6',
            )
# define 'clear' button font
        self.buttonClearFont = tkFont.Font(
            family='helvetica',
            size=6,
            )

# determine current source and executable files in the run-time directory
        self.filesInRunTimeDirectory()
#
        self.createWidgets()

# bring main window to top, ready for user selection        
        self.focus_set()
        
# Window Location
# Window location offset - used to slightly correct redisplaying a window to its prior location
#     since rootx and root y define the window as the upper left corner of the window without the
#     title bar, but windows manager re-displays the window according to the far upper left corner 
#     of the title bar. Hence, re-display is always offset the height of the title bar, causing the window
#     to creep downwards each time it is displayed. The offset value helps to mitigate or, if set to the 
#     precise height of the title bar, prevent this.
        self.offsetWindowX = 8
        self.offsetWindowY = 30

        self.windowEmailPylotDBProblems_xWindowLocation = 10
        self.windowEmailPylotDBProblems_yWindowLocation = 30
        
        return
        
        
# ===========================================#        
        
    def createWidgets(self):
        '''
        Purpose:
        main method for creating PylotDB's widgets
        '''
        
# make parent window expandable
        top=self.winfo_toplevel()
        
        top.rowconfigure(0,weight=1)
        top.columnconfigure(0,weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        
# place window
        top.geometry(
            '+%d+%d' % (x_Windows, y_Windows)
            )
            
# invoke Python MegaWidgets and start building tabs
        self.notebook=Pmw.NoteBook(self,
# can't use 'raisecommand' here since some methods have yet to be defined.
# use .configure after methods have been defined
#            raisecommand=self.linkSelectedTab_To_WindowsIOButton,
            borderwidth=3,
            )
        self.notebook.grid(
            row=0,
            column=0,
            sticky=N+S+E+W,
            )
            
# Setup external Input/Output Windows
        self.externalWindows_IO()
        
# now that the main window is shown, check for proper screen resolution.
# For PylotDB to display properly, the minimum screen resolution must be 1280x960
        currentScreenResolution_Width = int(top.winfo_screenwidth())
        currentScreenResolution_Height = int(top.winfo_screenheight())

# build each tab
        self.infoTab = self.buildInfo(
            currentScreenResolution_Width,
            currentScreenResolution_Height
            )
# ---------
# implement these tabs as time permits
        if HIDE_OTHER_TABS:
            pass
        else:
            self.cvssvnaccessTab = self.buildCvsSvnAccess()
            self.compileTab = self.buildCompile()
            self.setupTab = self.buildSetup()
            self.runTab = self.buildRun()
            self.statusTab = self.buildStatus()
            self.postprocessTab = self.buildPostProcess()
# ---------
        self.mysqlTab = self.buildMySQL()
        
#   setnaturalsize
        self.notebook.setnaturalsize(pageNames=None)
        self.notebook.recolorborders()
        
# Setup external Input/Output Windows
#        self.externalWindows_IO()
       

# link selected Tabs to Windows_IO Buttons
        self.notebook.configure(
            raisecommand=self.linkSelectedTab_To_WindowsIOButton
            )
        
        print(
            '\nCurrent screen resolution set to %s x %s.\n' +
            'Minimum screen resolution for proper display is %s x %s.' 
            ) % (
            currentScreenResolution_Width,
            currentScreenResolution_Height,
            minScreenResolution_Width,
            minScreenResolution_Height,
            )

        if currentScreenResolution_Width < minScreenResolution_Width \
        or \
        currentScreenResolution_Height < minScreenResolution_Height \
        :
            print(
                '\n\nScreen resolution needs to be at least %s x %s\n' +
                'for PylotDB to display correctly.\n' 
                ) % ( 
                str(minScreenResolution_Width), 
                str(minScreenResolution_Height)
                )
                
            self.displayScreenResolution(
                minScreenResolution_Width,
                minScreenResolution_Height,
                currentScreenResolution_Width,
                currentScreenResolution_Height)        
        
        return
        
        
    def displayScreenResolution(self,
        minWidth,
        minHeight,
        currentWidth,
        currentHeight
        ):
        '''
        Purpose: 
            display current and min screen resolution for PylotDB to display properly,
            if current resolution is not enough. Give user choice to continue (perhaps
            for use with a low-resolution projector) or quit PylotDB so user can set
            screen resolution and re-start PylotDB
        '''
        
        stringScreenResolution = (
            'For PylotDB to display properly, the minimum screen\n' +
            'resolution must be\n\n' +
            '   %s x %s\n\n' +
            'Current screen resolution is set to\n\n' +
            '   %s x %s\n\n' +
            'You can continue running PylotDB at the current screen\n' +
            'resolution by clicking YES, but certain windows will not\n' +
            'display properly.\n\n' +
            'To adjust resolution, click NO. PylotDB will exit. Set screen\n' +
            'resolution to at least the minimum and restart PylotDB.\n\n' +
            'DO YOU WISH TO CONTINUE?'
            ) % (
            minWidth,
            minHeight,
            currentWidth,
            currentHeight
            )
            
        ans=askyesno(
            'Info: screen resolution too low',
            stringScreenResolution,
            parent=self.winfo_toplevel()
            )
        if not ans:
            sys.exit()
            
        return
        

#INFO tab
    def buildInfo(self,screenResolution_Width,screenResolution_Height):
        '''
        Purpose:
        build the INFO tab
        '''
        
        tabInfo = self.notebook.add('HOST INFO')
# define self.frameInfo by calling this method
        self.frameInfoCreate(
            tabInfo,
            '-- HOST INFO TAB and COPYRIGHT NOTICE --'
            )      

# define top, mid, and bottom frames in Main Windows in 
#    which to place widgets 
        self.framesInterior_tabInfo(
            self.frameInfo.interior()
            )
        
# Top frame: INFO
        self.displayInfoHeader(
            self.tabInfo_TopFrame
            )
            
# Middle frame: INFO
        self.labelInfoLineInfoTab(
            self.tabInfo_MiddleFrame,
            screenResolution_Width,
            screenResolution_Height
            )
        
        self.frameInfo.reposition()
#        self.frameInfo.update_idletasks()
        
        return tabInfo
        
        
#CVS/SVN ACCESS tab
    def buildCvsSvnAccess(self):
        '''
        Purpose:
        build the CHECK-IN tab
        '''
        
        tabCvsSvnAccess=self.notebook.add('CVS/SVN ACCESS')
        
# Create the ScrolledFrame
        self.frameCvsSvnAccessCreate(
            tabCvsSvnAccess,
            '-- CVS/SVN ACCESS TAB --'
            )
    
# define top and bottom frames in which to place widgets    
        self.framesInterior_tabCvsSvnAccess(
            self.frameCvsSvnAccess.interior()
            )            
        self.frameCvsSvnAccess.reposition()
            
# Top frame: 
#   common header
        self.displayHeader(
            self.tabCvsSvnAccess_TopFrame,
            backgroundTopFrameCvsSvnAccessTab
            )
        
# Bottom frame:
#   checkin/checkout cvs files
        self.framesCvsSvnAccessTab(
            self.tabCvsSvnAccess_BottomFrame
            )
            
        return tabCvsSvnAccess
        

#COMPILE tab
    def buildCompile(self):
        '''
        Purpose:
        build the COMPILE tab
        '''
        
        tabCompile = self.notebook.add('COMPILE')

  # Create the ScrolledFrame
        self.frameCompileCreate(
        tabCompile,
        '-- COMPILE TAB --'
        )

        
# define top, mid, and bottom frames in Main Windows in 
#      which to place widgets    
        self.framesInterior_tabCompile(
            self.frameCompile.interior()
            )
        self.frameCompile.reposition()

# Top frame: COMPILE
  #   common header
        self.displayHeader(
            self.tabCompile_TopFrame,
            backgroundTopFrameCompileTab
            )

# Bottom frame: COMPILE
  #   Create COMMAND box with radiobuttons.
        self.boxCommandCompileTab(
            self.tabCompile_MiddleFrame
            )
  #   Create LANGUAGE boxes, depending on COMMAND picks
        self.boxLanguageCompileTab(
            self.tabCompile_MiddleFrame
            )
  #   Create OPTIONS box with radiobuttons, multi-select mode
        self.boxOptionsCompileTab(
            self.tabCompile_MiddleFrame
            )
  #   specify files and directory
        self.boxFilesCompileTab(
            self.tabCompile_MiddleFrame
            )
  #   create OTHER OPTIONS box with entry field and CLEAR button
        self.boxOtherCompileOptionsCompileTab(
            self.tabCompile_MiddleFrame
            )
  #   construct 'compile' and 'kill process' buttons
        self.buttonsCompileKillCompileTab(
            self.tabCompile_MiddleFrame
            )
  #   initialize grids and invoke default values
        self.initializeCompileTab()
              
        self.frameCompile.reposition()
        
        return tabCompile
        
        
    def buildSetup(self):
        '''
        Purpose:
        build the SETUP tab
        '''
        
        tabSetup = self.notebook.add('SETUP')

# Create the ScrolledFrame
        self.frameSetupCreate(
            tabSetup,
            '-- SETUP TAB --'
            )
       
# define top, mid, and bottom frames in which to place widgets 
        self.framesInterior_tabSetup(
            self.frameSetup.interior()
            )
        self.frameSetup.reposition()            

# Top frame:  SETUP         
        self.displayHeader(
            self.tabSetup_TopFrame,
            backgroundTopFrameSetupTab
            )
        
# Bottom frame: SETUP
        self.frameBottom_tabSetup(
            self.tabSetup_BottomFrame
            )

        self.frameSetup.reposition()
        
        
        return tabSetup
        
        
# RUN tab		
    def buildRun(self):
        '''
        Purpose:
            build the RUN tab
        '''
        
        tabRun = self.notebook.add('RUN')
        
# Create the ScrolledFrame
        self.frameRunCreate(
            tabRun,
            '-- RUN TAB --'
            )
        
# define top, mid, and bottom frames in which to place widgets  
        self.framesInterior_tabRun(
            self.frameRun.interior()
            )
        self.frameRun.reposition()            

# Top frame: RUN      
        self.displayHeader(
            self.tabRun_TopFrame,
            backgroundTopFrameRunTab
            )

# Bottom frame: RUN
#   bf: row 0
        self.buttonsHertRunTab(
            self.tabRun_BottomFrame
            )            
            
#   bf: row 1, col 0
        self.boxQueueRunTab(
            self.tabRun_BottomFrame
            )


#   bf: row1, col 1
        self.entryFrameRunTab(
            self.tabRun_BottomFrame
            )
            
#   bf: row 1, col 2
        self.boxFilesRunTab(
            self.tabRun_BottomFrame
            )
            
#   bf: row 2, col 1
        self.buttonsRunKillRunTab(
            self.tabRun_BottomFrame
            )
            
# initialize the RUN tab
        self.initializeRunTab()
            
# DELETE THIS and the method: 
#    Bottom frame: RUN
        '''
        self.frameEntireBottomRunTab(
            self.tabRun_BottomFrame
            )
         '''
       
        self.frameRun.reposition() 

        return tabRun
        

#STATUS tab		
    def buildStatus(self):
        '''
        Purpose:
        build the STATUS tab
        '''
        
        tabStatus = self.notebook.add('STATUS')

# Create the ScrolledFrame
        self.frameStatusCreate(
            tabStatus,
            '-- STATUS TAB --'
            )
        
# define top, mid, and bottom frames in which to place widgets    
        self.framesInterior_tabStatus(
            self.frameStatus.interior(),
            )
        self.frameStatus.reposition()             
       
# Top frame: STATUS
        self.displayHeader(
            self.tabStatus_TopFrame,
            backgroundTopFrameStatusTab
            )

# Bottom frame: STATUS
        self.labelTempStatusTab(
            self.tabStatus_BottomFrame
            )
            


# Bottom Frame: STATUS
        '''
        self.frameEntireBottomStatusTab(
            self.tabStatus_BottomFrame
            )
        '''

        self.frameStatus.reposition()
        
        return tabStatus
        

# POST-PROCESS tab		
    def buildPostProcess(self):
        '''
        Purpose:
        build the POST-PROCESS tab
        '''
        
        tabPostProcess = self.notebook.add('POST-PROCESS')
        
# Create the ScrolledFrame
        self.framePostProcessCreate(
            tabPostProcess,
            '-- POST-PROCESS TAB --'
            )


# define top, mid, and bottom frames in which to place widgets  
        self.framesInterior_tabPostProcess(
            self.framePostProcess.interior()
            )
        self.framePostProcess.reposition()            

# Top frame: POST-PROCESS
        self.displayHeader(
            self.tabPostProcess_TopFrame,
            backgroundTopFramePostProcessTab
            )
        
# Bottom frame: POST-PROCESS
        self.frameBottomPostProcessTab(
            self.tabPostProcess_BottomFrame
            )

        
        self.framePostProcess.reposition() 
        
        return tabPostProcess
        
        
# MySQL tab
    def buildMySQL(self):
        '''
        Purpose:
        build the MySQL ACCESS tab
        '''
        
        tabMySQL=self.notebook.add('MySQL ACCESS')
        
# Create the ScrolledFrame
        self.frameMySQLCreate(
            tabMySQL,
            '-- MySQL ACCESS TAB --'
            )

# define top and bottom frames in which to place widgets    
        self.framesInterior_tabMySQL(
            self.frameMySQL.interior()
            )            
        self.frameMySQL.reposition()
            
# Top frame: MYSQL 
#   common header
        self.displayHeader(
            self.tabMySQL_TopFrame,
            backgroundTopFrameMySQLTab
            )

# Bottom frame: MYSQL
        self.frameBottomMySQLTab(
            self.tabMySQL_BottomFrame
            )
            
        self.frameMySQL.reposition()
       
              
        return tabMySQL


# ----- end of tabs -----


# dummy def
    def ZZ___BUILD_EXTERNAL_WINDOWS_IO():
        pass
        
        return
        
        
# ----- External I/O Windows with buttons -----
    def externalWindows_IO(self):
        '''
        Purpose:
        set up external window with input and output frames
        '''
        
        self.frameCreateTopLevel()
            
        parent=self.frameExternalMainWindows_IO

# create buttons for each windows_IO needed
        self.buttonsExternalWindows_IO(parent)
        
# create 'lock display' button
        self.checkbuttonLockDisplayExternalWindows_IO(parent)
        
# create 'minimize' button
        self.buttonMinimizeExternalWindows_IO(parent)
               
# set up external window with input and output frames
#    frame: host-info windows_io
        self.frameExternalHostInfoWindows_IO(parent)
#    frame: cvs/svn access windows_io   
        self.frameExternalCvsSvnAccessWindows_IO(parent)
#    frame: compile windows_io
        self.frameExternalCompileWindows_IO(parent)
#    frame: setup windows_io
        self.frameExternalSetupWindows_IO(parent)
#    frame: run windows_io
        self.frameExternalRunWindows_IO(parent)
#    frame: status windows_io
        self.frameExternalStatusWindows_IO(parent)
#    frame: postprocess windows_io
        self.frameExternalPostProcessWindows_IO(parent)
#   frame: mysql windows_io
        self.frameExternalMySQLWindows_IO(parent)
        
# Hide all grids...
        self.hideAllGridsWindows_IO()
#   ... and default to show the INFO tab in the main external window
        self.frameHostInfoWindows_IO.grid()
        
        return
                
            
# ----- End of External I/O Windows with buttons ----- 


# =========================================================== #
#     METHODS FOR EACH TAB

# dummy def
    def ZZ___GENERAL_METHODS_FOR_MOST_TABS():
        pass
        
        return
        
        
# ----- System info -----
    def infoSystem_PylotDB(self):
        '''
        Purpose:
            determine system info of host
        '''

# define portable commands first
        try:
            self.processorBitWidth = platform.architecture()[0]
        except:
            self.processorBitWidth = 'UNK'
            
        try:
            self.versionPython = platform.python_version()
        except:
            self.versionPython = 'UNK'
            
        try:
            self.operatingSystem = platform.system()
        except:
            self.operatingSystem = 'UNK'
            
# if windows ...
        if os.name == 'nt':
            try:
                self.userName = os.environ['USERNAME']
            except:
                self.userName = 'UNK'
                
            try:
                self.computerName = os.environ['COMPUTERNAME']
            except:
                self.computerName = 'UNK'
                
#            self.operatingSystem = os.environ['OS']

            try:
                self.processorArchitecture = os.environ['PROCESSOR_ARCHITECTURE']
            except:
                self.processorArchitecture = 'UNK'
                
            try:
                self.processorIdentifier = os.environ['PROCESSOR_IDENTIFIER']
            except:
                self.processorIdentifier = 'UNK'
                
            try:
                self.sessionName = os.environ['SESSIONNAME']
            except:
                self.sessionName = 'UNK'
                
# if unix ...
        elif os.name == 'posix':
            try:
                self.userName = os.environ['USER']
            except:
                self.userName = 'UNK'
                
            try:
                self.computerName = socket.gethostname() 
            except:
                self.computerName = 'UNK'
                
#            self.operatingSystem = '*nix'

            self.processorArchitecture = 'UNK'
                
            self.processorIdentifier = 'UNK'
                
            self.sessionName = 'UNK'
                
# if unknown ...
        else:
        
            try:
                self.userName = os.environ['USER']
            except:
                self.userName = 'UNK'
                
            try:
                self.computerName = os.environ['HOSTNAME']
            except:
                self.computerName = 'UNK'
                
            try:
                self.operatingSystem = os.environ['OS']
            except:
                self.operatingSystem = 'UNK'
                
            try:
                self.processorArchitecture = os.environ['PROCESSOR_ARCHITECTURE']
            except:
                self.processorArchitecture = 'UNK'
                
            try:
                self.processorIdentifier = os.environ['PROCESSOR_IDENTIFIER']
            except:
                self.processorIdentifier = 'UNK'
                
            try:
                self.sessionName = os.environ['SESSIONNAME']
            except:
                self.sessionName = 'UNK'
                
            try:
                self.processorBitWidth = platform.architecture()[0]
            except:
                self.processorBitWidth = 'UNK'
                
            try:
                self.versionPython = platform.python_version()
            except:
                self.versionPython = 'UNK'
                

# just in case the following behaves differently for windows vs. *nix....
#        if subprocess.mswindows:
        self.currentDirectory = os.getcwd().split('\\').pop()
        self.currentDirectoryFullPath = os.getcwd()
#        else:
#            self.currentDirectory=os.getcwd().split('\\').pop()

# print date
#        localDateTime = time.ctime(time.time())
        localDateTime = time.ctime()
        print ' ... Date/Time: ',localDateTime
# print system info
        print(' ... Computer name: %s' % self.computerName)
        print(' ... Username: %s' % self.userName)
#        print ' ... Session name:',self.sessionName
        print(' ... Operating system: %s' % self.operatingSystem)
        print(' ... Processor architecture: %s, %s' % 
            (self.processorArchitecture, self.processorBitWidth)
            )
        print(' ... Processor identifier: %s' % self.processorIdentifier)
        print(' ... Session name: %s' % self.sessionName)
        print(' ... Current directory: %s' % self.currentDirectory)
        print(' ... Python version: %s' % self.versionPython)
# determine if platform is 'bigEndian' or 'littleEndian'
# ... reference: p. 109, O'Reilly's "Python Standard Library"
        self.littleEndian = ord(array.array("i",[1]).tostring()[0])
        if self.littleEndian:
            print(' ... little-endian platform (x86 or x86-64 instruction sets)') # also DEC alpha
        else:
            print(' ... big-endian platform (RISC or CISC instruction sets)')
            
        return
        
        
    def track_MySQL_Access_Usage(self):
        '''
        Purpose:
            track mysql access usage
        '''
        
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'track_MySQL_Access_Usage'
        
        import time
        
        localDateTime = time.ctime()
# days since my arbitrary start date
# ... timeStartDate = (yr, month, day, hr, min, sec, day of week, day of year, daylight savings flag)
# ...       start at Jan 1, 2011, Saturday (day 5), with no DST at this date
        timeStartDate = (2011,1,1,0,0,0,5,1,0)
        timeStartDateSinceEpoch_Seconds = time.mktime(timeStartDate)
        timeNow_Seconds = time.time()
        timeNowSinceStartDate_Days = \
            (timeNow_Seconds - timeStartDateSinceEpoch_Seconds)/3600./24. + 1
            
# send usage to database
        userName = self.userName
        codeName = 'pylotdb'
        versionPython = self.versionPython
        operatingSystem = self.operatingSystem
        dayNumber = int(timeNowSinceStartDate_Days)
        dayOfWeek,month,day,time,year = localDateTime.split()
        hostName = self.computerName
        osName = os.name
# cannot capture following with pylotdb, even tho table structure would take it
        name_first = ''
        name_last = ''
   
# start thread to send PylotDb stats to database
        if THREAD_STATS_PYLOTDB:
            import thread           # for starting threads
            thread.start_new_thread(
                self.threadSendUsage,
# attributes as *args
                (
                userName,
                name_first,
                name_last,
                codeName,
                versionPython,
                operatingSystem,
                osName,
                dayNumber,
                dayOfWeek,
                month,
                day,
                year,
                time,
                hostName,
                self.pylotdb_stats_server_valid,
                self.pylotdb_stats_server_username,
                self.pylotdb_stats_server_password,
                self.pylotdb_stats_server,
                self.pylotdb_stats_server_port,
                self.pylotdb_stats_database,
                self.pylotdb_stats_table,
                )                
                 )

        return

     
    def threadSendUsage(threadName,*vars):
        '''
        Purpose:
        store usage stats in a database table
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'threadSendUsage')
        
        if DEBUG_THREAD:
            print('\nvars = ')
            print(vars)
            
# assign *args to appropriate variables
        userName = vars[0]
        name_first = vars[1]
        name_last = vars[2]
        codeName = vars[3]
        versionPython = vars[4]
        operatingSystem = vars[5]
        osName = vars[6]
        day_Number_since_01jan2011 = vars[7]
        dayOfWeek = vars[8]
        month = vars[9]
        dayOfMonth = vars[10]
        year = vars[11]
        time = vars[12]
        hostName = vars[13]
        pylotdb_stats_server_valid = vars[14]
        pylotdb_stats_server_username = vars[15]
        pylotdb_stats_server_password = vars[16]
        pylotdb_stats_server = vars[17]
        pylotdb_stats_server_port = vars[18]
        pylotdb_stats_database = vars[19]
        pylotdb_stats_table = vars[20]
        
# ... attributes common to servers
        prt=3306

# connect to stats server
        myDbConnection_Track_PylotDB = ''
        if pylotdb_stats_server_valid:
            try:
                myDbConnection_Track_PylotDB = MySQLdb.connect(
                    user=pylotdb_stats_server_username,
                    passwd=pylotdb_stats_server_password,
                    host=pylotdb_stats_server,
                    port=pylotdb_stats_server_port
                    )
            except:
                if DEBUG_THREAD:
                    stringNoConnect = (
                        'Cannot connect to PylotDB stats database due to invalid\n' +
                        'values in the pylotdb.conf file.'
                        )
                    print('\n' + stringNoConnect)
                return        
        else:
# if values are not valid for server, just return and continue;
#   we don't want pylotdb stopped just because we can't capture stats
            if DEBUG_THREAD:
                stringNoConnect = (
                    'Cannot connect to PylotDB stats database due to blank\n' +
                    'or missing values in the pylotdb.conf file.'
                    )
                print('\n' + stringNoConnect)
            return
            
# ... if value is still blank, just return
        if myDbConnection_Track_PylotDB == '':
            stringNoConnect2 = (
                'Cannot connect to PylotDB stats database.\n' +
                ' Value for "myDbConnection_Track_PylotDB" is blank.\n' +
                ' Check "pylotdb_stats..." values in pylotdb_stats.conf'
                )
            print('\n' + stringNoConnect2 + '\n')
            return
            
# ... if we make it this far, connection to stats database and table is good
        stringConnectSuccess = (
            'Connected to PylotDB stats database server: %s'
            ) % (
                pylotdb_stats_server
                )
        print('\n' +stringConnectSuccess)
            
# get a cursor handle for executing SQL commands
        cursorHandleMySQL_Track_PylotDB = myDbConnection_Track_PylotDB.cursor()
# turn on autocommit; else, database will not update when you want
        cursorHandleMySQL_Track_PylotDB.execute("set autocommit = 1")  

# check for stats database; if it does not exist, create it
        statDatabases = []
        try:
            cursorHandleMySQL_Track_PylotDB.execute("SHOW DATABASES")
            statDatabases = cursorHandleMySQL_Track_PylotDB.fetchall() # tuple of tuples
            statDatabases_List = [item[0] for item in statDatabases]
        except:
            stringCannotShowDatabases = (
                'Unable to "SHOW DATABASES" for PylotDB stats.'
                )
            print('\n' + stringCannotShowDatabases)
            myDbConnection_Track_PylotDB.close()
            return
            
        if DEBUG_THREAD:
            print('\nPylotDB statDatabases_List:')
            print(statDatabases_List)
            
        if pylotdb_stats_database not in statDatabases_List:
            stringCreateDatabase = "CREATE DATABASE " + pylotdb_stats_database
            if DEBUG_THREAD:
                print('\nstringCreateDatabase = %s' % stringCreateDatabase)
                print('\npylotdb_stats_database = %s' % pylotdb_stats_database)
                print('\nstatDatabases = ')
                print(statDatabases)
            
            try:
                cursorHandleMySQL_Track_PylotDB.execute(stringCreateDatabase)
            except:
                stringCannotCreateStatsDatabase = (
                    'Unable to create PylotDB stats database\n' +
                    '   %s\n' 
                    ) % (
                        pylotdb_stats_database
                        )
                print('\n' + stringCannotCreateStatsDatabase)
                myDbConnection_Track_PylotDB.close()
                return
# 
            stringSuccess_CreateStatsDatabase = (
                'Created PylotDB stats database: %s'
                ) % (
                pylotdb_stats_database
                )
            print('\n' + stringSuccess_CreateStatsDatabase)
            
# check for stats database table; if it does not exist, create it
        statDatabaseTables = []
        tableStats_DatabaseDotTable = pylotdb_stats_database + '.' + pylotdb_stats_table
        
        try:
            cursorHandleMySQL_Track_PylotDB.execute(
                "SHOW TABLES FROM " + pylotdb_stats_database
                )
            statDatabaseTables = cursorHandleMySQL_Track_PylotDB.fetchall()
            statDatabase_Tables_List = [item[0] for item in statDatabaseTables]
            if DEBUG_THREAD:
                print('\nPylotDB statDatabaseTables =')
                print(statDatabaseTables)
                print('\nPylotDB statDatabase_Tables_List')
                print(statDatabase_Tables_List)
        except:
                stringCannotCreateStatsDatabase = (
                    'Unable to "SHOW TABLES" from PylotDB stats database.' 
                    ) 
                print('\n' + stringCannotCreateStatsDatabase)
                myDbConnection_Track_PylotDB.close()
                return
                
        if pylotdb_stats_table not in statDatabase_Tables_List:
            commandCreateTable = 'CREATE TABLE' + ' ' + tableStats_DatabaseDotTable + ' '
            subCommand = ''
            subCommand += (
                '(' +
                'user char(25) DEFAULT NULL,' +
                'name_first char(255) DEFAULT NULL,' +
                'name_last char(255) DEFAULT NULL,' +
                'code char(25) DEFAULT NULL,' +
                'python_version char(25) DEFAULT NULL,' +
                'os char(25) DEFAULT NULL,' +
                'os_name char(25) DEFAULT NULL,' +
                'day_number_since_01jan2011 int(5) DEFAULT NULL,' +
                'day_of_week char(3) DEFAULT NULL,' +
                'month char(3) DEFAULT NULL,' +
                'day_of_month int(2) DEFAULT NULL,' +
                'year int(6) DEFAULT NULL,' +
                'time char(8) DEFAULT NULL,' +
                'host_name char(25) DEFAULT NULL,' 
                )
# ... field 16: add auto_index field
            subCommand += (
                'auto_index INT(12) NOT NULL AUTO_INCREMENT PRIMARY KEY )' # field 34
                )
# ... put it all together
            commandCreateTable += subCommand
            
            if DEBUG_THREAD:
                print('PylotDB commandCreateTable = \n')
                print(commandCreateTable)
            
            try:
                cursorHandleMySQL_Track_PylotDB.execute(commandCreateTable)
            except:
                stringCannotCreateStatsTable = (
                    'Unable to create PylotDB stats table\n' +
                    '   %s\n' 
                    ) % (
                        pylotdb_stats_table
                        )
                print('\n' + stringCannotCreateStatsTable)
                myDbConnection_Track_PylotDB.close()
                return 

            stringSuccess_CreateStatsTable = (
                'Created PylotDB stats table: %s'
                ) % (
                pylotdb_stats_table
                )
            print('\n' + stringSuccess_CreateStatsTable)

# insert data into database
        if DEBUG_THREAD:
            print('\n>>>>> INSERTing into PylotDB stats table')
        stringInsert = (
            "INSERT INTO " + tableStats_DatabaseDotTable +
            " (user,name_first,name_last,code,python_version,os,os_name," +
            "day_number_since_01jan2011,day_of_week,month,day_of_month,year,time,host_name)" +                      
            " VALUES" +
            " ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"  
            ) % (
            userName,
            name_first,
            name_last,
            codeName,
            versionPython,
            operatingSystem,
            osName,
            day_Number_since_01jan2011,
            dayOfWeek,
            month,
            dayOfMonth,
            year,
            time,
            hostName
            )
            
        if DEBUG_THREAD:
            print('\n' + stringInsert)
            
        try:
            cursorHandleMySQL_Track_PylotDB.execute(
                stringInsert
                )
        except:
            if DEBUG_THREAD:
                currentModule = 'pylotdb.py'
                currentMethod = 'threadSendUsage'
                stringDatabaseProblem = (
                    'For\n\n' +
                    '  Database: %s\n' +
                    '     Table: %s\n\n' +
                    'either\n\n' +
                    '1. The database and/or table specified for usage stats\n' +
                    '   do not exist.\n' +
                    '   Solution: Use PylotDB to create the missing database/table;\n' +
                    '   table structure must match the INSERT statement.\n' +
                    '2. The database INSERT command to insert data into the\n' +
                    '   database is not correct.\n\n' +
                    '   Solution: Check format of INSERT statement.\n\n' +
                    '   Module: %s\n' +
                    '   Method: %s\n\n' +
                    'Correct and try again.'
                    ) % (
                    pylotdb_stats_database,
                    pylotdb_stats_table,
                    currentModule,
                    currentMethod
                    )
                print('\n' + stringDatabaseProblem)   
            return
            
# disconnect from PylotDB stats server
        if DEBUG_THREAD:
            print('\n>>>>> closing PylotDB stats server connection')
            
        print('\nPylotDB stats submitted')
        
        stringFlushPrivileges = (
            'FLUSH PRIVILEGES'
            )
        cursorHandleMySQL_Track_PylotDB.execute(stringFlushPrivileges)
        
        myDbConnection_Track_PylotDB.close()
        
        return         
        
        
# ----- end of System info -----     
        
# ----- Determine files -----
    def filesInRunTimeDirectory(self):
        '''
        Purpose:
            Determine source, executable, and output files
        for later use in Pmw combo boxes in the Compile
        and Run tabs
        
        Important output variables are:
            lists:
                self.listExecutableFiles
                self.listSourceFiles
                self.listOutputFiles
                self.listCompileOutputFiles
                self.listErrorOutputFiles
        '''
        if DEBUG_PRINT_METHOD:
            print '\n ** In ' + MODULE + '/' + 'filesInRunTimeDirectory'
# make sure of current directory
#        os.chdir(self.currentDirectory)
        
# get list of files
        files=os.listdir('.')
        
        self.listSourceFiles=[]
        self.listExecutableFiles=[]
        self.listCompileOutputFiles=[]
        self.listRunTimeOutputFiles=[]
        self.listRunTimeErrorOutputFiles=[]
        
        for file in files:
# get extension of each file
            filenameBase, extensionFile = os.path.splitext(file)
# determine source files (*.c, *.f)
            if extensionFile == '.c' or \
              extensionFile == '.cpp' or \
              extensionFile == '.f' or \
              extensionFile == '.for':
                self.listSourceFiles.append(file)
# determine executable files (*.exe)
            elif extensionFile == '.exe':
                self.listExecutableFiles.append(file)
# determine compile output files (*.Output)
            elif extensionFile == '.Output':
                self.listCompileOutputFiles.append(file)
# determine output files (*.out)
            elif extensionFile == '.out':
                self.listRunTimeOutputFiles.append(file)
# determine Error Output files (*.ErrorOutput)
            elif extensionFile == '.ErrorOutput':
                self.listRunTimeErrorOutputFiles.append(file)
                
        if DEBUG_FILES_IN_RUNTIME_DIRECTORY:
            print '\n ... Source files in directory:'
            for file in self.listSourceFiles:
                print '      ',file
                            
            print '\n ... Executable files in directory:'
            for file in self.listExecutableFiles:
                print '      ',file
            
            print '\n ... Compile Output files in directory:'
            for file in self.listCompileOutputFiles:
                print '      ',file
            
            print '\n ... Output files in directory:'
            for file in self.listRunTimeOutputFiles:
                print '      ', file
                       
            print '\n ... Error Output files in directory:'
            for file in self.listRunTimeErrorOutputFiles:
                print '      ',file

        return
        

# ----- end of Determine files -----


# ----- Header for each tab except INFO -----        
    def displayHeader(self,tab,colorBackGround): 
        '''
        Purpose:
            creates header boxes and buttons for all tabs
        except the INFO tab
        '''
# Help
        self.buttonClearForm=Button(
            tab,
            text="Help",
            bg='white',
            fg='blue',
            font=self.dataFont,
            borderwidth=5,
            width=10,
            justify=CENTER,
            relief=RAISED,
            command=self.handlerButtonHelp
            )
        self.buttonClearForm.grid(
            row=0, 
            column=0, 
            sticky=NW,
            )

# Clear form        
        self.buttonHelp=Button(
            tab,
            text="Clear form",
            bg='white',
            fg='blue',
            font=self.dataFont,
            borderwidth=5,
            justify=CENTER,
            relief=RAISED,
            command=self.handlerButtonClear
            )
        '''
        self.buttonHelp.grid(
            row=0,
            column=0,
            sticky=NE
            )
        '''

# Pylot version       
        newLine = self.newLine
        self.tabLabel_Mid = Label(
            tab, 
            text=' -- PylotDB --' + newLine +
#            'Sandia Job Submission and Database Analysis Tool' + newLine +
            'Database Management and Analysis Tool' + newLine +
            'Version: ' + self.msgPylotDBVersion + newLine +
            'Username: ' + self.userName + newLine +
            'Hostname: ' + self.computerName + ' ' + 
                            self.os_message + newLine + 
            'Working Directory: ' + newLine +
                self.currentDirectory,
            bg='white',
            fg='blue',
            font=self.dataFont,
            borderwidth=5,
            justify=CENTER,
            relief=RIDGE,
            width=50,
            )
        self.tabLabel_Mid.grid(
            row=0,
            column=2,
            rowspan=3,
            columnspan=1,
#            sticky='NEWS',
            sticky='N',
            padx=10,
            pady=0,
            )

# Quit         
        self.buttonQuit=Button(
            tab,
            text="Quit PylotDB",
            bg='white',
            fg='blue',
            font=self.buttonFont,
            borderwidth=5,
            width=10,
            justify=CENTER,
            relief=RAISED,
            command=self.handlerButtonQuit
            )
        self.buttonQuit.grid(
            row=0,
            column=4,
            pady=2,
            sticky='NE'
            )

# Email problems
        newLine = self.newLine
        msgHelp = (
            'Email problems, comments,' + 
            newLine + 'or suggestions to' + 
            newLine + 'pylotdb-help@sandia.gov'
            )
        self.buttonEmailProblems = Button(
            tab, 
            text = msgHelp, 
            bg='white',
            fg='blue',
            font=self.dataFont,
            width=25,
            height=3,
            borderwidth=5,
            justify=CENTER,
			relief=RAISED,
            command=self.handlerButtonEmailPylotDBProblems
            )
        self.buttonEmailProblems.grid(
            row=1,
            column=0, 
            sticky='N',
            pady=5
            )

# Save-state file label and button
# get all files and directories in current directory
        files=os.listdir('.')
#        print "All files:",files
#?        self.entrySaveStateFileNameVar=StringVar()
    # filter out directories, then all files without a ".sav" extension
        self.filelistExt=[]
        for file in files:
            if os.path.isfile(file):
#                print " file, splitext: ",file,os.path.splitext(file)
                base,ext=os.path.splitext(file)
                if ext == ".sav":
#                    print " file with .sav extension:",file
                    self.filelistExt.append(file) 
                    
        if DEBUG:
            print('self.filelistExt = %s' % self.filelistExt)

# Save-state Pmw.ComboBox
        self.pmwcomboSaveStateFileName=Pmw.ComboBox(
            tab,
            label_text="     Save-state file:",
            labelpos="wn",
            label_background=colorBackGround,
            scrolledlist_items=self.filelistExt,
            )
        '''    
        self.pmwcomboSaveStateFileName.grid(
            row=1,
            column=4,
            sticky='N',
            )
        '''
# cf p. 153 of Grayson's "Python and Tkinter Programming" book
#        Pmw.Color.changecolor(self.pmwcomboSaveStateFileName, background='lightgreen') 
        
# DWB: NOT USED
        try:
            entryInit = self.pmwcomboSaveStateFileName.selectitem(self.filelistExt[1])
        except IndexError:
            entryInit="<input filename>"
# -----END----
            
# Save-state file button
        self.entrySaveStateFileNameVar=StringVar()
# link field to variable
#        self.entrySaveStateFileNameVar.set('test3.sav')
        if len(self.filelistExt) <> 0:
            self.entrySaveStateFileNameVar.set(
                self.filelistExt[0]
                )
        else:
            self.entrySaveStateFileNameVar.set('')

# button
        self.buttonSaveStateFileName=Button(
            tab, 
            text='SAVE state',
#            command=(lambda v=self.entrySaveFileNameVar.get(): self.buttonSaveFileNameHandler(v) ) WILL NOT WORK; THE OUTPUT STAYS THE INITIAL VALUE!!!
            command=(lambda v=self.entrySaveStateFileNameVar: self.handlerButtonSaveStateFileName(v.get()) ),
            justify=CENTER,
            relief=RAISED,
            font=self.buttonFont,
            borderwidth=5,
            )
        '''
        self.buttonSaveStateFileName.grid(
            row=1,
            column=4,
            pady=5,
            )
        '''
        
# PYLOTDB home page
        self.buttonPylotDBHomePage=Button(
            tab,
            text='PYLOTDB\nhome page',
            font=self.dataFont,
            bg='white',
            fg='blue',
            command=self.handlerButtonPylotDBHomePage,
            width=25,
            height=3,
            justify=CENTER,
            borderwidth=5,
            relief=RAISED,
            )
        self.buttonPylotDBHomePage.grid(
            row=1,
            column=4,
            padx=0,
            pady=5,
            )
        
# Restore-state Pmw.ComboBox
        self.pmwcomboRestoreStateFileName=Pmw.ComboBox(
            tab,
            label_text="Restore-state file:",
            labelpos="wn",
            label_background=colorBackGround,
            scrolledlist_items=self.filelistExt,
            )
        '''
        self.pmwcomboRestoreStateFileName.grid(
            row=2,
            column=4,
            sticky='N'
            )
        '''
        
# Restore-state file button
        self.entryRestoreStateFileNameVar=StringVar()
# link field to variable
#        self.entrySaveStateFileNameVar.set('test3.sav')
        if len(self.filelistExt) <> 0:
            self.entryRestoreStateFileNameVar.set(
                self.filelistExt[0]
                )
        else:
            self.entryRestoreStateFileNameVar.set('')
#        print 
#        print ' >>>>> self.entrySaveStateFileNameVar =',self.entryRestoreStateFileNameVar
#        print ' >>>>>  type of self.entryRestoreStateFileNameVar = ',type(self.entryRestoreStateFileNameVar)
#        print 
# button
        self.buttonRestoreStateFileName=Button(
            tab, 
            text='RESTORE state',
#            command=(lambda v=self.entrySaveFileNameVar.get(): self.buttonSaveFileNameHandler(v) ) WILL NOT WORK; THE OUTPUT STAYS THE INITIAL VALUE!!!
            command=(lambda v=self.entryRestoreStateFileNameVar: self.handlerButtonRestoreStateFileName(v.get()) ),
            justify=CENTER,
            relief=RAISED,
            font=self.buttonFont,
            borderwidth=5,
            )
        '''
        self.buttonRestoreStateFileName.grid(
            row=2,
            column=4,
            pady=5,
            sticky=S,
            )
        '''
        
        return
        

# -----end of HEADER for each tab except INFO -----


# ================================================================ #

# dummy def
    def ZZ___GENERAL_NOTEBOOK_METHODS():
        pass
        
        return
        

# ----- GENERAL NOTEBOOK METHODS -----

    def linkSelectedTab_To_WindowsIOButton(self,tabName):
        '''
        Purpose:
            provides for linking the selected tab in the
        main window to the corresponding I/O tab in the
        WindowsIO frame
        '''
    
        if DEBUG_PRINT_METHOD:
            print ('\n>** In ' + MODULE + '/' + 'linkSelectTab_To_WindowsIOButton' )

            #            '\n  You have clicked on tab %s' % tabName )
# if display is locked, don't change anything
        if self.lockDisplay.get(): 
            print(
                '\n  You have clicked on tab "%s", but the I/O Windows display is LOCKED'
                % (tabName)
                )
            return
                 
        if tabName == 'HOST INFO':
            self.hideAllGridsWindows_IO()
            self.frameHostInfoWindows_IO.grid()     
        elif tabName == 'CVS/SVN ACCESS':
            self.hideAllGridsWindows_IO()
            self.frameCvsSvnAccessWindows_IO.grid()
        elif tabName == 'COMPILE':
            self.hideAllGridsWindows_IO()
            self.frameCompileWindows_IO.grid()
        elif tabName == 'SETUP':
            self.hideAllGridsWindows_IO()
            self.frameSetupWindows_IO.grid()
        elif tabName == 'RUN':
            self.hideAllGridsWindows_IO()
            self.frameRunWindows_IO.grid()
        elif tabName == 'STATUS':
            self.hideAllGridsWindows_IO()
            self.frameStatusWindows_IO.grid()
        elif tabName == 'POST-PROCESS':
            self.hideAllGridsWindows_IO()
            self.framePostProcessWindows_IO.grid()
        elif tabName == 'MySQL ACCESS':
            self.hideAllGridsWindows_IO()
            self.frameMySQLWindows_IO.grid()
        else:
            print '\n>> Method: linkSelectTab_To_WindowsIOButton'
            print '>> ERROR: fatal - tabName does not match any existing tabs'
            print '       tabName:%s\n' % tabName
            sys.exit()
            
        return
        

#----- end of GENERAL NOTEBOOK METHODS -----        


#----- INFO TAB METHODS -----

# dummy def
    def ZZ___INFO_TAB_METHODS():
        pass
        
        return
        

    def frameInfoCreate(self,parent,msg):
        ''' 
        Purpose:
            create the scrolled frame for the INFO tab
        '''
        self.frameInfo= Pmw.ScrolledFrame(
            parent,
            borderframe=10,
            labelpos=N,
            label_text=msg,
            label_font=self.titleFont,
            usehullsize=0,
            hull_width=globalHullWidth,
            hull_height=globalHullHeight,
            hscrollmode='dynamic',
            vscrollmode='dynamic',
            horizflex='elastic', # 'expand' centers interior frames when window is stretched; ...
            vertflex='fixed',  # ...   do not use 'elastic' which kills scrollbars
            )
        self.frameInfo.pack(
            padx=5,
            pady=5,
            fill='both',
            expand='YES',
            )

# following determines how fast the right widget boundary moves 
#    relative to when the frame boundary is moved.
# format:
#      self.frameInfo.interior().grid_rowconfigure(row#, distance_when_moved)

        
        self.frameInfo.interior().grid_rowconfigure(0,weight=1)
        self.frameInfo.interior().grid_columnconfigure(0,weight=1) 
        self.frameInfo.interior().grid_rowconfigure(1,weight=1)
        self.frameInfo.interior().grid_columnconfigure(1,weight=1)
        
        Pmw.Color.changecolor(parent, background=backgroundInfoTab) 
        
        return
        
        
    def framesInterior_tabInfo(self,parent):
        '''
        Purpose:
            create top and bottom frames for the INFO tab
        '''
# top    
        self.tabInfo_TopFrame=Frame(
            parent,
            relief=RIDGE,
            borderwidth=5,
            bg=backgroundTopFrameInfoTab,
            )
        self.tabInfo_TopFrame.grid(
            row=0,
            column=0,
            padx=0,
            pady=5,
            sticky=N,
            )

# bottom
        self.tabInfo_MiddleFrame=Frame(
            parent,
            relief=RIDGE,
            borderwidth=5,
            bg=backgroundBottomFrameInfoTab,
            )
        self.tabInfo_MiddleFrame.grid(
            row=1,
            column=0,
            padx=0,
            pady=0,
            )
            
        return
        

    def displayInfoHeader(self,parent):
        '''
        Purpose:
            widgets for header of INFO tab
        '''

# Widgets for top frame
        msgWelcome='Welcome\nto\nPylotDB'
#   tab label
        tabLabel_Left = Label(
            parent, 
            text = msgWelcome, 
            bg='white',
            fg='blue',
            font=self.dataFont,
            borderwidth=5,
            justify=CENTER,
            relief=RIDGE,
            width=15,
            )
        tabLabel_Left.grid(
            row=1, 
            column=0, 
#            rowspan=1,
#            columnspan=1,
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5,
#            sticky=W,
            )
#
        tabLabel_Right = Label(
            parent, 
            text=msgWelcome, 
            bg='white',
            fg='blue',
            font=self.dataFont,
            borderwidth=5,
            justify=CENTER,
            relief=RIDGE,
            width=15,
            )
        tabLabel_Right.grid(
            row=1, 
            column=2, 
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5,
#            sticky=E,
            )

        tabQuitButton=Button(
            parent, 
            text='Quit PylotDB',
            command=self.handlerButtonQuit,
            bg='white',
            fg='blue',
            font=self.buttonFont,
            justify=CENTER,
            borderwidth=5,
            relief=RAISED,
            )
        tabQuitButton.grid(
            row=0,
            column=2,
            padx=2,
            pady=2,
            ipadx=3,
            ipady=2,
#            sticky=NE,
            )
#
        newLine = self.newLine
        tabLabel_Mid = Label(
            parent, 
            text=
#                newLine +
                'PylotDB' + newLine +
                'Sandia Job Submission and Database Analysis Tool' + newLine +
                'Version: ' + self.msgPylotDBVersion + newLine +
                'Username: ' + self.userName + newLine +
                'Hostname: ' + self.computerName + ' ' + 
                                    self.os_message + newLine + 
                'Working Directory: ' + newLine +
                    self.currentDirectory,
            bg='white',
            fg='blue',
            font=self.dataFont,
            borderwidth=5,
            justify=CENTER,
            relief=RIDGE,
            width=40,
            )
        tabLabel_Mid.grid(
            row=0,
            column=1,
            rowspan=2,
            sticky=N,
            padx=30,
            pady=2,
            )
        
#flashing 'please wait'
# time
        now=time.localtime(time.time())
        year,month,day,hour,minute,second,weekday,yearday,daylight=now
        day_Word=('Mon','Tue','Wed','Thu','Fri','Sat','Sun')[weekday]
        newLine = self.newLine
        
        tabLabel_Time=Label(
            parent,
            text=
#                'This session start date and time: ' + newLine +
                'Start date: %s'%(day_Word) + ', ' + '%02d-%02d-%04d  '%(month, day, year) + 
                'Start time: %02d:%02d:%02d  '%(hour,minute,second),
            bg='white',
            fg='blue',
            font=self.dataFont,
            borderwidth=5,
            justify=CENTER,
            relief=RIDGE,
            width=35,
            )
        tabLabel_Time.grid(
            row=2,
            column=1,
            pady=2,
#            sticky=S,
            )
            
        return
        
            
    def labelInfoLineInfoTab(self,parent,screenResolution_Width,screenResolution_Height):
        '''
        Purpose:
            shows system, processor, user info
        '''    
# Frames
# ... header and info widgets
        frame_00 = Frame(
            parent,
            bg='maroon',
            )
        frame_00.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
#            sticky=N,
            sticky=E+W,
            )
# ... software license title
        frame_10 = Frame(
            parent,
            bg='maroon',
            )
        frame_10.grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            )
# ... textbox for software license
        frame_20 = Frame(
            parent,
            bg='maroon',
            )
        frame_20.grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky=E+W,
            )


#    Info line
        Row=0
        tabLabel_InfoLine=Label(
            frame_00,
            text=(
#            '-'*100 + '\n' +
            'HOST MACHINE INFO\n'
#            '-'*100 ,
            ),
#            bg='white',
            fg='black',
            bg='maroon',
#            font=self.dataFontBold,
            font=self.dataFont,
#            borderwidth=5,
#            justify=CENTER,
            anchor=N,
#            relief=RIDGE,
#            width=50,
            )
        tabLabel_InfoLine.grid(
            row=Row,
            column=0,
            columnspan=2,
            padx=0,
            pady=10,
            )
            
        Row += 1
        label = Label(
            frame_00,
            text='Computer name: ',
            fg='black',
            bg='maroon',
            font=self.dataFont
            )
        label.grid(
            row=Row,
            column=0,
            padx=0,
            pady=0,
            sticky=E,
            )
        self.varEntryComputerName = StringVar()
        self.varEntryComputerName.set(self.computerName)
        self.entryComputerName = Entry(
            frame_00,
            textvariable=self.varEntryComputerName,
            width=50,
            disabledforeground='black',
            disabledbackground='white',
            state='disabled',
            )
        self.entryComputerName.grid(
            row=Row,
            column=1,
            padx=0,
            pady=0,
            sticky=W,
            )
            
        Row += 1 
        label = Label(
            frame_00,
            text='Username: ',
            fg='black',
            bg='maroon',
            font=self.dataFont
            )
        label.grid(
            row=Row,
            column=0,
            padx=0,
            pady=0,
            sticky=E,
            )
        self.varEntryUsername = StringVar()
        self.varEntryUsername.set(self.userName)
        self.entryUsername = Entry(
            frame_00,
            textvariable=self.varEntryUsername,
            width=50,
            disabledforeground='black',
            disabledbackground='white',
            state='disabled',
            )
        self.entryUsername.grid(
            row=Row,
            column=1,
            padx=0,
            pady=0,
            sticky=W,
            )

        Row += 1
        label = Label(
            frame_00,
            text='Big-endian / little-endian: ',
            fg='black',
            bg='maroon',
            font=self.dataFont,
            )
        label.grid(
            row=Row,
            column=0,
            padx=0,
            pady=0,
            sticky=E,
            )
        self.varEntryEndian = StringVar()
        if self.littleEndian:
            self.varEntryEndian.set(
                'little-endian platform (intel, alpha)'
                )
        else:
            self.varEntryEndian.set(
                'big-endian platform (motorola, sparc)'
                )
        self.entryEndian = Entry(
            frame_00,
            textvariable=self.varEntryEndian,
            width=50,
            disabledforeground='black',
            disabledbackground='white',
            state='disabled',
            )
        self.entryEndian.grid(
            row=Row,
            column=1,
            padx=0,
            pady=0,
            sticky=W,
            )
            
        Row += 1
        label = Label(
            frame_00,
            text='Operating system: ',
            fg='black',
            bg='maroon',
            font=self.dataFont
            )
        label.grid(
            row=Row,
            column=0,
            padx=0,
            pady=0,
            sticky=E,
            )
        self.varEntryOperatingSystem = StringVar()
        self.varEntryOperatingSystem.set(
            self.operatingSystem + ', ' + self.processorBitWidth
            )
        self.entryOperatingSystem = Entry(
            frame_00,
            textvariable=self.varEntryOperatingSystem,
            width=50,
            disabledforeground='black',
            disabledbackground='white',
            state='disabled',
            )
        self.entryOperatingSystem.grid(
            row=Row,
            column=1,
            padx=0,
            pady=0,
            sticky=W,
            )
            
        Row += 1   
        label = Label(
            frame_00,
            text='Processor architecture: ',
            fg='black',
            bg='maroon',
            font=self.dataFont
            )
        label.grid(
            row=Row,
            column=0,
            padx=0,
            pady=0,
            sticky=E,
            )
        self.varEntryProcArch = StringVar()
        self.varEntryProcArch.set(self.processorArchitecture)
        self.entryProcArch = Entry(
            frame_00,
            textvariable=self.varEntryProcArch,
            width=50,
            disabledforeground='black',
            disabledbackground='white',
            state='disabled',
            )
        self.entryProcArch.grid(
            row=Row,
            column=1,
            padx=0,
            pady=0,
            sticky=W,
            )
            
        Row += 1   
        label = Label(
            frame_00,
            text='Processor identifier: ',
            fg='black',
            bg='maroon',
            font=self.dataFont,
            )
        label.grid(
            row=Row,
            column=0,
            padx=0,
            pady=0,
            sticky=E,
            )
        self.varProcID = StringVar()
        self.varProcID.set(self.processorIdentifier)
        self.entryProcID = Entry(
            frame_00,
            textvariable=self.varProcID,
            width=50,
            disabledforeground='black',
            disabledbackground='white',
            state='disabled',
            )
        self.entryProcID.grid(
            row=Row,
            column=1,
            padx=0,
            pady=0,
            sticky=W,
            )
            
        Row += 1  
        label = Label(
            frame_00,
            text='Session name: ',
            fg='black',
            bg='maroon',
            font=self.dataFont,
            )
        label.grid(
            row=Row,
            column=0,
            padx=0,
            pady=0,
            sticky=E,
            )
        self.varSessionName = StringVar()
        self.varSessionName.set(self.sessionName)
        self.entrySessionName = Entry(
            frame_00,
            textvariable=self.varSessionName,
            width=50,
            disabledforeground='black',
            disabledbackground='white',
            state='disabled',
            )
        self.entrySessionName.grid(
            row=Row,
            column=1,
            padx=0,
            pady=0,
            sticky=W,
            )
            
        Row += 1
        label = Label(
            frame_00,
            text='Python version: ',
            fg='black',
            bg='maroon',
            font=self.dataFont,
            )
        label.grid(
            row=Row,
            column=0,
            padx=0,
            pady=0,
            sticky=E,
            )
        self.varVersionPython = StringVar()
        self.varVersionPython.set(self.versionPython)
        self.entryVersionPython = Entry(
            frame_00,
            textvariable=self.varVersionPython,
            width=50,
            disabledforeground='black',
            disabledbackground='white',
            state='disabled',
            )
        self.entryVersionPython.grid(
            row=Row,
            column=1,
            padx=0,
            pady=0,
            sticky=W,
            )
            
        Row += 1
        label = Label(
            frame_00,
            text='Screen resolution: ',
            fg='black',
            bg='maroon',
            font=self.dataFont,
            )
        label.grid(
            row=Row,
            column=0,
            padx=0,
            pady=0,
            sticky=E,
            )
        self.varScreenResolution = StringVar()
        self.varScreenResolution.set(
            str(screenResolution_Width) + ' x ' + str(screenResolution_Height)
            )
        self.entryScreenResolution = Entry(
            frame_00,
            textvariable=self.varScreenResolution,
            width=50,
            disabledforeground='black',
            disabledbackground='white',
            state='disabled',
            )
        self.entryScreenResolution.grid(
            row=Row,
            column=1,
            padx=0,
            pady=0,
            sticky=W,
            )
            
# frame_10: title for software license
        tabLicenseTitle=Label(
            frame_10,
            text=(
#            '-'*100 + '\n' +
            '\nSANDIA LICENSE'
#            '-'*100 ,
            ),
#            bg='white',
            fg='black',
            bg='maroon',
#            font=self.dataFontBold,
            font=self.dataFont,
#            borderwidth=5,
#            justify=CENTER,
            anchor=N,
#            relief=RIDGE,
#            width=50,
            justify=CENTER,
            )
        tabLicenseTitle.grid(
            row=0,
            column=0,
            padx=0,
            pady=10,
            sticky=E+W,
            )
            
# frame_20: scrolled text box for Sandia license
            
#        fixedFont = Pmw.logicalfont('Fixed')
        scrolledtextLicenseSandia = Pmw.ScrolledText(
            frame_20,
#            labelpos='n',
#            label_text='Summary of field "' + varField + '"\n' +
#               'from table "' + myTable + '"',
#            label_font=self.titleFont,
#            label_background='lightgreen',
#            columnheader=1,
#            rowheader=1,
#            rowcolumnheader=1,
            usehullsize=1,
            hull_width=600,
            hull_height=300,
#            text_wrap='none',
#            text_font=fixedFont,
            text_font=self.dataFont,
#            Header_font=fixedFont,
#            Header_foreground='black',
#            Header_background='lightgreen',
#            rowheader_width=3,
#            rowcolumnheader_width=3,
            text_padx=3,
            text_pady=3,
#            Header_padx=3,
#            rowheader_pady=3,
            )
        scrolledtextLicenseSandia.grid(
            row=0,
            column=0,
            sticky='e'+'w',
            )
        scrolledtextLicenseSandia.insert('0.0',licenseSandia)
        scrolledtextLicenseSandia.component('text').configure(state=DISABLED)
            
        return            
    
# ----- end of INFO TAB METHODS ----- 

# ----- CVS/SVN CHECK-IN TAB METHODS ----- 

# dummy def
    def ZZ___CVS_SVN_ACCESS_TAB_METHODS():
        pass
        
        return
        
        
    def frameCvsSvnAccessCreate(self,parent,msg):
        '''
        Purpose:
            create the scrolled frame for this tab
        '''
        self.frameCvsSvnAccess = Pmw.ScrolledFrame(
            parent,
            borderframe = 5,
            labelpos = N,
            label_text = msg,
            label_font=self.titleFont,
            usehullsize = 1,
            hull_width = globalHullWidth,
            hull_height = globalHullHeight,
            hscrollmode='dynamic',
            vscrollmode='dynamic',
            horizflex='elastic', # 'expand' centers interior frames when window is stretched; ...
            vertflex='fixed',  # ...   do not use 'elastic' which kills scrollbars
            )
        self.frameCvsSvnAccess.pack(
            padx = 5, 
            pady = 5, 
            fill='both', 
            expand='YES',
            )
         
        self.frameCvsSvnAccess.interior().grid_rowconfigure(0,weight=1)
        self.frameCvsSvnAccess.interior().grid_columnconfigure(0,weight=1) 
        self.frameCvsSvnAccess.interior().grid_rowconfigure(1,weight=1)
        self.frameCvsSvnAccess.interior().grid_columnconfigure(1,weight=1)
            
        Pmw.Color.changecolor(parent, background=backgroundCvsSvnAccessTab) 
        
        return
        
               
    def framesInterior_tabCvsSvnAccess(self,parent):
        '''
        Purpose:
            create top and bottom frames for the CVS/SVN ACCESS tab
        ''' 

# top    
        self.tabCvsSvnAccess_TopFrame=Frame(
            parent,
            relief=RIDGE,
            borderwidth=5,
            bg=backgroundTopFrameCvsSvnAccessTab,
            )
        self.tabCvsSvnAccess_TopFrame.grid(
            row=0,
            column=0,
            padx=0,
            pady=10,
            sticky=N,
            )

# bottom
        self.tabCvsSvnAccess_BottomFrame=Frame(
            parent,
            relief=RIDGE,
            borderwidth=5,
            bg=backgroundBottomFrameCvsSvnAccessTab,
            )
        self.tabCvsSvnAccess_BottomFrame.grid(
            row=1,
            column=0,
            padx=0,
            pady=0,
            )
        
        return
        
 
    def framesCvsSvnAccessTab(self,parent):
        '''
        Purpose:
            construct widgets for access to CVS or SVN 
        version control repositories
        '''
        
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'framesCvsSvnAccessTab'
        
# frame TOP
        frameTop = Frame(
            parent,
            bg=backgroundBottomFrameCvsSvnAccessTab,
            )
        frameTop.grid(
            row=0,
            column=0,
            columnspan=99,
            pady=10,
            )
        
# frame LEFT
        frameLeft = Frame(
            parent,
#            bg=backgroundBottomFrameCvsSvnAccessTab,
            bg=backgroundBottomFrameCvsSvnAccessTab,
            )
        frameLeft.grid(
            row=1,
            column=0,
            padx=10,
            pady=20,
            )

# frame MIDDLE
        frameMiddle = Frame(
            parent,
            bg=backgroundBottomFrameCvsSvnAccessTab,
            )
        frameMiddle.grid(
            row=1,
            column=1,
            padx=10,
            pady=20,
            )

# frame RIGHT
        frameRight = Frame(
            parent,
            bg=backgroundBottomFrameCvsSvnAccessTab,
            )
        frameRight.grid(
            row=1,
            column=2,
            padx=10,
            pady=20,
            )
            
        labelChoose = Label(
            frameTop,
            text='CHOOSE VERSION CONTROL SYSTEM',
            bg=backgroundBottomFrameCvsSvnAccessTab,
            )
        labelChoose.grid(
            row=0,
            column=0,
            columnspan=99,
            pady=10,
            )
        
        self.varRadioButtonVersionControl = StringVar()
        radiobuttonSvn = Radiobutton(
            frameTop,
            text='Subversion (SVN)',
            variable=self.varRadioButtonVersionControl,
            value='SVN',
            bg=backgroundBottomFrameCvsSvnAccessTab,
            indicatoron=1,
            )
        radiobuttonSvn.grid(
            row=1,
            column=0,
            sticky=E,
            padx=10,
            )
            
        radiobuttonCvs = Radiobutton(
            frameTop,
            text='Concurrent Versions System (CVS)',
            variable=self.varRadioButtonVersionControl,
            value='CVS',
            bg=backgroundBottomFrameCvsSvnAccessTab,
            indicatoron=1,
            )
        radiobuttonCvs.grid(
            row=1,
            column=1,
            sticky=W,
            padx=10,
            )
            
        radiobuttonGit = Radiobutton(
            frameTop,
            text='GIT',
            variable=self.varRadioButtonVersionControl,
            value='GIT',
            bg=backgroundBottomFrameCvsSvnAccessTab,
            indicatoron=1,
            )
        radiobuttonGit.grid(
            row=1,
            column=2,
            sticky=W,
            padx=10,
            )
            
# browse for repository
        labelFrameLeft = Label(
            frameLeft,
            text='REPOSITORY ACCESS',
            bg=backgroundBottomFrameCvsSvnAccessTab,
            )
        labelFrameLeft.grid(
            row=0,
            column=0,
            columnspan=99,
            pady=5, 
            sticky=N
            )
            
        labelRepoFile = Label(
            frameLeft,
            text='Repository\npath/filename:',
            justify=LEFT,
            bg=backgroundBottomFrameCvsSvnAccessTab
            )
        labelRepoFile.grid(
            row=1,
            column=0,
            padx=5,
            sticky=W,
            )
        self.entryRepoFile = Entry(
            frameLeft
            )
        self.entryRepoFile.grid(
            row=1,
            column=1,
            padx=2
            )
        buttonRepoFile = Button(
            frameLeft,
            font=self.buttonFont,
#            command=self.handlerRepoFile,
            text='Browse',
            borderwidth=3,
            relief=RAISED,
            justify=CENTER,
            )
        buttonRepoFile.grid(
            row=2,
            column=1,
            pady=0,
            sticky=N,
            )
# if repository does not exist, create it            
        buttonRepoFileCreate = Button(
            frameLeft,
            text='Create Repository',
            borderwidth=5,
            relief=RAISED,
#            command=??
            )
        buttonRepoFileCreate.grid(
            row=3,
            column=0,
            columnspan=99,
            pady=20,
            )


# checkout label for middle frame
        labelFrameMiddle = Label(
            frameMiddle,
            text='CVS/SVN CHECKOUT',
            bg=backgroundBottomFrameCvsSvnAccessTab,
            )
        labelFrameMiddle.grid(
            row=0,
            column=0,
            columnspan=99,
            pady=5,  
            sticky=N,
            )
            
        labelRepoFileDestinationDir = Label(
            frameMiddle,
            text='Destination\ndirectory:',
            justify=LEFT,
            bg=backgroundBottomFrameCvsSvnAccessTab
            )
        labelRepoFileDestinationDir.grid(
            row=1,
            column=0,
            padx=5,
            sticky=W,
            )
        self.entryRepoFileDestinationDir = Entry(
            frameMiddle
            )
        self.entryRepoFileDestinationDir.grid(
            row=1,
            column=1,
            padx=2
            )
        buttonRepoFileDestinationDir = Button(
            frameMiddle,
            font=self.buttonFont,
#            command=self.handlerRepoFile,
            text='Browse',
            borderwidth=3,
            relief=RAISED,
            justify=CENTER,
            )
        buttonRepoFileDestinationDir.grid(
            row=2,
            column=1,
            pady=0,
            sticky=N,
            )
            
        buttonFrameMiddleCheckOut = Button(
            frameMiddle,
            text='Check out',
            borderwidth=5,
            relief=RAISED,
            width=10,
#            command=??
            )
        buttonFrameMiddleCheckOut.grid(
            row=3,
            column=0,
            columnspan=99,
            pady=20,
            )

# cvs/svn access label for right frame
        labelFrameRight = Label(
            frameRight,
            text='CVS/SVN CHECK-IN',
            bg=backgroundBottomFrameCvsSvnAccessTab,
            )
        labelFrameRight.grid(
            row=0,
            column=0,
            columnspan=99,
            pady=5,
            sticky=N,
            )  

        labelRepoFileSourceDir = Label(
            frameRight,
            text='Source\ndirectory:',
            justify=LEFT,
            bg=backgroundBottomFrameCvsSvnAccessTab
            )
        labelRepoFileSourceDir.grid(
            row=1,
            column=0,
            padx=5,
            sticky=W,
            )
        self.entryRepoFileSourceDir = Entry(
            frameRight
            )
        self.entryRepoFileSourceDir.grid(
            row=1,
            column=1,
            padx=2
            )
        buttonRepoFileSourceDir = Button(
            frameRight,
            font=self.buttonFont,
#            command=self.handlerRepoFile,
            text='Browse',
            borderwidth=3,
            relief=RAISED,
            justify=CENTER,
            )
        buttonRepoFileSourceDir.grid(
            row=2,
            column=1,
            pady=0,
            sticky=N,
            )
                       
        buttonFrameRightCheckOut = Button(
            frameRight,
            text='Check in',
            borderwidth=5,
            relief=RAISED,
            width=10,
#            command=??
            )
        buttonFrameRightCheckOut.grid(
            row=3,
            column=0,
            columnspan=99,
            pady=20,
            )


#  ----- end of CVS/SVN ACCESS TAB METHODS ----- 

#  ----- CVS/SVN CHECK-OUT TAB METHODS ----- 

# dummy def
    def ZZ___CVS_SVN_CHECKOUT_TAB_METHODS():
        pass
        
        return
        
        
    def frameCheckOutCreate(self,parent,msg):
        ''' 
        Purpose:
            create the scrolled frame for the CHECK-OUT tab
        '''
        self.frameCheckOut = Pmw.ScrolledFrame(
            parent,
            borderframe = 1,
            labelpos = N,
            label_text = msg,
            label_font=self.titleFont,
            usehullsize = 1,
            hull_width = globalHullWidth,
            hull_height = globalHullHeight,
            hscrollmode='dynamic',
            vscrollmode='dynamic',
            horizflex='elastic', # 'expand' centers interior frames when window is stretched; ...
            vertflex='fixed',  # ...   do not use 'elastic' which kills scrollbars
            )
        self.frameCheckOut.pack(
            padx=5, 
            pady=5, 
            fill='both', 
            expand='YES',
            )

        self.frameCheckOut.interior().grid_rowconfigure(0,weight=1)
        self.frameCheckOut.interior().grid_columnconfigure(0,weight=1) 
        self.frameCheckOut.interior().grid_rowconfigure(1,weight=1)
        self.frameCheckOut.interior().grid_columnconfigure(1,weight=1)
            
        Pmw.Color.changecolor(parent, background=backgroundCheckOutTab)  
        
        return
        

    def framesInterior_tabCheckOut(self,parent):
        '''
        Purpose:
            create top and bottom frames for the CHECK-OUT tab
        '''  

# top    
        self.tabCheckOut_TopFrame=Frame(
            self.frameCheckOut.interior(),
            relief=RIDGE,
            borderwidth=5,
            bg=backgroundTopFrameCheckOutTab,
            )
        self.tabCheckOut_TopFrame.grid(
            row=0,
            column=0,
            pady=5,
            sticky=N
            )
# bottom
        self.tabCheckout_BottomFrame=Frame(
            self.frameCheckOut.interior(),
            relief=RIDGE,
            borderwidth=5,
            bg=backgroundBottomFrameCheckOutTab
            )
        self.tabCheckout_BottomFrame.grid(
            row=1,
            column=0,
#            columnspan=5,
#            rowspan=1,
            pady=5,
#            sticky=NSEW,
            )

        Pmw.Color.changecolor(self.tabCheckOut_BottomFrame, background=backgroundCheckOutTab)
        
        return


# ----- end of CVS/SVN CHECKOUT TAB METHODS -----

# ----- COMPILE TAB METHODS -----

# dummy def
    def ZZ___COMPILE_TAB_METHODS():
        pass
        
        return
        
        
    def frameCompileCreate(self,parent,msg):
        ''' 
        Purpose:
            create the scrolled frame for COMPILE tab:
        self.frameCompile
        '''

        self.frameCompile = Pmw.ScrolledFrame(
            parent,
            borderframe = 1,
            labelpos = N,
            label_text = msg,
            label_font=self.titleFont,
            usehullsize = 1,
            hull_width = globalHullWidth,
            hull_height = globalHullHeight,
            hscrollmode='dynamic',
            vscrollmode='dynamic',
            horizflex='elastic', # 'expand' centers interior frames when window is stretched; ...
            vertflex='fixed',  # ...   do not use 'elastic' which kills scrollbars
            )
        self.frameCompile.pack(
            padx=5, 
            pady=5, 
            fill='both', 
            expand='YES',
            )
            
        self.frameCompile.interior().grid_rowconfigure(0,weight=1)
        self.frameCompile.interior().grid_columnconfigure(0,weight=1) 
        self.frameCompile.interior().grid_rowconfigure(1,weight=1)
        self.frameCompile.interior().grid_columnconfigure(1,weight=1)
            
        Pmw.Color.changecolor(parent, background=backgroundCompileTab)
        
        return
        
        
        
    def framesInterior_tabCompile(self,parent):
        '''
        Purpose:
            create top and bottom frames for the COMPILE tab
        '''
# top    
        self.tabCompile_TopFrame=Frame(
            parent,
            relief=RIDGE,
            borderwidth=5,
            bg=backgroundTopFrameCompileTab,
            )
        self.tabCompile_TopFrame.grid(
            row=0,
            column=0,
            pady=5,
            sticky=N
            )
# bottom
        self.tabCompile_MiddleFrame=Frame(
            parent,
            relief=RIDGE,
            borderwidth=5,
            bg=backgroundBottomFrameCompileTab,
            )
        self.tabCompile_MiddleFrame.grid(
            row=1,
            column=0,
            pady=5,
            )

        return


    def boxCommandCompileTab(self,parent):
        '''
        Purpose:
            construct Compile Commands for
        compile tab
        
        OUTPUT vars:
        Use .get() to get values for the following:
            > self.stringCommand 
            > self.stringCompileOptions 
                (only if self.stringCommand.get()==compile)
        '''

# create  frame for Command box        
        frameCommandCompileTab=Frame(
            parent,
            relief=RIDGE,
            borderwidth=5,
            )
        frameCommandCompileTab.grid(
            row=0,
            column=0,
            padx=10,
            pady=5,
            sticky=N,
            )

# label for Command box            
        labelCompileCommandCompileTab=Label(
            frameCommandCompileTab,
            text='COMMAND',
            justify=CENTER,
            )
        labelCompileCommandCompileTab.grid(
            row=0,
            column=0,
            columnspan=1,
            sticky=N,
            )

# string variable to set upon selection            
        self.stringCommandCompileTab=StringVar()
        self.stringCommandCompileTab.set('compileLocal')

# define radiobuttons
#    Compile for local run
        self.buttonCompileForLocalRunCompileTab=Radiobutton(
            frameCommandCompileTab,
            variable=self.stringCommandCompileTab,
            text='Compile\nfor local run',
            command=self.handlerCommandCompileTab,
            value='compileLocal',
            justify=LEFT,
            )
        self.buttonCompileForLocalRunCompileTab.grid(
            row=1,
            column=0,
            sticky=W,
            )
# Set the starting default value
#   invoke the first button as default in the COMMAND box
        self.buttonCompileForLocalRunCompileTab.select()

#    Compile        
        self.buttonCompileCompileTab=Radiobutton(
            frameCommandCompileTab,
            variable=self.stringCommandCompileTab,
            text='Compile',
            command=self.handlerCommandCompileTab,
            value='compile'
            )
        self.buttonCompileCompileTab.grid(
            row=2,
            column=0,
            sticky=W,
            )

#    frame for subcommands under Compile            
        frameUnderCompileCompileTab=Frame(
            frameCommandCompileTab
            )
        frameUnderCompileCompileTab.grid(
            row=3,
            column=0,
            )

#    Config            
        self.buttonConfigCommandCompileTab=Radiobutton(
            frameCommandCompileTab,
            variable=self.stringCommandCompileTab,
            text='Config',
            command=self.handlerCommandCompileTab,
            value='config',
            )
        self.buttonConfigCommandCompileTab.grid(
            row=4,
            column=0,
            sticky=W,
            )

#    Make            
        self.buttonMakeCommandCompileTab=Radiobutton(
            frameCommandCompileTab,
            variable=self.stringCommandCompileTab,
            text='Make',
            command=self.handlerCommandCompileTab,
            value='make',
            )
        self.buttonMakeCommandCompileTab.grid(
            row=5,
            column=0,
            sticky=W,
            )
            
#    sub-buttons under Compile
        self.stringSubCompileOptionsCommandCompileTab=StringVar()
        self.stringSubCompileOptionsCommandCompileTab.set('gnu')
   
#        gnu   
        self.subCompileOption1CommandCompileTab=Radiobutton(
            frameUnderCompileCompileTab,
            variable=self.stringSubCompileOptionsCommandCompileTab,
            command=self.handlerCommandCompileTab,
            text='gnu',
            value='gnu',
            )
        self.subCompileOption1CommandCompileTab.grid(
            row=0,
            column=0,
            padx=20,
            pady=0,
            sticky=W,
            )
# set as default for the sub-buttons
        self.subCompileOption1CommandCompileTab.select()

#        intel        
        self.subCompileOption2CommandCompileTab=Radiobutton(
            frameUnderCompileCompileTab,
            variable=self.stringSubCompileOptionsCommandCompileTab,
            command=self.handlerCommandCompileTab,
            text='intel',
            value='intel',
            )
        self.subCompileOption2CommandCompileTab.grid(
            row=1,
            column=0,
            padx=20,
            pady=0,
            sticky=W,
            )

#        mpi            
        self.subCompileOption3CommandCompileTab=Radiobutton(
            frameUnderCompileCompileTab,
            variable=self.stringSubCompileOptionsCommandCompileTab,
            command=self.handlerCommandCompileTab,
            text='mpi',
            value='mpi',
            )
        self.subCompileOption3CommandCompileTab.grid(
            row=2,
            column=0,
            padx=20,
            pady=0,
            sticky=W,
            )

#        pgi            
        self.subCompileOption4CommandCompileTab=Radiobutton(
            frameUnderCompileCompileTab,
            variable=self.stringSubCompileOptionsCommandCompileTab,
            command=self.handlerCommandCompileTab,
            text='pgi',
            value='pgi',
            )
        self.subCompileOption4CommandCompileTab.grid(
            row=3,
            column=0,
            padx=20,
            pady=0,
            sticky=W,
            )
            
        return
        
                          
    def boxLanguageCompileTab(self,parent):
        ''' 
        Purpose:
            construct Language, Config, or Make options for
        compile tab
        
        OUTPUT vars:
        Use .get() to get values for the following:
        if COMMAND == compile:
           if option == gnu: 
               self.radiobuttonsCompileGnuLanguageCompileTab.grid()
           if option == intel:
               self.radiobuttonsCompileIntelLanguageCompileTab.grid()
           if option == mpi:
               self.radiobuttonsCompileMpiLanguageCompileTab.grid()
           if option == pgi:
               self.radiobuttonsCompilePgiLanguageCompileTab.grid()
        '''
# Create frame
        frameLanguageCompileTab=Frame(
            parent,
            relief=None,
            borderwidth=0,
            width=100,
            height=150,
            bg=backgroundBottomFrameCompileTab,
            )
        frameLanguageCompileTab.grid(
            row=0,
            column=1,
            padx=2,
            pady=2,
            sticky=N,
            )
        frameLanguageCompileTab.grid_propagate(0)
        
# Create Language/Config/Make box, depending on COMMAND picks

# Compile for local run
        self.radiobuttonsCompileForLocalRunLanguageCompileTab=Pmw.RadioSelect(
            frameLanguageCompileTab,
            label_text = 'LANGUAGE',
            buttontype='radiobutton',
            orient = 'vertical',
            labelpos = 'n',
            command=self.handlerRadiobuttonsCompileLanguageCompileTab,
            hull_borderwidth = 5,
            hull_relief = 'ridge',
            )
        self.radiobuttonsCompileForLocalRunLanguageCompileTab.grid(
            row=0,
            column=0,
            columnspan=1,
            padx=0,
            pady=0,
            sticky=N,
            )
# Add some buttons to the radiobutton RadioSelect
        self.languages_local=['cc','f77','f90']
        for language in self.languages_local:
            self.radiobuttonsCompileForLocalRunLanguageCompileTab.add(language)
# set default button
        self.radiobuttonsCompileForLocalRunLanguageCompileTab.setvalue(self.languages_local[0])
        
# Compile/gnu (default)
        self.radiobuttonsCompileGnuLanguageCompileTab=Pmw.RadioSelect(
            frameLanguageCompileTab,
            label_text = 'LANGUAGE',
            buttontype = 'radiobutton',
            orient = 'vertical',
            labelpos = 'n',
            command = self.handlerRadiobuttonsCompileLanguageCompileTab,
            hull_borderwidth = 5,
            hull_relief = 'ridge',
            )
        self.radiobuttonsCompileGnuLanguageCompileTab.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=0,
            pady=0,
            sticky=N,
            )
# Add some buttons to the radiobutton RadioSelect.
        self.languages_gnu=['gcc','g77','g90']
        for language in self.languages_gnu:
            self.radiobuttonsCompileGnuLanguageCompileTab.add(language)
# set default button
        self.radiobuttonsCompileGnuLanguageCompileTab.setvalue(self.languages_gnu[0])
        
# Compile/intel
        self.radiobuttonsCompileIntelLanguageCompileTab=Pmw.RadioSelect(
            frameLanguageCompileTab,
            label_text = 'LANGUAGE',
            buttontype = 'radiobutton',
            orient = 'vertical',
            labelpos = 'n',
            command = self.handlerRadiobuttonsCompileLanguageCompileTab,
            hull_borderwidth = 5,
            hull_relief = 'ridge',
            )
# radiobuttons.pack(side = 'left', expand = 1, padx = 10, pady = 10)
        self.radiobuttonsCompileIntelLanguageCompileTab.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=0,
            pady=0,
            sticky=N,
            )
# Add some buttons to the radiobutton RadioSelect.
        self.languages_intel=['icc','if77','if90']
        for language in self.languages_intel:
            self.radiobuttonsCompileIntelLanguageCompileTab.add(language)
# set default button
        self.radiobuttonsCompileIntelLanguageCompileTab.setvalue(self.languages_intel[0])
        
# Compile/mpi
        self.radiobuttonsCompileMpiLanguageCompileTab=Pmw.RadioSelect(
            frameLanguageCompileTab,
            label_text = 'LANGUAGE',
            buttontype = 'radiobutton',
            orient = 'vertical',
            labelpos = 'n',
            command = self.handlerRadiobuttonsCompileLanguageCompileTab,
            hull_borderwidth = 5,
            hull_relief = 'ridge',
            )
        self.radiobuttonsCompileMpiLanguageCompileTab.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=0,
            pady=0,
            sticky=N,
            )
# Add some buttons to the radiobutton RadioSelect.
        self.languages_mpi=['mpicc','mpif77','mpif90']
        for language in self.languages_mpi:
            self.radiobuttonsCompileMpiLanguageCompileTab.add(language)  
# set default button            
        self.radiobuttonsCompileMpiLanguageCompileTab.setvalue(self.languages_mpi[0])
        
# Compile/pgi
        self.radiobuttonsCompilePgiLanguageCompileTab=Pmw.RadioSelect(  
            frameLanguageCompileTab,
            label_text = 'LANGUAGE',
            buttontype = 'radiobutton',
            orient = 'vertical',
            labelpos = 'n',
            command = self.handlerRadiobuttonsCompileLanguageCompileTab,
            hull_borderwidth = 5,
            hull_relief = 'ridge',
            )
        self.radiobuttonsCompilePgiLanguageCompileTab.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=0,
            pady=0,
            sticky=N,
            )
# Add some buttons to the radiobutton RadioSelect.
        self.languages_pgi=['pgcc','pf77','pf90']
        for language in self.languages_pgi:
            self.radiobuttonsCompilePgiLanguageCompileTab.add(language)
# set default button
        self.radiobuttonsCompilePgiLanguageCompileTab.setvalue(self.languages_pgi[0])

        
# Blank box, for use when anything other than COMPILE or its variants is clicked in the COMMAND tab
# Compile/gnu (default)
        self.radiobuttonsCompileNothingLanguageCompileTab=Label(
            frameLanguageCompileTab,
            text=' LANGUAGE \n\nNot\napplicable\nfor\nthis\nCOMMAND\n',
            anchor=N,
            justify=CENTER,
            fg='darkgray',
            relief=RIDGE,
            borderwidth=5,
            height=8,
            )
        self.radiobuttonsCompileNothingLanguageCompileTab.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=0,
            pady=0,
            sticky=N,
            )
            
        return
        


    def boxOptionsCompileTab(self,parent):
        '''
        Purpose:
            select multiple options for compile, config, or make
        '''
        frameOptionsCompileTab=Frame(
            parent,
            relief=None,
            borderwidth=0,
            bg=backgroundBottomFrameCompileTab,
            )
        frameOptionsCompileTab.grid(
            row=0,
            column=2,
            padx=10,
            pady=5,
            sticky=N,
            )
#        frameOptionsCompileTab.grid_propagate(0)
            
# Compile local cc           
 
        self.checkbuttonsCCMOptionsCompileTab_localcc=Pmw.RadioSelect(
            frameOptionsCompileTab,
            label_text = 'OPTIONS',
            buttontype = 'checkbutton',
            orient = 'vertical',
            labelpos = 'n',
            command = self.handlerCheckbuttonsCCMOptionsCompileTab,
            hull_borderwidth = 5,
            hull_relief = 'ridge',
            selectmode='multiple',
            )
# radiobuttons.pack(side = 'left', expand = 1, padx = 10, pady = 10)
        self.checkbuttonsCCMOptionsCompileTab_localcc.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=0,
            pady=0,
            sticky=N,
            )
# Add some buttons to the radiobutton RadioSelect.
        self.options_localcc=['opt1cc','opt2cc','opt3cc','opt4cc','opt5cc','opt6cc']
        for option in self.options_localcc:
            self.checkbuttonsCCMOptionsCompileTab_localcc.add(option)
# set default button
#        self.checkbuttonsCCMOptionsCompileTab_localcc.invoke(self.options_localcc[0])

        
# Compile local f77
        self.checkbuttonsCCMOptionsCompileTab_localf77=Pmw.RadioSelect(
            frameOptionsCompileTab,
            label_text = 'OPTIONS',
            buttontype = 'checkbutton',
            orient = 'vertical',
            labelpos = 'n',
            command = self.handlerCheckbuttonsCCMOptionsCompileTab,
            hull_borderwidth = 5,
            hull_relief = 'ridge',
            selectmode='multiple',
            )
# radiobuttons.pack(side = 'left', expand = 1, padx = 10, pady = 10)
        self.checkbuttonsCCMOptionsCompileTab_localf77.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=0,
            pady=0,
            sticky=N
            )
# Add some buttons to the radiobutton RadioSelect.
        self.options_localf77=['opt1f77','opt2f77','opt3f77','opt4f77','opt5f77','opt6f77']
        for option in self.options_localf77:
            self.checkbuttonsCCMOptionsCompileTab_localf77.add(option)
# set default button
#        self.checkbuttonsCCMOptionsCompileTab_localf77.invoke(self.options_localf77[0])


# Compile local f90

        self.checkbuttonsCCMOptionsCompileTab_localf90=Pmw.RadioSelect(
            frameOptionsCompileTab,
            label_text = 'OPTIONS',
            buttontype = 'checkbutton',
            orient = 'vertical',
            labelpos = 'n',
            command = self.handlerCheckbuttonsCCMOptionsCompileTab,
            hull_borderwidth = 5,
            hull_relief = 'ridge',
            selectmode='multiple',
            )
# radiobuttons.pack(side = 'left', expand = 1, padx = 10, pady = 10)
        self.checkbuttonsCCMOptionsCompileTab_localf90.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=0,
            pady=0,
            sticky=N
            )
# Add some buttons to the radiobutton RadioSelect.
        self.options_localf90=['opt1f90','opt2f90','opt3f90','opt4f90','opt5f90','opt6f90']
        for option in self.options_localf90:
            self.checkbuttonsCCMOptionsCompileTab_localf90.add(option)
# set default button
#        self.checkbuttonsCCMOptionsCompileTab_localf90.invoke(self.options_localf90[0])


# Compile gnu gcc

        self.checkbuttonsCCMOptionsCompileTab_gcc=Pmw.RadioSelect(
            frameOptionsCompileTab,
            label_text = 'OPTIONS',
            buttontype = 'checkbutton',
            orient = 'vertical',
            labelpos = 'n',
            command = self.handlerCheckbuttonsCCMOptionsCompileTab,
            hull_borderwidth = 5,
            hull_relief = 'ridge',
            selectmode='multiple',
            )
# radiobuttons.pack(side = 'left', expand = 1, padx = 10, pady = 10)
        self.checkbuttonsCCMOptionsCompileTab_gcc.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=0,
            pady=0,
            sticky=N
            )
# Add some buttons to the radiobutton RadioSelect.
        self.options_gcc=['opt1gcc','opt2gcc','opt3gcc','opt4gcc','opt5gcc','opt6gcc']
        for option in self.options_gcc:
            self.checkbuttonsCCMOptionsCompileTab_gcc.add(option)
# set default button
#        self.checkbuttonsCCMOptionsCompileTab_gcc.invoke(self.options_gcc[0])


# Compile gnu g77     

        self.checkbuttonsCCMOptionsCompileTab_g77=Pmw.RadioSelect(
            frameOptionsCompileTab,
            label_text = 'OPTIONS',
            buttontype = 'checkbutton',
            orient = 'vertical',
            labelpos = 'n',
            command = self.handlerCheckbuttonsCCMOptionsCompileTab,
            hull_borderwidth = 5,
            hull_relief = 'ridge',
            selectmode='multiple',
            )
# radiobuttons.pack(side = 'left', expand = 1, padx = 10, pady = 10)
        self.checkbuttonsCCMOptionsCompileTab_g77.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=0,
            pady=0,
            sticky=N
            )
# Add some buttons to the radiobutton RadioSelect.
        self.options_g77=['opt1g77','opt2g77','opt3g77','opt4g77','opt5g77','opt6g77']
        for option in self.options_g77:
            self.checkbuttonsCCMOptionsCompileTab_g77.add(option)
# set default button
#        self.checkbuttonsCCMOptionsCompileTab_g77.invoke(self.options_g77[0])

            
# Compile gnu g90

        self.checkbuttonsCCMOptionsCompileTab_g90=Pmw.RadioSelect(
            frameOptionsCompileTab,
            label_text = 'OPTIONS',
            buttontype = 'checkbutton',
            orient = 'vertical',
            labelpos = 'n',
            command = self.handlerCheckbuttonsCCMOptionsCompileTab,
            hull_borderwidth = 5,
            hull_relief = 'ridge',
            selectmode='multiple',
            )
# radiobuttons.pack(side = 'left', expand = 1, padx = 10, pady = 10)
        self.checkbuttonsCCMOptionsCompileTab_g90.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=0,
            pady=0,
            sticky=N
            )
# Add some buttons to the radiobutton RadioSelect.
        self.options_g90=['opt1g90','opt2g90','opt3g90','opt4g90','opt5g90','opt6g90']
        for option in self.options_g90:
            self.checkbuttonsCCMOptionsCompileTab_g90.add(option)
# set default button
#        self.checkbuttonsCCMOptionsCompileTab_g90.invoke(self.options_g90[0])


# Compile intel icc

        self.checkbuttonsCCMOptionsCompileTab_icc=Pmw.RadioSelect(
            frameOptionsCompileTab,
            label_text = 'OPTIONS',
            buttontype = 'checkbutton',
            orient = 'vertical',
            labelpos = 'n',
            command = self.handlerCheckbuttonsCCMOptionsCompileTab,
            hull_borderwidth = 5,
            hull_relief = 'ridge',
            selectmode='multiple',
            )
# radiobuttons.pack(side = 'left', expand = 1, padx = 10, pady = 10)
        self.checkbuttonsCCMOptionsCompileTab_icc.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=0,
            pady=0,
            sticky=N
            )
# Add some buttons to the radiobutton RadioSelect.
        self.options_icc=['opt1icc','opt2icc','opt3icc','opt4icc','opt5icc','opt6icc']
        for option in self.options_icc:
            self.checkbuttonsCCMOptionsCompileTab_icc.add(option)
# set default button
#        self.checkbuttonsCCMOptionsCompileTab_icc.invoke(self.options_icc[0])


# Compile intel if77

        self.checkbuttonsCCMOptionsCompileTab_if77=Pmw.RadioSelect(
            frameOptionsCompileTab,
            label_text = 'OPTIONS',
            buttontype = 'checkbutton',
            orient = 'vertical',
            labelpos = 'n',
            command = self.handlerCheckbuttonsCCMOptionsCompileTab,
            hull_borderwidth = 5,
            hull_relief = 'ridge',
            selectmode='multiple',
            )
# radiobuttons.pack(side = 'left', expand = 1, padx = 10, pady = 10)
        self.checkbuttonsCCMOptionsCompileTab_if77.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=0,
            pady=0,
            sticky=N
            )
# Add some buttons to the radiobutton RadioSelect.
        self.options_if77=['opt1if77','opt2if77','opt3if77','opt4if77','opt5if77','opt6if77']
        for option in self.options_if77:
            self.checkbuttonsCCMOptionsCompileTab_if77.add(option)
# set default button
#        self.checkbuttonsCCMOptionsCompileTab_if77.invoke(self.options_if77[0])


# Compile intel if90  

        self.checkbuttonsCCMOptionsCompileTab_if90=Pmw.RadioSelect(
            frameOptionsCompileTab,
            label_text = 'OPTIONS',
            buttontype = 'checkbutton',
            orient = 'vertical',
            labelpos = 'n',
            command = self.handlerCheckbuttonsCCMOptionsCompileTab,
            hull_borderwidth = 5,
            hull_relief = 'ridge',
            selectmode='multiple',
            )
# radiobuttons.pack(side = 'left', expand = 1, padx = 10, pady = 10)
        self.checkbuttonsCCMOptionsCompileTab_if90.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=0,
            pady=0,
            sticky=N
            )
# Add some buttons to the radiobutton RadioSelect.
        self.options_if90=['opt1if90','opt2if90','opt3if90','opt4if90','opt5if90','opt6if90']
        for option in self.options_if90:
            self.checkbuttonsCCMOptionsCompileTab_if90.add(option)
# set default button
#        self.checkbuttonsCCMOptionsCompileTab_if90.invoke(self.options_if90[0])


# Compile mpi mpicc

        self.checkbuttonsCCMOptionsCompileTab_mpicc=Pmw.RadioSelect(
            frameOptionsCompileTab,
            label_text = 'OPTIONS',
            buttontype = 'checkbutton',
            orient = 'vertical',
            labelpos = 'n',
            command = self.handlerCheckbuttonsCCMOptionsCompileTab,
            hull_borderwidth = 5,
            hull_relief = 'ridge',
            selectmode='multiple',
            )
# radiobuttons.pack(side = 'left', expand = 1, padx = 10, pady = 10)
        self.checkbuttonsCCMOptionsCompileTab_mpicc.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=0,
            pady=0,
            sticky=N
            )
# Add some buttons to the radiobutton RadioSelect.
        self.options_mpicc=['opt1mpicc','opt2mpicc','opt3mpicc','opt4mpicc','opt5mpicc','opt6mpicc']
        for option in self.options_mpicc:
            self.checkbuttonsCCMOptionsCompileTab_mpicc.add(option)
# set default button
#        self.checkbuttonsCCMOptionsCompileTab_mpicc.invoke(self.options_mpicc[0])


# Compile mpi mpif77

        self.checkbuttonsCCMOptionsCompileTab_mpif77=Pmw.RadioSelect(
            frameOptionsCompileTab,
            label_text = 'OPTIONS',
            buttontype = 'checkbutton',
            orient = 'vertical',
            labelpos = 'n',
            command = self.handlerCheckbuttonsCCMOptionsCompileTab,
            hull_borderwidth = 5,
            hull_relief = 'ridge',
            selectmode='multiple',
            )
# radiobuttons.pack(side = 'left', expand = 1, padx = 10, pady = 10)
        self.checkbuttonsCCMOptionsCompileTab_mpif77.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=0,
            pady=0,
            sticky=N
            )
# Add some buttons to the radiobutton RadioSelect.
        self.options_mpif77=['opt1mpif77','opt2mpif77','opt3mpif77','opt4mpif77','opt5mpif77','opt6mpif77']
        for option in self.options_mpif77:
            self.checkbuttonsCCMOptionsCompileTab_mpif77.add(option)
# set default button
#        self.checkbuttonsCCMOptionsCompileTab_mpif77.invoke(self.options_mpif77[0])

# Compile mpi mpif90

        self.checkbuttonsCCMOptionsCompileTab_mpif90=Pmw.RadioSelect(
            frameOptionsCompileTab,
            label_text = 'OPTIONS',
            buttontype = 'checkbutton',
            orient = 'vertical',
            labelpos = 'n',
            command = self.handlerCheckbuttonsCCMOptionsCompileTab,
            hull_borderwidth = 5,
            hull_relief = 'ridge',
            selectmode='multiple',
            )
# radiobuttons.pack(side = 'left', expand = 1, padx = 10, pady = 10)
        self.checkbuttonsCCMOptionsCompileTab_mpif90.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=0,
            pady=0,
            sticky=N
            )
# Add some buttons to the radiobutton RadioSelect.
        self.options_mpif90=['opt1mpif90','opt2mpif90','opt3mpif90','opt4mpif90','opt5mpif90','opt6mpif90']
        for option in self.options_mpif90:
            self.checkbuttonsCCMOptionsCompileTab_mpif90.add(option)
# set default button
#        self.checkbuttonsCCMOptionsCompileTab_mpif90.invoke(self.options_mpif90[0])

              
# Compile pgi pgcc

        self.checkbuttonsCCMOptionsCompileTab_pgcc=Pmw.RadioSelect(
            frameOptionsCompileTab,
            label_text = 'OPTIONS',
            buttontype = 'checkbutton',
            orient = 'vertical',
            labelpos = 'n',
            command = self.handlerCheckbuttonsCCMOptionsCompileTab,
            hull_borderwidth = 5,
            hull_relief = 'ridge',
            selectmode='multiple',
            )
# radiobuttons.pack(side = 'left', expand = 1, padx = 10, pady = 10)
        self.checkbuttonsCCMOptionsCompileTab_pgcc.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=0,
            pady=0,
            sticky=N
            )
# Add some buttons to the radiobutton RadioSelect.
        self.options_pgcc=['opt1pgcc','opt2pgcc','opt3pgcc','opt4pgcc','opt5pgcc','opt6pgcc']
        for option in self.options_pgcc:
            self.checkbuttonsCCMOptionsCompileTab_pgcc.add(option)
# set default button
#        self.checkbuttonsCCMOptionsCompileTab_pgcc.invoke(self.options_pgcc[0])

 
# Compile pgi pf77

        self.checkbuttonsCCMOptionsCompileTab_pf77=Pmw.RadioSelect(
            frameOptionsCompileTab,
            label_text = 'OPTIONS',
            buttontype = 'checkbutton',
            orient = 'vertical',
            labelpos = 'n',
            command = self.handlerCheckbuttonsCCMOptionsCompileTab,
            hull_borderwidth = 5,
            hull_relief = 'ridge',
            selectmode='multiple',
            )
# radiobuttons.pack(side = 'left', expand = 1, padx = 10, pady = 10)
        self.checkbuttonsCCMOptionsCompileTab_pf77.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=0,
            pady=0,
            sticky=N
            )
# Add some buttons to the radiobutton RadioSelect.
        self.options_pf77=['opt1pf77','opt2pf77','opt3pf77','opt4pf77','opt5pf77','opt6pf77']
        for option in self.options_pf77:
            self.checkbuttonsCCMOptionsCompileTab_pf77.add(option)
# set default button
#        self.checkbuttonsCCMOptionsCompileTab_pf77.invoke(self.options_pf77[0])


# Compile pgi pf90

        self.checkbuttonsCCMOptionsCompileTab_pf90=Pmw.RadioSelect(
            frameOptionsCompileTab,
            label_text = 'OPTIONS',
            buttontype = 'checkbutton',
            orient = 'vertical',
            labelpos = 'n',
            command = self.handlerCheckbuttonsCCMOptionsCompileTab,
            hull_borderwidth = 5,
            hull_relief = 'ridge',
            selectmode='multiple',
            )
# radiobuttons.pack(side = 'left', expand = 1, padx = 10, pady = 10)
        self.checkbuttonsCCMOptionsCompileTab_pf90.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=0,
            pady=0,
            sticky=N
            )
# Add some buttons to the radiobutton RadioSelect.
        self.options_pf90=['opt1pf90','opt2pf90','opt3pf90','opt4pf90','opt5pf90','opt6pf90']
        for option in self.options_pf90:
            self.checkbuttonsCCMOptionsCompileTab_pf90.add(option)
# set default button
#        self.checkbuttonsCCMOptionsCompileTab_pf90.invoke(self.options_pf90[0])


# Config

        self.checkbuttonsCCMOptionsCompileTab_config=Pmw.RadioSelect(
            frameOptionsCompileTab,
            label_text = 'OPTIONS',
            buttontype = 'checkbutton',
            orient = 'vertical',
            labelpos = 'n',
            command = self.handlerCheckbuttonsCCMOptionsCompileTab,
            hull_borderwidth = 5,
            hull_relief = 'ridge',
            selectmode='multiple',
            )
# radiobuttons.pack(side = 'left', expand = 1, padx = 10, pady = 10)
        self.checkbuttonsCCMOptionsCompileTab_config.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=0,
            pady=0,
            sticky=N
            )
# Add some buttons to the radiobutton RadioSelect.
        self.options_config=['opt1config','opt2config','opt3config','opt4congif','opt5config','opt6config']
        for option in self.options_config:
            self.checkbuttonsCCMOptionsCompileTab_config.add(option)
# set default button
#        self.checkbuttonsCCMOptionsCompileTab_config.invoke(self.options_config[0])


# Make

        self.checkbuttonsCCMOptionsCompileTab_make=Pmw.RadioSelect(
            frameOptionsCompileTab,
            label_text = 'OPTIONS',
            buttontype = 'checkbutton',
            orient = 'vertical',
            labelpos = 'n',
            command = self.handlerCheckbuttonsCCMOptionsCompileTab,
            hull_borderwidth = 5,
            hull_relief = 'ridge',
            selectmode='multiple',
            )
# radiobuttons.pack(side = 'left', expand = 1, padx = 10, pady = 10)
        self.checkbuttonsCCMOptionsCompileTab_make.grid(
            row=0,
            column=0,
            columnspan=1,
            rowspan=1,
            padx=0,
            pady=0,
            sticky=N
            )
# Add some buttons to the radiobutton RadioSelect.
        self.options_make=['opt1make','opt2make','opt3make','opt4make','opt5make','opt6make']
        for option in self.options_make:
            self.checkbuttonsCCMOptionsCompileTab_make.add(option)
# set default button
#        self.checkbuttonsCCMOptionsCompileTab_make.invoke(self.options_make[0])

        return
        
            
    def boxFilesCompileTab(self,parent):
        '''
        Purpose:
            Define the FILES box for the Compile Tab. Used to
        choose Source, Executable, and Compilation Output
        filenames.
        
        Important output variables:
          self.comboCompileSourceFilenameFilesCompileTab
          self.comboCompileExecutableFilenameFilesCompileTab
          self.comboCompileOutputFilenameFilesCompileTab
          
        '''
# first, create the surrounding frame
        frameFilesCompileTab=Frame(
            parent,
            width=500,
            height=300,
            relief=RIDGE,
            borderwidth=5,
            )
        frameFilesCompileTab.grid(
            row=0, 
            column=3,
            rowspan=1,
            columnspan=1,
            padx=10,
            pady=5,
            sticky=N,
            )
# Label at top of frame
        labelFilesCompileTab=Label(
            frameFilesCompileTab,
            text='FILES',
            )
        labelFilesCompileTab.grid(
            row=0,
            column=0,
            pady=2
            )
# Next, specify working directory
#   DWB - needs to be done!
# specify temporary source filename
#        filesSource = (' ','file1.c', 'file2.c', 'file3.c', 'file4.c')
        
        self.comboCompileSourceFilenameFilesCompileTab = Pmw.ComboBox(
            frameFilesCompileTab,
            label_text=' Source  \n filename    ',
            labelpos='w',
            selectioncommand=self.handlerComboCompileSourceFilenameFilesCompileTab,
            scrolledlist_items=self.listSourceFiles,
            scrolledlist_hull_width=500,
            )
# dropdown.pack(side = 'left', anchor = 'n', fill = 'x', expand = 1, padx = 8, pady = 8)
        self.comboCompileSourceFilenameFilesCompileTab.grid(
            row=1,
            column=0,
            padx=10,
            pady=2,
            )
# Display the default file
        if len(self.listSourceFiles) <> 0:
            self.comboCompileSourceFilenameFilesCompileTab.selectitem(self.listSourceFiles[0])
        else:
            self.comboCompileSourceFilenameFilesCompileTab.setentry('')
        
# specify temporary executables
#        filesExecutable = (' ','file1.exe','file2.exe','file3.exe')
        self.comboCompileExecutableFilenameFilesCompileTab = Pmw.ComboBox(
            frameFilesCompileTab,
            label_text = 'Executable\nfilename',
            labelpos = 'w',
            selectioncommand = self.handlerComboCompileExecutableFilenameFilesCompileTab,
            scrolledlist_items = self.listExecutableFiles,
            scrolledlist_hull_width=500,
            )
# dropdown.pack(side = 'left', anchor = 'n', fill = 'x', expand = 1, padx = 8, pady = 8)
        self.comboCompileExecutableFilenameFilesCompileTab.grid(
            row=2,
            column=0,
            padx=10,
            pady=2,
            )
# Display the default filename
        if len(self.listExecutableFiles) <> 0:
            self.comboCompileExecutableFilenameFilesCompileTab.selectitem(self.listExecutableFiles[0])
        else:
            self.comboCompileExecutableFilenameFilesCompileTab.setentry('')
        
# specify temporary compilation output filename
#        filesOutput = (' ','file1.out','file2.out','file3.out')
        self.comboCompileOutputFilenameFilesCompileTab = Pmw.ComboBox(
            frameFilesCompileTab,
            label_text = 'Compilation\noutput\nfilename',
            labelpos = 'w',
            selectioncommand = self.handlerComboCompileOutputFilenameFilesCompileTab,
            scrolledlist_items = self.listCompileOutputFiles,
            scrolledlist_hull_width=500,
            )
        self.comboCompileOutputFilenameFilesCompileTab.grid(
            row=3,
            column=0,
            padx=10,
            pady=2,
            )
# Display the default filename
        if len(self.listCompileOutputFiles) <> 0:
            self.comboCompileOutputFilenameFilesCompileTab.selectitem(self.listCompileOutputFiles[0])
        else:
            self.comboCompileOutputFilenameFilesCompileTab.setentry('')
            
        return
        
        
        
    def boxOtherCompileOptionsCompileTab(self,parent):
        '''
        Purpose:
            enter other compile options that are not
        specified in the OPTIONS box.
        '''
# create separate frame
        frameOtherCompileOptionsCompileTab=Frame(
            parent,
            background=backgroundBottomFrameCompileTab
            )
        frameOtherCompileOptionsCompileTab.grid(
            row=1,
            column=0,
            columnspan=99,
            rowspan=1,
            )

# for use when active            
        self.labelOtherCompileOptionsCompileTab=Label(
            frameOtherCompileOptionsCompileTab,
            text='Other compile\noptions:',
            relief=RIDGE,
            borderwidth=5,
            )
        self.labelOtherCompileOptionsCompileTab.grid(
            row=0,
            column=0,
            sticky=E,
            padx=5,
            )
            
        self.entryOtherCompileOptionsDataCompileTab=StringVar()
        self.entryOtherCompileOptionsDataCompileTab.set('')
        
        self.entryOtherCompileOptionsCompileTab=Entry(
            frameOtherCompileOptionsCompileTab,
            textvariable=self.entryOtherCompileOptionsDataCompileTab,
            borderwidth=5,
            relief=SUNKEN,
            width=75,
            )
        self.entryOtherCompileOptionsCompileTab.grid(
            row=0,
            column=1,
            sticky=W,
            padx=5,
            )
         
        self.buttonClearOtherCompileOptionsCompileTab=Button(
            frameOtherCompileOptionsCompileTab,
            command=self.handlerEntryOtherCompileOptionsCompileTab,
            text="Clear",
            justify=LEFT,
            relief=RAISED,
            borderwidth=5,
            )
        self.buttonClearOtherCompileOptionsCompileTab.grid(
            row=0,
            column=2,
            columnspan=1,
            padx=2,
            sticky=W,
            )
            
# for use when inactive

        self.labelOtherCompileOptionsCompileTab_Inactive=Label(
            frameOtherCompileOptionsCompileTab,
            text='Other compile\noptions:',
            relief=RIDGE,
            borderwidth=5,
            bg='lightgray',
            fg='darkgray',
            )
        self.labelOtherCompileOptionsCompileTab_Inactive.grid(
            row=0,
            column=0,
            sticky=E,
            padx=5
            )
        
        self.entryOtherCompileOptionsCompileTab_Inactive=Label(
            frameOtherCompileOptionsCompileTab,
            text='Not applicable for this COMMAND',
            borderwidth=5,
            relief=SUNKEN,
            width=66,
            bg='lightgray',
            fg='darkgray',
            anchor=W,
            )
        self.entryOtherCompileOptionsCompileTab_Inactive.grid(
            row=0,
            column=1,
            sticky=W,
            padx=5,
            )
         
        self.buttonClearOtherCompileOptionsCompileTab_Inactive=Label(
            frameOtherCompileOptionsCompileTab,
            text="Clear",
            justify=LEFT,
            relief=RAISED,
            borderwidth=5,
            bg='lightgray',
            fg='darkgray',
            )
        self.buttonClearOtherCompileOptionsCompileTab_Inactive.grid(
            row=0,
            column=2,
            columnspan=1,
            padx=2,
            sticky=W,
            )
# Hide now; invoke later
        self.handlerOtherCompileOptionsCompileTab_ActiveInactive(1)
        
        return
        
        
    def buttonsCompileKillCompileTab(self,parent):
        '''
        Purpose:
            COMPILE and KILL process buttons
        '''
# COMPILE and KILL PROCESS buttons
        frameAssembleCompileKillCompileTab=Frame(parent,
            relief=None,
            borderwidth=0,
            bg=backgroundBottomFrameCompileTab,
            )
        frameAssembleCompileKillCompileTab.grid(
            row=3,
            column=0,
            columnspan=99,
            )
            
        self.buttonAssembleCompileCommandCompileTab=Button(
            frameAssembleCompileKillCompileTab,
            command=self.handlerButtonAssembleCompileTab,
            text='ASSEMBLE command line',
            relief=RAISED,
            borderwidth=5,
            )
        self.buttonAssembleCompileCommandCompileTab.grid(
            row=0,
            column=0,
            padx=20,
            pady=2
            )
            
        self.buttonCompileCompileTab=Button(
            frameAssembleCompileKillCompileTab,
            command=self.handlerButtonCompileCompileTab,
            text='EXECUTE',
            relief=RAISED,
            borderwidth=5,
            )
        self.buttonCompileCompileTab.grid(
            row=0,
            column=1,
            padx=5,
            pady=2,
            )
            
        self.buttonKillCompileTab=Button(
            frameAssembleCompileKillCompileTab,
            command=self.handlerButtonKillCompileTab,
            text='KILL execution',
            relief=RAISED,
            borderwidth=5,
            )
        self.buttonKillCompileTab.grid(
            row=0,
            column=2,
#            sticky=W,
            padx=5,
            pady=2,
            )
            
        return
        
        
    def boxOutputCommandsCompileTab(self,parent):
        '''
        Purpose:
            define widgets for output commands for compile tab
        '''
        self.labelOutputCommandsCompileTab=Label(
            parent,
            text='OUTPUT',
            justify=CENTER,
            bg='darkgray',
            )
        self.labelOutputCommandsCompileTab.grid(
            row=2,
            padx=0,
            pady=0,
            )
        self.boxOutputCommandsCompileTab=Text(
            parent,
            font=self.dataFont,
            borderwidth=5,
            relief=RIDGE,
            wrap=WORD,
            height=10,
            width=100,
            bg='black',
            fg='green',
            )
        self.boxOutputCommandsCompileTab.grid(
            row=3,
            column=0,
            padx=0,
            pady=5,
            sticky=N+S+E+W
            )
        self.boxOutputCommandsCompileTab.insert(
            END,
            '<OUTPUT>'
            ) 

        return

# Initialize boxes in COMPILE TAB
    def initializeCompileTab(self):    
        '''
        Purpose:
            Initialize box
        '''
# initially disable subcommands under Compile
        self.subCompileOption1CommandCompileTab['state']=DISABLED
        self.subCompileOption2CommandCompileTab['state']=DISABLED
        self.subCompileOption3CommandCompileTab['state']=DISABLED
        self.subCompileOption4CommandCompileTab['state']=DISABLED

# Invoke and hide after all grids are defined; otherwise, handlers will fail       
# Invoke default values; hide all grids but one used as default
# LANGUAGE BOXES
# Local run: Invoke the default; do not hide
        self.radiobuttonsCompileForLocalRunLanguageCompileTab.grid()
# Gnu: Invoke the default and hide
        self.radiobuttonsCompileGnuLanguageCompileTab.grid_remove()
# Intel: Invoke the default and hide
        self.radiobuttonsCompileIntelLanguageCompileTab.grid_remove()
# Mpi: Invoke the default and hide
        self.radiobuttonsCompileMpiLanguageCompileTab.grid_remove()
# Pgi: Invoke the default and hide
        self.radiobuttonsCompilePgiLanguageCompileTab.grid_remove()
# Blank: Nothing to invoke; just hide
        self.radiobuttonsCompileNothingLanguageCompileTab.grid_remove()
      
# OPTIONS BOXES
#   localcc: do not hide the grid
        self.checkbuttonsCCMOptionsCompileTab_localcc.grid()
#   localf77: hide the grid
        self.checkbuttonsCCMOptionsCompileTab_localf77.grid_remove()
#   localf90: hide the grid
        self.checkbuttonsCCMOptionsCompileTab_localf90.grid_remove()
#   gcc: hide the grid
        self.checkbuttonsCCMOptionsCompileTab_gcc.grid_remove()
#   g77: hide the grid
        self.checkbuttonsCCMOptionsCompileTab_g77.grid_remove()
#   g90: hide the grid
        self.checkbuttonsCCMOptionsCompileTab_g90.grid_remove()
#   icc: hide the grid
        self.checkbuttonsCCMOptionsCompileTab_icc.grid_remove()
#   if77: hide the grid
        self.checkbuttonsCCMOptionsCompileTab_if77.grid_remove()
#   if90: hide the grid
        self.checkbuttonsCCMOptionsCompileTab_if90.grid_remove()
#   mpicc: hide the grid
        self.checkbuttonsCCMOptionsCompileTab_mpicc.grid_remove()
#   mpif77: hide the grid
        self.checkbuttonsCCMOptionsCompileTab_mpif77.grid_remove()
#   mpif90: hide the grid
        self.checkbuttonsCCMOptionsCompileTab_mpif90.grid_remove()
#   pgcc: hide the grid
        self.checkbuttonsCCMOptionsCompileTab_pgcc.grid_remove()
#   pf77: hide the grid
        self.checkbuttonsCCMOptionsCompileTab_pf77.grid_remove()
#   pf90: hide the grid
        self.checkbuttonsCCMOptionsCompileTab_pf90.grid_remove()
#   config: hide the grid
        self.checkbuttonsCCMOptionsCompileTab_config.grid_remove()
#   make: hide the grid
        self.checkbuttonsCCMOptionsCompileTab_make.grid_remove()
        
        return
        
                
            
#  ----- end of COMPILE TAB METHODS ----- 

#  ----- SETUP TAB METHODS ----- 

# dummy def
    def ZZ___SETUP_TAB_METHODS():
        pass
        
        return
        
        
    def frameSetupCreate(self,parent,msg):
        ''' 
        Purpose:
            create the scrolled frame for this tab
        '''
        
        self.frameSetup = Pmw.ScrolledFrame(
            parent,
            borderframe = 1,
            labelpos = N,
            label_text = msg,
            label_font=self.titleFont,
            usehullsize = 1,
            hull_width = globalHullWidth,
            hull_height = globalHullHeight,
            hscrollmode='dynamic',
            vscrollmode='dynamic',
            horizflex='elastic', # 'expand' centers interior frames when window is stretched; ...
            vertflex='fixed',  # ...   do not use 'elastic' which kills scrollbars
            )
        self.frameSetup.pack(
            padx=5, 
            pady=5, 
            fill='both', 
            expand='YES',
            )
            
        self.frameSetup.interior().grid_rowconfigure(0,weight=1)
        self.frameSetup.interior().grid_columnconfigure(0,weight=1) 
        self.frameSetup.interior().grid_rowconfigure(1,weight=1)
        self.frameSetup.interior().grid_columnconfigure(1,weight=1)
            
        Pmw.Color.changecolor(parent, background=backgroundSetupTab)  
        
        return
        

    def framesInterior_tabSetup(self,parent):
        '''
        Purpose:
            create top and bottom frames for the RUN tab
        '''  

# Top    
        self.tabSetup_TopFrame=Frame(
            parent,
            relief=RIDGE,
            borderwidth=5,
            bg=backgroundTopFrameSetupTab,
            )
        self.tabSetup_TopFrame.grid(
            row=0,
            column=0,
            padx=0,
            pady=5,
            sticky=N
            )
# Bottom
        self.tabSetup_BottomFrame=Frame(
            parent,
            relief=RIDGE,
            borderwidth=5,
            bg=backgroundBottomFrameSetupTab,
            )
        self.tabSetup_BottomFrame.grid(
            row=1,
            column=0,
#            columnspan=5,
#            rowspan=1,
            padx=0,
            pady=5,
            )

        Pmw.Color.changecolor(self.tabSetup_BottomFrame, background=backgroundSetupTab)
        
        return
        

    def frameBottom_tabSetup(self,parent):
        '''
        Purpose:
           setup frames, widgets, and editor for modifying
           input files
        '''
        
# import editor
        import module_Editor2
        
        self.frameLeftSetup = Frame(
            parent,
            bg=backgroundBottomFrameSetupTab,
            )
        self.frameLeftSetup.grid(
            row=0,
            column=0,
#            sticky=W,
            padx=10,
            pady=5,
            sticky=N,
            )

# for INPUT FILE editor buttons            
        self.frameLeftSetup00 = Frame(
            self.frameLeftSetup,
            bg=backgroundBottomFrameSetupTab,
            )
        self.frameLeftSetup00.grid(
            row=0,
            column=0,
            sticky=N,
            )
            
# for INPUT FILE modify buttons   
        self.frameLeftSetup10 = Frame(
            self.frameLeftSetup,
            bg=backgroundBottomFrameSetupTab,
            )
        self.frameLeftSetup10.grid(
            row=1,
            column=0,
            )
         
            
        self.frame1 = Frame(
            parent,
            bg=backgroundBottomFrameSetupTab,
            )
        self.frame1.grid(
            row=0,
            column=1,
#            sticky=E,
            padx=10,
            pady=5
            )

# put setup widgets in frame 0 and editor in frame 1
#        module_Editor.my_Editor
        instance_Setup = module_Editor2.Editor(
            self.frameLeftSetup00,
            self.frame1,
            backgroundBottomFrameSetupTab,
            'INPUT FILE',
            self.titleFont,
            self.dataFont,
            )
            
        labelModify = Label(
            self.frameLeftSetup10,
            text='MODIFY',
            bg=backgroundBottomFrameSetupTab,
            font=self.titleFont,
            )
        labelModify.grid(
            row=0,
            column=0,
            columnspan=99,
            pady=10,
            )
            
        self.buttonModifySetup_Topo = Button(
            self.frameLeftSetup10,
            text='topology',
            font=self.buttonFont,
            borderwidth=5,
            relief=RAISED,
            width=10,
            )
        self.buttonModifySetup_Topo.grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            )
            
        self.buttonModifySetup_Var2 = Button(
            self.frameLeftSetup10,
            text='frontEnd',
            font=self.buttonFont,
            borderwidth=5,
            relief=RAISED,
            width=10,
            )
        self.buttonModifySetup_Var2.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
            )
            
        self.buttonModifySetup_Var3 = Button(
            self.frameLeftSetup10,
            text='otherVar',
            font=self.buttonFont,
            borderwidth=5,
            relief=RAISED,
            width=10,
            )
        self.buttonModifySetup_Var3.grid(
            row=1,
            column=2,
            padx=5,
            pady=5,
            )
            
        return
        

#  ----- end of SETUP TAB METHODS ----- 

#  ----- RUN TAB METHODS ----- 

# dummy def
    def ZZ___RUN_TAB_METHODS():
        pass
        
        return
        
        
    def frameRunCreate(self,parent,msg):
        '''
        Purpose:
            create the scrolled frame for this tab
        '''
        self.frameRun = Pmw.ScrolledFrame(
            parent,
            borderframe = 1,
            labelpos = N,
            label_text = msg,
            label_font=self.titleFont,
            usehullsize = 1,
            hull_width = globalHullWidth,
            hull_height = globalHullHeight,
            hscrollmode='dynamic',
            vscrollmode='dynamic',
            horizflex='elastic', # 'expand' centers interior frames when window is stretched; ...
            vertflex='fixed',  # ...   do not use 'elastic' which kills scrollbars
            )
        self.frameRun.pack(
            padx=5, 
            pady=5, 
            fill='both', 
            expand='YES',
            )
            
        self.frameRun.interior().grid_rowconfigure(0,weight=1)
        self.frameRun.interior().grid_columnconfigure(0,weight=1) 
        self.frameRun.interior().grid_rowconfigure(1,weight=1)
        self.frameRun.interior().grid_columnconfigure(1,weight=1)
            
        Pmw.Color.changecolor(
            parent, 
            background=backgroundRunTab
            )
            
        return
        
        

    def framesInterior_tabRun(self,parent):
        '''
        Purpose:
            create top and bottom frames for the RUN tab
        '''  

# top    
        self.tabRun_TopFrame=Frame(
            parent,
            relief=RIDGE,
            borderwidth=5,
            bg=backgroundTopFrameRunTab,
            )
        self.tabRun_TopFrame.grid(
            row=0,
            column=0,
            padx=0,
            pady=5,
            sticky=N
            )
# bottom
        self.tabRun_BottomFrame=Frame(
            parent,
            relief=RIDGE,
            borderwidth=5,
            bg=backgroundBottomFrameRunTab,
            )
        self.tabRun_BottomFrame.grid(
            row=1,
            column=0,
            padx=0,
            pady=5,
            )

        Pmw.Color.changecolor(self.tabRun_BottomFrame, background=backgroundRunTab)

        return
        

    def buttonsHertRunTab(self,parent):
        '''
        Purpose:
            define HERT buttons on RUN tab
        '''
        
        frameHertRunTab=Frame(
            parent,
            bg=backgroundBottomFrameRunTab,
            )
        frameHertRunTab.grid(
            row=0,
            column=0,
            columnspan=99,
            )
        
        self.labelHert=Label(
            frameHertRunTab,
            text="Before running on Sandia's clusters and  \
            \nsupercomputers, submit a work estimate via HERT:",
            bg=backgroundBottomFrameRunTab,
            fg='white',
            relief=FLAT,
            borderwidth=5,
            justify=RIGHT,
            )
        self.labelHert.grid(
            row=0,
            column=0,
            sticky=E
            )

        self.buttonHert=Button(
            frameHertRunTab,
            text='Submit Work Estimate',
            justify=CENTER,
            relief=RAISED,
            borderwidth=5,
            command=self.handlerButtonHert,
            font=self.buttonFont,
            )
        self.buttonHert.grid(
            row=0,
            column=1,
            sticky=W
            )
        
        self.buttonWhatIsHert=Button(
            frameHertRunTab,
            text='What is HERT?',
            justify=CENTER,
            relief=RAISED,
            borderwidth=5,
            command=self.handlerButtonWhatIsHert,
            font=self.buttonFont,
            )
        self.buttonWhatIsHert.grid(
            row=0,
            column=2,
            sticky=W,
            padx=5
            )
            
        return
        
            
    def boxQueueRunTab(self,parent):
        '''
        Purpose:
            construct Run Queue selections using radiobuttons
        
        Output variables take on the following values:
       
        self.stringQueueRunTab:
           - queueNone
           - queueBatch
           - queueInteractive
       
        ...and when queueBatch is selected...
       
        self.stringSubBatchOptionsQueueRunTab:
           - queueBatchStandard
           - queueBatchExpress
           - queueBatchOther
           
        Use get() and set() methods to get and set values of the output variables
        '''
        
# create frame for Queue box
        frameQueueRunTab=Frame(
            parent,
            relief=RIDGE,
            borderwidth=5,
            )
        frameQueueRunTab.grid(
            row=1,
            column=0,
            padx=10,
            pady=5,
            sticky=N,
            )

# label for Queue box            
        labelQueueRunTab=Label(
            frameQueueRunTab,
            text='QUEUE',
            justify=CENTER,
            )
        labelQueueRunTab.grid(
            row=0,
            column=0,
            columnspan=1,
            pady=5,
            sticky=N,
            )

# string variable to set upon selection
        self.stringQueueRunTab=StringVar()
        self.stringQueueRunTab.set('queueNone')

# define radiobuttons
#    None (just run executable)
        self.buttonQueueNoneRunTab=Radiobutton(
            frameQueueRunTab,
            variable=self.stringQueueRunTab,
            text='None\n(just run executable)',
            command=self.handlerQueueRunTab,
            value='queueNone',
            justify=LEFT,
            )
        self.buttonQueueNoneRunTab.grid(
            row=1,
            column=0,
            sticky=W,
            )
#     set this button as default
        self.buttonQueueNoneRunTab.select()

#    Batch (uses QSUB)
        self.buttonQueueBatchRunTab=Radiobutton(
            frameQueueRunTab,
            variable=self.stringQueueRunTab,
            text='Batch\n(uses QSUB)',
            command=self.handlerQueueRunTab,
            value='queueBatch',
            justify=LEFT,
            )
        self.buttonQueueBatchRunTab.grid(
            row=2,
            column=0,
            sticky=W,
            )

# frame for subqueues under Batch
        frameUnderBatchQueueRunTab=Frame(
            frameQueueRunTab
            )
        frameUnderBatchQueueRunTab.grid(
            row=3,
            column=0,
            sticky=W,
            )        

#    Interactive (uses YOD)
        self.buttonQueueInteractiveRunTab=Radiobutton(
            frameQueueRunTab,
            variable=self.stringQueueRunTab,
            text='Interactive\n(uses YOD)',
            command=self.handlerQueueRunTab,
            value='queueInteractive',
            justify=LEFT,
            )
        self.buttonQueueInteractiveRunTab.grid(
            row=4,
            column=0,
            sticky=W,
            )
            
# sub-buttons under Batch
#    define variable to set upon selection of Batch
        self.stringSubBatchOptionsQueueRunTab=StringVar()
        self.stringSubBatchOptionsQueueRunTab.set('queueBatchStandard')
        
#    Batch standard queue
        self.subBatchOption1QueueRunTab=Radiobutton(
            frameUnderBatchQueueRunTab,
            variable=self.stringSubBatchOptionsQueueRunTab,
            text='Standard',
            command=self.handlerQueueRunTab,
            value='queueBatchStandard',
            justify=LEFT,
            )
        self.subBatchOption1QueueRunTab.grid(
            row=0,
            column=0,
            padx=20,
            pady=0,
            sticky=W,
            )
#     set as default for the sub-buttons
        self.subBatchOption1QueueRunTab.select()

#    Batch express queue
        self.subBatchOption2QueueRunTab=Radiobutton(
            frameUnderBatchQueueRunTab,
            variable=self.stringSubBatchOptionsQueueRunTab,
            text='Express',
            command=self.handlerQueueRunTab,
            value='queueBatchExpress',
            justify=LEFT,
            )
        self.subBatchOption2QueueRunTab.grid(
            row=1,
            column=0,
            padx=20,
            pady=0,
            sticky=W,
            ) 
            
#    Batch other queue
        self.subBatchOption3QueueRunTab = Radiobutton(
            frameUnderBatchQueueRunTab,
            variable=self.stringSubBatchOptionsQueueRunTab,
            text='Other',
            command=self.handlerQueueRunTab,
            value='queueBatchOther',
            justify=LEFT,
            )
        self.subBatchOption3QueueRunTab.grid(
            row=2,
            column=0,
            padx=20,
            pady=0,
            sticky=W,
            ) 
            
        return
        

    def entryFrameRunTab(self,parent):
        '''
        Purpose:
            Generates 3 frames, depending on the selection from
        the QUEUE box.
        
        Called by:
            buildRun
            
        Calls:
        
        Important output variables:
            If 'None (just run executable)' is selected, grid:
            
            self.runspecsNoneQueueFrame
        and if 'Batch'
            self.runspecsBatchQueuesFrame
        and if 'Interactive'
            self.runspecsInteractiveQueueFrame
            
        Depending on queue selected, user must 
        input number of nodes, processors, cores,
        max job runtime (hours, minutes), etc.
        
        Pmw widgets:
          - in frame frameLabelHrsMins:
                self.runtimeHrs
                self.runtimeMins
            
          - in frame frameRunSpecsEntry:
                self.numNodes
                self.numProcsPerNode
                self.numCoresPerProc
                self.numProcs
                self.numCores
                self.numProject
                self.numTask
                self.paramsQsub
                self.paramsYod
              
        Tk widgets:
          - in frame frameLabelHrsMins
                self.labelHrsMins
                
        Widgets not needed for a particular queue are disabled
        in handlers.
        
        To disable/enable Pmw widgets, 2 ways are shown below:          
          self.numCoresPerProc.configure(entry_state='disabled')
          self.numCoresPerProc['entry_state']='normal'
          
        To disable/enable Tk widgets, for example:
          self.labelHrsMins.configure(state=DISABLED)
          self.labelHrsMins['state']='disabled'
          and
          self.labelHrsMins.configure(state=NORMAL)
          self.labelHrsMins['state']='normal'
        '''

# define all Run Specs:   
#  main frame     
        self.runspecsBatchQueuesFrame=Frame(
            parent,
            relief=RIDGE,
            borderwidth=5,
            )
        self.runspecsBatchQueuesFrame.grid(
            row=1,
            column=1,
            sticky=N,
            padx=10,
            pady=5,
            )

# Define top label; put in separate frame          
        labelRunSpecsFrame=Frame(
            self.runspecsBatchQueuesFrame,
            )
        labelRunSpecsFrame.grid(
            row=0,
            column=0,
            )
            
        labelRunSpecs=Label(
            labelRunSpecsFrame,
            text='RUN SPECS FOR QUEUES',
            justify=CENTER
            )
        labelRunSpecs.grid(
            row=0,
            column=0,
            pady=5,
            )
            
# define frame for hours and minutes
        frameLabelHrsMins=Frame(
            self.runspecsBatchQueuesFrame,
            )
        frameLabelHrsMins.grid(
            row=1,
            column=0,
            pady=2,
            sticky=W,
            )
            
# define entry fields for hours and minutes
        self.labelHrsMins=Label(
            frameLabelHrsMins,
            text='Max run time',
            )       
        self.labelHrsMins.grid(
            row=0,
            column=0,
            padx=10,
            pady=0,
            sticky=SW,
            )
            
# define blank label for spacing
        labelBlank=Label(
            frameLabelHrsMins,
            text=' ',
            )
        labelBlank.grid(
            row=0,
            column=1,
            padx=20,
            pady=0,
            )
                        
# define EntryField for Hours            
        self.runtimeHrs=Pmw.EntryField(
            frameLabelHrsMins,
            labelpos=N,
            label_text='Hrs',
            validate={
                'validator':'integer',
                'min':0,
                'max':9999,
                'minstrict':1,
                'maxstrict':0},
            value=0,
            modifiedcommand=self.handlerRunHH,
            )
        self.runtimeHrs.grid(
            row=0,
            column=2,
            padx=5,
            pady=0,
            )
        self.runtimeHrs.configure(entry_width=4)
  
# use colon to separate Hrs and Mins            
        labelColon=Label(
            frameLabelHrsMins,
            text=':',
            )
        labelColon.grid(
            row=0,
            column=3,
            padx=5,
            pady=0,
            sticky=S
            )

# define EntryField for Mins            
        self.runtimeMins=Pmw.EntryField(
            frameLabelHrsMins,
            labelpos=N,
            label_text='Mins',
            validate={
                'validator':'integer',
                'min':0,
                'max':59,
                'minstrict':1,
                'maxstrict':1},
            value=10,
            modifiedcommand=self.handlerRunMM,
            )
        self.runtimeMins.grid(
            row=0,
            column=4,
            padx=5,
            pady=0,
            )
        self.runtimeMins.configure(entry_width=2) 
        
# define frame for remaining entry fields using Pmw.EntryField         
        frameRunSpecsEntry=Frame(
            self.runspecsBatchQueuesFrame,
            )
        frameRunSpecsEntry.grid(
            row=2,
            column=0,
            pady=5,
            )

# define remaining entry fields using Pmw.EntryField         
        self.numNodes=Pmw.EntryField(
            frameRunSpecsEntry,
            labelpos=W,
            label_text='Nodes',
            validate={
                'validator':'integer',
                'min':1,
                'max':999999,
                'minstrict':1,
                'maxstrict':1},
            value=1,
            modifiedcommand=self.handlerNumNodes,
            )
#        self.numNodes.configure(entry_width=6)
                
        self.numProcsPerNode=Pmw.EntryField(
            frameRunSpecsEntry,
            labelpos=W,
            label_text='Procs/node',
            validate={
                'validator':'integer',
                'min':1,
                'max':32,
                'minstrict':1,
                'maxstrict':1},
            value=1,
            modifiedcommand=self.handlerNumProcsPerNode,
            )
        
        self.numCoresPerProc=Pmw.EntryField(
            frameRunSpecsEntry,
            labelpos=W,
            label_text='Cores/proc',
            validate={
                'validator':'integer',
                'min':1,
                'max':32,
                'minstrict':1,
                'maxstrict':1},
            value=1,
            modifiedcommand=self.handlerNumCoresPerProc,
            )

        nodes=eval(self.numNodes.get())
        procsPerNode=eval(self.numProcsPerNode.get())
        totalProcs=nodes*procsPerNode
        
        self.numProcs=Pmw.EntryField(
            frameRunSpecsEntry,
            labelpos=W,
            label_text='* Total processors\n(calculated)',
            validate=None,
            value=totalProcs,
            modifiedcommand=self.calculateNumProcs,
            )
        self.numProcs.component('entry').configure(
            bg='lightblue',
            fg='red',
            )
 
        coresPerProc=eval(self.numCoresPerProc.get())
        totalCores=totalProcs*coresPerProc
        self.numCores=Pmw.EntryField(
            frameRunSpecsEntry,
            labelpos=W,
            label_text='* Total cores\n(calculated)',
            validate=None,
            value=totalCores,
            modifiedcommand=self.calculateNumCores,
            )
        self.numCores.component('entry').configure(
            bg='lightblue',
            fg='red'
            )    
        
        self.numProject=Pmw.EntryField(
            frameRunSpecsEntry,
            labelpos=W,
            label_text='Project No.',
            validate={
                'validator':'integer',
                'min':0,
                'max':999999,
                'minstrict':1,
                'maxstrict':1},
            value=0,
            modifiedcommand=self.handlerNumProject,
            )       
        
        self.numTask=Pmw.EntryField(
            frameRunSpecsEntry,
            labelpos=W,
            label_text='Task No.',
            validate={
                'validator':'real',
                'min':0,
                'max':99.99,
                'minstrict':1,
                'maxstrict':1},
            value=00.00,
            modifiedcommand=self.handlerNumTask,
            )       
        
        self.paramsQsub=Pmw.EntryField(
            frameRunSpecsEntry,
            labelpos=W,
            label_text='User-specified QSUB\ncommands\n(spaces to separate)',
            validate=None,
            modifiedcommand=self.handlerParamsQsub,
            ) 
            
# create widget for YOD parameters but do not show grid yet

        self.paramsYod=Pmw.EntryField(
            frameRunSpecsEntry,
            labelpos=W,
            label_text='User-specified YOD\ncommands\n(spaces to separate)',
            validate=None,
            modifiedcommand=self.handlerParamsYod,
            )
        self.paramsYod.grid(
            row=7,
            column=0,
            padx=10,
            pady=5,
            )
        self.paramsYod.grid_remove()
          
# grid all widgets        
        widgets=(
            self.numNodes,
            self.numProcsPerNode,
            self.numCoresPerProc,
            self.numProcs,
            self.numCores,
            self.numProject,
            self.numTask,
            self.paramsQsub,
            )
        rowWidget=0
        for widget in widgets:
#            widget.pack(
#                fill=X, 
#                expand=1, 
#                padx=10, 
#                pady=5
#                )
            widget.grid(
                row=rowWidget,
                column=0,
                padx=10,
                pady=5,
                )
            rowWidget+=1
        Pmw.alignlabels(widgets)
        self.numNodes.component('entry').focus_set() 
        
        return
        

# ----- end of Run Specs for BATCH QUEUES -----

# Run Specs for NO QUEUES (JUST RUN EXECUTABLE)         

# ----- end of Run Specs for NO QUEUES (JUST RUN EXECUTABLE) -----

    def initializeRunTab(self):
        '''
        Purpose:
            Initialize states and grids in the Run Tab
        
        Called by:
            boxQueueRunTab
        '''

        if self.stringQueueRunTab != 'queueBatch':
# disable sub-options        
            self.subBatchOption1QueueRunTab.configure(
                state=DISABLED
                )
            self.subBatchOption2QueueRunTab.configure(
                state=DISABLED
                )
            self.subBatchOption3QueueRunTab.configure(
                state=DISABLED
                )
                
# disable specific Run Spec parameters corresponding to NONE Queue
            self.runtimeHrs.configure(entry_state='disabled')
            self.runtimeMins.configure(entry_state='disabled')
# show QSUB Commands Run Spec and then disable; hide YOD Commands
            self.paramsYod.grid_remove()
            self.paramsQsub.grid()
            self.paramsQsub.configure(entry_state='disabled')
# disable Project No.
            self.numProject.configure(entry_state='disabled')
# disable Taks No.
            self.numTask.configure(entry_state='disabled')
        
        return
        
    def calculateNumProcs(self):
        '''
        Purpose:
            calculate the number of processors
        '''
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'calculateNumProcs:'
            
        nodes=eval(self.numNodes.get())
        procsPerNode=eval(self.numProcsPerNode.get())
        totalProcs=nodes*procsPerNode
        print '\nNumber of processors:',totalProcs 
        self.numProcs.setentry(totalProcs)
        
        return
        
        
    def calculateNumCores(self):
        '''
        Purpose:
            calcualate the number of cores
        '''
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'calculateNumCores:'
            
        nodes=eval(self.numNodes.get())
        procsPerNode=eval(self.numProcsPerNode.get())
        coresPerProc=eval(self.numCoresPerProc.get())
        totalCores=nodes*procsPerNode*coresPerProc
        print '\nNumber of cores: ', totalCores
        self.numCores.setentry(totalCores)
        
        return
        
        
    def enableAllRunTimeSpecs(self):
        '''
        Purpose:
            Enables all entries in Run Specs box in Run Tab
        
        Called by:
            handlerQueueRunTab           
        '''
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'enableAllRunTimeSpecs'
        
# Tk widgets   
        self.labelHrsMins.configure(state=NORMAL)
# Pmw widgets
        self.runtimeHrs.configure(entry_state='normal')
        self.runtimeMins.configure(entry_state='normal')
        self.numNodes.configure(entry_state='normal')
        self.numProcsPerNode.configure(entry_state='normal')
        self.numCoresPerProc.configure(entry_state='normal')
        self.numProcs.configure(entry_state='normal')
        self.numCores.configure(entry_state='normal')
        self.numProject.configure(entry_state='normal')
        self.numTask.configure(entry_state='normal')
        self.paramsQsub.configure(entry_state='normal')
        self.paramsYod.configure(entry_state='normal')
        
        return
        
        
    def boxFilesRunTab(self,parent):
        '''
        Purpose:
            Define the FILES box for the Run Tab. Used to
            choose Source, Executable, and Compilation Output
            filenames.
            
        Called by:
           buildRun
           
        Calls:
           handlerBrowseExecutableFilenameFilesRunTab
           handlerBrowseRunTimeOutputFilesRunTab
           handlerBrowseRunTimeErrorOutputFilesRunTab
           handlerBrowseForQsubFilenameRunTab
           handlerPropagateBaseNameFromExecutableRunTab
           handlerClearAllFilenamesRunTab
            
        Important output variables:            
           self.entryExecutableFilenameFilesRunTab
           self.entryRunTimeOutputFilesRunTab
           self.entryRunTimeErrorOutputFilesRunTab
           self.entryQsubFilenameRunTab                (value, disable, enable)
           self.buttonBrowseForQsubFilenameRunTab      (disable, enable)
          
        Notes:
           variables disabled/enabled

         '''
# first, create the surrounding frame
        frameAllFilesRunTab = Frame(
            parent,
            width=500,
            bg=backgroundBottomFrameRunTab,
            )
        frameAllFilesRunTab.grid(
            row=1, 
            column=2,
            rowspan=1,
            columnspan=1,
            padx=10,
            pady=5,
            sticky=N,
            )
            
# create frame for runtime files
        frameRunTimeFilesRunTab = Frame(
            frameAllFilesRunTab,
            relief=RIDGE,
            borderwidth=5
            )
        frameRunTimeFilesRunTab.grid(
            row=0,
            column=0,
            padx=0,
            pady=0,
            )
# Label at top of frame
        labelFilesRunTab=Label(
            frameRunTimeFilesRunTab,
            text='FILES',
            )
        labelFilesRunTab.grid(
            row=0,
            column=0,
            columnspan=99,
            pady=5,
            sticky=N
            )
                        
# create frame for QSUB filename; disable for queues other than BATCH
        frameQsubFilenameRunTab=Frame(
            frameAllFilesRunTab,
#            width=500,
#            height=350,
            relief=RIDGE,
            borderwidth=5,
            )
        frameQsubFilenameRunTab.grid(
            row=1, 
            column=0,
            rowspan=1,
            columnspan=1,
            padx=0,
            pady=10,
            sticky=N,
            )


# Next, specify working directory
#   DWB - needs to be done!
# specify temporary source filename
#        filesExecutable = (' ','file1.exe', 'file2.exe', 'file3.exe', 'file4.exe')
        labelExecutableFilenameFilesRunTab = Label(
            frameRunTimeFilesRunTab,
            text='Executable',
            justify=LEFT,
            )
        labelExecutableFilenameFilesRunTab.grid(
            row=1,
            column=0,
            padx=5,
            sticky=W,
            )
        self.entryExecutableFilenameFilesRunTab = Entry(
            frameRunTimeFilesRunTab,
            )
        self.entryExecutableFilenameFilesRunTab.grid(
            row=1,
            column=1,
            padx=2
            )
        buttonBrowseExecutableFilenameFilesRunTab = Button(
            frameRunTimeFilesRunTab,
            font=self.buttonFont,
            command=self.handlerBrowseExecutableFilenameFilesRunTab,
            text='Browse',
            justify=CENTER,
            relief=RAISED,
            )
        buttonBrowseExecutableFilenameFilesRunTab.grid(
            row=2,
            column=1,
            sticky=N
            )
            
# Run-time Output
#        filesRunTimeOutput = (' ','file1.Output','file2.Output','file3.Output')
        labelRunTimeOutputFilesRunTab = Label(
            frameRunTimeFilesRunTab,
            text='Run-time\nOutput',
            justify=LEFT,
            )
        labelRunTimeOutputFilesRunTab.grid(
            row=3,
            column=0,
            padx=5,
            sticky=W,
            )
        self.entryRunTimeOutputFilesRunTab = Entry(
            frameRunTimeFilesRunTab,
            )
        self.entryRunTimeOutputFilesRunTab.grid(
            row=3,
            column=1,
            padx=2,
            )
        buttonBrowseRunTimeOutputFilesRunTab = Button(
            frameRunTimeFilesRunTab,
            command=self.handlerBrowseRunTimeOutputFilesRunTab,
            text='Browse',
            font=self.buttonFont,
            justify=CENTER,
            relief=RAISED,
            )
        buttonBrowseRunTimeOutputFilesRunTab.grid(
            row=4,
            column=1,
            sticky=N,
            )
            
            
# Run-time Error Output
        labelRunTimeErrorOutputFilesRunTab = Label(
            frameRunTimeFilesRunTab,
            text='Run-time error\noutput',
            justify=LEFT,
            )
        labelRunTimeErrorOutputFilesRunTab.grid(
            row=5,
            column=0,
            padx=5,
            sticky=W,
            )
        self.entryRunTimeErrorOutputFilesRunTab = Entry(
            frameRunTimeFilesRunTab,
            )
        self.entryRunTimeErrorOutputFilesRunTab.grid(
            row=5,
            column=1,
            padx=2,
            )
        buttonBrowseRunTimeErrorOutputFilesRunTab = Button(
            frameRunTimeFilesRunTab,
            text='Browse',
            font=self.buttonFont,
            command=self.handlerBrowseRunTimeErrorOutputFilesRunTab,
            justify=CENTER,
            relief=RAISED,
            )
        buttonBrowseRunTimeErrorOutputFilesRunTab.grid(
            row=6,
            column=1,
            sticky=N,
            )
            
# create Qsub entry  
#  ... create Qsub label
        labelQsubFilename = Label(
#            frameQsubFilenameRunTab,
            frameRunTimeFilesRunTab,
            text='QSUB Filename\n(Batch queues only)',
            justify=LEFT,
            )
        labelQsubFilename.grid(
            row=7,
            column=0,
            padx=5,
            sticky=W,
            )
#  ... create Qsub entry field    
        self.entryQsubFilenameRunTab = Entry(
            frameRunTimeFilesRunTab,
            )
        self.entryQsubFilenameRunTab.grid(
            row=7,
            column=1,
            padx=2,
            )
# disable Qsub filename entry in Run Tab initially, since default queue is None
        self.entryQsubFilenameRunTab.configure(state=DISABLED)
            
# ... create Qsub entry browse button
        self.buttonBrowseForQsubFilenameRunTab = Button(
#            frameQsubFilenameRunTab,
            frameRunTimeFilesRunTab,
            command=self.handlerBrowseForQsubFilenameRunTab,
            text='Browse',
            justify=CENTER,
            font=self.buttonFont,
            relief=RAISED,
            )
        self.buttonBrowseForQsubFilenameRunTab.grid(
            row=8,
            column=1,
            sticky=N,
            )
# disable QSUB FILE Browse button in Run Tab initially, since default queue is None
        self.buttonBrowseForQsubFilenameRunTab.configure(state=DISABLED)
        
# button for propagating base filename from Executable filename
        buttonPropagateBaseNameFromExecutableRunTab = Button(
            frameRunTimeFilesRunTab,
            text='Propagate Executable base filename',
            command=self.handlerPropagateBaseNameFromExecutableRunTab,
            justify=CENTER,
            borderwidth=5,
            relief=RAISED,
            )
        buttonPropagateBaseNameFromExecutableRunTab.grid(
            row=9,
            column=0,
            columnspan=99,
            pady=10,
            padx=5,
            )

# button for clearing all filenames
        buttonClearAllFilenamesRunTab = Button(
            frameRunTimeFilesRunTab,
            text='Clear all filename entries',
            command=self.handlerClearAllFilenamesRunTab,
            justify=CENTER,
            borderwidth=5,
            relief=RAISED,
            )
        buttonClearAllFilenamesRunTab.grid(
            row=10,
            column=0,
            columnspan=99,
            pady=5,
            padx=5,
            )
            
        return
        

    def buttonsRunKillRunTab(self,parent):
        '''
        Purpose:
            create the buttons to assemble the run
            command, run the code, and kill the process.
            Initialize the frames with the appropriate buttons to
            correspond to the initial queue (which is queue None)
       
        Called by:
           buildRun
       
        Calls:
        - handlers:
            self.handlerAssembleForQueueNoneRunTab
            self.handlerExecuteForQueueNoneRunTab
            self.handlerAssembleForQueueBatchRunTab
            self.handlerExecuteForQueueBatchRunTab
            self.handlerAssembleForQueueInteractiveRunTab
            self.handlerExecuteForQueueInteractiveRunTab
           
        Important output variables:
         - frames:
        (used in:
            handlerQueueRunTab
         )
            self.frameAssembleExecuteForQueueNoneRunTab
            self.frameAssembleExecuteForQueueBatchRunTab
            self.frameAssembleExecuteForQueueInteractiveRunTab
        
        '''
# CREATE FRAMES
# Main frame for Assemble and Run buttons
#    ... there will be sub-frames for each queue
        frameAssembleExecuteRunTab = Frame(
            parent,
            relief=None,
            borderwidth=0,
            bg=backgroundBottomFrameRunTab,
            )
        frameAssembleExecuteRunTab.grid(
            row=2,
            column=0,
            columnspan=99,
            padx=5,
            )

# sub-frame for queue None, inside main frame for Assemble and Run Buttons            
        self.frameAssembleExecuteForQueueNoneRunTab = Frame(
            frameAssembleExecuteRunTab,
            relief=None,
            borderwidth=0,
            bg=backgroundBottomFrameRunTab,
            )
        self.frameAssembleExecuteForQueueNoneRunTab.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            )
            
# sub-frame for queue Batch, inside main frame for Assemble and Run Buttons            
        self.frameAssembleExecuteForQueueBatchRunTab = Frame(
            frameAssembleExecuteRunTab,
            relief=None,
            borderwidth=0,
            bg=backgroundBottomFrameRunTab,
            )
        self.frameAssembleExecuteForQueueBatchRunTab.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            )
            
# sub-frame for queue Interactive, inside main frame for Assemble and Run Buttons            
        self.frameAssembleExecuteForQueueInteractiveRunTab = Frame(
            frameAssembleExecuteRunTab,
            relief=None,
            borderwidth=0,
            bg=backgroundBottomFrameRunTab,
            )
        self.frameAssembleExecuteForQueueInteractiveRunTab.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            )
            
# Frame for 'Kill Job in Queue' and 'Kill running job'
        frameKillJobsRunTab=Frame(
            frameAssembleExecuteRunTab,
            relief=RIDGE,
            borderwidth=5,
#            bg=backgroundBottomFrameRunTab,
            )
        frameKillJobsRunTab.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            )
            
# grid buttons for sub-frames
# ... Assemble and execute buttons for queue None
        self.buttonAssembleForQueueNoneRunTab = Button(
            self.frameAssembleExecuteForQueueNoneRunTab,
            text='ASSEMBLE Run Command',
            command=self.handlerAssembleForQueueNoneRunTab,
            relief=RAISED,
            borderwidth=5,
            )
        self.buttonAssembleForQueueNoneRunTab.grid(
            row=0,
            column=0,
            padx=5,
            pady=2,
            )
        
        self.buttonExecuteForQueueNoneRunTab = Button(
            self.frameAssembleExecuteForQueueNoneRunTab,
            text='EXECUTE Run Command',
            command=self.handlerExecuteForQueueNoneRunTab,
            relief=RAISED,
            borderwidth=5,
            )
        self.buttonExecuteForQueueNoneRunTab.grid(
            row=0,
            column=1,
            padx=5,
            pady=2,
            )

# ... Assemble and execute buttons for queue Batch
        self.buttonAssembleForQueueBatchRunTab = Button(
            self.frameAssembleExecuteForQueueBatchRunTab,
            text='ASSEMBLE QSUB file',
            command=self.handlerAssembleForQueueBatchRunTab,
            relief=RAISED,
            borderwidth=5,
            )
        self.buttonAssembleForQueueBatchRunTab.grid(
            row=0,
            column=0,
            padx=5,
            pady=2,
            )
        
        self.buttonExecuteForQueueBatchRunTab = Button(
            self.frameAssembleExecuteForQueueBatchRunTab,
            text='SUBMIT QSUB file for execution\n(saves QSUB file)',
            command=self.handlerExecuteForQueueBatchRunTab,
            relief=RAISED,
            borderwidth=5,
            )
        self.buttonExecuteForQueueBatchRunTab.grid(
            row=0,
            column=1,
            padx=5,
            pady=2,
            )
               
# ... Assemble and execute buttons for queue Interactive               
        self.buttonAssembleForQueueInteractiveRunTab = Button(
            self.frameAssembleExecuteForQueueInteractiveRunTab,
            text='ASSEMBLE YOD Command',
            command=self.handlerAssembleForQueueInteractiveRunTab,
            relief=RAISED,
            borderwidth=5,
            )
        self.buttonAssembleForQueueInteractiveRunTab.grid(
            row=0,
            column=0,
            padx=5,
            pady=2,
            )
        
        self.buttonExecuteForQueueInteractiveRunTab = Button(
            self.frameAssembleExecuteForQueueInteractiveRunTab,
            text='EXECUTE YOD Command',
            command=self.handlerExecuteForQueueInteractiveRunTab,
            relief=RAISED,
            borderwidth=5,
            )
        self.buttonExecuteForQueueInteractiveRunTab.grid(
            row=0,
            column=1,
            padx=5,
            pady=2,
            )
            
# Entry fields and buttons for 'Kill a job in queue' and 'Kill a running job'
        self.labelKillJob = Label(
            frameKillJobsRunTab,
            text='KILL JOB',
            justify=CENTER,
            )
        self.labelKillJob.grid(
            row=0,
            column=0,
            columnspan=99,
            pady=2,
            )
            
        self.labelKillJobInQueue = Label(
            frameKillJobsRunTab,
            text='Kill a job in queue:',
            justify=LEFT,
            )
        self.labelKillJobInQueue.grid(
            row=1,
            column=0,
            padx=5,
            pady=2,
            )
            
        self.labelKillRunningJob = Label(
            frameKillJobsRunTab,
            text='Kill a running job:',
            justify=LEFT,
#            foreground='white',
#            background=backgroundBottomFrameRunTab,
            )
        self.labelKillRunningJob.grid(
            row=1,
            column=1,
            padx=5,
            pady=2,
            )
            
        self.buttonRefreshQueueRunTab = Button(
            frameKillJobsRunTab,
            text='Refresh queue',
            command=self.handlerRefreshQueueRunTab,
            justify=CENTER,
            font=self.buttonFont,
            )
        self.buttonRefreshQueueRunTab.grid(
            row=2,
            column=0,
            padx=5,
            pady=2,
            )
            
        self.buttonRefreshRunningJobListRunTab = Button(
            frameKillJobsRunTab,
            text='Refresh list',
            command=self.handlerRefreshRunningJobListRunTab,
            justify=CENTER,
            font=self.buttonFont,
            )
        self.buttonRefreshRunningJobListRunTab.grid(
            row=2,
            column=1,
            padx=5,
            pady=2,
            )
        
        self.entryKillJobInQueue = Entry(
            frameKillJobsRunTab,
#            width=20,
#            background=backgroundBottomFrameRunTab,
            )
        self.entryKillJobInQueue.grid(
            row=3,
            column=0,
            padx=10,
            pady=2,
            )
            
        self.entryKillRunningJob = Entry(
            frameKillJobsRunTab,
#            width=20,
#            background=backgroundBottomFrameRunTab,
            )
        self.entryKillRunningJob.grid(
            row=3,
            column=1,
            padx=10,
            pady=2,
            )
            
        self.buttonKillJobInQueueRunTab = Button(
            frameKillJobsRunTab,
            text='Kill job in queue',
            command=self.handlerKillJobInQueueRunTab,
            justify=CENTER,
            font=self.buttonFont,
            )
        self.buttonKillJobInQueueRunTab.grid(
            row=4,
            column=0,
            padx=5,
            pady=2,
            )
            
        self.buttonKillRunningJobRunTab = Button(
            frameKillJobsRunTab,
            text='Kill running job',
            command=self.handlerKillRunningJobRunTab,
            justify=CENTER,
            font=self.buttonFont,
            )
        self.buttonKillRunningJobRunTab.grid(
            row=4,
            column=1,
            padx=5,
            pady=2,
            )
            
            
            
# Initialize corresponding to default queue being None
        self.frameAssembleExecuteForQueueNoneRunTab.grid()
        self.frameAssembleExecuteForQueueBatchRunTab.grid_remove()
        self.frameAssembleExecuteForQueueInteractiveRunTab.grid_remove()                
        
#  ----- end of RUN TAB METHODS ----- 

#  ----- STATUS TAB METHODS ----- 

# dummy def
    def ZZ___STATUS_TAB_METHODS():
        pass
        
        return
        
        
    def frameStatusCreate(self,parent,msg):
        '''
        Purpose:
            create the scrolled frame for the STATUS tab
        '''
        
        self.frameStatus = Pmw.ScrolledFrame(
            parent,
            borderframe = 1,
            labelpos = N,
            label_text = msg,
            label_font=self.titleFont,
            usehullsize = 1,
            hull_width = globalHullWidth,
            hull_height = globalHullHeight,
            hscrollmode='dynamic',
            vscrollmode='dynamic',
            horizflex='elastic', # 'expand' centers interior frames when window is stretched; ...
            vertflex='fixed',  # ...   do not use 'elastic' which kills scrollbars
            )
        self.frameStatus.pack(
            padx=5, 
            pady=5, 
            fill='both', 
            expand='YES',
            )
            
        self.frameStatus.interior().grid_rowconfigure(0,weight=1)
        self.frameStatus.interior().grid_columnconfigure(0,weight=1) 
        self.frameStatus.interior().grid_rowconfigure(1,weight=1)
        self.frameStatus.interior().grid_columnconfigure(1,weight=1)
            
        Pmw.Color.changecolor(parent, background=backgroundStatusTab)
        
        return
        
        
    def framesInterior_tabStatus(self,parent):
        '''
        Purpose:
            create top and bottom frames for the STATUS tab
        '''  
        
# top    
        self.tabStatus_TopFrame=Frame(
            parent,
            relief=RIDGE,
            borderwidth=5,
            bg=backgroundTopFrameStatusTab,
            )
        self.tabStatus_TopFrame.grid(
            row=0,
            column=0,
            padx=0,
            pady=5,
            sticky=N
            )
# bottom
        self.tabStatus_BottomFrame=Frame(
            parent,
            relief=RIDGE,
            borderwidth=5,
            bg=backgroundBottomFrameStatusTab,
            )
        self.tabStatus_BottomFrame.grid(
            row=1,
            column=0,
            padx=0,
            pady=5,
            ) 

        Pmw.Color.changecolor(self.tabStatus_BottomFrame, background=backgroundStatusTab) 
        
        return
        
        
    def labelTempStatusTab(self,parent):
        '''
        Purpose:
            TO BE DELETED WHEN WORK ON BOTTOM FRAME IN STATUS TAB IS BEGUN
        '''
        
        label_Temp=Label(
            parent,
            text='STATUS goes here',
            justify=CENTER,
            )
        label_Temp.grid(
            row=0,
            column=0,
            padx=0,
            pady=10,
            )
            
        return
    
#  ----- end of STATUS TAB METHODS ----- 

#  ----- POST-PROCESS TAB METHODS ----- 

# dummy def
    def ZZ___POST_PROCESS_TAB_METHODS():
        pass
        
        return
        
        
    def framePostProcessCreate(self,parent,msg):
        '''
        Purpose:
            create the scrolled frame for this tab
        '''
        self.framePostProcess = Pmw.ScrolledFrame(
            parent,
            borderframe = 1,
            labelpos = N,
            label_text = msg,
            label_font=self.titleFont,
            usehullsize = 1,
            hull_width = globalHullWidth,
            hull_height = globalHullHeight,
            hscrollmode='dynamic',
            vscrollmode='dynamic',
            horizflex='elastic', # 'expand' centers interior frames when window is stretched; ...
            vertflex='fixed',  # ...   do not use 'elastic' which kills scrollbars
            )
        self.framePostProcess.pack(
            padx=5, 
            pady=5, 
            fill='both', 
            expand='YES',
            )
            
        self.framePostProcess.interior().grid_rowconfigure(0,weight=1)
        self.framePostProcess.interior().grid_columnconfigure(0,weight=1) 
        self.framePostProcess.interior().grid_rowconfigure(1,weight=1)
        self.framePostProcess.interior().grid_columnconfigure(1,weight=1)
            
        Pmw.Color.changecolor(parent, background=backgroundPostProcessTab)
        
        return
        

    def framesInterior_tabPostProcess(self,parent):
        '''
        Purpose:
            create top and bottom frames for the POST-PROCESS tab
        ''' 

# top    
        self.tabPostProcess_TopFrame=Frame(
            self.framePostProcess.interior(),
            relief=RIDGE,
            borderwidth=5,
            bg=backgroundTopFramePostProcessTab,
            )
        self.tabPostProcess_TopFrame.grid(
            row=0,
            column=0,
            pady=5,
            sticky=N
            )
# bottom
        self.tabPostProcess_BottomFrame=Frame(
            self.framePostProcess.interior(),
            relief=RIDGE,
            borderwidth=5,
            bg=backgroundBottomFramePostProcessTab,
            )
        self.tabPostProcess_BottomFrame.grid(
            row=1,
            column=0,
            pady=5,
            )
            
        return
  

    def frameBottomPostProcessTab(self,parent):
        '''
        Purpose:
            Calls module to set up frames and widgets in
        this tab
        '''

        import module_postprocess
        
        module_postprocess.main_postprocess(
            self,
            parent,
            self.shell,
            backgroundBottomFramePostProcessTab
            )
            
        return
        
      
#  ----- end of POST-PROCESS TAB METHODS ----- 

# ----- MYSQL ACCESS TAB METHODS -----

# dummy def
    def ZZ___MYSQL_ACCESS_TAB_METHODS():
        pass
        
        return
        
        
    def frameMySQLCreate(self,parent,msg):
        '''
        Purpose:
            create the scrolled frame for this tab
        '''
        self.frameMySQL = Pmw.ScrolledFrame(
            parent,
            borderframe = 1,
            labelpos = N,
            label_text = msg,
            label_font=self.titleFont,
            usehullsize = 1,
            hull_width = globalHullWidth,
            hull_height = globalHullHeight,
            hscrollmode='dynamic',
            vscrollmode='dynamic',
            horizflex='elastic', # 'expand' centers interior frames when window is stretched; ...
            vertflex='fixed',  # ...   do not use 'elastic' which kills scrollbars
            )
        self.frameMySQL.pack(
            padx=5, 
            pady=5, 
            fill='both', 
            expand='YES',
            )
            
        self.frameMySQL.interior().grid_rowconfigure(0,weight=1)
        self.frameMySQL.interior().grid_columnconfigure(0,weight=1) 
        self.frameMySQL.interior().grid_rowconfigure(1,weight=1)
        self.frameMySQL.interior().grid_columnconfigure(1,weight=1)
            
        Pmw.Color.changecolor(parent, background=backgroundMySQLTab)

        return
        
        
    def framesInterior_tabMySQL(self,parent):
        '''
        Purpose:
           create top and bottom frames for the MySQL ACCESS tab
        ''' 
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'framesInterior_tabMySQL'

# top    
        self.tabMySQL_TopFrame=Frame(
            self.frameMySQL.interior(),
            relief=RIDGE,
            borderwidth=5,
            bg=backgroundTopFrameMySQLTab,
            )
        self.tabMySQL_TopFrame.grid(
            row=0,
            column=0,
            padx=0,
            pady=5,
            sticky=N
            )
# Bottom
        self.tabMySQL_BottomFrame=Frame(
            self.frameMySQL.interior(),
            relief=RIDGE,
            borderwidth=5,
            bg=backgroundBottomFrameMySQLTab,
            )
        self.tabMySQL_BottomFrame.grid(
            row=1,
            column=0,
            padx=0,
            pady=5,
            )
            
        return
        
            
    def frameBottomMySQLTab(self,parent):
        '''
        Purpose:
            Create widgets in bottom frame of this tab.
           
        Called by:
            buildMySQL
            
        '''
        import module_accessMySQL
        
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'frameBottomMySQLTab'
         
        module_accessMySQL.AccessMySQL(
            parent,
            self,
            backgroundBottomFrameMySQLTab,
            self.textMySQLOutputWindows_IO,
            self.textMySQLCommandsWindows_IO,
            ) 

# returns with following values defined, used to collect stats on pylotdb
#       self.pylotdb_stats_server_valid       'True' if all attributes have values; else 'False'
#       self.pylotdb_stats_server             server name
#       self.pylotdb_stats_server_username    user name
#       self.pylotdb_stats_server_password    password
#       self.pylotdb_stats_server_port        port

        self.track_MySQL_Access_Usage()

        return
        

# ----- end of MYSQL ACCESS TAB METHODS -----

#  ----- EXTERNAL I/O WINDOWS TAB METHODS ----- 

# dummy def
    def ZZ___EXTERNAL_IO_WINDOWS_TAB_METHODS():
        pass
        return
        
    def frameCreateTopLevel(self):
        '''
        Purpose:
            create main window for external Windows_IO
        '''

        self.frameExternalMainWindows_IO=Toplevel(
            bg='gray',
            height=100,
            width=500,
            borderwidth=5,
            )
        self.frameExternalMainWindows_IO.grid()
# place window
        self.frameExternalMainWindows_IO.geometry(
            '+%d+%d' % (x_Windows_IO, y_Windows_IO)
            )
# fix window size so it does not change with tab picked
        self.frameExternalMainWindows_IO.propagate(0)
        self.frameExternalMainWindows_IO.title(
            'PylotDB - I/O Windows'
            )  
        
        return
        
        
    def buttonsExternalWindows_IO(self,parent):
        '''
        Purpose:
            define buttons for external windows_io frame
        '''
# frame for buttons     
        self.frameButtons_IO=Frame(
            parent,
            borderwidth=2,
            relief=RIDGE,
            )
        self.frameButtons_IO.grid(
            row=0,
            column=0,
            padx=2,
            pady=2,
            sticky=N,
            )
# label for buttons frame       
        labelButtons_IO=Label(
            self.frameButtons_IO,
            text='I/O Windows',
            justify=CENTER,
            relief=FLAT,
            )
        labelButtons_IO.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            ipadx=3,
            )
            
# create windows_IO buttons  
# 1/8 Host Info button
        buttonHostInfo_IO=Button(
            self.frameButtons_IO,
            text='HOST INFO',
            font=self.dataFont,
            borderwidth=5,
            justify=CENTER,
            relief=RAISED,
            command=self.handlerButtonHostInfo_IO,
            highlightthickness=5,
            )
        buttonHostInfo_IO.grid(
            row=1,
            column=0,
            padx=5,
            pady=2,
            sticky=EW,
            )
            
# 2/8 CVS/SVN Checkin button            
        buttonCvsSvnAccess_IO=Button(
            self.frameButtons_IO,
            text='CVS/SVN ACCESS',
            font=self.dataFont,
            borderwidth=5,
            justify=CENTER,
            relief=RAISED,
            command=self.handlerButtonCvsSvnAccess_IO,
            )
        '''
        buttonCvsSvnAccess_IO.grid(
            row=2,
            column=0,
            padx=5,
            pady=2,
            sticky=EW,
            )
        '''
            
            
# 3/8 COMPILE button           
        buttonCompile_IO=Button(
            self.frameButtons_IO,
            text='COMPILE',
            font=self.dataFont,
            borderwidth=5,
            justify=CENTER,
            relief=RAISED,
            command=self.handlerButtonCompile_IO,
            )
        '''
        buttonCompile_IO.grid(
            row=4,
            column=0,
            padx=5,
            pady=2,
            sticky=EW,
            )
        '''
            
# 4/8 SETUP button            
        buttonSetup_IO=Button(
            self.frameButtons_IO,
            text='SETUP',
            font=self.dataFont,
            borderwidth=5,
            justify=CENTER,
            relief=RAISED,
            command=self.handlerButtonSetup_IO,
            )
        '''
        buttonSetup_IO.grid(
            row=5,
            column=0,
            padx=5,
            pady=2,
            sticky=EW,
            )
        '''
            
# 5/8 RUN button            
        buttonRun_IO=Button(
            self.frameButtons_IO,
            text='RUN',
            font=self.dataFont,
            borderwidth=5,
            justify=CENTER,
            relief=RAISED,
            command=self.handlerButtonRun_IO,
            )
        '''
        buttonRun_IO.grid(
            row=6,
            column=0,
            padx=5,
            pady=2,
            sticky=EW,
            )
        '''

# 6/8 STATUS button            
        buttonStatus_IO=Button(
            self.frameButtons_IO,
            text='STATUS',
            font=self.dataFont,
            borderwidth=5,
            justify=CENTER,
            relief=RAISED,
            command=self.handlerButtonStatus_IO,
            )
        '''
        buttonStatus_IO.grid(
            row=7,
            column=0,
            padx=5,
            pady=2,
            sticky=EW,
            )
        '''

# 7/8 POST-PROCESS button            
        buttonPostProcess_IO=Button(
            self.frameButtons_IO,
            text='POST-PROCESS',
            font=self.dataFont,
            borderwidth=5,
            justify=CENTER,
            relief=RAISED,
            command=self.handlerButtonPostProcess_IO,
            )
        '''
        buttonPostProcess_IO.grid(
            row=8,
            column=0,
            padx=5,
            pady=2,
            sticky=EW,
            )
        '''
            
# 8/8 POST-PROCESS button            
        buttonPostProcess_IO=Button(
            self.frameButtons_IO,
            text='MySQL ACCESS',
            font=self.dataFont,
            borderwidth=5,
            justify=CENTER,
            relief=RAISED,
            command=self.handlerButtonMySQL_IO,
            )
        buttonPostProcess_IO.grid(
            row=9,
            column=0,
            padx=5,
            pady=2,
            sticky=EW,
            )
            
        return
            
    def checkbuttonLockDisplayExternalWindows_IO(self,parent):
        '''
        Purpose:
            define checkbutton to lock external windows_io display
        '''
# Frame for Lock Display checkbutton, just for the I/O Window
#   (In same frame as for Minimize button)
        frameCheckButtonLockDisplayWindows_IO=Frame(
            parent,
            relief=FLAT,
            bg='gray'
            )
        frameCheckButtonLockDisplayWindows_IO.grid(
            row=1,
            column=0,
            padx=2,
            pady=10,
#            sticky=N,
            )
           
        self.lockDisplay=IntVar()
        self.lockDisplay.set(0)
        checkbuttonLockDisplayWindows_IO = Checkbutton(
            frameCheckButtonLockDisplayWindows_IO,
            text='Lock display\nto current tab',
            variable=self.lockDisplay,
            command=self.handlerLockDisplay,
            bg='gray',
            font=self.dataFont,
            
            )
        checkbuttonLockDisplayWindows_IO.grid(
            row=0,
            column=0,
            )
            
        return
           
    def buttonMinimizeExternalWindows_IO(self,parent): 
        '''
        Purpose:
            define button to minimize external windows_io window
        '''
# Frame for minimize button, just for the I/O Window    
#  (In same frame as for Lock Display button)        
        frameButtonMinimizeWindows_IO=Frame(
            parent,
            relief=FLAT,
            bg='gray',
            )
        frameButtonMinimizeWindows_IO.grid(
            row=2,
            column=0,
            padx=2,
            pady=2,
            sticky=S,
            )
        buttonMinimizeWindows_IO = Button(
            frameButtonMinimizeWindows_IO,
            text='Minimize',
            borderwidth=5,
            command=lambda: self.frameExternalMainWindows_IO.iconify(),
            relief=RAISED,
            justify=CENTER,
            )
        buttonMinimizeWindows_IO.grid(
            row=0,
            column=0,
            padx=5,
            pady=2,
            sticky=EW,
            )
            
        return
            
            
    def frameExternalHostInfoWindows_IO(self,parent):
        '''
        Purpose:
            create external INFO frame
        '''
        
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'frameExternalHostInfoWindows_IO'
        
        self.frameHostInfoWindows_IO = Frame(
            parent,
            borderwidth=2,
            relief=RIDGE,
            height=externalFrameHeight,
            width=externalFrameWidth,
            bg=backgroundInfoTabWindows_IO,
            )
        self.frameHostInfoWindows_IO.grid(
            row=0,
            column=1,
            padx=2,
            pady=2,
            rowspan=3,
            sticky=NSEW,
            )
        self.frameHostInfoWindows_IO.grid_propagate(0)
        
        childFrame=self.frameHostInfoWindows_IO
        
        self.labelHostInfoWindows_IO = Label(
            childFrame,
            text='-- HOST INFO TAB I/O WINDOW --\n' +
                 '----------------------------\n',
            bg=backgroundInfoTabWindows_IO,
            font=self.titleFont,
            )
        self.labelHostInfoWindows_IO.grid(
            row=0,
            column=0,
            padx=0,
            pady=2,
            sticky=N,
            )
            
        self.labelHostInfoCommandsWindows_IO = Label(
            childFrame,
            text='COMMANDS',
            bg=backgroundInfoTabWindows_IO,
            )
        self.labelHostInfoCommandsWindows_IO.grid(
            row=1,
            padx=0,
            pady=2,
            ipady=2,
            sticky=N,
            )

# control variable used by all 'clear' radiobuttons for the i/o windows
        self.varClearWindows_IO = StringVar()
        
        self.radiobuttonClearHostInfoCommandsWindows_IO = Radiobutton(
            childFrame,
            variable=self.varClearWindows_IO,
            value='HostInfoCommandsWindows_IO',
            text='Clear',
            bg='white',
            fg='blue',
            font=self.buttonClearFont,
            borderwidth=3,
            indicatoron=0,
            relief=RAISED,
            width=5,         
            command=self.handlerClearWindows_IO,
            )
        self.radiobuttonClearHostInfoCommandsWindows_IO.grid(
            row=1,
            sticky=SE,
            padx=0,
            pady=2,
            )
            
        self.yScrollHostInfoCommandsWindows_IO = Scrollbar(
            childFrame,
            orient=VERTICAL,
            )
        self.yScrollHostInfoCommandsWindows_IO.grid(
            row=2,
            column=1,
            sticky=NS,
            )
        self.textHostInfoCommandsWindows_IO = Text(
            childFrame,
            font=self.dataFont,
            borderwidth=5,
            relief=RIDGE,
            wrap=WORD,
            height=5,
            width=100,
            bg=backgroundCommandsInfoTabWindows_IO,
            fg=foregroundCommandsInfoTabWindows_IO,
            yscrollcommand=self.yScrollHostInfoCommandsWindows_IO.set,
            )
        self.textHostInfoCommandsWindows_IO.grid(
            row=2, 
            column=0,  
            rowspan=1,
            padx=0,
            pady=0,
            sticky=NSEW
            )
        self.yScrollHostInfoCommandsWindows_IO.configure(
            command=self.textHostInfoCommandsWindows_IO.yview
            )
        
        '''
        self.textHostInfoCommandsWindows_IO.insert(
            END,
            '>$ '
            )
        '''
        
#output box
        self.labelHostInfoOutputWindows_IO=Label(
            childFrame,
            text='\n\nOUTPUT',
            bg=backgroundInfoTabWindows_IO,
            )
        self.labelHostInfoOutputWindows_IO.grid(
            row=3,
            padx=0,
            pady=2,
            )
            
        self.radiobuttonClearHostInfoOutputWindows_IO = Radiobutton(
            childFrame,
            variable=self.varClearWindows_IO,
            value='HostInfoOutputWindows_IO',
            text='Clear',
            bg='white',
            fg='blue',
            font=self.buttonClearFont,
            borderwidth=3,
            indicatoron=0,
            relief=RAISED,
            width=5,         
            command=self.handlerClearWindows_IO,
            )
        self.radiobuttonClearHostInfoOutputWindows_IO.grid(
            row=3,
            sticky=SE,
            padx=0,
            pady=2,
            )
            
        self.yScrollHostInfoOutputWindows_IO=Scrollbar(
            childFrame,
            orient=VERTICAL,
            )
        self.yScrollHostInfoOutputWindows_IO.grid(
            row=4,
            column=1,
            sticky=NS,
            )
        self.textHostInfoOutputWindows_IO = Text(
            childFrame,
            font=self.dataFont,
            borderwidth=5,
            relief=RIDGE,
            wrap=WORD,
            height=15,
            width=100,
            bg=backgroundOutputInfoTabWindows_IO,
            fg=foregroundOutputInfoTabWindows_IO,
            insertbackground=insertbackgroundOutputInfoTabWindows_IO,
            yscrollcommand=self.yScrollHostInfoOutputWindows_IO.set,
            )
        self.textHostInfoOutputWindows_IO.grid(
            row=4,
            column=0,
            padx=0,
            pady=0,
            sticky=N+S+E+W
            )
        self.yScrollHostInfoOutputWindows_IO.configure(
            command=self.textHostInfoOutputWindows_IO.yview
            )
        
        '''       
         self.textHostInfoOutputWindows_IO.insert(
            END,
            '>$ '
            )
         '''
        
        return
        

    def frameExternalCvsSvnAccessWindows_IO(self,parent):
        '''
        Purpose:
            create external CVS/SVN ACCESS frame
        '''
        
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'frameExternalCvsSvnAccess_IO'
        
        self.frameCvsSvnAccessWindows_IO = Frame(
            parent,
            borderwidth=2,
            relief=RIDGE,
            height=externalFrameHeight,
            width=externalFrameWidth,
            bg=backgroundCvsSvnAccessTabWindows_IO,
            )
        self.frameCvsSvnAccessWindows_IO.grid(
            row=0,
            column=1,
            padx=2,
            pady=2,
            rowspan=3,
            sticky=NSEW,
            )
        self.frameCvsSvnAccessWindows_IO.grid_propagate(0)
        
        childFrame=self.frameCvsSvnAccessWindows_IO
        
        self.labelCvsSvnAccessWindows_IO = Label(
            childFrame,
            text='-- CVS/SVN ACCESS TAB I/O WINDOW --\n' +
                 '----------------------------\n',
            bg=backgroundCvsSvnAccessTabWindows_IO,
            font=self.titleFont,
            )
        self.labelCvsSvnAccessWindows_IO.grid(
            row=0,
            column=0,
            padx=2,
            pady=2,
            sticky=N,
            )
            
        self.labelCvsSvnAccessCommandsWindows_IO = Label(
            childFrame,
            text='COMMANDS',
            bg=backgroundCvsSvnAccessTabWindows_IO,
            )
        self.labelCvsSvnAccessCommandsWindows_IO.grid(
            row=1,
            padx=0,
            pady=2,
            ipady=2,
            sticky=N,
            )
            
        self.radiobuttonClearCvsSvnAccessCommandsWindows_IO = Radiobutton(
            childFrame,
            variable=self.varClearWindows_IO,
            value='CvsSvnAccessCommandsWindows_IO',
            text='Clear',
            bg='white',
            fg='blue',
            font=self.buttonClearFont,
            borderwidth=3,
            indicatoron=0,
            relief=RAISED,
            width=5,         
            command=self.handlerClearWindows_IO,
            )
        self.radiobuttonClearCvsSvnAccessCommandsWindows_IO.grid(
            row=1,
            sticky=SE,
            padx=0,
            pady=2,
            )
            
        self.yScrollCvsSvnAccessCommandsWindows_IO = Scrollbar(
            childFrame,
            orient=VERTICAL,
            )
        self.yScrollCvsSvnAccessCommandsWindows_IO.grid(
            row=2,
            column=1,
            sticky=NS,
            )
        self.textCvsSvnAccessCommandsWindows_IO = Text(
            childFrame,
            font=self.dataFont,
            borderwidth=5,
            relief=RIDGE,
            wrap=WORD,
            height=5,
            width=100,
            bg=backgroundCommandsCvsSvnAccessTabWindows_IO,
            fg=foregroundCommandsCvsSvnAccessTabWindows_IO,
            yscrollcommand=self.yScrollCvsSvnAccessCommandsWindows_IO.set,
            )
        self.textCvsSvnAccessCommandsWindows_IO.grid(
            row=2, 
            column=0,  
            rowspan=1,
            padx=0,
            pady=0,
            sticky=NSEW
            )
        self.yScrollCvsSvnAccessCommandsWindows_IO.configure(
            command=self.textCvsSvnAccessCommandsWindows_IO.yview
            )
            
        '''
        self.textCvsSvnAccessCommandsWindows_IO.insert(
            END,
            '>$ '
            )
        '''
        
#output box
        self.labelCvsSvnAccessOutputWindows_IO = Label(
            childFrame,
            text='\n\nOUTPUT',
            bg=backgroundCvsSvnAccessTabWindows_IO,
            )
        self.labelCvsSvnAccessOutputWindows_IO.grid(
            row=3,
            padx=0,
            pady=2,
            )
            
        self.radiobuttonClearCvsSvnOutputWindows_IO = Radiobutton(
            childFrame,
            variable=self.varClearWindows_IO,
            value='CvsSvnAccessOutputWindows_IO',
            text='Clear',
            bg='white',
            fg='blue',
            font=self.buttonClearFont,
            borderwidth=3,
            indicatoron=0,
            relief=RAISED,
            width=5,         
            command=self.handlerClearWindows_IO,
            )
        self.radiobuttonClearCvsSvnOutputWindows_IO.grid(
            row=3,
            sticky=SE,
            padx=0,
            pady=2,
            ) 
            
        self.yScrollCvsSvnAccessOutputWindows_IO=Scrollbar(
            childFrame,
            orient=VERTICAL,
            )
        self.yScrollCvsSvnAccessOutputWindows_IO.grid(
            row=4,
            column=1,
            sticky=NS,
            )
        self.textCvsSvnAccessOutputWindows_IO = Text(
            childFrame,
            font=self.dataFont,
            borderwidth=5,
            relief=RIDGE,
            wrap=WORD,
            height=15,
            width=100,
            bg=backgroundOutputCvsSvnAccessTabWindows_IO,
            fg=foregroundOutputCvsSvnAccessTabWindows_IO,
            insertbackground=insertbackgroundOutputCvsSvnAccessTabWindows_IO,
            yscrollcommand=self.yScrollCvsSvnAccessOutputWindows_IO.set,
            )
        self.textCvsSvnAccessOutputWindows_IO.grid(
            row=4,
            column=0,
            padx=0,
            pady=0,
            sticky=N+S+E+W
            )
        self.yScrollCvsSvnAccessOutputWindows_IO.configure(
            command=self.textCvsSvnAccessOutputWindows_IO.yview
            )
            
        '''
         self.textCvsSvnAccessOutputWindows_IO.insert(
            END,
            '>$ '
            )
         '''
        
        return
        
        
    def frameExternalCompileWindows_IO(self,parent):
        '''
        Purpose:
            create external COMPILE frame
        '''
        
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'frameExternalCompileWindows_IO'
        
        self.frameCompileWindows_IO = Frame(
            parent,
            borderwidth=2,
            relief=RIDGE,
            height=externalFrameHeight,
            width=externalFrameWidth,
            bg=backgroundCompileTabWindows_IO,
            )
        self.frameCompileWindows_IO.grid(
            row=0,
            column=1,
            padx=2,
            pady=2,
            rowspan=3,
            sticky=NSEW,
            )
        self.frameCompileWindows_IO.grid_propagate(0)
        
        childFrame=self.frameCompileWindows_IO
        
        self.labelCompileWindows_IO = Label(
            childFrame,
            text='-- COMPILE TAB I/O WINDOW --\n' +
                 '----------------------------\n',
            bg=backgroundCompileTabWindows_IO,
            font=self.titleFont,
            )
        self.labelCompileWindows_IO.grid(
            row=0,
            column=0,
            padx=2,
            pady=2,
            sticky=N,
            )
            
        self.labelCompileCommandsWindows_IO = Label(
            childFrame,
            text='COMMANDS',
            bg=backgroundCompileTabWindows_IO,
            )
        self.labelCompileCommandsWindows_IO.grid(
            row=1,
            padx=0,
            pady=2,
            ipady=2,
            sticky=N,
            )
            
        self.radiobuttonClearCompileCommandsWindows_IO = Radiobutton(
            childFrame,
            variable=self.varClearWindows_IO,
            value='CompileCommandsWindows_IO',
            text='Clear',
            bg='white',
            fg='blue',
            font=self.buttonClearFont,
            borderwidth=3,
            indicatoron=0,
            relief=RAISED,
            width=5,         
            command=self.handlerClearWindows_IO,
            )
        self.radiobuttonClearCompileCommandsWindows_IO.grid(
            row=1,
            sticky=SE,
            padx=0,
            pady=2,
            )
            
        self.yScrollCompileCommandsWindows_IO = Scrollbar(
            childFrame,
            orient=VERTICAL,
            )
        self.yScrollCompileCommandsWindows_IO.grid(
            row=2,
            column=1,
            sticky=NS,
            )
        self.textCompileCommandsWindows_IO = Text(
            childFrame,
            font=self.dataFont,
            borderwidth=5,
            relief=RIDGE,
            wrap=WORD,
            height=5,
            width=100,
            bg=backgroundCommandsCompileTabWindows_IO,
            fg=foregroundCommandsCompileTabWindows_IO,
            yscrollcommand=self.yScrollCompileCommandsWindows_IO.set,
            )
        self.textCompileCommandsWindows_IO.grid(
            row=2, 
            column=0,  
            rowspan=1,
            padx=0,
            pady=0,
            sticky=NSEW
            )
        self.yScrollCompileCommandsWindows_IO.configure(
            command=self.textCompileCommandsWindows_IO.yview
            )
            
        '''
        self.textCompileCommandsWindows_IO.insert(
            END,
            '>$ '
            )
        '''
        
#output box
        self.labelCompileOutputWindows_IO=Label(
            childFrame,
            text='\n\nOUTPUT',
            bg=backgroundCompileTabWindows_IO,
            )
        self.labelCompileOutputWindows_IO.grid(
            row=3,
            padx=0,
            pady=2,
            )
            
        self.radiobuttonClearCompileOutputWindows_IO = Radiobutton(
            childFrame,
            variable=self.varClearWindows_IO,
            value='CompileOutputWindows_IO',
            text='Clear',
            bg='white',
            fg='blue',
            font=self.buttonClearFont,
            borderwidth=3,
            indicatoron=0,
            relief=RAISED,
            width=5,         
            command=self.handlerClearWindows_IO,
            )
        self.radiobuttonClearCompileOutputWindows_IO.grid(
            row=3,
            sticky=SE,
            padx=0,
            pady=2,
            )
            
        self.yScrollCompileOutputWindows_IO = Scrollbar(
            childFrame,
            orient=VERTICAL,
            )
        self.yScrollCompileOutputWindows_IO.grid(
            row=4,
            column=1,
            sticky=NS,
            )
        self.textCompileOutputWindows_IO = Text(
            childFrame,
            font=self.dataFont,
            borderwidth=5,
            relief=RIDGE,
            wrap=WORD,
            height=15,
            width=100,
            bg=backgroundOutputCompileTabWindows_IO,
            fg=foregroundOutputCompileTabWindows_IO,
            insertbackground=insertbackgroundOutputCompileTabWindows_IO,
            yscrollcommand=self.yScrollCompileOutputWindows_IO.set,
            )
        self.textCompileOutputWindows_IO.grid(
            row=4,
            column=0,
            padx=0,
            pady=0,
            sticky=N+S+E+W
            )
            
        self.yScrollCompileOutputWindows_IO.configure(
            command=self.textCompileOutputWindows_IO.yview
            )            
            
        '''
         self.textCompileOutputWindows_IO.insert(
            END,
            '>$ '
            )
         '''
         
        return
        
        
    def frameExternalSetupWindows_IO(self,parent):
        '''
        Purpose:
            set up external SETUP tab
        '''
        
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'frameExternalSetupWindows_IO'
        
        self.frameSetupWindows_IO = Frame(
            parent,
            borderwidth=2,
            relief=RIDGE,
            height=externalFrameHeight,
            width=externalFrameWidth,
            bg=backgroundSetupTabWindows_IO,
            )
        self.frameSetupWindows_IO.grid(
            row=0,
            column=1,
            padx=2,
            pady=2,
            rowspan=3,
            sticky=NSEW,
            )
        self.frameSetupWindows_IO.grid_propagate(0)
        
        childFrame=self.frameSetupWindows_IO
        
        self.labelSetupWindows_IO = Label(
            childFrame,
            text='-- SETUP TAB I/O WINDOW --\n' +
                 '----------------------------\n',
            bg=backgroundSetupTabWindows_IO,
            font=self.titleFont,
            )
        self.labelSetupWindows_IO.grid(
            row=0,
            column=0,
            padx=2,
            pady=2,
            sticky=N,
            )
            
        self.labelSetupCommandsWindows_IO = Label(
            childFrame,
            text='COMMANDS',
            bg=backgroundSetupTabWindows_IO,
            )
        self.labelSetupCommandsWindows_IO.grid(
            row=1,
            padx=0,
            pady=2,
            ipady=2,
            sticky=N,
            )
            
        self.radiobuttonClearSetupCommandsWindows_IO = Radiobutton(
            childFrame,
            variable=self.varClearWindows_IO,
            value='SetupCommandsWindows_IO',
            text='Clear',
            bg='white',
            fg='blue',
            font=self.buttonClearFont,
            borderwidth=3,
            indicatoron=0,
            relief=RAISED,
            width=5,         
            command=self.handlerClearWindows_IO,
            )
        self.radiobuttonClearSetupCommandsWindows_IO.grid(
            row=1,
            sticky=SE,
            padx=0,
            pady=2,
            )
            
        self.yScrollSetupCommandsWindows_IO=Scrollbar(
            childFrame,
            orient=VERTICAL,
            )
        self.yScrollSetupCommandsWindows_IO.grid(
            row=2,
            column=1,
            sticky=NS,
            )
            
        self.textSetupCommandsWindows_IO = Text(
            childFrame,
            font=self.dataFont,
            borderwidth=5,
            relief=RIDGE,
            wrap=WORD,
            height=5,
            width=100,
            bg=backgroundCommandsSetupTabWindows_IO,
            fg=foregroundCommandsSetupTabWindows_IO,
            yscrollcommand=self.yScrollSetupCommandsWindows_IO.set,
            )
        self.textSetupCommandsWindows_IO.grid(
            row=2, 
            column=0,  
            rowspan=1,
            padx=0,
            pady=0,
            sticky=NSEW
            )
        self.yScrollSetupCommandsWindows_IO.configure(
            command=self.textSetupCommandsWindows_IO.yview
            )
            
        '''
        self.textSetupCommandsWindows_IO.insert(
            END,
            '>$ '
            )
        '''
        
#output box
        self.labelSetupOutputWindows_IO=Label(
            childFrame,
            text='\n\nOUTPUT',
            bg=backgroundSetupTabWindows_IO,
            )
        self.labelSetupOutputWindows_IO.grid(
            row=3,
            padx=0,
            pady=2,
            )
          
        self.radiobuttonClearSetupOutputWindows_IO = Radiobutton(
            childFrame,
            variable=self.varClearWindows_IO,
            value='SetupOutputWindows_IO',
            text='Clear',
            bg='white',
            fg='blue',
            font=self.buttonClearFont,
            borderwidth=3,
            indicatoron=0,
            relief=RAISED,
            width=5,         
            command=self.handlerClearWindows_IO,
            )
        self.radiobuttonClearSetupOutputWindows_IO.grid(
            row=3,
            sticky=SE,
            padx=0,
            pady=2,
            )
            
        self.yScrollSetupOutputWindows_IO = Scrollbar(
            childFrame,
            orient=VERTICAL,
            )
        self.yScrollSetupOutputWindows_IO.grid(
            row=4,
            column=1,
            sticky=NS,
            )
        self.textSetupOutputWindows_IO = Text(
            childFrame,
            font=self.dataFont,
            borderwidth=5,
            relief=RIDGE,
            wrap=WORD,
            height=15,
            width=100,
            bg=backgroundOutputSetupTabWindows_IO,
            fg=foregroundOutputSetupTabWindows_IO,
            insertbackground=insertbackgroundOutputSetupTabWindows_IO,
            yscrollcommand=self.yScrollSetupOutputWindows_IO.set,
            )
        self.textSetupOutputWindows_IO.grid(
            row=4,
            column=0,
            padx=0,
            pady=0,
            sticky=N+S+E+W
            )          
        self.yScrollSetupOutputWindows_IO.configure(
            command=self.textSetupOutputWindows_IO.yview
            )
            
        '''
        self.textSetupOutputWindows_IO.insert(
            END,
            '>$ '
            )
        '''
        
        return
        
        
    def frameExternalRunWindows_IO(self,parent):
        '''
        Purpose:
           create external RUN frame  
        '''
        
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'frameExternalRunWindows_IO'
        
        self.frameRunWindows_IO = Frame(
            parent,
            borderwidth=2,
            relief=RIDGE,
            height=externalFrameHeight,
            width=externalFrameWidth,
            bg=backgroundRunTabWindows_IO,
            )
        self.frameRunWindows_IO.grid(
            row=0,
            column=1,
            padx=2,
            pady=2,
            rowspan=3,
            sticky=NSEW,
            )
        self.frameRunWindows_IO.grid_propagate(0)
        
        childFrame=self.frameRunWindows_IO
        
        self.labelRunWindows_IO = Label(
            childFrame,
            text='-- RUN TAB I/O WINDOW --\n' +
                 '----------------------------\n',
            bg=backgroundRunTabWindows_IO,
            font=self.titleFont,
            )
        self.labelRunWindows_IO.grid(
            row=0,
            column=0,
            padx=2,
            pady=2,
            sticky=N,
            )
            
        self.labelRunCommandsWindows_IO = Label(
            childFrame,
            text='COMMANDS',
            bg=backgroundRunTabWindows_IO,
            )
        self.labelRunCommandsWindows_IO.grid(
            row=1,
            padx=0,
            pady=2,
            ipady=2,
            sticky=N,
            )
            
        self.radiobuttonClearRunCommandsWindows_IO = Radiobutton(
            childFrame,
            variable=self.varClearWindows_IO,
            value='RunCommandsWindows_IO',
            text='Clear',
            bg='white',
            fg='blue',
            font=self.buttonClearFont,
            borderwidth=3,
            indicatoron=0,
            relief=RAISED,
            width=5,         
            command=self.handlerClearWindows_IO,
            )
        self.radiobuttonClearRunCommandsWindows_IO.grid(
            row=1,
            sticky=SE,
            padx=0,
            pady=2,
            )
            
        self.yScrollRunCommandsWindows_IO=Scrollbar(
            childFrame,
            orient=VERTICAL,
            )
        self.yScrollRunCommandsWindows_IO.grid(
            row=2,
            column=1,
            sticky=NS,
            )
        self.textRunCommandsWindows_IO = Text(
            childFrame,
            font=self.dataFont,
            borderwidth=5,
            relief=RIDGE,
            wrap=WORD,
            height=5,
            width=100,
            bg=backgroundCommandsRunTabWindows_IO,
            fg=foregroundCommandsRunTabWindows_IO,
            yscrollcommand=self.yScrollRunCommandsWindows_IO.set,
            )
        self.textRunCommandsWindows_IO.grid(
            row=2, 
            column=0,  
            rowspan=1,
            padx=0,
            pady=0,
            sticky=NSEW
            )
        self.yScrollRunCommandsWindows_IO.configure(
            command=self.textRunCommandsWindows_IO.yview
            )
            
        '''
        self.textRunCommandsWindows_IO.insert(
            END,
            '>$ '
            )
        '''
        
#output box
        self.labelRunOutputWindows_IO=Label(
            childFrame,
            text='\n\nOUTPUT',
            bg=backgroundRunTabWindows_IO,
            )
        self.labelRunOutputWindows_IO.grid(
            row=3,
            padx=0,
            pady=2,
            )
            
        self.radiobuttonClearRunOutputWindows_IO = Radiobutton(
            childFrame,
            variable=self.varClearWindows_IO,
            value='RunOutputWindows_IO',
            text='Clear',
            bg='white',
            fg='blue',
            font=self.buttonClearFont,
            borderwidth=3,
            indicatoron=0,
            relief=RAISED,
            width=5,         
            command=self.handlerClearWindows_IO,
            )
        self.radiobuttonClearRunOutputWindows_IO.grid(
            row=3,
            sticky=SE,
            padx=0,
            pady=2,
            )
            
        self.yScrollRunOutputWindows_IO = Scrollbar(
            childFrame,
            orient=VERTICAL,
            )
        self.yScrollRunOutputWindows_IO.grid(
            row=4,
            column=1,
            sticky=NS,
            )
        self.textRunOutputWindows_IO = Text(
            childFrame,
            font=self.dataFont,
            borderwidth=5,
            relief=RIDGE,
            wrap=WORD,
            height=15,
            width=100,
            bg=backgroundOutputRunTabWindows_IO,
            fg=foregroundOutputRunTabWindows_IO,
            insertbackground=insertbackgroundOutputRunTabWindows_IO,
            yscrollcommand=self.yScrollRunOutputWindows_IO.set,
            )
        self.textRunOutputWindows_IO.grid(
            row=4,
            column=0,
            padx=0,
            pady=0,
            sticky=N+S+E+W
            )
        self.yScrollRunOutputWindows_IO.configure(
            command=self.textRunOutputWindows_IO.yview
            )            
            
        '''
         self.textRunOutputWindows_IO.insert(
            END,
            '>$ '
            )
         '''
         
        return
        
        
    def frameExternalStatusWindows_IO(self,parent):
        '''
        Purpose:
            setup external STATUS tab
        '''
        
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'frameExternalStatusWindows_IO'
        
        self.frameStatusWindows_IO = Frame(
            parent,
            borderwidth=2,
            relief=RIDGE,
            height=externalFrameHeight,
            width=externalFrameWidth,
            bg=backgroundStatusTabWindows_IO,
            )
        self.frameStatusWindows_IO.grid(
            row=0,
            column=1,
            padx=2,
            pady=2,
            rowspan=3,
            sticky=NSEW,
            )
        self.frameStatusWindows_IO.grid_propagate(0)
        
        childFrame=self.frameStatusWindows_IO
        
        self.labelStatusWindows_IO = Label(
            childFrame,
            text='-- STATUS TAB I/O WINDOW --\n' +
                 '----------------------------\n',
            bg=backgroundStatusTabWindows_IO,
            font=self.titleFont,
            )
        self.labelStatusWindows_IO.grid(
            row=0,
            column=0,
            padx=2,
            pady=2,
            sticky=N,
            )
            
        self.labelStatusCommandsWindows_IO = Label(
            childFrame,
            text='COMMANDS',
            bg=backgroundStatusTabWindows_IO,
            )
        self.labelStatusCommandsWindows_IO.grid(
            row=1,
            padx=0,
            pady=2,
            ipady=2,
            sticky=N,
            )
            
        self.radiobuttonClearStatusCommandsWindows_IO = Radiobutton(
            childFrame,
            variable=self.varClearWindows_IO,
            value='StatusCommandsWindows_IO',
            text='Clear',
            bg='white',
            fg='blue',
            font=self.buttonClearFont,
            borderwidth=3,
            indicatoron=0,
            relief=RAISED,
            width=5,         
            command=self.handlerClearWindows_IO,
            )
        self.radiobuttonClearStatusCommandsWindows_IO.grid(
            row=1,
            sticky=SE,
            padx=0,
            pady=2,
            )
            
        self.yScrollStatusCommandsWindows_IO = Scrollbar(
            childFrame,
            orient=VERTICAL,
            )
        self.yScrollStatusCommandsWindows_IO.grid(
            row=2,
            column=1,
            sticky=NS,
            )
        self.textStatusCommandsWindows_IO = Text(
            childFrame,
            font=self.dataFont,
            borderwidth=5,
            relief=RIDGE,
            wrap=WORD,
            height=5,
            width=100,
            bg=backgroundCommandsStatusTabWindows_IO,
            fg=foregroundCommandsStatusTabWindows_IO,
            yscrollcommand=self.yScrollStatusCommandsWindows_IO.set,
            )
        self.textStatusCommandsWindows_IO.grid(
            row=2, 
            column=0,  
            rowspan=1,
            padx=0,
            pady=0,
            sticky=NSEW
            )
        self.yScrollStatusCommandsWindows_IO.configure(
            command=self.textStatusCommandsWindows_IO.yview
            )            
            
        '''
        self.textStatusCommandsWindows_IO.insert(
            END,
            '>$ '
            )
        '''
        
#output box
        self.labelStatusOutputWindows_IO=Label(
            childFrame,
            text='\n\nOUTPUT',
            bg=backgroundStatusTabWindows_IO,
            )
        self.labelStatusOutputWindows_IO.grid(
            row=3,
            padx=0,
            pady=2,
            )
            
        self.radiobuttonClearStatusOutputWindows_IO = Radiobutton(
            childFrame,
            variable=self.varClearWindows_IO,
            value='StatusOutputWindows_IO',
            text='Clear',
            bg='white',
            fg='blue',
            font=self.buttonClearFont,
            borderwidth=3,
            indicatoron=0,
            relief=RAISED,
            width=5,         
            command=self.handlerClearWindows_IO,
            )
        self.radiobuttonClearStatusOutputWindows_IO.grid(
            row=3,
            sticky=SE,
            padx=0,
            pady=2,
            )
            
        self.yScrollStatusOutputWindows_IO = Scrollbar(
            childFrame,
            orient=VERTICAL,
            )
        self.yScrollStatusOutputWindows_IO.grid(
            row=4,
            column=1,
            sticky=NS,
            )
        self.textStatusOutputWindows_IO = Text(
            childFrame,
            font=self.dataFont,
            borderwidth=5,
            relief=RIDGE,
            wrap=WORD,
            height=15,
            width=100,
            bg=backgroundOutputStatusTabWindows_IO,
            fg=foregroundOutputStatusTabWindows_IO,
            insertbackground=insertbackgroundOutputStatusTabWindows_IO,
            yscrollcommand=self.yScrollStatusOutputWindows_IO.set,
            )
        self.textStatusOutputWindows_IO.grid(
            row=4,
            column=0,
            padx=0,
            pady=0,
            sticky=N+S+E+W
            )
        self.yScrollStatusOutputWindows_IO.configure(
            command=self.textStatusOutputWindows_IO.yview
            )            
           
        '''
         self.textStatusOutputWindows_IO.insert(
            END,
            '>$ '
            )
         '''
        
    def frameExternalPostProcessWindows_IO(self,parent):
        '''
        Purpose:
            create external POST-PROCESS frame
        '''
        
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'frameExternalPostProcessWindows_IO'
        
        self.framePostProcessWindows_IO = Frame(
            parent,
            borderwidth=2,
            relief=RIDGE,
            height=externalFrameHeight,
            width=externalFrameWidth,
            bg=backgroundPostProcessTabWindows_IO,
            )
        self.framePostProcessWindows_IO.grid(
            row=0,
            column=1,
            padx=2,
            pady=2,
            rowspan=3,
            sticky=NSEW,
            )
        self.framePostProcessWindows_IO.grid_propagate(0)
        
        childFrame=self.framePostProcessWindows_IO
        
        self.labelPostProcessWindows_IO = Label(
            childFrame,
            text='-- POST-PROCESS TAB I/O WINDOW --\n' +
                 '----------------------------\n',
            bg=backgroundPostProcessTabWindows_IO,
            font=self.titleFont,
            )
        self.labelPostProcessWindows_IO.grid(
            row=0,
            column=0,
            padx=2,
            pady=2,
            sticky=N,
            )
            
        self.labelPostProcessCommandsWindows_IO = Label(
            childFrame,
            text='COMMANDS',
            bg=backgroundPostProcessTabWindows_IO,
            )
        self.labelPostProcessCommandsWindows_IO.grid(
            row=1,
            padx=0,
            pady=2,
            ipady=2,
            sticky=N,
            )
         
        self.radiobuttonClearPostProcessCommandsWindows_IO = Radiobutton(
            childFrame,
            variable=self.varClearWindows_IO,
            value='PostProcessCommandsWindows_IO',
            text='Clear',
            bg='white',
            fg='blue',
            font=self.buttonClearFont,
            borderwidth=3,
            indicatoron=0,
            relief=RAISED,
            width=5,         
            command=self.handlerClearWindows_IO,
            )
        self.radiobuttonClearPostProcessCommandsWindows_IO.grid(
            row=1,
            sticky=SE,
            padx=0,
            pady=2,
            )
            
        self.yScrollPostProcessCommandsWindows_IO = Scrollbar(
            childFrame,
            orient=VERTICAL,
            )
        self.yScrollPostProcessCommandsWindows_IO.grid(
            row=2,
            column=1,
            sticky=NS,
            )
        self.textPostProcessCommandsWindows_IO = Text(
            childFrame,
            font=self.dataFont,
            borderwidth=5,
            relief=RIDGE,
            wrap=WORD,
            height=5,
            width=100,
            bg=backgroundCommandsPostProcessTabWindows_IO,
            fg=foregroundCommandsPostProcessTabWindows_IO,
            yscrollcommand=self.yScrollPostProcessCommandsWindows_IO.set,
            )
        self.textPostProcessCommandsWindows_IO.grid(
            row=2, 
            column=0,  
            rowspan=1,
            padx=0,
            pady=0,
            sticky=NSEW
            )
        self.yScrollPostProcessCommandsWindows_IO.configure(
            command=self.textPostProcessCommandsWindows_IO.yview
            )            
            
        '''self.textPostProcessCommandsWindows_IO.insert(
            END,
            '>$ '
            )
        '''
        
#output box
        self.labelPostProcessOutputWindows_IO = Label(
            childFrame,
            text='\n\nOUTPUT',
            bg=backgroundPostProcessTabWindows_IO,
            )
        self.labelPostProcessOutputWindows_IO.grid(
            row=3,
            padx=0,
            pady=2,
            )
            
        self.radiobuttonClearPostProcessOutputWindows_IO = Radiobutton(
            childFrame,
            variable=self.varClearWindows_IO,
            value='PostProcessOutputWindows_IO',
            text='Clear',
            bg='white',
            fg='blue',
            font=self.buttonClearFont,
            borderwidth=3,
            indicatoron=0,
            relief=RAISED,
            width=5,         
            command=self.handlerClearWindows_IO,
            )
        self.radiobuttonClearPostProcessOutputWindows_IO.grid(
            row=3,
            sticky=SE,
            padx=0,
            pady=2,
            )
            
        self.yScrollPostProcessOutputWindows_IO = Scrollbar(
            childFrame,
            orient=VERTICAL,
            )
        self.yScrollPostProcessOutputWindows_IO.grid(
            row=4,
            column=1,
            sticky=NS,
            )
        self.textPostProcessOutputWindows_IO = Text(
            childFrame,
            font=self.dataFont,
            borderwidth=5,
            relief=RIDGE,
            wrap=WORD,
            height=15,
            width=100,
            bg=backgroundOutputPostProcessTabWindows_IO,
            fg=foregroundOutputPostProcessTabWindows_IO,
            insertbackground=insertbackgroundOutputPostProcessTabWindows_IO,
            yscrollcommand=self.yScrollPostProcessOutputWindows_IO.set,
            )
        self.textPostProcessOutputWindows_IO.grid(
            row=4,
            column=0,
            padx=0,
            pady=0,
            sticky=N+S+E+W
            )
        self.yScrollPostProcessOutputWindows_IO.configure(
            command=self.textPostProcessOutputWindows_IO.yview
            )            
            
        '''
        self.textPostProcessOutputWindows_IO.insert(
            END,
            '>$ '
            )
        '''
        
    def frameExternalMySQLWindows_IO(self,parent):
        '''
        Purpose:
            create external MySQL ACCESS frame    
        '''
        
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'frameExternalMySQLWindows_IO'
        
        self.frameMySQLWindows_IO = Frame(
            parent,
            borderwidth=2,
            relief=RIDGE,
            height=externalFrameHeight,
            width=externalFrameWidth,
            bg=backgroundMySQLTabWindows_IO,
            )
        self.frameMySQLWindows_IO.grid(
            row=0,
            column=1,
            padx=2,
            pady=2,
            rowspan=3,
            sticky=NSEW,
            )
        self.frameMySQLWindows_IO.grid_propagate(0)
        
        childFrame = self.frameMySQLWindows_IO
        
        self.labelMySQLWindows_IO = Label(
            childFrame,
            text='-- MySQL ACCESS TAB I/O WINDOW --\n' +
                 '----------------------------\n',
            bg=backgroundMySQLTabWindows_IO,
            font=self.titleFont,
            )
        self.labelMySQLWindows_IO.grid(
            row=0,
            column=0,
            padx=2,
            pady=2,
            sticky=N,
            )
            
        self.labelMySQLCommandsWindows_IO = Label(
            childFrame,
            text='COMMANDS',
            bg=backgroundMySQLTabWindows_IO,
            )
        self.labelMySQLCommandsWindows_IO.grid(
            row=1,
            padx=0,
            pady=2,
            ipady=2,
            sticky=N,
            )
            
        self.radiobuttonClearMySQLCommandsWindows_IO = Radiobutton(
            childFrame,
            variable=self.varClearWindows_IO,
            value='MySQLCommandsWindows_IO',
            text='Clear',
            bg='white',
            fg='blue',
            font=self.buttonClearFont,
            borderwidth=3,
            indicatoron=0,
            relief=RAISED,
            width=5,         
            command=self.handlerClearWindows_IO,
            )
        self.radiobuttonClearMySQLCommandsWindows_IO.grid(
            row=1,
            sticky=SE,
            padx=0,
            pady=2,
            )
            
        self.yScrollMySQLCommandsWindows_IO = Scrollbar(
            childFrame,
            orient=VERTICAL,
            )
        self.yScrollMySQLCommandsWindows_IO.grid(
            row=2,
            column=1,
            sticky=NS,
            )
        self.textMySQLCommandsWindows_IO = Text(
            childFrame,
            font=self.dataFont,
            borderwidth=5,
            relief=RIDGE,
            wrap=WORD,
            height=5,
            width=100,
            bg=backgroundCommandsMySQLTabWindows_IO,
            fg=foregroundCommandsMySQLTabWindows_IO,
            yscrollcommand=self.yScrollMySQLCommandsWindows_IO.set,
            )
        self.textMySQLCommandsWindows_IO.grid(
            row=2, 
            column=0,  
            rowspan=1,
            padx=0,
            pady=0,
            sticky=NSEW
            )
        self.yScrollMySQLCommandsWindows_IO.configure(
            command=self.textMySQLCommandsWindows_IO.yview
            )            
            
        '''
        self.textMySQLCommandsWindows_IO.insert(
            END,
            '>$ '
            )
        '''
        
#output box
        self.labelMySQLOutputWindows_IO=Label(
            childFrame,
            text='\n\nOUTPUT',
            bg=backgroundMySQLTabWindows_IO,
            )
        self.labelMySQLOutputWindows_IO.grid(
            row=3,
            padx=0,
            pady=2,
            )
            
        self.radiobuttonClearMySQLOutputWindows_IO = Radiobutton(
            childFrame,
            variable=self.varClearWindows_IO,
            value='MySQLOutputWindows_IO',
            text='Clear',
            bg='white',
            fg='blue',
            font=self.buttonClearFont,
            borderwidth=3,
            indicatoron=0,
            relief=RAISED,
            width=5,         
            command=self.handlerClearWindows_IO,
            )
        self.radiobuttonClearMySQLOutputWindows_IO.grid(
            row=3,
            sticky=SE,
            padx=0,
            pady=2,
            )
            
        self.yScrollMySQLOutputWindows_IO = Scrollbar(
            childFrame,
            orient=VERTICAL,
            )
        self.yScrollMySQLOutputWindows_IO.grid(
            row=4,
            column=1,
            sticky=NS,
            )
        self.textMySQLOutputWindows_IO = Text(
            childFrame,
            font=self.dataFont,
            borderwidth=5,
            relief=RIDGE,
            wrap=WORD,
            height=15,
            width=100,
            bg=backgroundOutputMySQLTabWindows_IO,
            fg=foregroundOutputMySQLTabWindows_IO,
            insertbackground=insertbackgroundOutputMySQLTabWindows_IO,
            yscrollcommand=self.yScrollMySQLOutputWindows_IO.set,
            )
        self.textMySQLOutputWindows_IO.grid(
            row=4,
            column=0,
            padx=0,
            pady=0,
            sticky=N+S+E+W
            )
        self.yScrollMySQLOutputWindows_IO.configure(
            command=self.textMySQLOutputWindows_IO.yview
            )            
            
        '''
        self.textMySQLOutputWindows_IO.insert(
            END,
            '>$ '
            )
        '''

    def hideAllGridsWindows_IO(self):
        '''
        Purpose:
            hide all frames in the external Windows IO window
        '''
        
# if display is locked, don't change anything
        if self.lockDisplay.get(): return
        
        self.frameHostInfoWindows_IO.grid_remove()
        self.frameCvsSvnAccessWindows_IO.grid_remove()
        self.frameCompileWindows_IO.grid_remove()
        self.frameSetupWindows_IO.grid_remove()
        self.frameRunWindows_IO.grid_remove()
        self.frameStatusWindows_IO.grid_remove()
        self.framePostProcessWindows_IO.grid_remove()
        self.frameMySQLWindows_IO.grid_remove()
        
#  ----- end of EXTERNAL I/O WINDOWS TAB METHODS ----- 

# ================================================================ #

#  ----- CALLBACK HANDLERS ----- 
#
#  ----- COMMON HANDLERS ----- 
#  ----- Header Handlers -----       
# Handlers for displayHeader method

# dummy def
    def ZZ___COMMON_CALLBACK_HANDLERS():
        pass
        
        return
        
        
    def handlerButtonClear(self):
        '''
        Purpose:
            clear the entry box
        '''
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'handlerButtonClear'
        
        self.handlerNotYetImplementedInPylotDB()
        
        return
        

    def handlerButtonHelp(self):
        '''
        Purpose:
            help button
        '''
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'handlerButtonHelp'
        
#        self.handlerNotYetImplementedInPylotDB()
        myURL = (
            "http://pmatwiki.sandia.gov/pmatwiki/how-to-use-pylotdb" +
            "#head-d8e8849b23047b9b6f9726edd31b8f50ee2dbab2"
            )
        stringOpenHelpPage = (
            'Opening PylotDB\'s "Help" page in web browser using\n' +
            '  - %s\n\n' + 
            'Check browser.'
            ) % (
            myURL
            )
        print('\n' + stringOpenHelpPage)
        self.HostInfo_Output(
            1,
            stringOpenHelpPage
            )
        showinfo(
            'Info: check browser',
            stringOpenHelpPage,
            )
        try:
            webbrowser.open_new(myURL)
        except:
            stringErrorOpeningHelpPage = (
                'Unable to access Help page.'
                )
            print('\n' + stringErrorOpeningHelpPage)
            self.HostInfo_Output(
                0,
                stringErrorOpeningHelpPage
                )
            showerror(
                'Error: unable to access',
                stringErrorOpeningHelpPage,
                )            
        
        return
        
            
    def handlerButtonQuit(self):
        '''
        Purpose:
            quit button
        '''
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'handlerButtonQuit'
            
        ans=askyesno(
            'Quit',
            '           --WARNING --\n\n' +
            'YOU ARE ABOUT TO QUIT PylotDB.\n\n' +
            'THIS WILL ALSO CLOSE ANY AND ALL PLOTS THAT\n' +
            'MAY BE OPEN!\n\n' +
            'SAVE ANY DESIRED PLOTS FIRST!\n\n' +
            'REALLY QUIT?'
            )
            
        if ans:
            sys.exit()
           
        return
            
            
    def handlerNotYetImplementedInPylotDB(self):
        '''
        Purpose:
            to pop-up a showinfo window saying that this functionality
        has not yet been implemented
        '''
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'handlerNotYetImplementedInPylotDB'
            
        stringNotImplemented = (
            'This function has not yet been implemented.'
            )
        print('\n' + stringNotImplemented)
        self.HostInfo_Output(
            0,
            stringNotImplemented
            )
        showinfo(
            'Info: not yet implemented',
            'This function has not yet been implemented.',
            )
            
        return
        
            
    def handlerButtonEmailPylotDBProblems(self):
        '''
        Purpose:
            gives user option to send email any time there is a problem
        with PylotDB
        '''
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'handlerButtonEmailoPylotDBProblems'

# destroy any old toplevel frames
        try:
            self.windowEmailPylotDBProblems.destroy()
            print '\nPrevious toplevel widget removed from screen.'
        except: 
            print '\nNo previous toplevel widget to remove from screen.'
        self.windowEmailPylotDBProblems = Toplevel()
        self.windowEmailPylotDBProblems.transient(self.winfo_toplevel())
        self.windowEmailPylotDBProblems.title(
            "PylotDB - send email to pylotdb-help.sandia.gov"
            )
        xWindowLocation = \
            self.windowEmailPylotDBProblems_xWindowLocation
        yWindowLocation = \
            self.windowEmailPylotDBProblems_yWindowLocation
        self.windowEmailPylotDBProblems.geometry(
            '+%d+%d' % (xWindowLocation, yWindowLocation)
            )
# set the frame to be on top
        self.windowEmailPylotDBProblems.focus_set()
        
# print that user is sending email
        stringSendEmail = (
            'Sending email to pylotdb-help.sandia.gov'
            )
        print('\n' + stringSendEmail)
        self.HostInfo_Output(
            0,
            stringSendEmail
            )
        
# instantiate SendEmail in file email_dialog.py
        email = SendEmail(self.windowEmailPylotDBProblems)
        
#   ... and create the widgets to send email to pylotdb-help
        email.createEmailWidgets()
        
        return

            
    def handlerButtonPylotDBHomePage(self):
        '''
        Purpose:
            open PylotDB's home web site
        '''
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'handlerButtonPylotDBHomePage'

        myURL = 'http://oso.sandia.gov/pylotdb/'
        
        stringSiteNotAvailable = (
            'Sorry -- PylotDB\'s web site is currently under construction.'
            )
        print('\n' + stringSiteNotAvailable)
        self.HostInfo_Output(
            0,
            stringSiteNotAvailable
            )
        showinfo(
        'Info: site not available',
        stringSiteNotAvailable,
        )

# execute these lines when web site is available; comment above lines or delete       
        '''
        stringOpenHomePage = (
            'Opening PylotDB\'s home page in web browser using\n'
            '  - %s\n\n' +
            'Check browser'
            ) % (
            myURL
            )
        print('\n' + stringOpenHomePage)
        self.HostInfo_Output(
            1,
            stringOpenHomePage
            )
        showinfo(
            'Info: check browser',
            stringOpenHomePage,
            )
        try:
            webbrowser.open_new(myURL)
        except:
            stringErrorOpeningHomePage = (
                'Unable to open PylotDB home page.'
                )
            print('\n' + stringErrorOpeningHomePage)
            self.HostInfo_Output(
                0,
                stringErrorOpeningHomePage
                )
            showerror(
                'Error: cannot open site',
                stringErrorOpeningHomePage,
                )
        '''
        
        return
        
        
#  ----- end of Header Handlers ----- 

# ----- Clear Windows_IO Handlers -----
    def handlerClearWindows_IO(self):
        '''
        Purpose:
        clears the designated Windows_IO window, where the window is
        determined by the value of the control variable
            self.varClearWindows_IO
            
        INPUT:            
        Window  /  Control variable string:
        HOST INFO:
         self.textHostInfoCommandsWindows_IO / 'HostInfoCommandsWindows_IO'
         self.textHostInfoOutputWindows_IO   / 'HostInfoOutputWindows_IO'
            
        CVS/SVN ACCESS:
         self.textCvsSnvAccessCommandsWindows_IO / 'CvsSvnAccessCommandsWindows_IO'
         self.textCvsSvnAccessOutputWindows_IO   / 'CvsSvnAccessOutputWindows_IO'
        
        COMPILE:
         self.textCompileCommandsWindows_IO / 'CompileCommandsWindows_IO'
         self.textCompileOutputWindows_IO   / 'CompileOutputWindows_IO'
        
        SETUP:
         self.textSetupCommandsWindows_IO / 'SetupCommandsWindows_IO'
         self.textSetupOutputWindows_IO   / 'SetupOutputWindows_IO'
        
        RUN:
         self.textRunCommandsWindows_IO / 'RunCommandsWindows_IO'
         self.textRunOutputWindows_IO   / 'RunOutputWindows_IO'
        
        STATUS:
         self.textStatusCommandsWindows_IO / 'StatusCommandsWindows_IO'
         self.textStatusOutputWindows_IO   / 'StatusOutputWindows_IO'
        
        POST-PROCESS:
         self.textPostProcessCommandsWindows_IO / 'PostProcessCommandsWindows_IO'
         self.textPostProcessOutputWindows_IO   / 'PostProcessOutputWindows_IO'
        
        MySQL ACCESS:
         self.textMySQLCommandsWindows_IO / 'MySQLCommandsWindows_IO'
         self.textMySQLOutputWindows_IO   / 'MySQLOutputWindows_IO'
         
        '''
        
        if DEBUG_PRINT_METHOD:
            print('\n*** In ' + MODULE + '/' + 'handlerClearWindows_IO')
            
        print '\n  self.varClearWindows_IO =',self.varClearWindows_IO.get()
        
# for HOST INFO        
        if self.varClearWindows_IO.get() == 'HostInfoCommandsWindows_IO':
            self.textHostInfoCommandsWindows_IO.delete(
                1.0,
                END
                )
            '''
            self.textHostInfoCommandsWindows_IO.insert(
                END,
                '>$ '
                )
            '''
            self.radiobuttonClearHostInfoCommandsWindows_IO.deselect()
            return
        elif self.varClearWindows_IO.get() == 'HostInfoOutputWindows_IO':
            self.textHostInfoOutputWindows_IO.delete(
                1.0,
                END
                )
            '''
            self.textHostInfoOutputWindows_IO.insert(
                END,
                '>$ '
                )
            '''
            self.radiobuttonClearHostInfoOutputWindows_IO.deselect()
            return
                
# for CVS/SVN ACCESS
        elif self.varClearWindows_IO.get() == 'CvsSvnAccessCommandsWindows_IO':
            self.textCvsSvnAccessCommandsWindows_IO.delete(
                1.0,
                END
                )
            '''
            self.textCvsSvnAccessCommandsWindows_IO.insert(
                END,
                '>$ '
                )
            '''
            self.radiobuttonClearCvsSvnAccessCommandsWindows_IO.deselect()
            return
        elif self.varClearWindows_IO.get() == 'CvsSvnAccessOutputWindows_IO':
            self.textCvsSvnAccessOutputWindows_IO.delete(
                1.0,
                END
                )
            '''
            self.textCvsSvnAccessOutputWindows_IO.insert(
                END,
                '>$ '
                )
            '''
            self.radiobuttonClearCvsSvnOutputWindows_IO.deselect()
            return

# for COMPILE
        elif self.varClearWindows_IO.get() == 'CompileCommandsWindows_IO':
            self.textCompileCommandsWindows_IO.delete(
                1.0,
                END
                )
            '''
            self.textCompileCommandsWindows_IO.insert(
                END,
                '>$ '
                )
            '''
            self.radiobuttonClearCompileCommandsWindows_IO.deselect()
            return
        elif self.varClearWindows_IO.get() == 'CompileOutputWindows_IO':
            self.textCompileOutputWindows_IO.delete(
                1.0,
                END
                )
            '''
            self.textCompileOutputWindows_IO.insert(
                END,
                '>$ '
                )
            '''
            self.radiobuttonClearCompileOutputWindows_IO.deselect()
            return
            
# for SETUP
        elif self.varClearWindows_IO.get() == 'SetupCommandsWindows_IO':
            self.textSetupCommandsWindows_IO.delete(
                1.0,
                END
                )
            '''
            self.textSetupCommandsWindows_IO.insert(
                END,
                '>$ '
                )
            '''
            self.radiobuttonClearSetupCommandsWindows_IO.deselect()
            return
        elif self.varClearWindows_IO.get() == 'SetupOutputWindows_IO':
            self.textSetupOutputWindows_IO.delete(
                1.0,
                END
                )
            '''
            self.textSetupOutputWindows_IO.insert(
                END,
                '>$ '
                )
            '''
            self.radiobuttonClearSetupOutputWindows_IO.deselect()
            return
            
# for RUN
        elif self.varClearWindows_IO.get() == 'RunCommandsWindows_IO':
            self.textRunCommandsWindows_IO.delete(
                1.0,
                END
                )
            '''
            self.textRunCommandsWindows_IO.insert(
                END,
                '>$ '
                )
            '''
            self.radiobuttonClearRunCommandsWindows_IO.deselect()
            return
        elif self.varClearWindows_IO.get() == 'RunOutputWindows_IO':
            self.textRunOutputWindows_IO.delete(
                1.0,
                END
                )
            '''
            self.textRunOutputWindows_IO.insert(
                END,
                '>$ '
                )
            '''
            self.radiobuttonClearRunOutputWindows_IO.deselect()
            return

# for STATUS
        elif self.varClearWindows_IO.get() == 'StatusCommandsWindows_IO':
            self.textStatusCommandsWindows_IO.delete(
                1.0,
                END
                )
            '''
            self.textStatusCommandsWindows_IO.insert(
                END,
                '>$ '
                )
            '''
            self.radiobuttonClearStatusCommandsWindows_IO.deselect()
            return
        elif self.varClearWindows_IO.get() == 'StatusOutputWindows_IO':
            self.textStatusOutputWindows_IO.delete(
                1.0,
                END
                )
            '''
            self.textStatusOutputWindows_IO.insert(
                END,
                '>$ '
                )
            '''
            self.radiobuttonClearStatusOutputWindows_IO.deselect()
            return

# for POST-PROCESS
        elif self.varClearWindows_IO.get() == 'PostProcessCommandsWindows_IO':
            self.textPostProcessCommandsWindows_IO.delete(
                1.0,
                END
                )
            '''
            self.textPostProcessCommandsWindows_IO.insert(
                END,
                '>$ '
                )
            '''
            self.radiobuttonClearPostProcessCommandsWindows_IO.deselect()
            return
        elif self.varClearWindows_IO.get() == 'PostProcessOutputWindows_IO':
            self.textPostProcessOutputWindows_IO.delete(
                1.0,
                END
                )
            '''
            self.textPostProcessOutputWindows_IO.insert(
                END,
                '>$ '
                )
            '''
            self.radiobuttonClearPostProcessOutputWindows_IO.deselect()
            return

# for MySQL ACCESS
        elif self.varClearWindows_IO.get() == 'MySQLCommandsWindows_IO':
            self.textMySQLCommandsWindows_IO.delete(
                1.0,
                END
                )
            '''
            self.textMySQLCommandsWindows_IO.insert(
                END,
                '>$ '
                )
            '''
            self.radiobuttonClearMySQLCommandsWindows_IO.deselect()
            return
        elif self.varClearWindows_IO.get() == 'MySQLOutputWindows_IO':
            self.textMySQLOutputWindows_IO.delete(
                1.0,
                END
                )
            '''
            self.textMySQLOutputWindows_IO.insert(
                END,
                '>$ '
                )
            '''
            self.radiobuttonClearMySQLOutputWindows_IO.deselect()
            return
            
        else:
            print(
                '\nError: invalid control variable\n' +
                '  self.varClearWindows_IO = %s'
                ) % self.varClearWindows_IO

        return
        
                
# ----- end of Clear Windows_IO Handlers -----
#  ----- end of COMMON HANDLERS ----- 

# ============================================================== #    

#  ----- INFO TAB HANDLERS ----- 

# dummy def
    def ZZ___INFO_TAB_CALLBACK_HANDLERS():
        pass
        
        return
        
        
    def handlerPanic(self):
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'handlerPanic'
        text="This is handlerPanic \n"
        self.outputBox.insert(END,text)
        self.outputBox.see(END)

    def dirCommands(self):
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'dirCommands'
        if subprocess.mswindows:
            commands = ('dir c:', 'echo HELLO WORLD', 'echo The End')
        else:
            commands = ('ls', 'echo HELLO WORLD')
        self.printCommands(commands)
        
        return
        
            
    def printCommands(self,commands):
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'printCommands'
        ''' 
        Reference:
               http://www.oreillynet.com/onlamp/blog/2007/08/pymotw_subprocess_1.html
        '''
        for cmd in commands:
            self.outputBox.insert(
                END,
                '\n==============================\n\n'
                )
            self.outputBox.insert(
                END,
                'COMMAND: '+ cmd + '\n\n'
                )
            proc=subprocess.Popen(cmd,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                )
            result1=proc.communicate()[0]
            self.outputBox.insert(
                END,
                result1
                )
            self.outputBox.insert(
                END,
                '\n------end of command: %s--------\n' % cmd
                )
            self.outputBox.see(END)
            
            return
            
            
#  ----- end of INFO tab handlers ----- 
           
#  ----- CVS/SVN ACCESS TAB HANDLERS ----- 

# dummy def
    def ZZ___CVS_SVN_CHECK_IN_TAB_CALLBACK_HANDLERS():
        pass
        
        return
 

#  ----- end of CVS/SVN ACCESS handlers ----- 

#  ----- COMPILE TAB HANDLERS ----- 

# dummy def
    def ZZ___COMPILE_TAB_CALLBACK_HANDLERS():
        pass
        
        return
        

    def handlerCommandCompileTab(self):
        '''
        This handler is called for COMPILE main options, not
        for the subOptions, under COMMAND.
        For subOptions,
                handlerRadiobuttonsCompileLanguageCompileTab(self,compileLanguage)
        is called.
        
        Here, if Compile is selected, choose a sub-option;
        if Compile is NOT selected, gray out its suboptions.
                compileOption1CommandCompileTab: gnu
                compileOption2CommandCompileTab: intel
                compileOption3CommandCompileTab: mpi
                compileOption4CommandCompileTab: pgi
        '''
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'handlerCommandCompileTab'
        
# determine Language associated with Command, and with subCommand if Command='compile'            
        command=self.stringCommandCompileTab.get()
        print '\nCommand in handlerCommandCompileTab:\n',command
        
        if command == 'compile':
            subCommand=self.stringSubCompileOptionsCommandCompileTab.get()
            if subCommand == 'gnu':
                language = self.radiobuttonsCompileGnuLanguageCompileTab.getcurselection()
            elif subCommand == 'intel':
                language = self.radiobuttonsCompileIntelLanguageCompileTab.getcurselection()
            elif subCommand == 'mpi':
                language = self.radiobuttonsCompileMpiLanguageCompileTab.getcurselection()
            elif subCommand == 'pgi':
                language = self.radiobuttonsCompilePgiLanguageCompileTab.getcurselection()
            else:
                print "\n command = %s, subCommand = %s" % (command, subCommand)
                print "ERROR: fatal - problem with subCommand matching up with command"
                sys.exit()
        elif command == 'compileLocal':
            language = self.radiobuttonsCompileForLocalRunLanguageCompileTab.getcurselection() 
#            print '\ndirect command - language:', \
#                self.radiobuttonsCompileForLocalRunLanguageCompileTab.getcurselection()
            print '\nCommand = %s, language = %s' % (command,language) 
        else:
            if command != 'config' and command != 'make':
                print '\nCommand =',command
                print '  ERROR: fatal - command does not match any of the proper options.\n'
                sys.exit()
                
        print '\n*****'
        print 'Command =',command
        if command == 'compile':
            print 'subCommand =',subCommand
        if command != 'config' and command != 'make':
            print 'language =',language
        print '*****\n'
            
            
        if command == 'compile':
            self.subCompileOption1CommandCompileTab['state']=NORMAL
            self.subCompileOption2CommandCompileTab['state']=NORMAL
            self.subCompileOption3CommandCompileTab['state']=NORMAL
            self.subCompileOption4CommandCompileTab['state']=NORMAL
            print ">>> Command: %s\n  sub-Command: %s\n" %(command, subCommand)
        else:
            self.subCompileOption1CommandCompileTab['state']=DISABLED
            self.subCompileOption2CommandCompileTab['state']=DISABLED
            self.subCompileOption3CommandCompileTab['state']=DISABLED
            self.subCompileOption4CommandCompileTab['state']=DISABLED
            print " >>> Command: %s\n" % command


# display the next frame appropriate for Language, Congif, or Make
        if command=='compile':
            self.radiobuttonsCompileForLocalRunLanguageCompileTab.grid_remove()
            self.radiobuttonsCompileNothingLanguageCompileTab.grid_remove()
            self.handlerOtherCompileOptionsCompileTab_ActiveInactive(1)
# options
            self.checkbuttonsCCMOptionsCompileTab_localcc.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_localf77.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_localf90.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_gcc.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_g77.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_g90.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_icc.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_if77.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_if90.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_mpicc.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_mpif77.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_mpif90.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_pgcc.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_pf77.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_pf90.grid_remove()
# other options'
            self.checkbuttonsCCMOptionsCompileTab_config.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_make.grid_remove()

            if subCommand=='gnu':
                self.radiobuttonsCompileGnuLanguageCompileTab.grid()
                self.radiobuttonsCompileIntelLanguageCompileTab.grid_remove()
                self.radiobuttonsCompileMpiLanguageCompileTab.grid_remove()
                self.radiobuttonsCompilePgiLanguageCompileTab.grid_remove()
                if language=='gcc':
                    self.checkbuttonsCCMOptionsCompileTab_gcc.grid()
                elif language=='g77':
                    self.checkbuttonsCCMOptionsCompileTab_g77.grid()
                elif language=='g90':
                    self.checkbuttonsCCMOptionsCompileTab_g90.grid()
                else:
                    print '\nlanguage =',language
                    print "\nERROR: fatal - should be a gnu language\n"
                    sys.exit()
            elif subCommand=='intel':
                self.radiobuttonsCompileGnuLanguageCompileTab.grid_remove()
                self.radiobuttonsCompileIntelLanguageCompileTab.grid()
                self.radiobuttonsCompileMpiLanguageCompileTab.grid_remove()
                self.radiobuttonsCompilePgiLanguageCompileTab.grid_remove()
                if language=='icc':
                    self.checkbuttonsCCMOptionsCompileTab_icc.grid()
                elif language=='if77':
                    self.checkbuttonsCCMOptionsCompileTab_if77.grid()
                elif language=='if90':
                    self.checkbuttonsCCMOptionsCompileTab_if90.grid()
                else:
                    print '\nlanguage =',language
                    print "\nERROR: fatal - should be an intel language\n"
                    sys.exit()
            elif subCommand=='mpi':
                self.radiobuttonsCompileGnuLanguageCompileTab.grid_remove()
                self.radiobuttonsCompileIntelLanguageCompileTab.grid_remove()
                self.radiobuttonsCompileMpiLanguageCompileTab.grid()
                self.radiobuttonsCompilePgiLanguageCompileTab.grid_remove()
                if language=='mpicc':
                    self.checkbuttonsCCMOptionsCompileTab_mpicc.grid()
                elif language=='mpi77':
                    self.checkbuttonsCCMOptionsCompileTab_mpif77.grid()
                elif language=='mpi90':
                    self.checkbuttonsCCMOptionsCompileTab_mpif90.grid()             
                else:
                    print '\nlanguage =',language
                    print "\nERROR: fatal - should be a mpi language\n"
                    sys.exit()
            elif subCommand=='pgi':
                self.radiobuttonsCompileGnuLanguageCompileTab.grid_remove()
                self.radiobuttonsCompileIntelLanguageCompileTab.grid_remove()
                self.radiobuttonsCompileMpiLanguageCompileTab.grid_remove()
                self.radiobuttonsCompilePgiLanguageCompileTab.grid()
                if language=='pgcc':
                    self.checkbuttonsCCMOptionsCompileTab_pgcc.grid()
                elif language=='pf77':
                    self.checkbuttonsCCMOptionsCompileTab_pf77.grid()
                elif language=='pf90':
                    self.checkbuttonsCCMOptionsCompileTab_pf90.grid()
                else:
                    print '\nlanguage =',language
                    print "\nERROR: fatal - should be a pgi language\n"
                    sys.exit()
        elif command=='compileLocal':
# grid ForLocalRunLanguage
            self.radiobuttonsCompileForLocalRunLanguageCompileTab.grid()
# remove all others used in COMMAND/LANGUAGE
            self.radiobuttonsCompileGnuLanguageCompileTab.grid_remove()
            self.radiobuttonsCompileIntelLanguageCompileTab.grid_remove()
            self.radiobuttonsCompileMpiLanguageCompileTab.grid_remove()
            self.radiobuttonsCompilePgiLanguageCompileTab.grid_remove()
            self.radiobuttonsCompileNothingLanguageCompileTab.grid_remove()
            self.handlerOtherCompileOptionsCompileTab_ActiveInactive(1)
# remove all OPTIONS grids
            self.checkbuttonsCCMOptionsCompileTab_localcc.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_localf77.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_localf90.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_gcc.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_g77.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_g90.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_icc.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_if77.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_if90.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_mpicc.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_mpif77.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_mpif90.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_pgcc.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_pf77.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_pf90.grid_remove()
            if language=='cc':
                self.checkbuttonsCCMOptionsCompileTab_localcc.grid()
            elif language=='f77':
                self.checkbuttonsCCMOptionsCompileTab_localf77.grid()
            elif language=='f90':
                self.checkbuttonsCCMOptionsCompileTab_localf90.grid()
            else:
                print '\nlanguage =',language
                print "\nERROR: fatal - problem with local languages (cc, f77, f90, etc.\n"
                sys.exit()
        elif command=='config'or command=='make':
# language
            self.radiobuttonsCompileForLocalRunLanguageCompileTab.grid_remove()
            self.radiobuttonsCompileGnuLanguageCompileTab.grid_remove()
            self.radiobuttonsCompileIntelLanguageCompileTab.grid_remove()
            self.radiobuttonsCompileMpiLanguageCompileTab.grid_remove()
            self.radiobuttonsCompilePgiLanguageCompileTab.grid_remove()
            self.radiobuttonsCompileNothingLanguageCompileTab.grid()
# options
            self.checkbuttonsCCMOptionsCompileTab_localcc.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_localf77.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_localf90.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_gcc.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_g77.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_g90.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_icc.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_if77.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_if90.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_mpicc.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_mpif77.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_mpif90.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_pgcc.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_pf77.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_pf90.grid_remove()
# other options
            self.handlerOtherCompileOptionsCompileTab_ActiveInactive(0)

            if command=='config':
                self.checkbuttonsCCMOptionsCompileTab_config.grid()
                self.checkbuttonsCCMOptionsCompileTab_make.grid_remove()
            elif command=='make':
                self.checkbuttonsCCMOptionsCompileTab_config.grid_remove()
                self.checkbuttonsCCMOptionsCompileTab_make.grid()
        else:
            print "ERROR: fatal - no command option!"
            sys.exit()

    def handlerOtherCompileOptionsCompileTab_ActiveInactive(self,state):
        if state:
            self.labelOtherCompileOptionsCompileTab.grid()
            self.entryOtherCompileOptionsCompileTab.grid()
            self.buttonClearOtherCompileOptionsCompileTab.grid()
            self.labelOtherCompileOptionsCompileTab_Inactive.grid_remove()
            self.entryOtherCompileOptionsCompileTab_Inactive.grid_remove()
            self.buttonClearOtherCompileOptionsCompileTab_Inactive.grid_remove()        
        else:
            self.labelOtherCompileOptionsCompileTab_Inactive.grid()
            self.entryOtherCompileOptionsCompileTab_Inactive.grid()
            self.buttonClearOtherCompileOptionsCompileTab_Inactive.grid() 
            self.labelOtherCompileOptionsCompileTab.grid_remove()
            self.entryOtherCompileOptionsCompileTab.grid_remove()
            self.buttonClearOtherCompileOptionsCompileTab.grid_remove()   

        return
        

    def handlerEntryOtherCompileOptionsCompileTab(self):
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'handlerEntryOtherCompileOptionsCompileTab'
        print "\n>>> Clear Other Compile options\n"
        print "   Before clearing, string is", \
            self.entryOtherCompileOptionsDataCompileTab.get()
            
        self.entryOtherCompileOptionsDataCompileTab.set('')
        
        print "   After clearing, string is", \
            self.entryOtherCompileOptionsDataCompileTab.get()
            
        return
        

    def handlerRadiobuttonsCompileLanguageCompileTab(self,compileLanguage):
        ''' 
        This is called for 'Compile for local run' and 'Compile' suboptions
        and languages under LANGUAGE, not
        for the main options under COMMAND
        For main options,
            handlerCommandCompileTab(self)
        is called.
        '''
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'handlerRadiobuttonsCompileLanguageCompileTab'
        
        language = compileLanguage
        self.language = language
        
        print '\nIn handlerRadiobuttonsCompileLanguageCompileTab:'
        print '   Compile language :',language
        
# make sure command is 'compile'
        command=self.stringCommandCompileTab.get()
        print '   Command :',command

        if command == 'compile' or command == 'compileLocal':
# at first, hide all OPTIONS grids
#   for local
            self.checkbuttonsCCMOptionsCompileTab_localcc.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_localf77.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_localf90.grid_remove()
#   for gnu
            self.checkbuttonsCCMOptionsCompileTab_gcc.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_g77.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_g90.grid_remove()
#   for intel
            self.checkbuttonsCCMOptionsCompileTab_icc.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_if77.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_if90.grid_remove()
#   for mpi
            self.checkbuttonsCCMOptionsCompileTab_mpicc.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_mpif77.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_mpif90.grid_remove()
#   for pgi
            self.checkbuttonsCCMOptionsCompileTab_pgcc.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_pf77.grid_remove()
            self.checkbuttonsCCMOptionsCompileTab_pf90.grid_remove()
#   for config
            self.checkbuttonsCCMOptionsCompileTab_config.grid_remove()
#   for make
            self.checkbuttonsCCMOptionsCompileTab_make.grid_remove()
        else:
            return
        
# get subCommand from COMMAND box        
        subCommand=self.stringSubCompileOptionsCommandCompileTab.get()
        
        print '   subCommand:',subCommand
        
# grid appropriate OPTIONS box   
        if command == 'compile':
            if subCommand == 'gnu':        
                if language=='gcc':
                    self.checkbuttonsCCMOptionsCompileTab_gcc.grid()
                elif language=='g77':
                    self.checkbuttonsCCMOptionsCompileTab_g77.grid()
                elif language=='g90':
                    self.checkbuttonsCCMOptionsCompileTab_g90.grid()
                else:
                    print '\nsubCommand = %s, language = %s' % (subCommand,language)
                    print '\nERROR: fatal - language not allowed for this subCommand\n'
                    sys.exit()
            elif subCommand == 'intel':
                if language=='icc':
                    self.checkbuttonsCCMOptionsCompileTab_icc.grid()
                elif language=='if77':
                    self.checkbuttonsCCMOptionsCompileTab_if77.grid()
                elif language=='if90':
                    self.checkbuttonsCCMOptionsCompileTab_if90.grid()
                else:
                    print '\nsubCommand = %s, language = %s' % (subCommand,language)
                    print '\nERROR: fatal - language not allowed for this subCommand\n'
                    sys.exit()
            elif subCommand == 'mpi':
                if language == 'mpicc':
                    self.checkbuttonsCCMOptionsCompileTab_mpicc.grid()
                elif language == 'mpif77':
                    self.checkbuttonsCCMOptionsCompileTab_mpif77.grid()
                elif language == 'mpif90':
                    self.checkbuttonsCCMOptionsCompileTab_mpif90.grid()
                else:
                    print '\nsubCommand = %s, language = %s' % (subCommand,language)
                    print '\nERROR: fatal - language not allowed for this subCommand\n'
                    sys.exit()            
            elif subCommand == 'pgi':
                if language == 'pgcc':
                    self.checkbuttonsCCMOptionsCompileTab_pgcc.grid()
                elif language == 'pf77':
                    self.checkbuttonsCCMOptionsCompileTab_pf77.grid()
                elif language == 'pf90':
                    self.checkbuttonsCCMOptionsCompileTab_pf90.grid()
                else:
                    print '\nsubCommand = %s, language = %s' % (subCommand,language)
                    print '\nERROR: fatal - language not allowed for this subCommand\n'
                    sys.exit()                   
            else:
                print '\nsubCommand =',subCommand
                print "\nERROR: fatal - subCommand does not match those allowed\n"
                sys.exit()
        elif command == 'compileLocal':
            if language == 'cc':
                self.checkbuttonsCCMOptionsCompileTab_localcc.grid()
            elif language == 'f77':
                self.checkbuttonsCCMOptionsCompileTab_localf77.grid()
            elif language == 'f90':
                self.checkbuttonsCCMOptionsCompileTab_localf90.grid()
            else:
                print '\nCommand = %s, language = %s' % (command,language)
                print "\nERROR: fatal = wrong language for command 'compileLocal'\n"
                sys.exit()
        else:
            print '\nCommand: ',command
            print 'Unknown command in handlerRadiobuttonsCompileLanguageCompileTab\n'
            sys.exit()
            
        return

        
    def handlerCheckbuttonsCCMOptionsCompileTab(self,compileOption,state):
#        self.compileOption=compileOption
        if DEBUG_PRINT_METHOD:
            print '\n** In ' + MODULE + '/' + 'handlerCheckbuttonsCCMOptionsCompileTab'
        
        command=self.stringCommandCompileTab.get()
        
        if command == 'compileLocal':
            language = self.radiobuttonsCompileForLocalRunLanguageCompileTab.getvalue()
            if language == 'cc':
                selection = self.checkbuttonsCCMOptionsCompileTab_localcc.getvalue()
            elif language == 'f77':
                selection = self.checkbuttonsCCMOptionsCompileTab_localf77.getvalue()
            elif language == 'f90':
                selection = self.checkbuttonsCCMOptionsCompileTab_localf90.getvalue()
            else:
                print '\n>>Command = %s, language = %s' % (command,language)
                print 'ERROR: fatal - language is not an allowed match.'
                sys.exit()           
        elif command == 'compile':
            subCommand=self.stringSubCompileOptionsCommandCompileTab.get()
            if subCommand == 'gnu':
                language = self.radiobuttonsCompileGnuLanguageCompileTab.getvalue()
                if language == 'gcc':
                    selection = self.checkbuttonsCCMOptionsCompileTab_gcc.getvalue()
                elif language == 'g77':
                    selection = self.checkbuttonsCCMOptionsCompileTab_g77.getvalue()
                elif language == 'g90':
                    selection = self.checkbuttonsCCMOptionsCompileTab_g90.getvalue()
                else:
                    print '\n>>> Command = %s, subCommand = %s, language = %s' % \
                        (command, subCommand, language)
                    print '\n>>> ERROR - fatal: command, subCommand, or language do not match.'
                    sys.exit()
            elif subCommand == 'intel':
                language = self.radiobuttonsCompileIntelLanguageCompileTab.getvalue()
                if language == 'icc':
                    selection = self.checkbuttonsCCMOptionsCompileTab_icc.getvalue()
                elif language == 'if77':
                    selection = self.checkbuttonsCCMOptionsCompileTab_if77.getvalue()
                elif language == 'if90':    
                    selection = self.checkbuttonsCCMOptionsCompileTab_if90.getvalue()
                else:
                    print '\n>>> Command = %s, subCommand = %s, language = %s' % \
                        (command, subCommand, language)
                    print '\n>>> ERROR - fatal: command, subCommand, or language do not match.'
                    sys.exit()               
            elif subCommand == 'mpi':
                language = self.radiobuttonsCompileMpiLanguageCompileTab.getvalue()
                if language == 'mpicc':
                    selection = self.checkbuttonsCCMOptionsCompileTab_mpicc.getvalue()
                elif language == 'mpif77':
                    selection = self.checkbuttonsCCMOptionsCompileTab_mpif77.getvalue()
                elif language == 'mpif90':
                    selection = self.checkbuttonsCCMOptionsCompileTab_mpif90.getvalue()
                else:
                    print '\n>>> Command = %s, subCommand = %s, language = %s' % \
                        (command, subCommand, language)
                    print '\n>>> ERROR - fatal: command, subCommand, or language do not match.'
                    sys.exit()
            elif subCommand == 'pgi':
                language = self.radiobuttonsCompilePgiLanguageCompileTab.getvalue()
                if language == 'pgcc':
                    selection = self.checkbuttonsCCMOptionsCompileTab_pgcc.getvalue()
                elif language == 'pf77':
                    selection = self.checkbuttonsCCMOptionsCompileTab_pf77.getvalue()
                elif language == 'pf90':
                    selection = self.checkbuttonsCCMOptionsCompileTab_pf90.getvalue()
                else:
                    print '\n>>> Command = %s, subCommand = %s, language = %s' % \
                        (command, subCommand, language)
                    print '\n>>> ERROR - fatal: command, subCommand, or language do not match.'
                    sys.exit()
        elif command == 'config':
            selection = self.checkbuttonsCCMOptionsCompileTab_config.getvalue()
        elif command == 'make':
            selection = self.checkbuttonsCCMOptionsCompileTab_make.getvalue()
        else:
            print '\n>>Command =',command
            print 'ERROR: fatal - command is not an allowed match.'
            sys.exit()

        print '\n>>>Command =',command
        if command == 'compileLocal' or command == 'compile':
            print '   language =',language
        print '   compileOption = %s' % compileOption             
        
        
        if state:
           action = 'added.'
        else:
           action = 'removed.'
        print '  Button', compileOption, 'was', action,'\n' \
                '    Selection:', selection, \
                '\n'
                
        return
        
   
    def handlerButtonAssembleCompileTab(self):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerButtonAssembleCompileTab')
            
        if DEBUG_YOUCLICKEDON:
            print('\nYou clicked on ASSEMBLE')
        
        return
        

    def handlerButtonCompileCompileTab(self):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerButtonCompileCompileTab')
            
        if DEBUG_YOUCLICKEDON:
            print('\nYou clicked on COMPILE')
        
        return
        

    def handlerButtonKillCompileTab(self):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerButtonKillCompileTab')
        
        if DEBUG_YOUCLICKEDON:
            print('\nYou clicked on KILL PROCESS')
        
        return
        
        
    def handlerComboCompileSourceFilenameFilesCompileTab(self,fileSourceName):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerComboCompileSourceFilenameFilesCompileTab')
            
        self.fileSourceName=fileSourceName
        
        return
        
        
    def handlerComboCompileExecutableFilenameFilesCompileTab(self,fileExecutable):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerComboCompileExecutableFilenameFilesCompileTab')
            
        self.fileExecutableFilesCompileTab=fileExecutable
# set the same in the Run Tab
        self.comboExecutableFilenameFilesRunTab.selectitem(
            fileExecutable
            )
        
        return
        
        
    def handlerComboCompileOutputFilenameFilesCompileTab(self,fileOutputName):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerComboCompileOutputFilenameFilesCompileTab')

        self.fileOutputName=fileOutputName
        
        return
        
        
#  ----- end of COMPILE tab handlers -----       

#  ----- RUN TAB HANDLERS ----- 

# dummy def
    def ZZ___RUN_TAB_CALLBACK_HANDLERS():
        pass
        
        return
        
        
    def handlerButtonHert(self):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerButtonHert')
            
        webbrowser.open_new(
            'https://computing.sandia.gov/hert/create_usage_estimate/'
            )
        
        return
        
        
    def handlerButtonWhatIsHert(self):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerButtonWhatIsHert')
            
        webbrowser.open_new(
            'https://computing.sandia.gov/hert/'
            )
        
        return
        
            
    def handlerQueueRunTab(self):
        '''
        This handler is called by method
            boxQueueRunTab(self,parent)
        for QUEUE options in the Run Tab:
        --------name--------------------   -----variable-----
            - None (just run executable)    queueNone
            - Batch (uses QSUB)             queueBatch
                - Standard                      queueBatchStandard
                - Express                       queueBatchExpress
                - Other                         queueBatchOther
            - Interactive (uses YOD)        queueInteractive
        
        Value of main options:
            self.stringQueueRunTab.get()
        
        Value of sub-options:
            self.stringSubBatchOptionsQueueRunTab.get()
            
        Main output variables:
            self.queueMain
            self.queueSub
        
        Also enables or disables Run Specs depending on queue.
        
        Also determines which ASSEMBLE and EXECUTE buttons to present,
        depending on queue selection
        '''
        
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerQueueRunTab')
        
        self.queueMain=self.stringQueueRunTab.get()
        
        if DEBUG_YOUCLICKEDON:
            print('\nQUEUE selected: %s' % self.queueMain)

# enable all Run Specs, then disable select ones below if needed   
        self.enableAllRunTimeSpecs()
        
        if self.queueMain == 'queueBatch':
# enable all sub-queues
            self.subBatchOption1QueueRunTab.configure(state=NORMAL)
            self.subBatchOption2QueueRunTab.configure(state=NORMAL)
            self.subBatchOption3QueueRunTab.configure(state=NORMAL)
# show QSUB Commands Run Spec, hide YOD Commands
            self.paramsYod.grid_remove()
            self.paramsQsub.grid()
            
# show appropriate ASSEMBLE/EXECUTE buttons
            self.frameAssembleExecuteForQueueNoneRunTab.grid_remove()
            self.frameAssembleExecuteForQueueBatchRunTab.grid()
            self.frameAssembleExecuteForQueueInteractiveRunTab.grid_remove()
            
# enable Qsub filename entry in Run Tab
            self.entryQsubFilenameRunTab.configure(state=NORMAL)
# enable QSUB FILE Browse button in Run Tab
            self.buttonBrowseForQsubFilenameRunTab.configure(state=NORMAL)

# get which sub-queue has been chosen and print it 
            self.queueSub=self.stringSubBatchOptionsQueueRunTab.get()
            print '\n  Batch queue:',self.queueSub
            
        elif self.queueMain == 'queueNone' or self.queueMain == 'queueInteractive':
# disable all sub-queues
            self.subBatchOption1QueueRunTab.configure(state=DISABLED)
            self.subBatchOption2QueueRunTab.configure(state=DISABLED)
            self.subBatchOption3QueueRunTab.configure(state=DISABLED)
            
# disable Qsub filename entry in Run Tab
            self.entryQsubFilenameRunTab.configure(state=DISABLED)
# disable QSUB FILE Browse button in Run Tab
            self.buttonBrowseForQsubFilenameRunTab.configure(state=DISABLED)
            
            if self.queueMain == 'queueNone':
# disable some Run Specs
                self.runtimeHrs.configure(entry_state='disabled')
                self.runtimeMins.configure(entry_state='disabled')
# show QSUB Commands Run Spec and then disable; hide YOD Commands
                self.paramsYod.grid_remove()
                self.paramsQsub.grid()
                self.paramsQsub.configure(entry_state='disabled')
# disable Project No.
                self.numProject.configure(entry_state='disabled')
# disable Taks No.
                self.numTask.configure(entry_state='disabled')
                
# show appropriate ASSEMBLE/EXECUTE buttons
                self.frameAssembleExecuteForQueueNoneRunTab.grid()
                self.frameAssembleExecuteForQueueBatchRunTab.grid_remove()
                self.frameAssembleExecuteForQueueInteractiveRunTab.grid_remove()
                
            elif self.queueMain == 'queueInteractive':
# disable some Run Specs
# show QSUB Commands Run Spec and then disable; hide YOD Commands
                self.paramsYod.grid()
                self.paramsQsub.grid_remove()
                self.paramsQsub.configure(entry_state='disabled')
                
# show appropriate ASSEMBLE/EXECUTE buttons
                self.frameAssembleExecuteForQueueNoneRunTab.grid_remove()
                self.frameAssembleExecuteForQueueBatchRunTab.grid_remove()
                self.frameAssembleExecuteForQueueInteractiveRunTab.grid()
        
        else:
            print '\n** ERROR: fatal'
            print '     No match found for main queueu'
            print '      Main queue selected:', queueMain
            print 
            sys.exit()
        
        return
        
        
    def handlerNumNodes(self):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerNumNodes')
            
        try:
            nodes=eval(self.numNodes.get())
        except SyntaxError:
            print '\nNumber of nodes: undefined'
            return
        except:
            stringNodesUndefined = (
                'Number of nodes is undefined.\n\n' +
                'Value must be a positive integer.\n\n' +
                'Please re-enter...'
                )
            print('\n' + stringNodesUndefined)
            self.HostInfo_Output(
                0,
                stringNodesUndefined
                )
            showerror(
                'ERROR in number of nodes...',
                stringNodesUndefined,
                )
        else: 
            print '\nNumber of nodes:', nodes
            self.calculateNumProcs()
            self.calculateNumCores()
        
        return
        
        
    def handlerNumProcsPerNode(self):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerNumProcsPerNode')
            
        try:
            procs=eval(self.numProcsPerNode.get())
        except SyntaxError:
            print '\nNumber of procs: undefined'
            return
        except:
            stringProcsUndefined = (
                'Number of processors is undefined.\n' +
                'Value must be a positive integer.\n\n' +
                'Please re-enter...'
                )
            print('\n' + stringProcsUndefined)
            showerror(
                'ERROR in number of processors...',
                stringProcsUndefined,
                )
        else:
            print '\nNumber of processers per node:', procs
            self.calculateNumProcs()
            self.calculateNumCores()
        
        return
        
        
    def handlerNumCoresPerProc(self):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerNumCoresPerProc')
            
        try:
            cores=eval(self.numCoresPerProc.get())
        except SyntaxError:
            print '\nNumber of cores: undefined'
            return
        except:
            stringCoresUndefined = (
                'Number of cores is undefined.\n\n' +
                'Value must be a positive integer.\n\n' +
                'Please re-enter...'
                )
            print('\n' + stringCoresUndefined)
            showerror(
                'ERROR in number of cores...',
                stringCoresUndefined,
                )
        else:
            print '\nNumber of cores per processer:', cores
            self.calculateNumProcs()
            self.calculateNumCores()
        
        return
        
        
    def handlerRunHH(self):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerRunHH')
            
        print('\nMax runtime - hrs: %s' % self.runtimeHrs.get())
        
        return
        
        
    def handlerRunMM(self):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerRunMM')
            
        print('\nMax runtime - minutes: %s' % self.runtimeMins.get())
        
        return
        
      
    def handlerNumProject(self):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerNumProject')
            
        print('\nProject #: %s' % self.numProject.get())
        
        return
        
        
    def handlerNumTask(self):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerNumTask')
            
        print('\nTask #: %s' % self.numTask.get())
        
        return
        
        
    def handlerParamsQsub(self):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerParamsQsub')
            
        print('\nAdditional QSUB commands: %s' % self.paramsQsub.get())
        
        return
        
        
    def handlerParamsYod(self):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerParamsYod')
            
        print('\nAdditional YOD commands: %s' % self.paramsYod.get())
        
        return
        
        
    def handlerBrowseExecutableFilenameFilesRunTab(self):
        '''
        Called by:
            boxFilesRunTab
        
        Calls:
            os.path.split(askopenfilename(**options))
                
        Important output variables:
            self.fileExecutableFilenameFilesRunTab
            
        Input variables:
            self.entryExecutableFilenameFilesRunTab
             
        Purpose:
            define the Executable Error output file in Run Tab
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerBrowseExecutableFilenameFilesRunTab')
        
# define dictionary of options for askopenfilename()
        options = {}
        options = {
            'defaultextension' : '.exe',
            'filetypes' : [('executable','.exe'),('All files','*')],
            'initialdir' : self.currentDirectory,
            'initialfile' : '',
            'parent' : self.runTab,
            'title' : 'Pick executable filename'
            }      

# get current filename in entry field
        currentFileName = self.entryExecutableFilenameFilesRunTab.get()
        print '     Current filename:',currentFileName
# get filename using askopenfilename
        dirname, filename = os.path.split(askopenfilename(**options))
#        dirname, filename = os.path.split(asksaveasfilename(**options))
# dwb - NOTE
#   os.path.split(askopenfilename()) gives forward slashes in the filename
#   os.getcwd() gives backward slashes in the filename
#       Hence, one cannot compare the results of these two methods to ensure the user stays in the same directory.
#       Too bad :(
        if filename == '' and currentFileName == '':
            stringNoFileChosen = (
                'You must enter a filename for the executable file'
                )
            print('\n' + stringNoFileChosen)
            self.HostInfo_Output(
                0,
                stringNoFileChosen
                )
            showinfo(
                'No .exe filename chosen...',
                stringNoFileChosen,
                )
        else:
            print '    dirname =',dirname
            print '    filename =',filename
            self.fileExecutableFilenameFilesRunTab = filename
        
# set entry field
#  ... first, clear the selection
            self.entryExecutableFilenameFilesRunTab.select_clear()
#  ... and next, clear the entry
            self.entryExecutableFilenameFilesRunTab.delete(0,END)
# insert QSUB filename into entry field
            self.entryExecutableFilenameFilesRunTab.insert(
                END,
                self.fileExecutableFilenameFilesRunTab
                )
        
        return
        

        
    def handlerBrowseRunTimeOutputFilesRunTab(self):
        '''
        Called by:
            boxFilesRunTab
        
        Calls:
            os.path.split(askopenfilename(**options))
        
        Important output variables:
            self.fileRunTimeOutputFilesRunTab
            
        Input variables:
            self.entryRunTimeOutputFilesRunTab
        
        Purpose:
            define the Run-time output file in Run Tab
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerBrowseRunTimeOutputFilesRunTab')

# define dictionary of options for askopenfilename()
        options = {}
        options = {
            'defaultextension' : '.out',
            'filetypes' : [('output','.out'),('All files','*')],
            'initialdir' : self.currentDirectory,
            'initialfile' : '',
            'parent' : self.runTab,
            'title' : 'Pick output filename'
            }      
        
# get filename
        dirname, filename = os.path.split(askopenfilename(**options))
#        dirname, filename = os.path.split(asksaveasfilename(**options))
# dwb - NOTE
#   os.path.split(askopenfilename()) gives forward slashes in the filename
#   os.getcwd() gives backward slashes in the filename
#       Hence, one cannot compare the results of these two methods to ensure the user stays in the same directory.
#       Too bad :(
        if filename == '':
            stringNoFileChosen = (
                'You must enter a filename for the executable file.'
                )
            print('\n' + stringNoFileChosen)
            self.HostInfo_Output(
                0,
                stringNoFileChosen
                )
            showinfo(
                'No .exe filename chosen...',
                stringNoFileChosen,
                )
        else:
            print '    dirname =',dirname
            print '    filename =',filename
            self.fileRunTimeOutputFilesRunTab = filename
        
# set entry field
#  ... first, clear the selection
            self.entryRunTimeOutputFilesRunTab.select_clear()
#  ... and next, clear the entry
            self.entryRunTimeOutputFilesRunTab.delete(0,END)
# insert QSUB filename into entry field
            self.entryRunTimeOutputFilesRunTab.insert(
                END,
                self.fileRunTimeOutputFilesRunTab
                )
        
        return
        
               
    def handlerBrowseRunTimeErrorOutputFilesRunTab(self):
        '''
        Called by:
            boxFilesRunTab
        
        Calls:
            os.path.split(askopenfilename(**options))
              
        Important output variables:
            self.fileRunTimeErrorOutputFilesRunTab
            
        Input variables:
            self.entryRunTimeErrorOutputFilesRunTab
        
        
        Purpose:
            define the Run-time Error output file in Run Tab
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerBrowseRunTimeErrorOutputFilesRunTab')
        
# define dictionary of options for askopenfilename()
        options = {}
        options = {
            'defaultextension' : '.err',
            'filetypes' : [('error','.err'),('All files','*')],
            'initialdir' : self.currentDirectory,
            'initialfile' : '',
            'parent' : self.runTab,
            'title' : 'Pick output error filename'
            }      
        
# get filename
        dirname, filename = os.path.split(askopenfilename(**options))
#        dirname, filename = os.path.split(asksaveasfilename(**options))
# dwb - NOTE
#   os.path.split(askopenfilename()) gives forward slashes in the filename
#   os.getcwd() gives backward slashes in the filename
#       Hence, one cannot compare the results of these two methods to ensure the user stays in the same directory.
#       Too bad :(
        if filename == '':
            stringNoFileChosen = (
                'You must enter a filename for the .err file.'
                )
            print('\n' + stringNoFileChosen)
            self.HostInfo_Output(
                0,
                stringNoFileChosen
                )
            showinfo(
                'No .err filename chosen...',
                stringNoFileChosen,
                )
        else:
            print '    dirname =',dirname
            print '    filename =',filename
            self.fileRunTimeErrorOutputFilesRunTab = filename
        
# set entry field
#  ... first, clear the selection
            self.entryRunTimeErrorOutputFilesRunTab.select_clear()
#  ... and next, clear the entry
            self.entryRunTimeErrorOutputFilesRunTab.delete(0,END)
# insert QSUB filename into entry field
            self.entryRunTimeErrorOutputFilesRunTab.insert(
                END,
                self.fileRunTimeErrorOutputFilesRunTab
                )
        
        return
        

        
    def handlerBrowseForQsubFilenameRunTab(self):
        '''
        Called by:
            boxFilesRunTab
            
        Calls:
            os.path.split(askopenfilename(**options))
            
        Important output variables:
            self.filenameQsubForBatchQueue
            
        Input variables:
            None
        
        Purpose:
            Browse for filename for QSUB file to submit in Batch queues.
            Sets QSUB entry field in Run Tab to selected filename.
            
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerBrowseForQsubFilenameRunTab')
        
# define dictionary of options for askopenfilename()
# ... first way
#        options['key'] = 'value'

# ... second way
        options = {}
        options = {
            'defaultextension' : '.qsub',
            'filetypes' : [('qsub','.qsub'),('All files','*')],
            'initialdir' : self.currentDirectory,
            'initialfile' : '',
            'parent' : self.runTab,
            'title' : 'Pick QSUB filename'
            }
        
        
# get filename
        dirname, filename = os.path.split(askopenfilename(**options))
#        dirname, filename = os.path.split(asksaveasfilename(**options))
# dwb - NOTE
#   os.path.split(askopenfilename()) gives forward slashes in the filename
#   os.getcwd() gives backward slashes in the filename
#       Hence, one cannot compare the results of these two methods to ensure the user stays in the same directory.
#       Too bad :(
        if filename == '':
            stringNoFileChosen = (
                'You must enter a filename for the QSUB file.'
                )
            print('\n' + stringNoFileChosen)
            self.HostInfo_Output(
                0,
                stringNoFileChosen
                )
            showinfo(
                'No QSUB filename chosen...',
                stringNoFileChosen,
                )
        else:
            print '    dirname =',dirname
            print '    filename =',filename
            self.filenameQsubForBatchQueueRunTab = filename
        
# set entry field
#  ... first, clear the selection
            self.entryQsubFilenameRunTab.select_clear()
#  ... and next, clear the entry
            self.entryQsubFilenameRunTab.delete(0,END)
# insert QSUB filename into entry field
            self.entryQsubFilenameRunTab.insert(
                END,
                self.filenameQsubForBatchQueueRunTab
                )
        
        return
        
                
    def handlerPropagateBaseNameFromExecutableRunTab(self):
        '''
        Called by:
            boxFilesRunTab
            
        Calls:
            
            
        Important output variables:
            
            
        Input variables:
            self.entryExecutableFilenameFilesRunTab
            self.entryRunTimeOutputFilesRunTab
            self.entryRunTimeErrorOutputFilesRunTab
            self.entryQsubFilenameRunTab
            
        
        Purpose:
            Takes the executable base filename in Run Tab and propagates
            this basename to all other file entries
            
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerPropagateBaseNameFromExecutableRunTab')
        
        ans=askokcancel(
            'Propagate filenames',
            'Do you really want to propagate executable base\n' + 
            'filename to other filename entries? \n' +
            'WARNING: Current entries, if any, will be replaced!'
            )
            
        if ans:        
# get base filename from executable file
            if self.entryExecutableFilenameFilesRunTab.get() == '':
                stringNoFile = (
                    'There is no executable filename from which to\n' +
                    'extract a base filename. Operation canceled.'
                    )
                print('\n' + stringNoFile)
                self.HostInfo(
                    0,
                    stringNoFile
                    )
                showinfo(
                    'No executable filename',
                    stringNoFile,
                    )
                return
            else:
# extract base filename
                filenameBase, filenameExt = os.path.splitext(
                    self.entryExecutableFilenameFilesRunTab.get()
                    )
# Output
            self.entryRunTimeOutputFilesRunTab.delete(0,END)
            self.entryRunTimeOutputFilesRunTab.select_clear()
            self.entryRunTimeOutputFilesRunTab.insert(0,filenameBase + '.out')
# Error
            self.entryRunTimeErrorOutputFilesRunTab.delete(0,END)
            self.entryRunTimeErrorOutputFilesRunTab.select_clear()
            self.entryRunTimeErrorOutputFilesRunTab.insert(0,filenameBase + '.err')
# QSUB
            self.entryQsubFilenameRunTab.delete(0,END)
            self.entryQsubFilenameRunTab.select_clear()  
            self.entryQsubFilenameRunTab.insert(0,filenameBase + '.qsub')
    
    
    def handlerClearAllFilenamesRunTab(self):
        '''
        Called by:
            boxFilesRunTab
            
        Calls:
            askokcancel
            
            
        Important output variables:
            
            
        Input variables:
            self.entryExecutableFilenameFilesRunTab
            self.entryRunTimeOutputFilesRunTab
            self.entryRunTimeErrorOutputFilesRunTab
            self.entryQsubFilenameRunTab
            
        
        Purpose:
            Clears all filename entries in FILES box
            in the Run Tab
            
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerClearAllFilenamesRunTab')
        
        ans=askokcancel(
            'Clear filenames',
            'Do you really want to clear all filenames?'
            )
            
        if ans:
# Executable
            self.entryExecutableFilenameFilesRunTab.delete(0,END)
            self.entryExecutableFilenameFilesRunTab.select_clear()
# Output
            self.entryRunTimeOutputFilesRunTab.delete(0,END)
            self.entryRunTimeOutputFilesRunTab.select_clear()
# Error
            self.entryRunTimeErrorOutputFilesRunTab.delete(0,END)
            self.entryRunTimeErrorOutputFilesRunTab.select_clear()
# QSUB
            self.entryQsubFilenameRunTab.delete(0,END)
            self.entryQsubFilenameRunTab.select_clear()
        
        return       
    
        
    def handlerAssembleForQueueNoneRunTab(self):
        '''
        Called by:
            buttonsRunKillRunTab

        Calls:
            None

        Assembles run command for queue None in Run Tab.
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerAssembleForQueueNoneRunTab')
            
        if DEBUG_YOUCLICKEDON:
            print('\nASSEMBLE Run Command button pressed')
        
        return
        

    def handlerExecuteForQueueNoneRunTab(self):
        '''
        Called by:
            buttonsRunKillRunTab

        Calls:
            None

        Executes Run command for queue None in Run Tab.
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerExecuteForQueueNoneRunTab')
            
        print('\nExecute Run Command button pressed')
        
        return
        

    def handlerAssembleForQueueBatchRunTab(self):
        '''
        Called by:
            buttonsRunKillRunTab

        Calls:
            None

        Assembles QSUB file for queue Batch in Run Tab.
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerAssembleForQueueBatchRunTab')
            
        if DEBUG_YOUCLICKEDON:
            print('\nASSEMBLE QSUB File button pressed')
        
        return
        

    def handlerExecuteForQueueBatchRunTab(self):
        '''
        Called by:
            buttonsRunKillRunTab

        Calls:
            None

        Submits QSUB file for queue Batch in Run Tab.
        Also, saves the QSUB file in local directory for re-use.
        
        Notes:
        This needs re-factoring.
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerAssembleForQueueBatchRunTab')
            
        print('\nSUBMIT QSUB File button pressed')
        
# get the QSUB filename
        qsubFileName = self.entryQsubFilename.get()
        
# if no QSUB filename has been entered, show warning and exit
        if qsubFileName == '':
            print '  WARNING: no QSUB filename has been entered.'
            showwarning(
                'ERROR - no QSUB filename',
                'No QSUB filename has been designated. Return\n' +
                'to RUN tab and enter QSUB Filename.'
                )
            return

# if file exists, query user to see if ok to overwrite; if not, enter new QSUB filename        
        if os.path.exists(qsubFileName):
            print '    qsubFileName exists:',qsubFileName
            overWriteFile = askokcancel(
                'Warning: file overwrite',
                'You are about to overwrite an existing file.\n' +
                'Do you wish to continue?'
                )
                
            if overWriteFile:
                print '    Writing QSUB file.'
                qsubFile = open(qsubFileName,'wb')
        
                if qsubFile:
                    qsubFile.write('This is line 1\n')
                    qsubFile.write(' This is line 2\n')
                    
                    qsubFile.close()
      
        
                else:
                    stringCannotOpenFile = (
                        'Could not open file %s for writing.'
                        ) % qsubFile
                    print(stringCannotOpenFile)
                    self.HostInfo_Output(
                        0,
                        stringCannotOpenFile
                        )
                    showerror(
                        'ERROR - could not open',
                        stringCannotOpenFile,
                        )  
            else:
                stringNoOverwrite = (
                    'You chose not to overwrite file.\n' +
                    'Return to RUN Tab and enter a new QSUB filename.'
                    )
                print('\n' + stringNoOverwrite)
                self.HostInfo_Output(
                    0,
                    stringNoOverwrite
                    )
                showinfo(
                    'No overwrite',
                    stringNoOverwrite,
                    )

        else:
# create the new file and write to it        
            qsubFile = open(self.entryQsubFilename.get(),'wb')
        
            if qsubFile:
                qsubFile.write('This is line 1\n')
                qsubFile.write(' This is line 2\n')
                
                qsubFile.close()
        
            else:
                stringCannotOpenFile = (
                    'Could not open file\n' +
                    '  %s\n' +
                    'for writing.'
                    ) % qsubFile
                print(stringCannotOpenFile)
                showerror(
                    'ERROR - could not open',
                    stringCannotOpenFile,
                    ) 
        
        return 
        

    def handlerAssembleForQueueInteractiveRunTab(self):
        '''
        Called by:
            buttonsRunKillRunTab

        Calls:
            None

        Assembles YOD command for queue Interactive in Run Tab.
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerAssembleForQueueInteractiveRunTab')
            
        print('\nASSEMBLE YOD Command button pressed')
        
        return
        

    def handlerExecuteForQueueInteractiveRunTab(self):
        '''
        Called by:
            buttonsRunKillRunTab

        Calls:
            None

        Executes YOD command for queue Interactive in Run Tab.
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerAssembleForQueueInteractiveRunTab')
            
        print('\nExecute YOD Command button pressed')
        
        return
        
            
    def handlerRefreshQueueRunTab(self):
        '''
        Called by:
            buttonsRunKillRunTab
            
        Calls:
            None
            
        Important variables:
            
        Purpose:
            Refreshes list of jobs in queue; used to kill a job
            in queue
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerRefreshQueueFilesRunTab')
            
        print('\nREFRESH QUEUE button pressed')
        
        return
        
        
    def handlerRefreshRunningJobListRunTab(self):
        '''
        Called by:
            buttonsRunKillRunTab
            
        Calls:
            None
            
        Important variables:
        
        Purpose:
            Refeshes list of running jobs; used to kill a running job
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerRefreshRunningJobListRunTab')
            
        print('\nREFRESH LIST button pressed')
        
        return
        
        
    def handlerKillJobInQueueRunTab(self):
        '''
        Called by:
            buttonsRunKillRunTab
            
        Calls:
            None
            
        Important variables:
        
        Purpose:
            Kills the selected job in queue
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerRefreshRunningJobListRunTab')
            
        print('\nKILL JOB IN QUEUE button pressed')
        
        return
        
    
    def handlerKillRunningJobRunTab(self):
        '''
        Called by:
            buttonsRunKillRunTab
            
        Calls:
            None
            
        Important variables:
        
        Purpose:
            Kills the selected running job
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerRefreshRunningJobListRunTab')
            
        print('\nKILL RUNNING JOB button pressed')
        
        return
        
        
#  ----- end of RUN handlers ----- 

#  ----- STATUS TAB HANDLERS ----- 

# dummy def
    def ZZ___STATUS_TAB_CALLBACK_HANDLERS():
        pass
        
        return
        

#  ----- end of STATUS handlers ----- 

#  ----- POST-PROCESS TAB HANDLERS ----- 

# dummy def
    def ZZ___POST_PROCESS_TAB_CALLBACK_HANDLERS():
        pass
        
        return
        

#  ----- end of POST-PROCESS handlers ----- 


# ------ print to Host Info I/O Window ------

    def HostInfo_Commands(self,prepend,msg):
        '''
        Purpose:
            print to special I/O Windows if they exist; otherwise,
        print to standard output; can prepend prefix if desired.
        
        Inputs: 
            prepend
            msg
            Window: self.textHostInfoCommandsWindows_IO
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'HostInfo_Commands')
            
        if prepend != 0 and prepend != 1:
            self.wrongPrependValue(prepend,'Commands', MODULE)
            return
        
        if self.textHostInfoCommandsWindows_IO:
# windows IO exist, so display there instead of stdout
            if prepend:
# use prefix         
                try:
                    self.textHostInfoCommandsWindows_IO.insert(
                        END,
                        prefix + msg + '\n'
                        )
                except:
# separate since cannot combine list and tuple in one command
                    self.textHostInfoCommandsWindows_IO.insert(
                        END,
                        prefix + ' '
                        )
                    self.textHostInfoCommandsWindows_IO.insert(
                        END,
                        msg
                        )
                    self.textHostInfoCommandsWindows_IO.insert(
                        END,
                        '\n'
                        )
                        
            else:
# do not use prefix
                try:
                    self.textHostInfoCommandsWindows_IO.insert(
                        END,
                        msg + '\n'
                        )
                except:
                    self.textHostInfoCommandsWindows_IO.insert(
                        END,
                        msg
                        )
                    self.textHostInfoCommandsWindows_IO.insert(
                        END,
                        ' ' + '\n'
                        )
            self.textHostInfoCommandsWindows_IO.see(
                END
                )
        else:
            print msg
            
        self.textHostInfoCommandsWindows_IO.update_idletasks()
        
        return
        

    def HostInfo_Output(self,prepend,msg):
        '''
        Purpose:
        print to special I/O Windows if they exist; otherwise,
        print to standard output; can prepend prefix if desired.
        
        Inputs: 
        prepend
        msg
        Window: self.textHostInfoOutputWindows_IO
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'HostInfo_Output')
            
        if prepend != 0 and prepend != 1:
            self.wrongPrependValue_HostInfo(prepend,'Output', MODULE)
            return
            
        if self.textHostInfoOutputWindows_IO:
# windows IO exist, so display there instead of stdout
            if prepend:
# use prefix
                try:
                    self.textHostInfoOutputWindows_IO.insert(
                        END,
                        prefix + msg + '\n'
                        )
                except:
# separate since cannot combine list and tuple in one command
                    self.textHostInfoOutputWindows_IO.insert(
                        END,
                        prefix + ' '
                        )
                    self.textHostInfoOutputWindows_IO.insert(
                        END,
                        '\n'
                        )
            else:
# do not use prefix
                try:
                    self.textHostInfoOutputWindows_IO.insert(
                        END,
                        msg + '\n'
                        )
                except:
                    self.textHostInfoOutputWindows_IO.insert(
                        END,
                        msg
                        )
                    self.textHostInfoOutputWindows_IO.insert(
                        END,
                        ' ' + '\n'
                        )
            self.textHostInfoOutputWindows_IO.see(
                END
                )            
        else:
            if DEBUG_PRINT_MISC:
                print msg               
            
        self.textHostInfoOutputWindows_IO.update_idletasks()
        
        return
        
        
    def wrongPrependValue_HostInfo(self,value,window,module):
        '''
        Purpose:
        tell user that the wrong prepend value was used, and what
        module to check
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'wrongPrependValue_HostInfo')
        
        stringPrependValue = (
            'Error in determining whether to prepend a\n' +
            'print statement with a prompt. The value must be\n' +
            'either 0 or 1. The current value is\n' +
            '   prepend = ' + value + '\n\n' +
            'Check code in the following file:\n' +
            '   ' + module + ' for the ' + window + ' window.' +  '\n'
            )
        print('\n' + stringPrependValue)
        self.HostInfo_Output(
            0,
            stringPrependValue
            )
        showerror(
            'Error: incorrect prepend value',
            stringPrependValue,
            )
            
        return 
          

#  ----- WINDOWS-IO  HANDLERS ----- 

# dummy def
    def ZZ___WINDOWS_IO_CALLBACK_HANDLERS():
        pass
        
        return
        

# handler: button Host-Info
    def handlerButtonHostInfo_IO(self):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerButtonHostInfo_IO')
            
        if DEBUG_YOUCLICKEDON:
            print('\nYou clicked on HOST INFO')
            
# if display is locked, don't change anything
        if self.lockDisplay.get(): 
            if DEBUG_YOUCLICKEDON:
                print('     but I/O Display is locked.')
            return 
            
        self.hideAllGridsWindows_IO()
        self.frameHostInfoWindows_IO.grid()
        
        return
        

# handler: button CVS/SVN CheckIn
    def handlerButtonCvsSvnAccess_IO(self):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerButtonCvsSvnAccess_IO')
            
        if DEBUG_YOUCLICKEDON:
            print('\nYou clicked on CVS/SVN ACCESS')
            
# if display is locked, don't change anything
        if self.lockDisplay.get(): 
            if DEBUG_YOUCLICKEDON:
                print('     but I/O Display is locked.')
            return 
            
        self.hideAllGridsWindows_IO()
        self.frameCvsSvnAccessWindows_IO.grid()
        
        return
        

# handler: button Compile        
    def handlerButtonCompile_IO(self):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerButtonCompile_IO')
            
        if DEBUG_YOUCLICKEDON:
            print('\nYou clicked on COMPILE')
        
# if display is locked, don't change anything
        if self.lockDisplay.get(): 
            if DEBUG_YOUCLICKEDON:
                print('     but I/O Display is locked.')
            return 
            
        self.hideAllGridsWindows_IO()
        self.frameCompileWindows_IO.grid()
        
        return
        

# handler: button Setup        
    def handlerButtonSetup_IO(self):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerButtonSetup_IO')
            
        if DEBUG_YOUCLICKEDON:
            print('\nYou clicked on SETUP')
            
# if display is locked, don't change anything
        if self.lockDisplay.get(): 
            if DEBUG_YOUCLICKEDON:
                print('     but I/O Display is locked.')
            return 
            
        self.hideAllGridsWindows_IO()
        self.frameSetupWindows_IO.grid()
        
        return
        

# handler: button Run        
    def handlerButtonRun_IO(self):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerButtonRun_IO')
            
        if DEBUG_YOUCLICKEDON:
            print('\nYou clicked on RUN')
            
# if display is locked, don't change anything
        if self.lockDisplay.get(): 
            if DEBUG_YOUCLICKEDON:
                print('     but I/O Display is locked.')
            return 
            
        self.hideAllGridsWindows_IO()
        self.frameRunWindows_IO.grid()
        
        return
        

# handler: button Status        
    def handlerButtonStatus_IO(self):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerButtonStatus_IO')
            
        if DEBUG_YOUCLICKEDON:
            print('\nYou clicked on STATUS')
# if display is locked, don't change anything
        if self.lockDisplay.get(): 
            if DEBUG_YOUCLICKEDON:
                print('     but I/O Display is locked.')
            return 
            
        self.hideAllGridsWindows_IO()
        self.frameStatusWindows_IO.grid()
        
        return
        
        
# handler: button Post-Process    
    def handlerButtonPostProcess_IO(self):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerButtonPostProcess_IO')
            
        if DEBUG_YOUCLICKEDON:
            print('\nYou clicked on POST-PROCESS')
# if display is locked, don't change anything
        if self.lockDisplay.get(): 
            if DEBUG_YOUCLICKEDON:
                print('     but I/O Display is locked.')
            return 
            
        self.hideAllGridsWindows_IO()
        self.framePostProcessWindows_IO.grid()
        
        return
        
        
# handler: button MySQL    
    def handlerButtonMySQL_IO(self):
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerButtonMySQL_IO')
            
        if DEBUG_YOUCLICKEDON:
            print('\nYou clicked on MySQL ACCESS')
# if display is locked, don't change anything
        if self.lockDisplay.get(): 
            if DEBUG_YOUCLICKEDON:
                print('     but I/O Display is locked.')
            return 
            
        self.hideAllGridsWindows_IO()
        self.frameMySQLWindows_IO.grid()
        
        return
        
        
# handler: button LockDisplay
    def handlerLockDisplay(self):
        '''
        print whether lockDisplay checkbox is checked, indicating
        that external Windows_IO is locked on current tab,
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerLockDisplay')
      
        if DEBUG_YOUCLICKEDON:
            print('\nYou clicked on Lock Display')
            print('self.lockDisplay.get() = %s ' % self.lockDisplay.get())
            
        if self.lockDisplay.get():
            print('\nI/O Windows display is LOCKED')
        else:
            print('\nI/O Windows display is UNLOCKED')
        print
        
        return

        
#  ----- end of WINDOWS-IO  HANDLERS ----- 

#  ----- end of Handlers ----- 

# ----- END OF PylotDB -----

#==============================================================================
        
app=PylotDB()
app.master.title("PylotDB - Sandia Database Management and Analysis Tool ")
app.tk_focusFollowsMouse()
app.mainloop()

	
