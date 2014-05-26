#! /usr/local/bin/python # for *nix runs
# Filename: co-pylotdb.py
# Author: dwbarne
# Creation date: Feb 2009, with numerous modifications afterwards
# Purpose:
#   provides access to MySQL servers, databases, and tables
#   accessible to the user and the ability to send files and limited
#   data to the database/table selected

SANDIA_COPYRIGHT_NOTICE = (
    'COPYRIGHT NOTICE\n' +
    '\n' +
    'Copyright 2012 Sandia Corporation. Under the terms of Contract\n' +
    'DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government\n' +
    'retains certain rights in this software.'
    )

OPEN_SOURCE_SOFTWARE_LICENSE = (
    ' '*20 + 'OPEN SOURCE SOFTWARE LICENSE\n' +
    '\n' +
    'Redistribution and use in source and binary forms, with or without ' +
    'modification, are permitted provided that the following conditions ' +
    'are met:\n' +
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
    'THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS ' +
    '"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,INCLUDING, BUT NOT ' +
    'LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR ' +
    'A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT ' +
    'OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, ' +
    'SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT ' +
    'LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, ' +
    'DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY ' +
    'THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT ' +
    '(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE ' +
    'OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n' +
    '\n' +
    'Suggested reference wording for articles:\n' +
    '\n' +
    'D. W. Barnette, "PYLOTDB: A Python-MySQL Framework for Database Management ' +
    'and Data Analysis," Sandia National Laboratories, Albuquerque, New Mexico, 2012.'
    )
    
# Sandia National Laboratories software license with Open-Source software license attached
licenseSandia = (
    ' '*5 + 'COPYRIGHT NOTICE AND OPEN SOURCE LICENSE\n' +
    '\n' +
    'Copyright 2012 Sandia Corporation. Under the terms of Contract ' +
    'DE-AC04-94AL85000 with Sandia Corporation, the U.S. ' +
    'Government retains certain rights in this software.\n' +
    '\n' +
    'Redistribution and use in source and binary forms, with or without ' +
    'modification, are permitted provided that the following conditions ' +
    'are met:\n' +
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
    'THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS ' +
    '"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT ' +
    'LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR ' +
    'A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT ' +
    'OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, ' +
    'SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT ' +
    'LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, ' +
    'DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY ' +
    'THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT ' +
    '(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE ' +
    'OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n' +
    '\n' +
    'Suggested reference wording for articles:\n' +
    '\n' +
    'D. W. Barnette, "PYLOTDB: A Python-MySQL Framework for Database Management ' +
    'and Data Analysis," Sandia National Laboratories, Albuquerque, New Mexico, 2012.'
    )

# ===== Global Imports =====
from Tkinter import *           # Tkinter widgets
from tkMessageBox import *      # dialogs such as askokcancel, showinfo, showerror, etc.
import tkFileDialog             # askopenfilename, asksaveasfilename, askdirectory
import tkFont                   # fonts
import os                       # environment variables, current directory, username, etc.
import string                   # process standard Python strings
import errno                    # for error handling
import sys                      # for sys.exit()
import time                     # for time to execute commands
import glob                     # for batch processing all files with same extension
import cPickle                  # for saving Python objects to file
import platform                 # portable interface to platform information
import yaml                     # for reading "co-pylotdb.conf" file
import socket                   # for defining hostname on non-window non-posix machines

# for debugging
DEBUG = 0                       # = 1, general debugging
DEBUG_CO_PYLOT_CONF_FILE = 0    # = 1, print variables related to reading or generating the file "co-pylotdb.conf"
DEBUG_PRINTDISCONNECT = 0         # = 1, print variables related to disconnecting from server and re-setting various attributes
DEBUG_PRINTMETHODNAME = 0       # = 1, print name of current method
DEBUG_SAVEMYSQLCOMMAND = 0      # = 1, print variables related to saving the mysql command
DEBUG_SHOWMYSQLCOMMAND = 1      # = 1, print mysqlcommand to be sent to mysql server

# ... stats
DEBUG_THREAD_STATS = 0          # = 1, print variables from running thread to track usage
THREAD_STATS_COPYLOTDB = 1      # = 1 start thread for Co-PylotDB usage stats info to database

# Global variables
# ... Main-window placement relative to top left of screen
x_Windows = 10
y_Windows = 0

# height of entry fields for input file, output file, etc.
HULL_HEIGHT_0 = 45
# height of user comments field
HULL_HEIGHT_1 = 80

# import external modules
stringErrorExternalModules = ''
errflagExternalModules = 0

# ========== Pmw ==========
try:
    import Pmw                    # Python megawidgets
except:
    errflagExternalModules = 1
    stringErrorExternalModules += (
        'The Python Megawidget package "Pmw" must be installed ' + 
        'for Co-PylotDB to run.\n' +
        'Go to http://pmw.sourceforge.net\n\n'
        )
        
# ========== MySQLdb ==========
try:
    import MySQLdb                # MySQL database connectivity
except:
    errflagExternalModules = 1
    stringErrorExternalModules += (
        'The package "MySQLdb" must be installed for Co-PylotDB to run.\n' +
        'Go to http://sourceforge.net/projects/mysql-python\n\n'
        )

# if errors in import, print errors and quit
if errflagExternalModules:
    print stringErrorExternalModules
    showinfo(
        'Error: plot modules',
        '\n' + 
        stringErrorExternalModules + 
        '\n'
        )
    sys.exit()
    
# ------- end of external module imports -----

# Define globals

# ... define minimum screen resolution (resolution of 1280 x 960 or higher)
minScreenResolution_Width = 1280
minScreenResolution_Height = 960

# ========================== main class ======================== # 
class AccessMySQL(Frame):
    def __init__(self, 
        parent, 
        colorbg,
#        textMySQLOutputWindows_IO,
#        textMySQLCommandsWindows_IO,
#        shell
        ):
        
        Frame.__init__(self)

        self.frameParent = parent    

        print(
            '\n***** Co-PylotDB - For Remote Sends to a User-Selected Database  *****\n\n'
            )

# make instance resizable            
        self.rowconfigure(1, weight=1)       
        self.columnconfigure(0, weight=1)
            
        self.colorbg = colorbg
        
# beginning number of filename characters to match
        self.lengthBeginningFileNameLettersToMatch = 5
        
# define some constants which depend on operating system
        if os.name == 'nt':
            self.userName = os.environ['USERNAME']
            self.computerName = os.environ['COMPUTERNAME']
        elif os.name == 'posix':
            self.userName = os.environ['USER']
#            self.computerName = os.environ['HOSTNAME']
            self.computerName = socket.gethostname()
        else:
            try:
                self.userName = os.environ['USER']
            except:
                self.userName = 'UNK'
            try:
 #               self.computerName = os.environ['HOSTNAME']
                self.computerName = socket.gethostname()
            except:
                self.computerName = 'UNK'
                
        self.currentDirectory = os.getcwd().split('\\').pop()
        self.currentDirectoryFullPath = os.getcwd()        
# verify
        stringMisc = (
            '  Username: %s\n' +
            '  Computer name: %s\n' +
            '  Current directory: %s\n' 
            ) % (
            self.userName,
            self.computerName,
            self.currentDirectory
            )
        print(stringMisc)           
            
# server connection        
        self.myDbConnection = 0    

# fonts
# define title font 
        self.titleFont = tkFont.Font(
            family='arial',
            size='9',
            weight='bold',
            )
# define sub-title font
        self.subtitleFont = tkFont.Font(
            family='arial',
            size='7',
            weight='bold',
            )
# define title font big bold
        self.titleFontBigBold = tkFont.Font(
            family='arial',
            size='10',
            weight='bold'
            )
# define title font big
        self.titleFontBig = tkFont.Font(
            family='arial',
            size='10',
#            weight='bold',
            )
# define regular button font
        self.buttonFont = tkFont.Font(
            family='arial',
            size='9',
            )
# define small button font
        self.buttonFontSmall = tkFont.Font(
            family='arial',
            size='9',
            )
# define smallest button font
        self.buttonFontSmallest = tkFont.Font(
            family='arial',
            size='6',
            )
# define data font
        self.dataFont = tkFont.Font(
            family='lucida console',
            size='8',
            )
# define data font large
        self.dataFontLarge = tkFont.Font(
            family='lucida console',
            size='10',
            )
# define data font bold
        self.dataFontBold = tkFont.Font(
            family='lucida console',
            size='8',
            weight='bold',
            )
# define table font
        self.tableFont = tkFont.Font(
            family='terminal',
            size='9',
            )
# define smaller table font
        self.tableFont8 = tkFont.Font(
            family='terminal',
            size='8',
            )
# define medium text font for labels
        self.labelFontMedium = tkFont.Font(
            family='arial',
            size='9',
            )  
            
# days since my arbitrary start date
# ... timeStartDate = (yr, month, day, hr, min, sec, day of week, day of year, daylight savings flag)
# ...       start at Jan 1, 2011, Saturday (day 5), with no DST at this date
        import time
        timeStartDate = (2011,1,1,0,0,0,5,1,0)
        timeStartDateSinceEpoch_Seconds = time.mktime(timeStartDate)
        timeNow_Seconds = time.time()
        timeNowSinceStartDate_Days = \
            (timeNow_Seconds - timeStartDateSinceEpoch_Seconds)/3600./24. + 1
                    

# set date and time, but update before sending to table
        self.date = time.ctime(time.time())[4:10] + ' ' + time.ctime(time.time())[20:24]
        self.month = time.ctime(time.time())[4:7]
        self.dayofweek = time.ctime(time.time())[0:3]
        self.dayofmonth = time.ctime(time.time())[8:10]
        self.year = time.ctime(time.time())[20:24]
        self.time = time.ctime(time.time())[11:19]
        
# define month dictionary
        self.dictMonth = {
            'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 
            'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'
            }
# NOTE: for sorting purposes, use date format of yyyy/mm/dd when storing to database
        self.date = self.year + '/' + self.dictMonth[self.month] + '/' + self.dayofmonth

# default values for some variables
        self.fileInput = ''
        self.fileOutput = ''
        self.fileMake = ''
        self.fileSource = ''
        self.fileQsub = ''
        self.filepathInput = ''
        self.filepathOutput = ''
        self.filepathMake = ''
        self.filepathSource = ''
        self.filepathExecutable = ''
        self.filepathQsub = ''
        self.initialDir = '.'
        
        
        
# define servers from conf file it conf file exists;
#  otherwise, default to blank entries and user has to input values

# if posix (any *nix version), find which directory co-pylotdb.py is in, so that
#   new ".conf" file can be found in if it exists, or written to if it doesn't,
#   that directory   
        if os.name == 'posix':
            homeDir = '/home/' + self.userName
            file2find = 'co-pylotdb.py'
            foundCoPylotDB = 0
# do a directory tree walk, starting in home directory
            for root, dirs, files in os.walk(homeDir):
                    for file in files:
                        if file2find == file:
                            coPylotDBHomeDir = root + '/'
                            foundCoPylotDB = 1
                            break
                    if foundCoPylotDB:
                        break

# for windows, just use current directory; will be ok most of the time, unless
#   an alias is used for "pylotdb.py"
        else:
            coPylotDBHomeDir = './'

        self.co_pylotDotConf_Exists = 0
        self.servers = []
        self.usernameForRemoteServer = ''
        self.usernameForLocalServer = ''
        try:
            co_pylotDotConf = open(coPylotDBHomeDir + 'co-pylotdb.conf','r')
            self.co_pylotDotConf_Exists = 1
        except:
            stringNoConfFile = (
                'The file "co-pylotdb.conf" could not be found or cannot be opened.\n\n' +
                '"co-pylotdb.conf" allows the user to define parameters for the\n' +
                'database and table used for tracking usage of co-pylotdb.py.\n\n' +
                'If you wish to continue, click YES. Co-pylotdb will continue to run\n' +
                'without usage statistics being recorded.\n\n' +
                'If you do NOT wish to continue, click NO. In this case, co-pylotdb will\n' +
                'generate a generic template, save it as "co-pylotdb.conf_template", and exit.\n' +
                'Next, edit the file to define appropriate parameters listed so these will\n' +
                'be read by co-pylotdb next time it is run. Finally, rename or copy the file\n' +
                'to "co-pylotdb.conf" and re-run co-pylotdb.py.'
                )
            print('\n' + stringNoConfFile + '\n')
            co_pylotDotConf_Continue = askyesno(
                'QUESTION',
                stringNoConfFile
                )
            if not co_pylotDotConf_Continue:
                stringConfFileTemplate = (
                    '# file: co-pylotdb.conf\n' +
                    '# called by: co-pylotdb.py\n' +
                    '# author: Daniel W. Barnette, dwbarne@sandia.gov\n' +
                    '# date created: May 2011, with modifications since then\n' +
                    '\n' +
                    '#COMMENTS\n' +
                    '# 1. If not done already, rename this file from "co-pylotdb.conf_template"\n' +
                    '#    to "co-pylotdb.conf" after filling in data below.\n' +
                    '# 2. This file is used to define various parameters for "co-pylotdb.py".\n' +
                    '# 3. This file is read and used as object self.yamlDotLoad[<key>] where <key>\n' +
                    '#    is "co_pylotdb_stats_server", for example, to designate tracking server.\n' +
                    '# 4. "main_database_servers" below should contain all of the database servers\n' +
                    '#    you are likely to access; top value is the default value for the database\n' +
                    '#    server login widgets in co-pylotdb.\n' +
                    '# 5. Blank fields are not allowed; all fields must have at least one value.\n' +
                    '\n' +
                    '# Co-PylotDB MAIN DATABASE ACCESS\n' +
                    '# ... add as many servers as you have access to on separate lines; one should be \'localhost\'\n' +
                    '# ... username_for_remote_server: can leave blank for security purposes, but will\n' +
                    '#      need to enter each time Co-PylotDB is launched\n' +
                    '# ... for security reasons, there is no entry here for server password; user must enter\n' +
                    '#      manually in co-pylotdb.py\n' +
                    '# ... main_database_servers_port: default MySQL value is 3306\n' +
                    '\n' +
                    'main_database_servers:\n' +
                    '# examples: localhost, myServer.myCompany.myDomain\n' +
                    '   - <server1>\n' +
                    '   - <server2>\n' +
                    '   - <server3>\n' +
                    '\n' +
                    'username_for_remote_server:\n' +
                    '   - <myusername_remote>\n' +
                    '\n' +
                    'username_for_local_server:\n' +
                    '   - <myusername_local>\n' +
                    '\n' +
                    'main_database_servers_port:\n' +
                    '   - 3306'+
                    '\n\n' +
                    '# Co-PYLOT STATS DATABASE\n' +
                    '# ... co_pylotdb_stats_server: usually \'localhost\' if a local MySQL server is installed\n' +
                    '# ... co_pylotdb_stats_database: typical name is \'usage_stats\'\n' +
                    '# ... co_pylotdb_stats_table: typical name is \'stats_co_pylotdb\'\n' +
                    '# ... co_pylotdb_stats_server_username: if blank, usage will not be tracked\n' +
                    '# ... co_pylotdb_stats_server_password: if blank, usage will not be tracked\n' +
                    '# ... co_pylotdb_stats_server_port: default MySQL value is 3306\n' +
                    '\n' +
                    'co_pylotdb_stats_server:\n' +
                    '   - <server>\n' +
                    '\n' +
                    'co_pylotdb_stats_database:\n' +
                    '   - <database_name>\n' +
                    '\n' +
                    'co_pylotdb_stats_table:\n' +
                    '   - <table_name>\n' +
                    '\n' +
                    'co_pylotdb_stats_server_username:\n' +
                    '    - <server_username>\n' +
                    '\n' +
                    'co_pylotdb_stats_server_password:\n' +
                    '    - <server_password>\n' +
                    '\n' +
                    'co_pylotdb_stats_server_port:\n' +
                    '    - 3306'  
                    )
                    
                stringWriteTemplate = (
                    '\nWriting following to "co-pylotdb.conf_template" as template\n' +
                    'for file "co-pylotdb.conf":\n%s\n' 
                    )
                    
                print(
                    stringWriteTemplate % stringConfFileTemplate
                    )
                    
                try:
                    fileConf = open(coPylotDBHomeDir + './co-pylotdb.conf_template','w')
                    fileConf.write(stringConfFileTemplate)
                    fileConf.close()
                except:
                    stringCantOpenConfFile = (
                        '\nCan\t open "co-pylotdb.conf_template" file to write template.\n\n' +
                        'Likely reason is you don\'t have permission to write\n' +
                        'the file to this directory.\n\n' +
                        'Program exiting.'
                        )
                    print('\n' + stringCantOpenConfFile + '\n')
                    showerror(
                        'Error: cannot open file',
                        stringCantOpenConfFile
                        )
                    sys.exit()
                else:
                    stringConfFileWritten = (
                        'A configuration template has been written to file "co-pylotdb.conf_template".\n\n' +
                        'Edit this file, fill in data specific to your environment, then\n' +
                        'copy the file to "co-pylotdb.conf" which will be read by "co-pylotdb.py" the next\n' +
                        'the next time it\'s run.\n\n' +
                        'Program exiting'
                        )
                    print('\n' + stringConfFileWritten + '\n')
                    showinfo(
                        'Info: conf file written',
                        stringConfFileWritten
                        )
                    sys.exit() 

# return and just continue even though co-pylotdb.conf does not exist;
#  in this case, most fields will be left blank when co-pylotdb.py is run
            else:
                return
                
# no exceptions raised
        else:
            if DEBUG_CO_PYLOT_CONF_FILE:
                print(
                    '\nco-pylotdb.conf file found in following directory:\n%s'
                    % (
                    coPylotDBHomeDir + 'co-pylotdb.conf'
                    )
                     )
                
# pylotDotConf does exist
        if self.co_pylotDotConf_Exists:
            self.yamlDotLoad = yaml.load(co_pylotDotConf)
            if DEBUG_CO_PYLOT_CONF_FILE:
                print('\nself.yamlDotLoad:\n%s\n' % self.yamlDotLoad)
# define parameters for main database
            self.servers = self.yamlDotLoad['main_database_servers']
#            self.servers.sort()
            self.portForRemoteServer = self.yamlDotLoad['main_database_servers_port'][0]
            self.usernameForRemoteServer = self.yamlDotLoad['username_for_remote_server'][0]
            self.usernameForLocalServer = self.yamlDotLoad['username_for_local_server'][0]
            if DEBUG_CO_PYLOT_CONF_FILE:
                stringForRemoteServer = (
                    'For remote server:\n' +
                    '  username (remote) = %s\n' +
                    'For local server:\n' +
                    '  username (local) = %s\n' +
                    'For either:\n' +
                    '  port = %s\n' +
                    'For remote access:\n' +
                    '  servers = %s\n'
                    ) % (
                    self.usernameForRemoteServer,
                    self.usernameForLocalServer,
                    self.portForRemoteServer,
                    self.servers
                    )
                print('\n' + stringForRemoteServer)

# define parameters for pylotdb stats database
            self.co_pylotdb_stats_server = self.yamlDotLoad['co_pylotdb_stats_server'][0]
            self.co_pylotdb_stats_database = self.yamlDotLoad['co_pylotdb_stats_database'][0]
            self.co_pylotdb_stats_table = self.yamlDotLoad['co_pylotdb_stats_table'][0]
            self.co_pylotdb_stats_server_username = self.yamlDotLoad['co_pylotdb_stats_server_username'][0]
            self.co_pylotdb_stats_server_password = self.yamlDotLoad['co_pylotdb_stats_server_password'][0]
            self.co_pylotdb_stats_server_port = self.yamlDotLoad['co_pylotdb_stats_server_port'][0]

                    
# set 'valid' parameter; any blank parameter will mean pylotdb stats are not collected
            if(
            self.co_pylotdb_stats_server == ''
            or
            self.co_pylotdb_stats_database == ''
            or
            self.co_pylotdb_stats_table == ''
            or
            self.co_pylotdb_stats_server_username == ''
            or
            self.co_pylotdb_stats_server_password == ''
            or
            self.co_pylotdb_stats_server_port == ''
            ):
                self.co_pylotdb_stats_server_valid = False
            else:
                self.co_pylotdb_stats_server_valid = True

            if DEBUG_CO_PYLOT_CONF_FILE:
                stringForCoPylotDBStats = (
                    'For co_pylotdb stats:\n' +
                    '  username = %s\n' +
                    '  password = %s\n' +
                    '  port = %s\n' +
                    '  server = %s\n'
                    '  database = %s\n' +
                    '  table = %s\n' 
                    ) % (
                    self.co_pylotdb_stats_server_username,
                    self.co_pylotdb_stats_server_password,
                    self.co_pylotdb_stats_server_port,
                    self.co_pylotdb_stats_server,
                    self.co_pylotdb_stats_database,
                    self.co_pylotdb_stats_table
                    )
                print('\n' + stringForCoPylotDBStats)
        
# send usage to database
        userName = self.userName
        codeName = 'co-pylot'
        versionPython = platform.python_version()
#        operatingSystem = os.environ['OS'] # doesn't work on Linux
        operatingSystem = platform.system()
        day_number_since_01jan2011 = int(timeNowSinceStartDate_Days)
        dayOfWeek,month,day,time,year = time.ctime().split()
        hostName = self.computerName
        osName = os.name
# cannot capture following with pylot, even tho table structure would take it
        name_first = ''
        name_last = ''
        
# start thread to send Co-PylotDB stats to database
        if THREAD_STATS_COPYLOTDB:
            import thread # for starting threads
            thread.start_new_thread(
                self.threadSendUsage_Co_PylotDB,
# attributes as *args
                (
                userName,
                name_first,
                name_last,
                codeName,
                versionPython,
                operatingSystem,
                osName,
                day_number_since_01jan2011,
                dayOfWeek,
                month,
                day,
                year,
                time,
                hostName,
                self.co_pylotdb_stats_server_valid,
                self.co_pylotdb_stats_server_username,
                self.co_pylotdb_stats_server_password,
                self.co_pylotdb_stats_server,
                self.co_pylotdb_stats_server_port,
                self.co_pylotdb_stats_database,
                self.co_pylotdb_stats_table
                )                
                  )
        
# start creating widgets        
        self.createWidgets()
        
#===================================================================
        
    def createWidgets(self):
        '''
        defines widgets for accessing MySQL
        
        Output:
            username:   self.varUserMySQL
            password:   self.varPasswordMySQL
            server:     self.comboServerMySQL
            port:       self.varPortMySQL
            
            total databases:    self.varDbTotal
            total tables:       self.varDbTablesTotal
        '''
        

# FRAMES

#---------------- Title
# ... mainframe_10
        self.frameMySQL_10 = Frame(
            self.frameParent,
            bg=self.colorbg,
#            borderwidth=2,
#            relief=RIDGE,
            )
        self.frameMySQL_10.grid(
            row=0,
            column=0,
#            columnspan=99,
            padx=5,
            pady=0,
            sticky=N,
            )
        self.frameMySQL_10_00 = Frame(
            self.frameMySQL_10,
            bg=self.colorbg,
            )
        self.frameMySQL_10_00.grid(
            row=0,
            column=0,
            columnspan=99,
            padx=5,
            pady=5,
            sticky=N,
            )
        self.frameMySQL_10_10 = Frame(
            self.frameMySQL_10,
            bg=self.colorbg,
            )
        self.frameMySQL_10_10.grid(
            row=1,
            column=0,
            columnspan=99,
            padx=5,
            pady=5,
            sticky=N,
            )

# -- SCROLLABLE CANVAS --            
# set up scrollable canvas frame in self.frameParent for the remaining widgets
        frameForCanvas = Frame(
            self.frameParent,
            bg=self.colorbg,
            borderwidth=5,
            relief=RIDGE,
#            width=1200,
#            height=600,
            )
        frameForCanvas.grid(
            row=1,
            column=0,
#            columnspan=99,
            padx=5,
            pady=5,
            sticky=N+S,
            )

# scrollbars for this frame
        xscrollFrameForCanvas = Scrollbar(
            self.frameParent,
            orient=HORIZONTAL,
            )
        '''
        xscrollFrameForCanvas.grid(
            row=2,
            column=0,
            sticky=N+E+W,
            )
        '''
        yscrollFrameForCanvas = Scrollbar(
            self.frameParent,
            orient=VERTICAL,
            )
        yscrollFrameForCanvas.grid(
            row=1,
            column=1,
            sticky=E+N+S,   
            )   
        xscrollFrameForCanvas.config(
            command=self.handlerXScrollFrameForCanvas
            )
        yscrollFrameForCanvas.config(
            command=self.handlerYScrollFrameForCanvas
            )
# canvas inside frameForCanvas
        self.canvasMain = Canvas(
            frameForCanvas,
            bg=self.colorbg,
            highlightbackground=self.colorbg,
#            width=widthTable,
#            height=heightTable,
            width=1350, #1175,
            height=850,     # use 600 for presentations if it won't fit due to projector
            xscrollcommand=xscrollFrameForCanvas.set,
            yscrollcommand=yscrollFrameForCanvas.set,
            )
        self.canvasMain.grid(
            row=0,
            column=0,
            padx=2,
            pady=2,
#            sticky=N+S,
            )
# frame inside canvas
        self.frameInCanvas = Frame(
            self.canvasMain,
            bg=self.colorbg,
            padx=0,
            pady=0,
            )
        '''
        self.frameInCanvas.grid_rowconfigure(1,weight=1)
        self.canvasMain.create_window(
            0,
            0,
            anchor=NW,
            window=self.frameInCanvas,
            )
        self.frameInCanvas.update_idletasks()
        self.canvasMain.config(scrollregion=self.canvasMain.bbox('all'))
        '''
        
# -- END OF CANVAS --           

#---------------- File and info widgets
# ... mainframe_20
        self.frameMySQL_20 = Frame(
            self.frameInCanvas,
            bg=self.colorbg,
            borderwidth=2,
            relief=RIDGE
            )
        self.frameMySQL_20.grid(
            row=0,
            column=0,
            columnspan=99,
            padx=10,
            pady=0,
            )
# ... input file
        self.frameMySQL_20_00 = Frame(
            self.frameMySQL_20,
            bg=self.colorbg,
            )
        self.frameMySQL_20_00.grid(
            row=0,
            column=0,
            padx=10,
            pady=5,
            sticky=N,
            )
# ... output file
        self.frameMySQL_20_01 = Frame(
            self.frameMySQL_20,
            bg=self.colorbg,
            )
        self.frameMySQL_20_01.grid(
            row=0,
            column=1,
            padx=10,
            pady=5,
            sticky=N,
            )
# ...   sub-frame for processing options
        self.frameMySQL_20_02 = Frame(
            self.frameMySQL_20,
            bg=self.colorbg,
            )
        self.frameMySQL_20_02.grid(
            row=0,
            column=2,
            padx=0,
            pady=0,
            sticky=N,
            )
# ... make file
        self.frameMySQL_20_03 = Frame(
            self.frameMySQL_20,
            bg=self.colorbg,
            )
        self.frameMySQL_20_03.grid(
            row=0,
            column=3,
            padx=10,
            pady=5,
            sticky=N,
            )
# ... source file
        self.frameMySQL_20_04 = Frame(
            self.frameMySQL_20,
            bg=self.colorbg,
            )
        self.frameMySQL_20_04.grid(
            row=0,
            column=4,
            padx=5,
            pady=5,
            sticky=N,
            )
            
# ... executable file
        self.frameMySQL_20_10 = Frame(
            self.frameMySQL_20,
            bg=self.colorbg,
            )
        self.frameMySQL_20_10.grid(
            row=1,
            column=0,
            columnspan=1,
            padx=0,
            pady=10,
            sticky=N,
            )
# ... machine name
        self.frameMySQL_20_11 = Frame(
            self.frameMySQL_20,
            bg=self.colorbg,
            )
        self.frameMySQL_20_11.grid(
            row=1,
            column=1,
            columnspan=1,
            padx=0,
            pady=25,
            sticky=N,
            )
# ... tester name file
        self.frameMySQL_20_12 = Frame(
            self.frameMySQL_20,
            bg=self.colorbg,
            )
        self.frameMySQL_20_12.grid(
            row=1,
            column=2,
            columnspan=1,
            padx=0,
            pady=10,
            )
# ... qsub file
        self.frameMySQL_20_13 = Frame(
            self.frameMySQL_20,
            bg=self.colorbg,
            )
        self.frameMySQL_20_13.grid(
            row=1,
            column=3,
            columnspan=1,
            padx=0,
            pady=10,
            )
            
# ... compile and execute lines
        self.frameMySQL_20_20 = Frame(
            self.frameMySQL_20,
            bg=self.colorbg,
            )
        self.frameMySQL_20_20.grid(
            row=2,
            column=0,
            columnspan=99,
            padx=5,
            pady=5,
            sticky=N,
            )
# ... compile statement sub-frame
        self.frameMySQL_20_20_00 = Frame(
            self.frameMySQL_20_20,
            bg=self.colorbg,
            )
        self.frameMySQL_20_20_00.grid(
            row=0,
            column=0,
            padx=0,
            pady=0,
            )
# ... execute statement sub-frame
        self.frameMySQL_20_20_01 = Frame(
            self.frameMySQL_20_20,
            bg=self.colorbg,
            )
        self.frameMySQL_20_20_01.grid(
            row=0,
            column=1,
            padx=20,
            pady=0,
            )

# ... user comment
        '''
        self.frameMySQL_20_11 = Frame(
            self.frameMySQL_20,
            bg=self.colorbg,
            )
        self.frameMySQL_20_11.grid(
            row=1,
            column=1,
            columnspan=99,
            padx=0,
            pady=5,
            sticky=N,
            )
        '''
        self.frameMySQL_21 = Frame(
            self.frameInCanvas,
            bg=self.colorbg,
            borderwidth=2,
            relief=RIDGE,
            )
        self.frameMySQL_21.grid(
            row=1,
            column=0,
            columnspan=99,
            padx=5,
            pady=5,
            )
            

#---------------- Database access
        self.frameMySQL_3_MAIN = Frame(
            self.frameInCanvas,
            bg=self.colorbg,
#            borderwidth=2,
#            relief=RIDGE,
            )
        self.frameMySQL_3_MAIN.grid(
            row=2,
            column=0,
            columnspan=99,
            padx=5,
            pady=5,
            )
# ... frame LEFT: mysql access
        self.frameMySQL_3 = Frame(
            self.frameMySQL_3_MAIN,
            bg=self.colorbg,
            borderwidth=2,
            relief=RIDGE,
            )
        self.frameMySQL_3.grid(
            row=0,
            column=0,
            padx=5,
            pady=0,
            )
            
# ... frame RIGHT: send, save, cancel
        self.frameMySQL_4 = Frame(
            self.frameMySQL_3_MAIN,
            bg=self.colorbg,
#            borderwidth=2,
#            relief=RIDGE,
            )
        self.frameMySQL_4.grid(
            row=0,
            column=1,
#            columnspan=2,
            padx=50,
            pady=5,
#            sticky=E,
            )
        
# ... mainframe_30
        self.frameMySQL_30 = Frame(
            self.frameMySQL_3,
            bg=self.colorbg,
            )
        self.frameMySQL_30.grid(
            row=0,
            column=0,
            padx=10,
            pady=5,
            )

# ... subframe_30_00 Left
        self.frameMySQL_30_00 = Frame(
            self.frameMySQL_30,
            bg=self.colorbg,
            )
        self.frameMySQL_30_00.grid(
            row=0,
            column=0,
            padx=5,
            pady=2,
            )

# ... subframe_30_10 Left
        self.frameMySQL_30_10 = Frame(
            self.frameMySQL_30,
            bg=self.colorbg
            )
        self.frameMySQL_30_10.grid(
            row=1,
            column=0,
            padx=5,
            pady=2,
            )
          
# ... main_31
        self.frameMySQL_31 = Frame(
            self.frameMySQL_3,
            bg=self.colorbg,
            )
        self.frameMySQL_31.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            )
# ... subframe_31_00
        self.frameMySQL_31_00 = Frame(
            self.frameMySQL_31,
            bg=self.colorbg,
            )
        self.frameMySQL_31_00.grid(
            row=0,
            column=0,
            padx=0,
            pady=0,
            )
# ... subframe_31_10
        self.frameMySQL_31_10 = Frame(
            self.frameMySQL_31,
            bg=self.colorbg,
            )
        self.frameMySQL_31_10.grid(
            row=1,
            column=0,
            padx=0,
            pady=0,
            )        

# ... main_32
        self.frameMySQL_32 = Frame(
            self.frameMySQL_3,
            bg=self.colorbg,
            )
        self.frameMySQL_32.grid(
            row=0,
            column=2,
            padx=5,
            pady=5,
            )
# ... subframe_32_00
        self.frameMySQL_32_00 = Frame(
            self.frameMySQL_32,
            bg=self.colorbg,
            )
        self.frameMySQL_32_00.grid(
            row=0,
            column=0,
            padx=0,
            pady=0,
            )
# ... subframe_32_10
        self.frameMySQL_32_10 = Frame(
            self.frameMySQL_32,
            bg=self.colorbg,
            )
        self.frameMySQL_32_10.grid(
            row=1,
            column=0,
            padx=0,
            pady=0,
            ) 
        '''    
#---------------- Send to database
        self.frameMySQL_40 = Frame(
            self.frameInCanvas,
            bg=self.colorbg,
            )
        self.frameMySQL_40.grid(
#            row=3,
#            column=0,
            row=2,
            column=2,
#            columnspan=2,
            padx=10,
            pady=0,
            sticky=W,
            )
        '''

#---------------- Reset, cancel widgets
        self.frameMySQL_50 = Frame(
            self.frameInCanvas,
            bg=self.colorbg,
            )
        '''
        self.frameMySQL_50.grid(
            row=4,
            column=0,
            columnspan=99,
            padx=10,
            pady=0,
            ) 
        '''

# WIDGETS

# ... Title
        labelTitle = Label(
            self.frameMySQL_10_00,
            text=(
                ' --- Co-PylotDB Version 1.0 ---\n' + 
                'Send Test Files Info to a MySQL Database Table,\n' + 
                'Or Save MySQL Command to a File to be Read by PylotDB\n' +
                '(all user fields optional except OUTPUT file)' # and MACHINE on which executable was run)'
                ),
            bg=self.colorbg,
            font=self.titleFontBig,
            )
        labelTitle.grid(
            row=0,
            column=0,
            padx=5,
            pady=0,
            )
# ... user label
        self.labelUser = Label(
            self.frameMySQL_10_10,
            text='User',
            justify=RIGHT,
            bg=self.colorbg,
            )
        self.labelUser.grid(
            row=0,
            column=0,
            padx=5,
            pady=0,
            sticky=E,
            )
# ... user entry
        self.varEntryUser = StringVar()
        self.entryUser = Entry(
            self.frameMySQL_10_10,
            justify=LEFT,
            textvariable=self.varEntryUser,
            width=12,
            disabledforeground='black',
            disabledbackground='white',
            state='disable',
            )
        self.entryUser.grid(
            row=0,
            column=1,
            padx=0,
            pady=0,
            sticky=W,
            )
        self.varEntryUser.set(self.userName)
# ... directory label
        self.labelDirectory = Label(
            self.frameMySQL_10_10,
            text='Current\ndirectory',
            justify=RIGHT,
            bg=self.colorbg,
            )
        self.labelDirectory.grid(
            row=0,
            column=2,
            padx=5,
            pady=0,
            sticky=E,
            )
# ... directory entry
        self.varEntryDirectory = StringVar()
        self.entryDirectory = Entry(
            self.frameMySQL_10_10,
            justify=LEFT,
            textvariable=self.varEntryDirectory,
            width=25,
            disabledforeground='black',
            disabledbackground='white',
            state='disable',
            )
        self.entryDirectory.grid(
            row=0,
            column=3,
            padx=0,
            pady=0,
            sticky=E,
            )
        self.varEntryDirectory.set(self.currentDirectory)
# ... host
        self.labelHostName = Label(
            self.frameMySQL_10_10,
            text='Local\nhostname:',
            justify=RIGHT,
            bg=self.colorbg,
            )
        self.labelHostName.grid(
            row=0,
            column=4,
            padx=5,
            pady=0,
            sticky=E,
            )
        self.varEntryHostName = StringVar()
        self.entryHostName = Entry(
            self.frameMySQL_10_10,
            justify=LEFT,
            textvariable=self.varEntryHostName,
            width=20,
            disabledforeground='black',
            disabledbackground='white',
            state='disable',
            )
        self.entryHostName.grid(
            row=0,
            column=5,
            padx=0,
            pady=0,
            sticky=W,
            )
        self.varEntryHostName.set(self.computerName)
#        self.entrySendHostName.configure(state='disable')
# ... date
        self.labelDate = Label(
            self.frameMySQL_10_10,
            text='Date:\nyyyy/mm/dd',
            justify=RIGHT,
            bg=self.colorbg,
            )
        self.labelDate.grid(
            row=0,
            column=6,
            padx=5,
            pady=0,
            sticky=E,
            )
        self.varEntryDate = StringVar()
        self.entryDate = Entry(
            self.frameMySQL_10_10,
            justify=LEFT,
            textvariable=self.varEntryDate,
            width=20,
            disabledforeground='black',
            disabledbackground='white',
            state='disable',
            )
        self.entryDate.grid(
            row=0,
            column=7,
            padx=0,
            pady=0,
            sticky=W,
            )
        self.varEntryDate.set(
            self.date
            )
# ... time
        self.labelTime = Label(
            self.frameMySQL_10_10,
            text='Time of\nlast send:',
            justify=RIGHT,
            bg=self.colorbg,
            )
        self.labelTime.grid(
            row=0,
            column=8,
            padx=5,
            pady=0,
            sticky=E,
            )
        self.varEntryTime = StringVar()
        self.entryTime = Entry(
            self.frameMySQL_10_10,
            justify=LEFT,
            textvariable=self.varEntryTime,
            width=20,
            disabledforeground='black',
            disabledbackground='white',
            state='disable',
            )
        self.entryTime.grid(
            row=0,
            column=9,
            padx=0,
            pady=0,
            sticky=W,
            )
        self.varEntryTime.set(
            '--:--:--'
#            self.time
            )
#Test Files and Data
            
# ...  input file
        self.labelInputFile = Label(
            self.frameMySQL_20_00,
            text='INPUT file\n(sample)',
            justify=RIGHT,
            bg=self.colorbg,
            )
        self.labelInputFile.grid(
            row=0,
            column=0,
            padx=5,
            pady=2,
            sticky=E,
            )
        self.entryInputFile = Pmw.ScrolledText(
            self.frameMySQL_20_00,
            usehullsize=1,
            hull_width=150,
            hull_height=HULL_HEIGHT_0,
            text_wrap='none',
            hscrollmode='static',
            vscrollmode='none',
            text_font=self.buttonFontSmall,
            )
        self.entryInputFile.grid(
            row=0,
            column=1,
            columnspan=2,
            padx=0,
            pady=2,
            sticky=W,
            )
        self.entryInputFile.configure(
            text_state='disabled'
            )
        self.entryInputFile.setvalue(
            ''
            )
# ... browse for input file
        self.buttonBrowseForInputFile = Button(
            self.frameMySQL_20_00,
            text='Browse',
            width=6,
            background='white',
            foreground='blue',
            font=self.buttonFont,
            borderwidth=3,
            relief=RAISED,
            command=self.handlerBrowseForInputFile,
            )
        self.buttonBrowseForInputFile.grid(
            row=1,
            column=1,
            padx=0,
            pady=0,
            sticky=N,
            )
# ... clear input file and dir
        self.buttonClearInputFile = Button(
            self.frameMySQL_20_00,
            text='Clear',
            width=6,
            background='white',
            foreground='blue',
            font=self.buttonFont,
            borderwidth=3,
            relief=RAISED,
            command=self.handlerClearInputFile,
            )
        self.buttonClearInputFile.grid(
            row=1,
            column=2,
            padx=2,
            pady=0,
            sticky=N,
            )
# ... directory for input file
        self.labelInputFileDirectory = Label(
            self.frameMySQL_20_00,
            text='INPUT file dir',
            justify=RIGHT,
            bg=self.colorbg,
            )
        self.labelInputFileDirectory.grid(
            row=2,
            column=0,
            padx=5,
            pady=2,
            sticky=E,
            )
        self.entryInputFileDirectory = Pmw.ScrolledText(
            self.frameMySQL_20_00,
            usehullsize=1,
            hull_width=150,
            hull_height=HULL_HEIGHT_0,
            text_wrap='none',
            hscrollmode='static',
            vscrollmode='none',
            text_font=self.buttonFontSmall,
            )
        self.entryInputFileDirectory.grid(
            row=2,
            column=1,
            columnspan=2,
            padx=0,
            pady=5,
            )
        self.entryInputFileDirectory.configure(
            text_state='disabled'
            )
        self.entryInputFileDirectory.setvalue(
            ''
            )            
            
# ...  output file
        self.labelOutputFile = Label(
            self.frameMySQL_20_01,
            text='OUTPUT file\n(REQUIRED INPUT)',
            justify=RIGHT,
            bg=self.colorbg,
            )
        self.labelOutputFile.grid(
            row=0,
            column=0,
            padx=5,
            pady=2,
            sticky=E,
            )  
        self.scrolledtextOutputFile = Pmw.ScrolledText(
            self.frameMySQL_20_01,
            usehullsize=1,
            hull_width=150,
            hull_height=HULL_HEIGHT_0,
            text_wrap='none',
            hscrollmode='static',
            vscrollmode='none',
            text_font=self.buttonFontSmall,
            )
        self.scrolledtextOutputFile.grid(
            row=0,
            column=1,
            columnspan=2,
            padx=0,
            pady=2,
            sticky=W,
            )
        self.scrolledtextOutputFile.configure(
            text_state='disabled'
            )
        self.scrolledtextOutputFile.setvalue(
            ''
            )
# ... browse for output file
        self.buttonBrowseForOutputFile = Button(
            self.frameMySQL_20_01,
            text='Browse',
            width=6,
            background='white',
            foreground='blue',
            font=self.buttonFont,
            borderwidth=3,
            relief=RAISED,
            command=self.handlerBrowseForOutputFile,
            )
        self.buttonBrowseForOutputFile.grid(
            row=1,
            column=1,
            padx=0,
            pady=0,
            sticky=N,
            )
# ... clear output file and dir
        self.buttonClearOutputFile = Button(
            self.frameMySQL_20_01,
            text='Clear',
            width=6,
            background='white',
            foreground='blue',
            font=self.buttonFont,
            borderwidth=3,
            relief=RAISED,
            command=self.handlerClearOutputFile,
            )
        self.buttonClearOutputFile.grid(
            row=1,
            column=2,
            padx=2,
            pady=0,
            sticky=N,
            )
# ... directory for output file
        self.labelOutputFileDirectory = Label(
            self.frameMySQL_20_01,
            text='OUTPUT file dir',
            justify=RIGHT,
            bg=self.colorbg,
            )
        self.labelOutputFileDirectory.grid(
            row=2,
            column=0,
            padx=5,
            pady=0,
            sticky=E,
            )
        self.scrolledtextOutputFileDirectory = Pmw.ScrolledText(
            self.frameMySQL_20_01,
            usehullsize=1,
            hull_width=150,
            hull_height=HULL_HEIGHT_0,
            text_wrap='none',
            hscrollmode='static',
            vscrollmode='none',
            text_font=self.buttonFontSmall,
            )
        self.scrolledtextOutputFileDirectory.grid(
            row=2,
            column=1,
            columnspan=2,
            padx=0,
            pady=5,
            )
        self.scrolledtextOutputFileDirectory.configure(
            text_state='disabled'
            )
        self.scrolledtextOutputFileDirectory.setvalue(
            ''
            )
        '''
        self.varOutputFileDirectory = StringVar()
        self.scrolledtextOutputFileDirectory = Entry(
            self.frameMySQL_20_01,
            textvariable=self.varOutputFileDirectory,
            justify=LEFT,
            width=20,
            disabledforeground='black',
            disabledbackground='white',
            state='disable',
            )
        self.scrolledtextOutputFileDirectory.grid(
            row=2,
            column=1,
            padx=0,
            pady=2,
            sticky=W,
            )
        '''
        
# select option for which OUTPUT file(s) to copy to database
# ... batch process (in row 0, column 2, self.frameMySQL_20)
        Row = 0
        '''
        labelText = Label(
            self.frameMySQL_20_02,
            text='Process these OUTPUT files...',
            bg=self.colorbg,
            justify=LEFT,
            font=self.buttonFont,
            )
        labelText.grid(
            row=Row,
            column=0,
            padx=0,
            pady=0,
            sticky=W,
            )
        '''
# ...   just this file
        Row =0
        self.varRadiobutton_ProcessFiles = StringVar()
        self.radiobutton_JustThisFile = Radiobutton(
            self.frameMySQL_20_02,
            text='just this file',
            font=self.buttonFont,
            bg=self.colorbg,
            borderwidth=0,
            variable=self.varRadiobutton_ProcessFiles,
            value='just_this_file',
            )
        self.radiobutton_JustThisFile.grid(
            row=Row,
            column=0,
            padx=0,
            pady=0,
            sticky=W,
            )
# ...   all files with this extension
        Row += 1
        self.radiobutton_WithThisExtension = Radiobutton(
            self.frameMySQL_20_02,
            text='all 00/00 files with extension',
            font=self.buttonFont,
            bg=self.colorbg,
            borderwidth=0,
            variable=self.varRadiobutton_ProcessFiles,
            value='with_this_extension',
            )
        self.radiobutton_WithThisExtension.grid(
            row=Row,
            column=0,
            padx=0,
            pady=0,
            sticky=W,
            )
        Row += 1   
        self.varEntry_WithThisExtension = StringVar()
        self.entry_WithThisExtension = Entry(
            self.frameMySQL_20_02,
            bg=self.colorbg,
            borderwidth=3,
            background='white',
            foreground='black',
            state='disable',
            disabledbackground='white',
            disabledforeground='black',
            width=15,
            textvariable=self.varEntry_WithThisExtension,
            )
        self.entry_WithThisExtension.grid(
            row=Row,
            column=0,
            padx=0,
            pady=0,
            sticky=N,
            )     
# ...   all files that begin with
        Row += 1
        self.radiobutton_ThatBeginWith = Radiobutton(
            self.frameMySQL_20_02,
            text='all 00/00 files that begin with',
            font=self.buttonFont,
            bg=self.colorbg,
            borderwidth=0,
            variable=self.varRadiobutton_ProcessFiles,
            value='that_begin_with',
            command=self.methodRadiobutton_ThatBeginWith,
            )
        self.radiobutton_ThatBeginWith.grid(
            row=Row,
            column=0,
            padx=0,
            pady=0,
            sticky=W,
            )
        Row += 1
        self.varEntry_ThatBeginWith = StringVar()
        self.entry_ThatBeginWith = Entry(
            self.frameMySQL_20_02,
            bg=self.colorbg,
            borderwidth=3,
            background='white',
            foreground='black',
            state='disable',
            disabledbackground='white',
            disabledforeground='black',
            width=15,
            textvariable=self.varEntry_ThatBeginWith,
            )
        self.entry_ThatBeginWith.grid(
            row=Row,
            column=0,
            padx=0,
            pady=0,
            sticky=N,
            )  
# ...   all files containing the phrase
        Row += 1
        self.radiobutton_ContainsThePhrase = Radiobutton(
            self.frameMySQL_20_02,
            text='all 00/00 files that contain the phrase',
            font=self.buttonFont,
            bg=self.colorbg,
            borderwidth=0,
            variable=self.varRadiobutton_ProcessFiles,
            value='contains_the_phrase',
            command=self.handlerRadiobutton_ContainsThePhrase,
            )
        self.radiobutton_ContainsThePhrase.grid(
            row=Row,
            column=0,
            padx=0,
            pady=0,
            sticky=W,
            )
        Row += 1
        self.varEntry_ContainsThePhrase = StringVar()
        self.entry_ContainsThePhrase = Entry(
            self.frameMySQL_20_02,
            bg=self.colorbg,
            borderwidth=3,
            background='white',
            foreground='black',
 #           state='disable',
 #           disabledbackground='white',
 #           disabledforeground='black',
            width=15,
            textvariable=self.varEntry_ContainsThePhrase,
            )
        self.entry_ContainsThePhrase.grid(
            row=Row,
            column=0,
            padx=0,
            pady=0,
            sticky=N,
            )  
# ...   all files in this directory
        Row += 1
        self.radiobutton_InThisDirectory = Radiobutton(
            self.frameMySQL_20_02,
            text='all 0 files in this directory',
            font=self.buttonFont,
            bg=self.colorbg,
            borderwidth=0,
            variable=self.varRadiobutton_ProcessFiles,
            value='in_this_directory',
            )
        self.radiobutton_InThisDirectory.grid(
            row=Row,
            column=0,
            padx=0,
            pady=0,
            sticky=W,
            )
            
# ... select first option as default: "just this file"
        self.radiobutton_JustThisFile.select()
            
# makefile
        self.labelMakeFile = Label(
            self.frameMySQL_20_03,
            text='MAKEFILE\n(sample)',
            justify=RIGHT,
            bg=self.colorbg,
            )
        self.labelMakeFile.grid(
            row=0,
            column=0,
            padx=5,
            pady=2,
            sticky=E,
            ) 
        self.entryMakeFile = Pmw.ScrolledText(
            self.frameMySQL_20_03,
            usehullsize=1,
            hull_width=150,
            hull_height=HULL_HEIGHT_0,
            text_wrap='none',
            hscrollmode='static',
            vscrollmode='none',
            text_font=self.buttonFontSmall,
            )
        self.entryMakeFile.grid(
            row=0,
            column=1,
            columnspan=2,
            padx=0,
            pady=2,
            sticky=W,
            )
        self.entryMakeFile.configure(
            text_state='disabled'
            )
        self.entryMakeFile.setvalue(
            ''
            )
# ... browse for make file
        self.buttonBrowseForMakeFile = Button(
            self.frameMySQL_20_03,
            text='Browse',
            width=6,
            background='white',
            foreground='blue',
            font=self.buttonFont,
            borderwidth=3,
            relief=RAISED,
            command=self.handlerBrowseForMakeFile,
            )
        self.buttonBrowseForMakeFile.grid(
            row=1,
            column=1,
            padx=0,
            pady=0,
            sticky=N,
            )
# ... clear make file and dir
        self.buttonClearMakeFile = Button(
            self.frameMySQL_20_03,
            text='Clear',
            width=6,
            background='white',
            foreground='blue',
            font=self.buttonFont,
            borderwidth=3,
            relief=RAISED,
            command=self.handlerClearMakeFile,
            )
        self.buttonClearMakeFile.grid(
            row=1,
            column=2,
            padx=2,
            pady=0,
            sticky=N,
            )
# ... directory for make file
        self.labelMakeFileDirectory = Label(
            self.frameMySQL_20_03,
            text='MAKEFILE dir',
            justify=RIGHT,
            bg=self.colorbg,
            )
        self.labelMakeFileDirectory.grid(
            row=2,
            column=0,
            padx=5,
            pady=2,
            sticky=E,
            )
        self.entryMakeFileDirectory = Pmw.ScrolledText(
            self.frameMySQL_20_03,
            usehullsize=1,
            hull_width=150,
            hull_height=HULL_HEIGHT_0,
            text_wrap='none',
            hscrollmode='static',
            vscrollmode='none',
            text_font=self.buttonFontSmall,
            )
        self.entryMakeFileDirectory.grid(
            row=2,
            column=1,
            columnspan=2,
            padx=0,
            pady=5,
            )
        self.entryMakeFileDirectory.configure(
            text_state='disabled'
            )
        self.entryMakeFileDirectory.setvalue(
            ''
            )

# source file
        self.labelSourceFile = Label(
            self.frameMySQL_20_04,
            text='SOURCE file\n(sample)',
            justify=RIGHT,
            bg=self.colorbg,
            )
        self.labelSourceFile.grid(
            row=0,
            column=0,
            padx=5,
            pady=2,
            sticky=E,
            ) 
        self.entrySourceFile = Pmw.ScrolledText(
            self.frameMySQL_20_04,
            usehullsize=1,
            hull_width=150,
            hull_height=HULL_HEIGHT_0,
            text_wrap='none',
            hscrollmode='static',
            vscrollmode='none',
            text_font=self.buttonFontSmall,
            )
        self.entrySourceFile.grid(
            row=0,
            column=1,
            columnspan=2,
            padx=0,
            pady=2,
            sticky=W,
            )
        self.entrySourceFile.configure(
            text_state='disabled'
            )
        self.entrySourceFile.setvalue(
            ''
            )
# ... browse for source file
        self.buttonBrowseForSourceFile = Button(
            self.frameMySQL_20_04,
            text='Browse',
            width=6,
            background='white',
            foreground='blue',
            font=self.buttonFont,
            borderwidth=3,
            relief=RAISED,
            command=self.handlerBrowseForSourceFile,
            )
        self.buttonBrowseForSourceFile.grid(
            row=1,
            column=1,
            padx=0,
            pady=0,
            sticky=N,
            )
# ... clear source file and dir
        self.buttonClearSourceFile = Button(
            self.frameMySQL_20_04,
            text='Clear',
            width=6,
            background='white',
            foreground='blue',
            font=self.buttonFont,
            borderwidth=3,
            relief=RAISED,
            command=self.handlerClearSourceFile,
            )
        self.buttonClearSourceFile.grid(
            row=1,
            column=2,
            padx=2,
            pady=0,
            sticky=N,
            )
# ... directory for source file
        self.labelSourceFileDirectory = Label(
            self.frameMySQL_20_04,
            text='SOURCE file dir',
            justify=RIGHT,
            bg=self.colorbg,
            )
        self.labelSourceFileDirectory.grid(
            row=2,
            column=0,
            padx=5,
            pady=2,
            sticky=E,
            )
        self.entrySourceFileDirectory = Pmw.ScrolledText(
            self.frameMySQL_20_04,
            usehullsize=1,
            hull_width=150,
            hull_height=HULL_HEIGHT_0,
            text_wrap='none',
            hscrollmode='static',
            vscrollmode='none',
            text_font=self.buttonFontSmall,
            )
        self.entrySourceFileDirectory.grid(
            row=2,
            column=1,
            columnspan=2,
            padx=0,
            pady=5,
            )
        self.entrySourceFileDirectory.configure(
            text_state='disabled'
            )
        self.entrySourceFileDirectory.setvalue(
            ''
            )
        
# executable file & dir
        self.labelExecutableFile = Label(
            self.frameMySQL_20_10,
            text='EXECUTABLE\nfile\n(sample) ',
            justify=RIGHT,
            bg=self.colorbg,
            )
        self.labelExecutableFile.grid(
            row=0,
            column=0,
            padx=5,
            pady=2,
            sticky=E,
            ) 
        self.entryExecutableFile = Pmw.ScrolledText(
            self.frameMySQL_20_10,
            usehullsize=1,
            hull_width=150,
            hull_height=HULL_HEIGHT_0,
            text_wrap='none',
            hscrollmode='static',
            vscrollmode='none',
            text_font=self.buttonFontSmall,
            )
        self.entryExecutableFile.grid(
            row=0,
            column=1,
            columnspan=2,
            padx=0,
            pady=2,
            sticky=W,
            )
        self.entryExecutableFile.configure(
            text_state='disabled'
            )
        self.entryExecutableFile.setvalue(
            ''
            )
# ... browse for executable file
        self.buttonBrowseForExecutableFile = Button(
            self.frameMySQL_20_10,
            text='Browse',
            width=6,
            background='white',
            foreground='blue',
            font=self.buttonFont,
            borderwidth=3,
            relief=RAISED,
            command=self.handlerBrowseForExecutableFile,
            )
        self.buttonBrowseForExecutableFile.grid(
            row=1,
            column=1,
            padx=0,
            pady=0,
            sticky=N,
            )
# ... clear executable file and dir
        self.buttonClearExecutableFile = Button(
            self.frameMySQL_20_10,
            text='Clear',
            width=6,
            background='white',
            foreground='blue',
            font=self.buttonFont,
            borderwidth=3,
            relief=RAISED,
            command=self.handlerClearExecutableFile,
            )
        self.buttonClearExecutableFile.grid(
            row=1,
            column=2,
            padx=2,
            pady=0,
            sticky=N,
            )
# ... directory for executable file
        self.labelExecutableFileDirectory = Label(
            self.frameMySQL_20_10,
            text='EXECUTABLE\nfile directory ',
            justify=RIGHT,
            bg=self.colorbg,
            )
        self.labelExecutableFileDirectory.grid(
            row=2,
            column=0,
            padx=5,
            pady=2,
            sticky=E,
            )
        self.entryExecutableFileDirectory = Pmw.ScrolledText(
            self.frameMySQL_20_10,
            usehullsize=1,
            hull_width=150,
            hull_height=HULL_HEIGHT_0,
            text_wrap='none',
            hscrollmode='static',
            vscrollmode='none',
            text_font=self.buttonFontSmall,
            )
        self.entryExecutableFileDirectory.grid(
            row=2,
            column=1,
            columnspan=2,
            padx=0,
            pady=5,
            )
        self.entryExecutableFileDirectory.configure(
            text_state='disabled'
            )
        self.entryExecutableFileDirectory.setvalue(
            ''
            )
            
# ... machine on which executable was run
        labelText = Label(
            self.frameMySQL_20_11,
            text='Machine on which\nexecutable was run', #\n(REQUIRED INPUT)',
            justify=RIGHT,
            bg=self.colorbg,
            )
        labelText.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=0,
            pady=0,
#            sticky=S,
            )
        self.varMachineOnWhichExecutableWasRun = StringVar()
        self.entryMachineOnWhichExecutableWasRun = Entry(
            self.frameMySQL_20_11,
            justify=LEFT,
            textvariable=self.varMachineOnWhichExecutableWasRun,
            width=15,
            borderwidth=3,
            foreground='black',
            background='white',
            )
        self.entryMachineOnWhichExecutableWasRun.grid(
            row=0,
            column=1,
#            rowspan=2,
            padx=10,
            pady=0,
            sticky=S
            )
        self.buttonClearMachineOnWhichExecutableWasRun = Button(
            self.frameMySQL_20_11,
            text='Clear',
            width=6,
            background='white',
            foreground='blue',
            font=self.buttonFont,
            borderwidth=3,
            relief=RAISED,
            command=self.handlerClearMachineOnWhichExecutableWasRun,
            )
        self.buttonClearMachineOnWhichExecutableWasRun.grid(
            row=1,
            column=1,
            padx=5,
            pady=2,
            sticky=N,
            )
# ... tester name: first and last
        label = Label(
            self.frameMySQL_20_12,
            text='Tester\'s\nname',
            justify=RIGHT,
            bg=self.colorbg,
            )
        label.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=2,
            pady=2,
            sticky=E,
            )
        label = Label(
            self.frameMySQL_20_12,
            text='first: ',
            justify=RIGHT,
            bg=self.colorbg,
            )
        label.grid(
            row=0,
            column=1,
            padx=0,
            pady=2,
            sticky=E,
            )
        self.varEntryTesterName_First = StringVar()
        self.entryTesterName_First = Entry(
            self.frameMySQL_20_12,
            justify=LEFT,
            textvariable=self.varEntryTesterName_First,
            width=15,
            borderwidth=3,
            foreground='black',
            background='white',
            )
        self.entryTesterName_First.grid(
            row=0,
            column=2,
            padx=0,
            pady=0,
            sticky=W
            )
        label = Label(
            self.frameMySQL_20_12,
            text='last: ',
            justify=RIGHT,
            bg=self.colorbg,
            )
        label.grid(
            row=1,
            column=1,
            padx=0,
            pady=2,
            sticky=E,
            )
        self.varEntryTesterName_Last = StringVar()
        self.entryTesterName_Last = Entry(
            self.frameMySQL_20_12,
            justify=LEFT,
            textvariable=self.varEntryTesterName_Last,
            width=15,
            borderwidth=3,
            foreground='black',
            background='white',
            )
        self.entryTesterName_Last.grid(
            row=1,
            column=2,
            padx=0,
            pady=2,
            sticky=W
            )
        buttonClearTesterNameFirstAndLast = Button(
            self.frameMySQL_20_12,
            text='Clear',
            width=6,
            background='white',
            foreground='blue',
            font=self.buttonFont,
            borderwidth=3,
            relief=RAISED,
            command=self.handlerClearTesterNameFirstAndLast,
            )
        buttonClearTesterNameFirstAndLast.grid(
            row=2,
            column=2,
            padx=5,
            pady=0,
            sticky=N,
            )
            
# ... qsub file
        self.labelQsubFile = Label(
            self.frameMySQL_20_13,
            text='QSUB file\n(sample)',
            justify=RIGHT,
            bg=self.colorbg,
            )
        self.labelQsubFile.grid(
            row=0,
            column=0,
            padx=5,
            pady=2,
            sticky=E,
            ) 
        self.entryQsubFile = Pmw.ScrolledText(
            self.frameMySQL_20_13,
            usehullsize=1,
            hull_width=150,
            hull_height=HULL_HEIGHT_0,
            text_wrap='none',
            hscrollmode='static',
            vscrollmode='none',
            text_font=self.buttonFontSmall,
            )
        self.entryQsubFile.grid(
            row=0,
            column=1,
            columnspan=2,
            padx=0,
            pady=2,
            sticky=W,
            )
        self.entryQsubFile.configure(
            text_state='disabled'
            )
        self.entryQsubFile.setvalue(
            ''
            )
# ... browse for qsub file
        self.buttonBrowseForQsubFile = Button(
            self.frameMySQL_20_13,
            text='Browse',
            width=6,
            background='white',
            foreground='blue',
            font=self.buttonFont,
            borderwidth=3,
            relief=RAISED,
            command=self.handlerBrowseForQsubFile,
            )
        self.buttonBrowseForQsubFile.grid(
            row=1,
            column=1,
            padx=0,
            pady=0,
            sticky=N,
            )
# ... clear qsub file and dir
        self.buttonClearQsubFile = Button(
            self.frameMySQL_20_13,
            text='Clear',
            width=6,
            background='white',
            foreground='blue',
            font=self.buttonFont,
            borderwidth=3,
            relief=RAISED,
            command=self.handlerClearQsubFile,
            )
        self.buttonClearQsubFile.grid(
            row=1,
            column=2,
            padx=2,
            pady=0,
            sticky=N,
            )
# ... directory for qsub file
        self.labelQsubFileDirectory = Label(
            self.frameMySQL_20_13,
            text='QSUB file dir ',
            justify=RIGHT,
            bg=self.colorbg,
            )
        self.labelQsubFileDirectory.grid(
            row=2,
            column=0,
            padx=5,
            pady=2,
            sticky=E,
            )
        self.entryQsubFileDirectory = Pmw.ScrolledText(
            self.frameMySQL_20_13,
            usehullsize=1,
            hull_width=150,
            hull_height=HULL_HEIGHT_0,
            text_wrap='none',
            hscrollmode='static',
            vscrollmode='none',
            text_font=self.buttonFontSmall,
            )
        self.entryQsubFileDirectory.grid(
            row=2,
            column=1,
            columnspan=2,
            padx=0,
            pady=5,
            )
        self.entryQsubFileDirectory.configure(
            text_state='disabled'
            )
        self.entryQsubFileDirectory.setvalue(
            ''
            )

# compile line
# ... clear compile line
        self.buttonClearCompileLine = Button(
            self.frameMySQL_20_20_00,
            text='Clear',
            width=5,
            background='white',
            foreground='blue',
            font=self.buttonFont,
            borderwidth=3,
            relief=RAISED,
            command=self.handlerClearCompileLine,
            )
        self.buttonClearCompileLine.grid(
            row=0,
            column=2,
            padx=2,
            pady=2,
            )
# ... label for compile line
        self.labelCompileLine = Label(
            self.frameMySQL_20_20_00,
            text='Copy/Paste\ncompile line\n(sample)',
            justify=RIGHT,
            bg=self.colorbg,
            fg='black',
            )
        self.labelCompileLine.grid(
            row=0,
            column=0,
            padx=0,
            pady=2,
            )
# ... entry for compile line
        '''
        self.varCompileLine = StringVar()
        self.entryCompileLine = Entry(
            self.frameMySQL_20_10_00,
            textvariable=self.varCompileLine,
            justify=LEFT,
            width=50,
            )
        self.entryCompileLine.grid(
            row=0,
            column=2,
            padx=0,
            pady=2,
            )
        '''
        self.entryCompileLine = Pmw.ScrolledText(
            self.frameMySQL_20_20_00,
            usehullsize=1,
            hull_width=400,
            hull_height=HULL_HEIGHT_0,
            text_wrap='none',
            hscrollmode='static',
            vscrollmode='none',
            text_font=self.buttonFontSmall,
            )
        self.entryCompileLine.grid(
            row=0,
            column=1,
            padx=0,
            pady=2,
            )
        self.entryCompileLine.setvalue(
            ''
            )
            
# ... clear execute line
        self.buttonClearExecuteLine = Button(
            self.frameMySQL_20_20_01,
            text='Clear',
            width=5,
            background='white',
            foreground='blue',
            font=self.buttonFont,
            borderwidth=3,
            relief=RAISED,
            command=self.handlerClearExecuteLine,
            )
        self.buttonClearExecuteLine.grid(
            row=0,
            column=2,
            padx=2,
            pady=2,
            )            
# ... label for execute line
        self.labelExecuteLine = Label(
            self.frameMySQL_20_20_01,
            text='Copy/Paste\nexecute line\n(sample)',
            justify=RIGHT,
            bg=self.colorbg,
            fg='black',
            )
        self.labelExecuteLine.grid(
            row=0,
            column=0,
            padx=0,
            pady=2,
            )
# ... entry for execute line
        '''
        self.varExecuteLine = StringVar()
        self.entryExecuteLine = Entry(
            self.frameMySQL_20_10_01,
            textvariable=self.varExecuteLine,
            justify=LEFT,
            width=50,
            )
        self.entryExecuteLine.grid(
            row=0,
            column=2,
            padx=0,
            pady=2,
            ) 
        '''
        self.entryExecuteLine = Pmw.ScrolledText(
            self.frameMySQL_20_20_01,
            usehullsize=1,
            hull_width=400,
            hull_height=HULL_HEIGHT_0,
            text_wrap='none',
            hscrollmode='static',
            vscrollmode='none',
            text_font=self.buttonFontSmall,
            )
        self.entryExecuteLine.grid(
            row=0,
            column=1,
            padx=0,
            pady=2,
            )
        self.entryExecuteLine.setvalue(
            ''
            )

# ... label for user comment
        self.labelUserComment = Label(
            self.frameMySQL_21,
            text='User comments\n(approx 8,000 characters max; no double quotes)',
            justify=RIGHT,
            bg=self.colorbg,
            fg='black',
            )
        self.labelUserComment.grid(
            row=0,
            column=0,
            padx=5,
            pady=2,
            )
        self.buttonClearUserComment = Button(
            self.frameMySQL_21,
            text='Clear text',
            bg='white',
            fg='blue',
            borderwidth=3,
            font=self.buttonFont,
            width=10,
            relief=RAISED,
            command=self.handlerClearUserComment,
            )
        self.buttonClearUserComment.grid(
            row=1,
            column=0,
            padx=5,
            pady=2,
            )
            
# ...   User comment
        fixedFont = Pmw.logicalfont('Fixed')
        self.scrolledtextUserComment = Pmw.ScrolledText(
            self.frameMySQL_21,
#            labelpos='n',
#            label_text='Summary of field "' + varField + '"\n' +
#               'from table "' + myTable + '"',
#            label_font=self.titleFont,
#            label_background='lightgreen',
            columnheader=0,
            rowheader=0,
            rowcolumnheader=0,
            usehullsize=1,
            hull_width=600,
            hull_height=HULL_HEIGHT_1,
#            text_wrap='none',
            text_wrap='word',
#            text_font=fixedFont,
            text_font=self.buttonFontSmall,
#            text_font=self.dataFontLarge,
#            Header_font=fixedFont,
#            Header_foreground='tan',
#            Header_background='lightgreen',
#            rowheader_width=3,
#            rowcolumnheader_width=3,
            text_padx=3,
            text_pady=3,
#            Header_padx=3,
#            rowheader_pady=3,
            vscrollmode='static',
            hscrollmode='static',
            )
        self.scrolledtextUserComment.grid(
            row=0,
            column=1,
            rowspan=99,
            padx=5,
            pady=2,
            sticky=E+W,
            )
# create row header from list of field names
#        headerFieldNames = self.dictColumnHeaders.keys()
#        headerFieldNames = ['Count','Field Values']
#        scrolledtextSummary.component('rowcolumnheader').insert('end','No.')

# ... LEFT TOP       
        labelConnect = Label(
            self.frameMySQL_30_00,
            text='CONNECT TO MySQL SERVER\n(skip if saving to file)',
            bg=self.colorbg,
            font=self.titleFontBig,
            )
        labelConnect.grid(
            row=0,
            column=0,
            columnspan=99,
            padx=0,
            pady=0,
            )
# ... label for server            
        labelConnect = Label(
            self.frameMySQL_30_00,
            text='Server ',
            bg=self.colorbg,
            )
        labelConnect.grid(
            row=1,
            column=0,
            sticky=E,
            pady=2
            ) 
# servers        
        self.comboServerMySQL = Pmw.ComboBox(
            self.frameMySQL_30_00,
            scrolledlist_items=self.servers,
            listheight=100,
            entry_width=20,
            scrolledlist_hull_width=500,
            selectioncommand=self.handlerAssignUserName,
            )
        self.comboServerMySQL.grid(
            row=1,
            column=1,
            sticky=W,
            pady=2,
            ) 
#        self.comboServerMySQL.component('scrolledlist').configure(
#            hull_width=20,
#            hull_width=self.comboServerMySQL.component('entryfield').winfo_reqwidth()
#            )
        self.comboServerMySQL.selectitem(self.servers[0])
# ... label for username            
        labelConnect = Label(
            self.frameMySQL_30_00,
            text='Username ',
            bg=self.colorbg,
            )
        labelConnect.grid(
            row=2,
            column=0,
            sticky=E,
            pady=2
            ) 
# ... entry field for username
        self.varUserMySQL = StringVar()
        self.varUserMySQL.set(self.userName)
        self.entryUserMySQL = Entry(
            self.frameMySQL_30_00,
            width=20,
            textvariable=self.varUserMySQL,
            )
        self.entryUserMySQL.grid(
            row=2,
            column=1,
            sticky=W,
            pady=2
            )
# ... label for password            
        labelConnect = Label(
            self.frameMySQL_30_00,
            text='Password ',
            bg=self.colorbg,
            )
        labelConnect.grid(
            row=3,
            column=0,
            sticky=E,
            pady=2
            ) 
# ... entry for password
        self.varPasswordMySQL = StringVar()
        self.varPasswordMySQL.set('')
        self.entryPasswordMySQL = Entry(
            self.frameMySQL_30_00,
            width=20,
            show='*',
            textvariable=self.varPasswordMySQL
            )
        self.entryPasswordMySQL.grid(
            row=3,
            column=1,
            sticky=W,
            pady=2
            )
        self.entryPasswordMySQL.bind(
            "<KeyPress-Return>",
            self.handlerConnectAfterPassword,
            )

# ... label for Port      
        labelPort = Label(
            self.frameMySQL_30_00,
            text='Port ',
            bg=self.colorbg,
            )
        labelPort.grid(
            row=4,
            column=0,
            sticky=E,
            pady=2
            ) 
# ... entry for port
        self.varPortMySQL = StringVar()
        self.varPortMySQL.set('3306')
        self.entryPortMySQL = Entry(
            self.frameMySQL_30_00,
            width=20,
            textvariable=self.varPortMySQL,
            )
        self.entryPortMySQL.grid(
            row=4,
            column=1,
            sticky=W,
            )
            
# set some parameters
        try:
            self.comboServerMySQL.selectitem(self.servers[0])
        except:
            self.comboServerMySQL.setentry(' ')
        if self.comboServerMySQL.get().strip() == 'localhost':
#            self.varUserMySQL.set('root')
            self.varUserMySQL.set(self.usernameForLocalServer)
        else:
            self.varUserMySQL.set(self.usernameForRemoteServer)
            
# ... clear all
        self.buttonClearInputsMySQL = Button(
            self.frameMySQL_30_00,
            text='Clear All',
            font=self.buttonFont,
            borderwidth=3,
            width=7,
            relief=RAISED,
            background='white',
            foreground='blue',
            command=self.handlerClearValuesMySQL,
            )
        self.buttonClearInputsMySQL.grid(
            row=5,
            column=1,
#            columnspan=99,
            padx=2,
            pady=0,
            sticky=W,
            )
            
# ... reset to default values
        self.buttonResetInputsMySQL = Button(
            self.frameMySQL_30_00,
            text='Default',
            font=self.buttonFont,
            borderwidth=3,
            width=7,
            relief=RAISED,
            background='white',
            foreground='blue',
            command=self.handlerResetValuesMySQL,
            )
        self.buttonResetInputsMySQL.grid(
            row=5,
            column=1,
#            columnspan=99,
            padx=2,
            pady=0,
            sticky=E
            )

# ... connect button
        self.buttonConnectToMySQL = Button(
            self.frameMySQL_30_10,
            text='Connect',
#            bg=self.colorbg,
            borderwidth=5,
            relief=RAISED,
            command=self.handlerMySQLConnect,
            )
        self.buttonConnectToMySQL.grid(
            row=1,
            column=0,
            padx=10,
            )
            
# ... status label
        labelStatus = Label(
            self.frameMySQL_30_10,
            text=' STATUS',
            font=self.titleFontBig,
            bg=self.colorbg,
            )
        labelStatus.grid(
            row=1,
            column=1,
            pady=5,
            )
            
# ... status checkbuttons
#       not connected
        self.varStatusDbNotConnected = StringVar()
        self.varStatusDbNotConnected.set(0)
        self.checkbuttonStatusDbNotConnected = Radiobutton(
            self.frameMySQL_30_10,
            text='Not connected',
            justify=LEFT,
            variable=self.varStatusDbNotConnected,
            indicatoron=1,
            selectcolor='red',
            bg=self.colorbg,
            fg='black',
            disabledforeground='black',
            )
        self.checkbuttonStatusDbNotConnected.grid(
            row=0,
            column=2,
            sticky=W,
            )

#       attempting to connect
        self.varStatusDbAttemptConnect = StringVar()
        self.varStatusDbAttemptConnect.set(0)
        self.checkbuttonStatusDbAttemptConnect = Radiobutton(
            self.frameMySQL_30_10,
            text='Attempting to connect',
            justify=LEFT,
            variable=self.varStatusDbAttemptConnect,
            indicatoron=1,
            selectcolor='yellow',
            bg=self.colorbg,
            fg='black',
            disabledforeground='black',
            )
        self.checkbuttonStatusDbAttemptConnect.grid(
            row=1,
            column=2,
            sticky=W,
            )

#       connected
        self.varStatusDbConnected = StringVar()
        self.varStatusDbConnected.set(0)
        self.checkbuttonStatusDbConnected = Radiobutton(
            self.frameMySQL_30_10,
            text='Connected',
            justify=LEFT,
            variable=self.varStatusDbConnected,
            indicatoron=1,
            selectcolor='green',
            bg=self.colorbg,
            fg='black',
            disabledforeground='black',
            )
        self.checkbuttonStatusDbConnected.grid(
            row=2,
            column=2,
            sticky=W,
            )
 
# disable all but the 'Not connected' indicator
        self.checkbuttonStatusDbNotConnected.configure(state='normal')
        self.checkbuttonStatusDbAttemptConnect.configure(state='disabled')
        self.checkbuttonStatusDbConnected.configure(state='disabled')

# button to disconnect from server        
        self.buttonMySQLDisconnect = Button(
            self.frameMySQL_30_10,
            text='Disconnect from MySQL server',
            borderwidth=5,
            relief=RAISED,
            command=self.handlerMySQLDisconnect,
            )
        self.buttonMySQLDisconnect.grid(
            row=3,
            column=0,
            columnspan=99,
            padx=0,
            pady=0,
            )
            
# ... Send to Database
        self.buttonSend2Db = Button(
            self.frameMySQL_4,
            text='Send to MySQL table',
            borderwidth=5,
            relief=RAISED,
            background='white',
            foreground='blue',
            width=25,
            command=self.handlerSend2MySQLTable,
            )
        self.buttonSend2Db.grid(
            row=0,
            column=0,
            padx=10,
            pady=5,
            )
            
# ... Save MySQL command to file for later input to PylotDB; used particulary if
#       database server is not accessible from current machine
        self.buttonSaveMySQLCommand = Button(
            self.frameMySQL_4,
            text='Save MySQL command to file',
            borderwidth=5,
            relief=RAISED,
            background='white',
            foreground='blue',
            width=25,
            command=self.handlerSaveMySQLCommand,
            )
        self.buttonSaveMySQLCommand.grid(
            row=1,
            column=0,
            padx=10,
            pady=5,
            )

# Reset and Cancel
        self.buttonReset = Button(
            self.frameMySQL_50,
            text='Reset',
            borderwidth=5,
            relief=RAISED,
            width=20,
#            command=???,
            )
        '''
        self.buttonReset.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            )
        '''
        
# DATABASES ON SERVER
# initialize myDatabases as empty       
        self.myDatabases = []
# graph combobox widget
        self.mysql_ComboDatabases()

# TABLES IN DATABASE
# initialize myDatabaseTables as empty
        self.myDatabaseTables = []
# graph combobox widget
        self.mysql_ComboDatabaseTables()
       
# update canvas
        self.frameInCanvas.grid_rowconfigure(1,weight=1)
        self.frameInCanvas.grid_columnconfigure(1,weight=1)
        self.canvasMain.create_window(
            0,
            0,
            anchor=NW,
            window=self.frameInCanvas,
            )
        self.frameInCanvas.update_idletasks()
        self.canvasMain.config(scrollregion=self.canvasMain.bbox('all'))


# check screen resolution

# For PylotDB to display properly, the minimum screen resolution must be 1280x960
        currentScreenResolution_Width = int(self.frameParent.winfo_screenwidth())
        currentScreenResolution_Height = int(self.frameParent.winfo_screenheight())
        
        stringScreenResolution = (
            'Current screen resolution: %s x %s\n' +
            'Minimum screen resolution required: %s x %s'
            ) % (
                currentScreenResolution_Width,
                currentScreenResolution_Height,
                str(minScreenResolution_Width),
                str(minScreenResolution_Height)
                )                
        
# place current screen resolution on main window
# ... screen resolution label
        labelScreenResolution = Label(
            self.frameMySQL_4,
            text=stringScreenResolution,
            bg=self.colorbg,
            )
        labelScreenResolution.grid(
            row=2,
            column=0,
            padx=0,
            pady=5,
            )
            
# copyright notice
        labelCopyright = Label(
            self.frameMySQL_4,
            text=SANDIA_COPYRIGHT_NOTICE,
            bg=self.colorbg,
            font=self.tableFont8,
            justify=CENTER,
            width=65,
            )
        labelCopyright.grid(
            row=3,
            column=0,
            padx=0,
            pady=2,
            )
            
# button to display open source license
        button = Button(
            self.frameMySQL_4,
            text='Co-PylotDB Copyright & Open Source License',
            font=self.buttonFontSmall,
            justify=CENTER,
            relief=RAISED,
            borderwidth=5,
            background='lightgreen',
            foreground='black',
            command=self.copyrightandosslicenseDisplay,
            )
        button.grid(
            row=4,
            column=0,
            padx=0,
            pady=2,
            )
        
        self.buttonCancel = Button(
            self.frameMySQL_4,
            text='Quit',
            borderwidth=5,
            relief=RAISED,
            width=15,
            command=self.handlerQuit,
            )
        self.buttonCancel.grid(
            row=5,
            column=0,
            padx=0,
            pady=20,
            sticky=S
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
                'for Co-PylotDB to display correctly.\n' 
                ) % ( 
                str(minScreenResolution_Width), 
                str(minScreenResolution_Height)
                )
                
            self.displayScreenResolution(
                minScreenResolution_Width,
                minScreenResolution_Height,
                currentScreenResolution_Width,
                currentScreenResolution_Height)

# =============== DEFS ===============================

    def copyrightandosslicenseDisplay(self):
        '''
        Purpose:
            display open source license
        '''

        
        showinfo(
            'Info: copyright and open source license',
            licenseSandia
            )
        
        '''
        toplevelOSS = Toplevel(
            self.frameParent,
            bg='white',
            )
        toplevelOSS.title(
            'OPEN-SOURCE LICENSE FOR CO-PYLOTDB'
            )
        toplevelOSS.transient(
            self.frameParent
            )
        toplevelOSS.geometry(
            '+100+20'
            )
        
        text = Text(
            toplevelOSS,
            height=30,
            relief=RAISED,
            wrap=WORD,
            width=85,
            )
        text.grid(
            row=0,
            column=0,
            padx=2,
            pady=2,
            sticky=N,
            )
        text.configure(state='normal')
        text.insert(
            1.0,
            OPEN_SOURCE_SOFTWARE_LICENSE
            )
        text.configure(state='disabled')
        '''
            
        return
        

    def displayScreenResolution(self,
        minWidth,
        minHeight,
        currentWidth,
        currentHeight
        ):
        '''
        Purpose: 
            display current and min screen resolution for Co-PylotDB to display properly,
            if current resolution is not enough. Give user choice to continue (perhaps
            for use with a low-resolution projector) or quit Co-PylotDB so user can set
            screen resolution and re-start Co-PylotDB
        '''
        
        stringScreenResolution = (
            'For Co-PylotDB to display properly, the minimum screen\n' +
            'resolution must be\n\n' +
            '   %s x %s\n\n' +
            'Current screen resolution is set to\n\n' +
            '   %s x %s\n\n' +
            'You can continue running Co-PylotDB at the current screen\n' +
            'resolution by clicking YES, but certain windows will not\n' +
            'display properly.\n\n' +
            'To adjust resolution, click NO. Co-PylotDB will exit. Set screen\n' +
            'resolution to at least the minimum and restart Co-PylotDB.\n\n' +
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

    def handlerAssignUserName(self,value):
        '''
        Purpose:
            assign Username each time a Server is picked
        
        '''
        if DEBUG_PRINTMETHODNAME:
            print('\n** In ' + MODULE + '/' + 'handlerAssignUserName')
        
        if value == 'localhost':
#            self.varUserMySQL.set('root')
            self.varUserMySQL.set(self.usernameForLocalServer)
        else:
            self.varUserMySQL.set(self.usernameForRemoteServer)
            
        return
        

    def handlerClearTesterNameFirstAndLast(self):
        '''
        Purpose:
            clears tester's first and last names from fields
        '''
        self.varEntryTesterName_First.set('')
        self.varEntryTesterName_Last.set('')
        
        return
        

    def handlerXScrollFrameForCanvas(self,*args):
        '''
        allows x scrolling of frame
        '''
        self.canvasMain.xview(*args)
        return
        
    def handlerYScrollFrameForCanvas(self,*args):
        '''
        allows y scrolling of frame
        '''
        self.canvasMain.yview(*args)
        return

    def handlerBrowseForMakeFile(self):
        '''
        Purpose:
            Search for and select make file
        '''
        if DEBUG_PRINTMETHODNAME:
            print('\n** In handlerBrowseForMakeFile **')
# define dictionary of options for askopenfilename()
        options = {}
        options = {
#            'defaultextension' : '.',
            'defaultextension' : '',
#            'filetypes' : [('Comma-Separated Values','.csv'),('All files','.*')],
            'filetypes' : [('All files','*')],
#            'initialdir' : '.',
            'initialdir' : self.initialDir,          
            'initialfile' : '',
            'parent' : self.frameParent,
            'title' : 'Select make file'
            } 
            
# full filepath
        try:
            self.filepathMake = tkFileDialog.askopenfilename(**options)
        except:
            stringError = (
                'Cannot open MAKEFILE'
                )
            print stringError
            showinfo(
                'Error opening MAKEFILE',
                stringError
                )
            return
# split into directory name and filename
        dirname, filename = os.path.split(self.filepathMake)
# reset self.initialDir
        self.initialDir = dirname
        '''
# get filename
        dirname, filename = os.path.split(
            tkFileDialog.askopenfilename(**options)
            )
        '''
# check            
        if filename == '':
            print '   No make filename chosen!'
            '''
            showinfo(
                'No make filename chosen...',
                'You must enter a filename for the file to be read'
                )
            '''
            return
        else:
            print '\n    makefile dirname =',dirname
            print '    makefile filename =',filename  
            
# read file contents as one string
        try:
            self.fileMake = open(self.filepathMake,'r').read()
        except:
            stringError = (
                'Cannot read MAKEFILE\n\n' +
                '%s\n\n'
                ) % (filename)
            print stringError
            showinfo(
                'Error reading MAKEFILE',
                stringError
                )
            return
            
        print 'contents of fileMake =\n',self.fileMake
        
# put name and directory into proper widgets
#        self.varMakeFile.set(filename)
        self.entryMakeFile.setvalue(filename)
#        self.varMakeFileDirectory.set(dirname)
        self.entryMakeFileDirectory.setvalue(dirname)
            
        return
            
    
    def handlerBrowseForSourceFile(self):
        '''
        Purpose:
            Search for and select source file
        '''
        if DEBUG_PRINTMETHODNAME:
            print('\n** In handlerBrowseForSourceFile **')
# define dictionary of options for askopenfilename()
        options = {}
        options = {
#            'defaultextension' : '.',
            'defaultextension' : '',
#            'filetypes' : [('Comma-Separated Values','.csv'),('All files','.*')],
            'filetypes' : [('All files','*')],
#            'initialdir' : '.',
            'initialdir' : self.initialDir,
            'initialfile' : '',
            'parent' : self.frameParent,
            'title' : 'Select source file'
            } 
            
# full filepath
        try:
            self.filepathSource = tkFileDialog.askopenfilename(**options)
        except:
            stringError = (
                'Cannot open the SOURCE file'
                )
            print stringError
            showinfo(
                'Error opening SOURCE file',
                stringError
                )
            return
# split into directory name and filename
        dirname, filename = os.path.split(self.filepathSource)
# reset self.initialDir
        self.initialDir = dirname
        '''
# get filename
        dirname, filename = os.path.split(
            tkFileDialog.askopenfilename(**options)
            )
        '''
# check            
        if filename == '':
            print '   No source filename chosen!'
            '''
            showinfo(
                'No source filename chosen...',
                'You must enter a filename for the file to be read'
                )
            '''
            return
        else:
            print '\n    Source dirname =',dirname
            print '    Source filename =',filename
            
# read file contents as one string
        try:
            self.fileSource = open(self.filepathSource,'r').read()
        except:
            stringError = (
                'Cannot read the SOURCE file\n\n' +
                '%s\n\n'
                ) % (filename)
            print stringError
            showinfo(
                'Error reading SOURCE file',
                stringError
                )
            return
            
        print 'contents of fileSource =\n',self.fileSource
        
# put name and directory into proper widgets
#        self.varSourceFile.set(filename)
        self.entrySourceFile.setvalue(filename)
#        self.varSourceFileDirectory.set(dirname)
        self.entrySourceFileDirectory.setvalue(dirname)
            
        return
            

    def handlerBrowseForInputFile(self):
        '''
        Purpose:
            Search for and select the input file
        ''' 
        if DEBUG_PRINTMETHODNAME:        
            print('\n** In handlerBrowseForInputFile **')
            
# define dictionary of options for askopenfilename()
        options = {}
        options = {
#            'defaultextension' : '.csv',
            'defaultextension' : '',
#            'filetypes' : [('Comma-Separated Values','.csv'),('All files','.*')],
            'filetypes' : [('All files','*')],
#            'initialdir' : '.',
            'initialdir' : self.initialDir,
            'initialfile' : '',
            'parent' : self.frameParent,
            'title' : 'Select input file'
            } 
# full filepath
        try:
            self.filepathInput = tkFileDialog.askopenfilename(**options)
        except:
            stringError = (
                'Cannot open the INPUT file'
                )
            print stringError
            showinfo(
                'Error opening INPUT file',
                stringError
                )
            return
        
# split into directory name and filename
        dirname, filename = os.path.split(self.filepathInput)
# reset self.initialDir
        self.initialDir = dirname
        '''
# get filename
        dirname, filename = os.path.split(
            tkFileDialog.askopenfilename(**options)
            )
        '''
# check
        if filename == '':
            print '   No input filename chosen!'
            '''
            showinfo(
                'No input filename chosen...',
                'You must enter a filename for the file to be read'
                )
            '''
            return
        else:
            print '\n    Input dirname =',dirname
            print '    Input filename =',filename
            
# read file contents as one string
        try:
            self.fileInput = open(self.filepathInput,'r').read()
        except:
            stringError = (
                'Cannot read the INPUT file\n\n' +
                '%s\n\n'
                ) % (filename)
            print stringError
            showinfo(
                'Error reading INPUT file',
                stringError
                )
            return
            
        print 'contents of fileInput =\n',self.fileInput
        
# put name and directory into proper widgets
#        self.varInputFile.set(filename)
        self.entryInputFile.setvalue(filename)
#        self.varInputFileDirectory.set(dirname)
        self.entryInputFileDirectory.setvalue(dirname)
                   
        return
        
    def handlerBrowseForOutputFile(self):
        '''
        Purpose:
            Search for and select the output file
        '''
        if DEBUG_PRINTMETHODNAME:
            print('\n** In handlerBrowseForOutputFile **')
            
# define dictionary of options for askopenfilename()
        options = {}
        options = {
#            'defaultextension' : '.',
            'defaultextension' : '',
#            'filetypes' : [('Comma-Separated Values','.csv'),('All files','.*')],
            'filetypes' : [('All files','*')],
#            'initialdir' : '.',
            'initialdir' : self.initialDir,
            'initialfile' : '',
            'parent' : self.frameParent,
            'title' : 'Select output file'
            } 
            
# full filepath
        try:
            self.filepathOutput = tkFileDialog.askopenfilename(**options)
        except:
            stringError = (
                'Cannot open the OUTPUT file'
                )
            print stringError
            showinfo(
                'Error opening OUTPUT file',
                stringError
                )
            return
            
# clear '... contain the phrase'
        self.radiobutton_ContainsThePhrase.configure(
            text=('all 00/00 files that contain the phrase')
            )
        self.varEntry_ContainsThePhrase.set('')

# split into directory name and filename
        dirname, filename = os.path.split(self.filepathOutput)
# reset self.initialDir
        self.initialDir = dirname
        '''
# get filename
        dirname, filename = os.path.split(
            tkFileDialog.askopenfilename(**options)
            )
        '''
# check            
        if filename == '':
            print '   No output filename chosen!'
            '''
            showinfo(
                'No output filename chosen...',
                'You must enter a filename for the file to be read'
                )
            '''
            return
        else:
            if DEBUG:
                print '\n    Output dirname =',dirname
                print '    Output filename =',filename
            
        fnNoExtension, extension = os.path.splitext(filename)
        if DEBUG:
            print('  > fnNoExtension = %s' % fnNoExtension)
            print('  > extension = %s' % extension)
        
# put name and directory into proper widgets
#        self.varOutputFile.set(filename)
        self.scrolledtextOutputFile.setvalue(filename)
#        self.varOutputFileDirectory.set(dirname)
        self.scrolledtextOutputFileDirectory.setvalue(dirname)

# since output files may be batch processed, read contents in 'def handlerSend2MySQLTable'   
        
# put first few chars of filename in entry field for 'all files that begin with'
        check = self.methodRadiobutton_ThatBeginWith()
# make sure 'ThatBeginWith' field is not empty
        if check:
            return
        
# determine how many files are affected
        numberOfFilesAffected_WithThisExtension = 0
        numberOfFilesAffected_ThatBeginWith = 0
        numberOfFilesTotal = 0
#        extension = os.path.splitext(filename)[1]
        beginwith = self.varEntry_ThatBeginWith.get()
        length = self.lengthBeginningFileNameLettersToMatch
        for myfile in os.listdir(dirname):
            numberOfFilesTotal += 1
            fnWithNoExtension,extensionMyFile = os.path.splitext(myfile)
            if extensionMyFile == extension:
                numberOfFilesAffected_WithThisExtension += 1
            if len(fnWithNoExtension) > length:
                beginwithMyFile = fnWithNoExtension[0:length]
            else:
                beginwithMyFile = fnWithNoExtension
            if beginwithMyFile == beginwith:
                numberOfFilesAffected_ThatBeginWith += 1
        
# put extension of filename in entry field for 'all files with this extension'
        try:
            self.varEntry_WithThisExtension.set(extension)
        except:
            pass
# show number of files affected for each option
        self.radiobutton_WithThisExtension.configure(
            text=('all %s/%s files with this extension' % 
            (numberOfFilesAffected_WithThisExtension,numberOfFilesTotal) )
            )
        self.radiobutton_ThatBeginWith.configure(
            text=('all %s/%s files that begin with' %
            (numberOfFilesAffected_ThatBeginWith,numberOfFilesTotal) )
            )
        self.radiobutton_InThisDirectory.configure(
            text=('all %s files in this directory' %
            (numberOfFilesTotal) )
            )
            
        return
        
    def handlerBrowseForExecutableFile(self):
        '''
        Purpose:
            Search for and select executable file
        '''
        if DEBUG_PRINTMETHODNAME:
            print('\n** In handlerBrowseForExecutableFile **')
            
# define dictionary of options for askopenfilename()
        options = {}
        options = {
#            'defaultextension' : '.',
            'defaultextension' : '',
#            'filetypes' : [('Comma-Separated Values','.csv'),('All files','.*')],
            'filetypes' : [('All files','*')],
#            'initialdir' : '.',
            'initialdir' : self.initialDir,
            'initialfile' : '',
            'parent' : self.frameParent,
            'title' : 'Select executable file'
            } 
            
# full filepath
        try:
            self.filepathExecutable = tkFileDialog.askopenfilename(**options)
        except:
            stringError = (
                'Cannot open the EXECUTABLE file'
                )
            print stringError
            showinfo(
                'Error opening EXECUTABLE file',
                stringError
                )
            return
# split into directory name and filename
        dirname, filename = os.path.split(self.filepathExecutable)
# reset self.initialDir
        self.initialDir = dirname
        '''
# get filename
        dirname, filename = os.path.split(
            tkFileDialog.askopenfilename(**options)
            )
        '''
# check            
        if filename == '':
            print '   No executable filename chosen!'
            '''
            showinfo(
                'No executable filename chosen...',
                'You must enter a filename for the file to be read'
                )
            '''
            return
        else:
            if DEBUG:
                print '\n    Executable dirname =',dirname
                print '    Executable filename =',filename
            
# read file contents as one string
        try:
            self.fileExecutable = open(self.filepathExecutable,'r').read()
        except:
            stringError = (
                'Cannot read the EXECUTABLE file\n\n' +
                '%s\n\n'
                ) % (filename)
            print stringError
            showinfo(
                'Error reading EXECUTABLE file',
                stringError
                )
            return
            
        if DEBUG:
            print 'contents of fileExecutable =\n',self.fileExecutable
        
# put name and directory into proper widgets
        self.entryExecutableFile.setvalue(filename)
        self.entryExecutableFileDirectory.setvalue(dirname)
            
        return
        
    def handlerBrowseForQsubFile(self):
        '''
        Purpose:
            Search for and select qsub file
        '''
        if DEBUG_PRINTMETHODNAME:
            print('\n** In handlerBrowseForQsubFile **')
        
# define dictionary of options for askopenfilename()
        options = {}
        options = {
#            'defaultextension' : '.',
            'defaultextension' : '',
#            'filetypes' : [('Comma-Separated Values','.csv'),('All files','.*')],
            'filetypes' : [('All files','*')],
#            'initialdir' : '.',
            'initialdir' : self.initialDir,
            'initialfile' : '',
            'parent' : self.frameParent,
            'title' : 'Select qsub file'
            } 
            
# full filepath
        try:
            self.filepathQsub = tkFileDialog.askopenfilename(**options)
        except:
            stringError = (
                'Cannot open the QSUB file'
                )
            print stringError
            showinfo(
                'Error opening QSUB file',
                stringError
                )
            return
# split into directory name and filename
        dirname, filename = os.path.split(self.filepathQsub)
# reset self.initialDir
        self.initialDir = dirname
        
        print '\n  Qsub dirname = ',dirname
        print '\n  Qsub filename = ',filename
        
        '''
# get filename
        dirname, filename = os.path.split(
            tkFileDialog.askopenfilename(**options)
            )
        '''
# check            
        if filename == '':
            print '   No qsub filename chosen!'
            '''
            showinfo(
                'No qsub filename chosen...',
                'You must enter a filename for the file to be read'
                )
            '''
            return
        else:
            if DEBUG:
                print '\n    Qsub dirname =',dirname
                print '    Qsub filename =',filename
            
# read file contents as one string
        try:
            self.fileQsub = open(self.filepathQsub,'r').read()
        except:
            stringError = (
                'Cannot read the QSUB file\n\n' +
                '%s\n\n'
                ) % (filename)
            print stringError
            showinfo(
                'Error reading QSUB file',
                stringError
                )
            return
            
        if DEBUG:
            print 'contents of fileQsub =\n',self.fileQsub
        
# put name and directory into proper widgets
#        self.varSourceFile.set(filename)
        self.entryQsubFile.setvalue(filename)
#        self.varSourceFileDirectory.set(dirname)
        self.entryQsubFileDirectory.setvalue(dirname)
            
        return
        

    def handlerQuit(self):
        '''
        Purpose:
            closes program
        '''
        stringQuit=(
            '\nAre you sure you want to quit? \n'
            )
        close = askokcancel(
            'Quit?',
            stringQuit
            )
        if close:
            sys.exit()
            
        return
        
    def handlerSend2MySQLTable(self):
        '''
        Purpose:
            send all fields to selected database table
            
        Variables:
            sendToTable
                = 1     try to send data to MySQL database table
                = 0     save MySQL command as file, to move to another
                        machine that can reach a database server
        '''
        if DEBUG_PRINTMETHODNAME:
            print('\n** In handlerSend2MySQLTable')
        
# check for connection
        self.checkMySQLConnection()
        if self.connectionFlag == 0:
            return
        
# error checks
# ... 1. check for entries in required fields

        entryOutputFile = self.scrolledtextOutputFile.get().strip()
#        entryMachineForExecutable = self.varMachineOnWhichExecutableWasRun.get().strip()
        stringNoEntry = ''
        if entryOutputFile == '': # or entryMachineForExecutable == '':
            if entryOutputFile == '':
                stringNoEntry += (
                    '\nNo entry in field for "OUTPUT file".\n\n' +
                    'This is a REQUIRED field.\n\n' +
                    'Specify an output file and try again.\n'
                    )
            '''
            if entryMachineForExecutable == '':
                stringNoEntry += (
                    '\n> No entry in field "Machine on which executable was run".\n\n' +
                    'This is a REQUIRED field.\n\n' +
                    'Specify a machine name and try again.'
                    )
            '''              
        if stringNoEntry <> '':
            print stringNoEntry
            showinfo(
                'Error: no entry',
                stringNoEntry
                )
            return

            
# ... 2. if 'all files that begin with' is chosen, the first few chars
#       specified in this field MUST match the same first few chars in
#       the entry in 'OUTPUT file'
        stringErrorMatchingFirstFewCharacters = ''
        lengthBeginWith = len(self.varEntry_ThatBeginWith.get())
        lengthOutputFile = len(self.scrolledtextOutputFile.get())
        if lengthOutputFile > lengthBeginWith:
            firstCharsOutputFile = self.scrolledtextOutputFile.get()[0:lengthBeginWith]
        else:
            firstCharsOutputFile = self.scrolledtextOutputFile.get()[0:lengthOutputFile]
            
        if self.varRadiobutton_ProcessFiles.get() == 'that_begin_with':
# make sure length of first few characters is <= entry in 'OUTPUT file'
            if lengthBeginWith > lengthOutputFile:
                stringErrorMatchingFirstFewCharacters = (
                    'The length of the entry for "all files that begin with"\n' +
                    'is greater than the length for the "OUTPUT file".\n\n' +
                    'Shorten the entry for the "all files that begin with" field or\n' +
                    'select another OUTPUT file and try again.'
                    )
# make sure lengthBeginWith > 0
            elif lengthBeginWith == 0:
                stringErrorMatchingFirstFewCharacters = (
                    'There is no entry in the field "all files that begin with".\n\n' +
                    'The characters in this field must match the corresponding\n' +
                    'characters for the "OUTPUT file" entry.\n\n' +
                    'Specify the characters to match and try again.'
                    )
# make sure first few chars match in both entry fields
            elif self.varEntry_ThatBeginWith.get() <> firstCharsOutputFile:
                stringErrorMatchingFirstFewCharacters = (
                    'The characters in the field "all files that begin with"\n' +
                    'must match the same number of characters in the "OUTPUT file" field.\n\n' +
                    'Specify a new OUTPUT file or modify the entry for the first\n' +
                    'few characters to match the OUTPUT file, and try again.'
                    )
            else:
                pass
                
        if stringErrorMatchingFirstFewCharacters <> '':
            print stringErrorMatchingFirstFewCharacters
            showinfo(
                'Error: char mismatch',
                stringErrorMatchingFirstFewCharacters
                )
            return
            
# ----- end of error checks -----
        
# set params to empty; 23 total
        inputFile = ''
        inputFileDir = ''
        inputFileContents = ''
        outputFile = ''
        outputFileDir = ''
        outputFileContents = ''
        makeFile = ''
        makeFileDir = ''
        makeFileContents = ''
        sourceFile = ''
        sourceFileDir = ''
        sourceFileContents = ''
        executableFile = ''
        executableFileDir = ''
        machineForExecutable = ''
        testerNameFirst = ''
        testerNameLast = ''
        qsubFile = ''
        qsubFileDir = ''
        qsubFileContents = ''
        compileLine = ''
        executeLine = ''
        userComments = ''
        
# get user, current directory, hostname
        user = self.varEntryUser.get()
        currentDirectory = self.varEntryDirectory.get()
        hostName = self.varEntryHostName.get()
#        date = self.varEntryDate.get()
        
# update date and time before sending to table
        date = time.ctime(time.time())[4:10] + ' ' + time.ctime(time.time())[20:24]
        month = time.ctime(time.time())[4:7]
        dayofweek = time.ctime(time.time())[0:3]
        dayofmonth = time.ctime(time.time())[8:10]
        year = time.ctime(time.time())[20:24]        
        dateOfLastSend = year + '/' + self.dictMonth[month] + '/' + dayofmonth
        timeOfLastSend = time.ctime(time.time())[11:19]
        
        timeStartDate = (2011,1,1,0,0,0,5,1,0)
        timeStartDateSinceEpoch_Seconds = time.mktime(timeStartDate)
        timeNow_Seconds = time.time()
        timeNowSinceStartDate_Days = \
            (timeNow_Seconds - timeStartDateSinceEpoch_Seconds)/3600./24. + 1
        day_number_since_01jan2011 = int(timeNowSinceStartDate_Days)

# input file
#        inputFile = self.varInputFile.get().strip()
        inputFile = self.entryInputFile.getvalue().strip()
        inputFileDir = self.entryInputFileDirectory.getvalue().strip()
        inputFileContents = self.fileInput.strip()
# output file(s)        
        outputFile = self.scrolledtextOutputFile.getvalue().strip()
        outputFileDir = self.scrolledtextOutputFileDirectory.getvalue().strip()
#        outputFileContents = self.fileOutput.strip()
# make file       
        makeFile = self.entryMakeFile.getvalue().strip()
        makeFileDir = self.entryMakeFileDirectory.getvalue().strip()
        makeFileContents = self.fileMake.strip()
# source file      
        sourceFile = self.entrySourceFile.getvalue().strip()
        sourceFileDir = self.entrySourceFileDirectory.getvalue().strip()
        sourceFileContents = self.fileSource.strip()
# executable file
        executableFile = self.entryExecutableFile.getvalue().strip()
        executableFileDir = self.entryExecutableFileDirectory.getvalue().strip()
# machine for executable
        machineForExecutable = self.varMachineOnWhichExecutableWasRun.get().strip()
# tester name first
        testerNameFirst = self.varEntryTesterName_First.get().lower().strip()
# tester name last
        testerNameLast = self.varEntryTesterName_Last.get().lower().strip()
# qsub file
        qsubFile = self.entryQsubFile.getvalue().strip()
        qsubFileDir = self.entryQsubFileDirectory.getvalue().strip()
        qsubFileContents = self.fileQsub.strip()
# compile line        
        compileLine = self.entryCompileLine.getvalue().strip()
# execute line
        executeLine = self.entryExecuteLine.getvalue().strip()
# user comments        
        userComments = self.scrolledtextUserComment.getvalue().strip()
# ... no double quotes allowed!
        userComments = userComments.replace('"',"'")
# ... get rid of any unicode that gives problems
        userComments = userComments.replace(u'\u200e',' ')
        
# display time of this send in main window
        self.varEntryTime.set(
            timeOfLastSend
            )
        self.varEntryDate.set(
            dateOfLastSend
            )

# define myDatabase and myTable using values in main window
        myDatabase = self.comboboxDbSelect.get()
        myTable = self.comboboxDbTableSelect.get()

        batchProcess = self.varRadiobutton_ProcessFiles.get()
        allOutputFiles = []
# get directory; important to strip off trailing white space
        allDirectory = self.scrolledtextOutputFileDirectory.getvalue().strip()

# process following files

# ... just this file
        if batchProcess == 'just_this_file':
            splitOutputFile = self.scrolledtextOutputFile.getvalue().split('.')
            outputFileExtension = splitOutputFile[len(splitOutputFile)-1].strip()          
            allOutputFiles.append(self.filepathOutput)
            
# ... with this extension
        elif batchProcess == 'with_this_extension':            
# get filename extension; important to strip off trailing white space
            splitOutputFile = self.scrolledtextOutputFile.getvalue().split('.')
            outputFileExtension = splitOutputFile[len(splitOutputFile)-1].strip()
# use glob.glob to get list of files using above extension and directory
            filesLocation = allDirectory + '/*.' + outputFileExtension
            allOutputFiles = glob.glob(filesLocation)
            
# ... that begin with
        elif batchProcess == 'that_begin_with':
# use glob.glob to get list of files using above directory
            fileBeginsWith = self.varEntry_ThatBeginWith.get().strip()
# check that entry field for fileBeginsWith is not empty
            if fileBeginsWith == '':
                stringEmptyBeginsWith = (
                    'The entry field for this option is empty.\n\n' +
                    'Specify the desired beginning letters and/or numbers\n' +
                    'in the entry field and try again.'
                    )
                print stringEmptyBeginsWith
                showinfo(
                    'Error: empty entry field',
                    stringEmptyBeginsWith
                    )
                return
            filesLocation = allDirectory + '/' + fileBeginsWith + '*.*'
            allOutputFiles = glob.glob(filesLocation)
            
# ... contains the phrase
        elif batchProcess == 'contains_the_phrase':
# use glob.glob to get list of files using above directory
            fileContainsThePhrase = self.varEntry_ContainsThePhrase.get().strip()
            if DEBUG_CONTAINS_THE_PHRASE:
                print('\nfileContainsThePhrase = %s' % fileContainsThePhrase)
            
# check that entry field for fileContains is not empty
            if fileContainsThePhrase == '':
                stringEmptyContainsThePhrase = (
                    'The entry field for this option is empty.\n\n' +
                    'Specify the desired phrase to match in the\n' +
                    'entry field and try again.'
                    )
                print stringEmptyContainsThePhrase
                showinfo(
                    'Error: empty entry field',
                    stringEmptyContainsThePhrase
                    )
                return
            filesLocation = allDirectory + '/*' + fileContainsThePhrase + '*.*'
            allOutputFiles = glob.glob(filesLocation)
            if DEBUG_CONTAINS_THE_PHRASE:
                print('allOutputFiles = ')
                print(allOutputFiles)
                print('\n> For files containing the phrase %s:' % fileContainsThePhrase)
                icount = 0
                for file in allOutputFiles:
                    if file <> '':
                        icount += 1
                        print('%s. %s' % (icount, file))
                print()
            
# ... all files in this directory
        elif batchProcess == 'in_this_directory':
# use glob.glob to get list of files using above directory
            filesLocation = allDirectory + '/*.*'
            allOutputFiles = glob.glob(filesLocation)
# ... failure
        else:
            stringErrorProcess = (
                'The attribute "batchProcess" must equal one of the following:\n\n' +
                ' > "just_this_file"\n' +
                ' > "with_this_extension"\n' +
                ' > "that_begin_with"\n' +
                ' > "contains_the_phrase"\n' +
                ' > "in_this_directory"\n\n' +
                'Current value: %s\n\n' +
                'This represents a coding error. Contact code administrator.'
                ) % batchProcess
            print stringErrorProcess
            showinfo(
                'Error: batchProcess',
                stringErrorProcess
                )
            return
                                
        if DEBUG:
            print '\nallOutputFiles =\n\n', allOutputFiles
# 

# check all text files for special character " (double quote) and
# \" (backslash + double quotes). 
# If this exists in the file, add a backslash in front of the special
#    character, i.e., \" if the special character is a double quote.
# Files to check:
#   1. INPUT file: self.fileInput --> inputFileContents
#   2. MAKEFILE: self.fileMake --> makeFileContents
#   3. SOURCE file: self.fileSource --> sourceFileContents
#   4. QSUB file: self.fileQsub --> qsubFileContents
# ... and taken care of farther below...
#   5. OUTPUT file: self.scrolledtextOutputFile --> outputFileContents 

# ... escape double quotes, and backslash double quotes,
#    since they are considered special characters
# ... inputFileContents
        if '\\\"' in inputFileContents:
            inputFileContents = inputFileContents.replace('\\\"','\\\\\\"')
        elif '\"' in inputFileContents:
            inputFileContents = inputFileContents.replace("\"","\\\"")
        else:
            pass
# ... makeFileContents  
        if '\\\"' in makeFileContents:
            makeFileContents = makeFileContents.replace('\\\"','\\\\\\"')
        elif '\"' in makeFileContents:     
            makeFileContents = makeFileContents.replace("\"","\\\"")
        else:
            pass
# ... sourceFileContents
        if '\\\"' in sourceFileContents:
            sourceFileContents = sourceFileContents.replace('\\\"','\\\\\\"')
        elif '\"' in sourceFileContents:     
            sourceFileContents = sourceFileContents.replace("\"","\\\"")
        else:
            pass
# ... qsubFileContents
        if '\\\"' in qsubFileContents:
            qsubFileContents = qsubFileContents.replace('\\\"','\\\\\\"')
        elif '\"' in qsubFileContents:     
            qsubFileContents = qsubFileContents.replace("\"","\\\"")
        else:
            pass


# print all variables
        if DEBUG:
            print('')
            print(' ----- start of variables -----')
            print('user = %s' % user)
            print('testerNameFirst = %s' % testerNameFirst)
            print('testerNameLast = %s' % testerNameLast)
            print('currentDirectory = %s' % currentDirectory)
            print('hostName = %s' % hostName)
            print('machineForExecutable = %s' % machineForExecutable)
            print('day_number_since_01jan2011 = %s' % day_number_since_01jan2011)
            print('dayofweek = %s' % dayofweek)
            print('month = %s' % month)
            print('year = %s' % year)
            print('dateOfLastSend = %s' % dateOfLastSend)
            print('timeOfLastSend = %s' % timeOfLastSend)
            print('inputFile = %s' % inputFile)
            print('inputFileDir = %s' % inputFileDir)
            print('outputFile = %s' % outputFile)
            print('outputFileDir = %s' % outputFileDir)
            print('makeFile = %s' % makeFile)
            print('sourceFile = %s' % sourceFile)
            print('sourceFileDir = %s' % sourceFileDir)
            print('executableFile = %s' % executableFile)
            print('executableFileDir = %s' % executableFileDir)
            print('qsubFile = %s' % qsubFile)
            print('qsubFileDir = %s' % qsubFileDir)
            print('compileLine = %s' % compileLine)
            print('executeLine = %s' % executeLine)
            print('userComments = %s' % userComments)
            print('myDatabase = %s' % myDatabase)
            print('myTable = %s' % myTable)
            print('allOutputFiles = %s' % allOutputFiles)
            print(' ----- end of variables -----')
            
        stringPrintAllVariables = (
        '----- VARIABLES TO SEND TO DATABASE TABLE -----\n' +
        'user = %s\n' +
        'testerNameFirst = %s\n' + 
        'testerNameLast = %s\n' + 
        'currentDirectory = %s\n' + 
        'hostName = %s\n' + 
        'machineForExecutable = %s\n' + 
        'day_number_since_01jan2011 = %s\n' + 
        'dayofweek = %s\n' +
        'month = %s\n' +
        'dayofmonth = %s\n' +
        'year = %s\n' +
        'dateOfLastSend = %s\n' + 
        'timeOfLastSend = %s\n' +
        'inputFile = %s\n' + 
        'inputFileDir = %s\n' + 
        'outputFile = %s\n' + 
        'outputFileDir = %s\n' +             
        'makeFile = %s\n' + 
        'makeFileDir = %s\n' + 
        'sourceFile = %s\n' + 
        'sourceFileDir = %s\n' + 
        'executableFile = %s\n' + 
        'executableFileDir = %s\n' + 
        'qsubFile = %s\n' + 
        'qsubFileDir = %s\n' + 
        'compileLine = %s\n' + 
        'executeLine = %s\n' + 
        'userComments = %s\n' + 
        'myDatabase = %s\n' + 
        'myTable = %s\n' +
        'allOutputFiles = %s'
        )%(
        user,
        testerNameFirst,
        testerNameLast,
        currentDirectory,
        hostName,
        machineForExecutable,
        day_number_since_01jan2011,
        dayofweek,
        month,
        dayofmonth,
        year,
        dateOfLastSend,
        timeOfLastSend,
        inputFile,
        inputFileDir,
        outputFile,
        outputFileDir,
        makeFile,
        makeFileDir,
        sourceFile,
        sourceFileDir,
        executableFile,
        executableFileDir,
        qsubFile,
        qsubFileDir,
        compileLine,
        executeLine,
        userComments,
        myDatabase,
        myTable,
        allOutputFiles
        )
        
        if DEBUG:
            print(stringPrintAllVariables)
        
        if len(allOutputFiles) == 0:
                stringNoOutputFile = (
                    'Specify an OUTPUT file'
                    )
                showinfo(
                    'Error: no OUTPUT file (send)',
                    stringNoOutputFile
                    )
        
        rangeLenAllOutputFiles = []
        rangeLenAllOutputFiles = range(len(allOutputFiles))
                
        for numrow in rangeLenAllOutputFiles:
            print('\n>> working on file #%s of %s total' % (numrow + 1, len(allOutputFiles)))
            
# separate directory from filename
            outputFileDir, outputFile = os.path.split(allOutputFiles[numrow]) 
            if DEBUG:
                print '\noutputFile =',outputFile
                print 'outputFileDir =',outputFileDir
                print 'allOutputFiles[%s] = %s' % (numrow, allOutputFiles[numrow])

# read file contents as one string
            try:
                outputFileContents = open(allOutputFiles[numrow],'r').read()
            except:
                if allOutputFiles[numrow] == '':
                    stringError = (
                        'OUTPUT file must be specified.'
                        )
                    print stringError
                    showinfo(
                        'Error: OUTPUT file (send)',
                        stringError
                        )
                    return
                else:
                    stringError = (
                        'Cannot read the OUTPUT file\n\n' +
                        '%s\n'
                        ) % (allOutputFiles[numrow])
                    print stringError
                    showinfo(
                        'Error: OUTPUT file (send)',
                        stringError
                        )
                    return
                    
#check for double quotes, and backslash with double quotes; 
# use backslash to denote special character
            if '\\\"' in outputFileContents:
                outputFileContents = outputFileContents.replace('\\\"','\\\\\\"')
            elif '\"' in outputFileContents:
                outputFileContents = outputFileContents.replace('\"','\\\"')
            else:
                pass
                
# print output file
#            print('\noutputFileContents:\n%s\n' % outputFileContents)
            
            if DEBUG:
                print(
                    '\n\n***** contents of "outputFileContents:\n%s\n',outputFileContents
                    )
        
# collect in list the data to send to mysql table; 26 elements in all
# ... these MUST match database table fields!!
            data2send = []
# system data                                           datatype    length
            data2send.append(user)                  #1  char        20
            data2send.append(testerNameFirst)       #2  char        255
            data2send.append(testerNameLast)        #3  char        255
            data2send.append(currentDirectory)      #4  char        60
            data2send.append(hostName)              #5  char        20
# REQUIRED: machine on which executable was run
            data2send.append(machineForExecutable)  #6  char        25
            data2send.append(day_number_since_01jan2011)             #7  int         5
            data2send.append(dayofweek)             #8  char        3
            data2send.append(month)                 #9  char        3
            data2send.append(dayofmonth)            #10 int         2
            data2send.append(year)                  #11 int         6
            data2send.append(dateOfLastSend)        #12 char        15
            data2send.append(timeOfLastSend)        #13 char        15
# input file, dir, and content
            data2send.append(inputFile)             #14 char        50
            data2send.append(inputFileDir)          #15 char        60
            data2send.append(inputFileContents)     #16 text
# REQUIRED: output file, dir, and content
            data2send.append(outputFile)            #17 char        50
            data2send.append(outputFileDir)         #18 char        60
            data2send.append(outputFileContents)    #19 text
#  make file, dir, and content      
            data2send.append(makeFile)              #20 char        50
            data2send.append(makeFileDir)           #21 char        60
            data2send.append(makeFileContents)      #22 text
# source file, dir, and content
            data2send.append(sourceFile)            #23 char        50
            data2send.append(sourceFileDir)         #24 char        60
            data2send.append(sourceFileContents)    #25 text
# executable file and dir (binary content will not be stored)
            data2send.append(executableFile)        #26 char        50
            data2send.append(executableFileDir)     #27 char        60
# qsub file, dir, and content
            data2send.append(qsubFile)              #28 char        50
            data2send.append(qsubFileDir)           #29 char        60
            data2send.append(qsubFileContents)      #30 text
# compile line
            data2send.append(compileLine)           #31 char        200
# execute line
            data2send.append(executeLine)           #32 char        200
# user comments
            data2send.append(userComments)          #33 text
        
# ERROR CHECKING
            '''
# ... make sure OUTPUT file is defined -- this is the minimum needed to run Co-PylotDB
            if outputFile == '':
                stringNoOutputFile = (
                    'No OUTPUT file has been specified\n\n' +
                    'An OUTPUT must be specified for this program to run.\n\n' +
                    'Specify an OUTPUT file and try again.'
                    )
                print stringNoOutputFile
                showinfo(
                    'Error: no OUTPUT file specified',
                    stringNoOutputFile
                    )
                return
            '''
            
# ... make sure database and table have been specified
            stringNoDatabaseOrTable = ''
            if myDatabase.strip() == '' or myTable.strip() == '':
                stringNoDatabaseOrTable += 'Correct the following:\n\n'
                if myDatabase == '':
                    stringNoDatabaseOrTable += '  > Database has not been specified.\n\n'
                if myTable == '':
                    stringNoDatabaseOrTable += '  > Table has not been specified.\n\n'
                stringNoDatabaseOrTable += 'Use main window to select missing value(s) and try again.'
                stringNoDatabaseOrTable += (
                    '\n\nIf database server is not accessible, try saving the MySQL\n' + 
                    '  command to a file, then moving that file to a machine from which\n' +
                    '  the database server is accessible. PylotDB can then be used to read \n' +
                    '  the command and insert the data into a selected database table\n' +
                    '  using the "READ MySQL COMMAND FILE" button. This button is available\n' +
                    '  when the target database table is displayed.'
                    )
                print( '\n' + stringNoDatabaseOrTable)
                showinfo(
                    'Error: missing value(s)',
                    stringNoDatabaseOrTable
                    )
                return
                
# ... end of ERROR CHECKING
            
# ... make sure table has enough fields to handle input; if not, table does not match INSERT command
            commandDescribe = (
                'DESCRIBE %s.%s' % (myDatabase, myTable)
                )
            self.cursorHandleMySQL.execute(commandDescribe)
            tableStructure = self.cursorHandleMySQL.fetchall()
            if DEBUG_SHOWMYSQLCOMMAND:
                print('tableStructure = \n')
                print tableStructure
            numfieldsTable = len(tableStructure)
            if DEBUG_SHOWMYSQLCOMMAND:
                print(
                    '\nNumber of fields in table %s: %s' % 
                    (myTable,numfieldsTable)
                    )
                
            numfieldsData2Send = len(data2send)
            
            if DEBUG_SHOWMYSQLCOMMAND:
                print(
                    'Number of data fields (including auto_index) to send to table "%s": %s ' %
                    (myTable, numfieldsData2Send)
                    )
            
# check if data fields + 1 (for auto_index) is greater than number of fields available
            if numfieldsData2Send > numfieldsTable:
                stringMismatch = (
                    '\nNumber of data fields is greater than number of\n' +
                    'table fields, indicating a mismatch between data\n' + 
                    'and table, or the wrong table has been selected.\n\n' +
                    'Verify table and data and try again.'
                    )
                print stringMismatch
                showinfo(
                    'Error: data/table mismatch',
                    stringMismatch
                    )
                return        

# check to make sure connection to database is still valid
            self.checkMySQLConnection()
            if self.connectionFlag == 0:
                stringNotConnected = (
                    'Connection to the database has been broken.\n\n' +
                    'Login to database server and try again.'
                    )
                print stringNotConnected
                showinfo(
                    'Error: not connected',
                    stringNotConnected
                    )
                return

# --- END OF ERROR CHECKING

# form MySQL command
# ... start @ line 10736 in module_accessMySQL.py
            '''
            stringUseDatabase = (
                'USE' + ' ' + database
                )
            self.cursorHandleMySQL.execute(stringUseDatabase)
            '''            
        
# insert co-pylotdb data into database table
# ... use following form to enable INSERT of data into select columns; this is needed when
# ...   adding data to an existing table with more fields than the original created for
# ...   co-pylotdb and the auto-index column field location is not field #29
# ... form first part of command
            self.myMySQLCommand = (
                'INSERT INTO ' + myDatabase + '.' + myTable + 
                ' (' +
                'user,' +                       # 1
                'tester_name_first,' +          # 2
                'tester_name_last,' +           # 3
                'current_dir,' +                # 4
                'host_name,' +                  # 5
                'target_machine,' +             # 6
                'day_number_since_01jan2011,' + # 7
                'day_of_week,' +                # 8
                'month,' +                      # 9
                'day_of_month,' +               # 10
                'year,' +                       # 11
                'date_of_last_send,' +          # 12
                'time_of_last_send,' +          # 13
                'input_file_name,' +            # 14
                'input_file_dir,' +             # 15
                'input_file_contents,' +        # 16
                'output_file_name,' +           # 17
                'output_file_dir,' +            # 18
                'output_file_contents,' +       # 19
                'makefile_name,' +              # 20
                'makefile_dir,' +               # 21
                'makefile_contents,' +          # 22
                'source_file_name,' +           # 23
                'source_file_dir,' +            # 24
                'source_file_contents,' +       # 25
                'executable_file_name,' +       # 26
                'executable_file_dir,' +        # 27
                'qsub_file_name,' +             # 28
                'qsub_file_dir,' +              # 29
                'qsub_file_contents,' +         # 30
                'compile_line,' +               # 31
                'execute_line,' +               # 32
                'user_comments'                 # 33
                ')' +
                ' VALUES ('
                )

# ... form format of insert command
            for numField in range(numfieldsData2Send):
# without auto_index
#            if numField < numfieldsData2Send - 1:
# with auto_index
# ... write all data to first fields in table
                if numField < numfieldsData2Send - 1:
                    self.myMySQLCommand += "(\"" + str(data2send[numField]) + "\")" + ', '
                    if DEBUG_SHOWMYSQLCOMMAND:
                        print(
                            '\n' + str(numField + 1) + ". " + "\"" + str(data2send[numField]) + "\""   
                            )
                else:
# if last row of last command, do NOT include end comma
#                    if numrow < (len(rangeLenAllOutputFiles) - 1):
#                        self.myMySQLCommand += "(\"" + data2send[numField] + "\")" + ' )\','
 #                   else:
                    self.myMySQLCommand += "(\"" + str(data2send[numField]) + "\")" + " )" 
                    if DEBUG_SHOWMYSQLCOMMAND:
                        print( 
                            '\n' + str(numField + 1) + ". " + "\"" + str(data2send[numField]) + "\"\n\n"
                            )
                    
# OLD WAY
                '''
# ... if there are more fields in table than data, use commas with empty fields to specify
                elif (numField >= numfieldsData2Send - 1) and (numField < numfieldsTable - 2):
                    self.myMySQLCommand += ', '
# ... write auto index in last field always; each table in PylotDB will have the last field designated as 'auto_index' to have at least one unique field                   
                else:
#                    command += "\"" + str(data2send[numField]) + "\")"
#                    print '\n' + str(numField) + ". " + "\"" + str(data2send[numField])
                    self.myMySQLCommand += "auto_index" + ')'
                    print '\n' + str(numField + 1) + ". " + "\"auto_index\n\n"
                '''

# see the whole command
            if DEBUG_SHOWMYSQLCOMMAND:
                print ' \nself.myMySQLCommand =',self.myMySQLCommand       
                print
            
            try:
#                i=1
                self.cursorHandleMySQL.execute(self.myMySQLCommand)
            except:
                insertErrorString = (
                    'Not able to insert data into database.\n\n' +
                    'Check INSERT command for mismatch errors with table.\n\n' + 
                    'INSERT process halted.\n\n'
                    )
                    
                print ' >>Error: ' + insertErrorString
                showinfo(
                    'Error: not able to insert data',
                    insertErrorString,
                    parent=self.frameParent
                    )
                return
#            else:
#                print ' ... skipping line #',line
        stringSuccess = (
            'Co-PYLOT data export SUCCESSFUL.\n\n' + 
            'Number of rows added to table: ' + str(len(allOutputFiles)) + '\n\n'
            )
        print('\n' + stringSuccess)
        showinfo(
            'Success: data inserted',
            stringSuccess
            )

        return
        
        
    def handlerSaveMySQLCommand(self):
        '''
        Purpose: 
            saves the assembled MySQL command to a file so that
            the file can be transferred to another machine from
            which PylotDB can execute the command to insert the data
            into a selected database table.
            
            At this point, then, the targeted database and table
            will not have been specified. These parameters will
            be specified in PylotDB.
        ''' 
        if DEBUG_PRINTMETHODNAME:
            print('\n** In handlerSaveMySQLCommand')
        
# error checks
# ... 1. check for entries in required fields
        entryOutputFile = self.scrolledtextOutputFile.get().strip()
        entryMachineForExecutable = self.varMachineOnWhichExecutableWasRun.get().strip()
        stringNoEntry = ''
        if entryOutputFile == '': # or entryMachineForExecutable == '':
            if entryOutputFile == '':
                stringNoEntry += (
                    '\n> No entry in field for "OUTPUT file".\n\n' +
                    'This is a REQUIRED field.\n\n' +
                    'Specify an output file and try again.\n'
                    )
            '''        
            if entryMachineForExecutable == '':
                stringNoEntry += (
                    '\n> No entry in field "Machine on which executable was run".\n\n' +
                    'This is a REQUIRED field.\n\n' +
                    'Specify a machine name and try again.'
                    )
            '''                            
        if stringNoEntry <> '':
            print stringNoEntry
            showinfo(
                'Error: no entry',
                stringNoEntry
                )
            return
            
# ... 2. if 'all files that begin with' is chosen, the first few chars
#       specified in this field MUST match the same first few chars in
#       the entry in 'OUTPUT file'
        stringErrorMatchingFirstFewCharacters = ''
        lengthBeginWith = len(self.varEntry_ThatBeginWith.get())
        lengthOutputFile = len(self.scrolledtextOutputFile.get())
        if lengthOutputFile > lengthBeginWith:
            firstCharsOutputFile = self.scrolledtextOutputFile.get()[0:lengthBeginWith]
        else:
            firstCharsOutputFile = self.scrolledtextOutputFile.get()[0:lengthOutputFile]
            
        if self.varRadiobutton_ProcessFiles.get() == 'that_begin_with':
# make sure length of first few characters is <= entry in 'OUTPUT file'
            if lengthBeginWith > lengthOutputFile:
                stringErrorMatchingFirstFewCharacters = (
                    'The length of the entry for "all files that begin with"\n' +
                    'is greater than the length for the "OUTPUT file".\n\n' +
                    'Shorten the entry for the "all files that begin with" field or\n' +
                    'select another OUTPUT file and try again.'
                    )
# make sure lengthBeginWith > 0
            elif lengthBeginWith == 0:
                stringErrorMatchingFirstFewCharacters = (
                    'There is no entry in the field "all files that begin with".\n\n' +
                    'The characters in this field must match the corresponding\n' +
                    'characters for the "OUTPUT file" entry.\n\n' +
                    'Specify the characters to match and try again.'
                    )
# make sure first few chars match in both entry fields
            elif self.varEntry_ThatBeginWith.get() <> firstCharsOutputFile:
                stringErrorMatchingFirstFewCharacters = (
                    'The characters in the field "all files that begin with"\n' +
                    'must match the same number of characters in the "OUTPUT file" field.\n\n' +
                    'Specify a new OUTPUT file or modify the entry for the first\n' +
                    'few characters to match the OUTPUT file, and try again.'
                    )
            else:
                pass
                
        if stringErrorMatchingFirstFewCharacters <> '':
            print stringErrorMatchingFirstFewCharacters
            showinfo(
                'Error: char mismatch',
                stringErrorMatchingFirstFewCharacters
                )
            return
            
# ----- end of error checks -----
        
        
        user = self.varEntryUser.get()
        currentDirectory = self.varEntryDirectory.get()
        hostName = self.varEntryHostName.get()
#        date = self.varEntryDate.get()

# set params to empty
        inputFile = ''
        inputFileDir = ''
        inputFileContents = ''
        outputFile = ''
        outputFileDir = ''
        outputFileContents = ''
        makeFile = ''
        makeFileDir = ''
        makeFileContents = ''
        sourceFile = ''
        sourceFileDir = ''
        sourceFileContents = ''
        executableFile = ''
        executableFileDir = ''
        machineForExecutable = ''
        testerNameFirst = ''
        testerNameLast = ''
        qsubFile = ''
        qsubFileDir = ''
        qsubFileContents = ''
        compileLine = ''
        executeLine = ''
        userComments = ''
        
# get user, current directory, hostname
        user = self.varEntryUser.get()
        currentDirectory = self.varEntryDirectory.get()
        hostName = self.varEntryHostName.get()
#        date = self.varEntryDate.get()
        
# update date and time before sending to table
        date = time.ctime(time.time())[4:10] + ' ' + time.ctime(time.time())[20:24]
        month = time.ctime(time.time())[4:7]
        dayofweek = time.ctime(time.time())[0:3]
        dayofmonth = time.ctime(time.time())[8:10]
        year = time.ctime(time.time())[20:24]        

        dateOfLastSend = year + '/' + self.dictMonth[month] + '/' + dayofmonth
        timeOfLastSend = time.ctime(time.time())[11:19]
        
        timeStartDate = (2011,1,1,0,0,0,5,1,0)
        timeStartDateSinceEpoch_Seconds = time.mktime(timeStartDate)
        timeNow_Seconds = time.time()
        timeNowSinceStartDate_Days = \
            (timeNow_Seconds - timeStartDateSinceEpoch_Seconds)/3600./24. + 1
        day_number_since_01jan2011 = int(timeNowSinceStartDate_Days)
# input file
#        inputFile = self.varInputFile.get().strip()
        inputFile = self.entryInputFile.getvalue().strip()
        inputFileDir = self.entryInputFileDirectory.getvalue().strip()
        inputFileContents = self.fileInput.strip()
# output file(s)        
        outputFile = self.scrolledtextOutputFile.getvalue().strip()
        outputFileDir = self.scrolledtextOutputFileDirectory.getvalue().strip()
#        outputFileContents = self.fileOutput.strip()
# make file       
        makeFile = self.entryMakeFile.getvalue().strip()
        makeFileDir = self.entryMakeFileDirectory.getvalue().strip()
        makeFileContents = self.fileMake.strip()
# source file      
        sourceFile = self.entrySourceFile.getvalue().strip()
        sourceFileDir = self.entrySourceFileDirectory.getvalue().strip()
        sourceFileContents = self.fileSource.strip()
# executable file
        executableFile = self.entryExecutableFile.getvalue().strip()
        executableFileDir = self.entryExecutableFileDirectory.getvalue().strip()
# machine on which executable was run
        machineForExecutable = self.varMachineOnWhichExecutableWasRun.get().strip()
# tester name first
        testerNameFirst = self.varEntryTesterName_First.get().lower().strip()
# tester name last
        testerNameLast = self.varEntryTesterName_Last.get().lower().strip()
# qsub file
        qsubFile = self.entryQsubFile.getvalue().strip()
        qsubFileDir = self.entryQsubFileDirectory.getvalue().strip()
        qsubFileContents = self.fileQsub.strip()
# compile line        
        compileLine = self.entryCompileLine.getvalue().strip()
# execute line
        executeLine = self.entryExecuteLine.getvalue().strip()
# user comments        
        userComments = self.scrolledtextUserComment.getvalue().strip()
# ... no double quotes allowed!
        userComments = userComments.replace('"',"'")
        
# display time of this send in main window
        self.varEntryTime.set(
            timeOfLastSend
            )
        self.varEntryDate.set(
            dateOfLastSend
            )

# define myDatabase and myTable using ghost values that will be replaced when file is read into PylotDB
#        myDatabase = self.comboboxDbSelect.get()
#        myTable = self.comboboxDbTableSelect.get()
        myDatabase = 'XXDATABASE'
        myTable = 'YYTABLE'

        batchProcess = self.varRadiobutton_ProcessFiles.get()
        allOutputFiles = []
# get directory; important to strip off trailing white space
        allDirectory = self.scrolledtextOutputFileDirectory.getvalue().strip()
        
# process following files

# ... just this file
        if batchProcess == 'just_this_file':
            splitOutputFile = self.scrolledtextOutputFile.getvalue().split('.')
            outputFileExtension = splitOutputFile[len(splitOutputFile)-1].strip()          
            allOutputFiles.append(self.filepathOutput)
            
# ... with this extension
        elif batchProcess == 'with_this_extension':            
# get filename extension; important to strip off trailing white space
            splitOutputFile = self.scrolledtextOutputFile.getvalue().split('.')
            outputFileExtension = splitOutputFile[len(splitOutputFile)-1].strip()
# use glob.glob to get list of files using above extension and directory
            filesLocation = allDirectory + '/*.' + outputFileExtension
            allOutputFiles = glob.glob(filesLocation)
            
# ... that begin with
        elif batchProcess == 'that_begin_with':
# use glob.glob to get list of files using above directory
            fileBeginsWith = self.varEntry_ThatBeginWith.get().strip()
# check that entry field for fileBeginsWith is not empty
            if fileBeginsWith == '':
                stringEmptyBeginsWith = (
                    'The entry field for this option is empty.\n\n' +
                    'Specify the desired beginning letters and/or numbers\n' +
                    'in the entry field and try again.'
                    )
                print stringEmptyBeginsWith
                showinfo(
                    'Error: empty entry field',
                    stringEmptyBeginsWith
                    )
                return
            filesLocation = allDirectory + '/' + fileBeginsWith + '*.*'
            allOutputFiles = glob.glob(filesLocation)
            
# ... contains the phrase
        elif batchProcess == 'contains_the_phrase':
# use glob.glob to get list of files using above directory
            fileContainsThePhrase = self.varEntry_ContainsThePhrase.get().strip()
            if DEBUG_CONTAINS_THE_PHRASE:
                print('\nfileContainsThePhrase = %s' % fileContainsThePhrase)
            
# check that entry field for fileContains is not empty
            if fileContainsThePhrase == '':
                stringEmptyContainsThePhrase = (
                    'The entry field for this option is empty.\n\n' +
                    'Specify the desired phrase to match in the\n' +
                    'entry field and try again.'
                    )
                print stringEmptyContainsThePhrase
                showinfo(
                    'Error: empty entry field',
                    stringEmptyContainsThePhrase
                    )
                return
            filesLocation = allDirectory + '/*' + fileContainsThePhrase + '*.*'
            allOutputFiles = glob.glob(filesLocation)
            if DEBUG_CONTAINS_THE_PHRASE:
                print('allOutputFiles = ')
                print(allOutputFiles)
                print('\n> For files containing the phrase %s:' % fileContainsThePhrase)
                icount = 0
                for file in allOutputFiles:
                    if file <> '':
                        icount += 1
                        print('%s. %s' % (icount, file))
                print()
            
# ... all files in this directory
        elif batchProcess == 'in_this_directory':
# use glob.glob to get list of files using above directory
            filesLocation = allDirectory + '/*.*'
            allOutputFiles = glob.glob(filesLocation)
# ... failure
        else:
            stringErrorProcess = (
                'The attribute "batchProcess" must equal one of the following:\n\n' +
                ' > "just_this_file"\n' +
                ' > "with_this_extension"\n' +
                ' > "that_begin_with"\n' +
                ' > "contains_the_phrase"\n' +
                ' > "in_this_directory"\n\n' +
                'Current value: %s\n\n' +
                'This represents a coding error. Contact code administrator.'
                ) % batchProcess
            print stringErrorProcess
            showinfo(
                'Error: batchProcess',
                stringErrorProcess
                )
            return
            
        if DEBUG_SAVEMYSQLCOMMAND:
            print '\nallOutputFiles =\n', allOutputFiles
        
# ERROR check
# 

# print all variables
        stringPrintAllVariables = (
        '----- VARIABLES TO SEND TO DATABASE TABLE -----\n' +
        'user = %s\n' +
        'testerNameFirst = %s\n' + 
        'testerNameLast = %s\n' + 
        'currentDirectory = %s\n' + 
        'hostName = %s\n' + 
        'machineForExecutable = %s\n' + 
        'day_number_since_01jan2011 = %s\n' + 
        'dayofweek = %s\n' +
        'mont/h = %s\n' +
        'dayofmonth = %s\n' +
        'year = %s\n' +
        'dateOfLastSend = %s\n' + 
        'timeOfLastSend = %s\n' +
        'inputFile = %s\n' + 
        'inputFileDir = %s\n' + 
        'outputFile = %s\n' + 
        'outputFileDir = %s\n' +             
        'makeFile = %s\n' + 
        'makeFileDir = %s\n' + 
        'sourceFile = %s\n' + 
        'sourceFileDir = %s\n' + 
        'executableFile = %s\n' + 
        'executableFileDir = %s\n' + 
        'qsubFile = %s\n' + 
        'qsubFileDir = %s\n' + 
        'compileLine = %s\n' + 
        'executeLine = %s\n' + 
        'userComments = %s\n' + 
        'myDatabase = %s\n' + 
        'myTable = %s\n' +
        'allOutputFiles = %s'
        )%(
        user,
        testerNameFirst,
        testerNameLast,
        currentDirectory,
        hostName,
        machineForExecutable,
        day_number_since_01jan2011,
        dayofweek,
        month,
        dayofmonth,
        year,
        dateOfLastSend,
        timeOfLastSend,
        inputFile,
        inputFileDir,
        outputFile,
        outputFileDir,
        makeFile,
        makeFileDir,
        sourceFile,
        sourceFileDir,
        executableFile,
        executableFileDir,
        qsubFile,
        qsubFileDir,
        compileLine,
        executeLine,
        userComments,
        myDatabase,
        myTable,
        allOutputFiles
        )
        
        if DEBUG_SAVEMYSQLCOMMAND:
            print(stringPrintAllVariables)
        
        saveMySQLCommand = []

# if no output file specified, say so and return 
        if DEBUG_SAVEMYSQLCOMMAND:
            print '>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<'
            print 'allOutputFiles =',allOutputFiles
            print 'len() =',len(allOutputFiles)
            print 'self.scrolledtextOutputFile.getvalue() =',self.scrolledtextOutputFile.getvalue()
            print 'len() =',len(self.scrolledtextOutputFile.getvalue())

        if allOutputFiles[0] == '':
            stringNoOutputFile = (
                'Specify an OUTPUT file'
                )
            showinfo(
                'Error: no OUTPUT file (save)',
                stringNoOutputFile
                )
            return
      
        rangeLenAllOutputFiles = []
        rangeLenAllOutputFiles = range(len(allOutputFiles))
        
        if DEBUG_SAVEMYSQLCOMMAND:
            print('\n***** len(allOutputFiles) = %s' % len(allOutputFiles))
                
        for numrow in rangeLenAllOutputFiles:
# separate directory from filename
            outputFileDir, outputFile = os.path.split(allOutputFiles[numrow])
            if DEBUG_SAVEMYSQLCOMMAND:
                print '\noutputFile =',outputFile
                print 'outputFileDir =',outputFileDir
                print('allOutputFiles[%s] = %s' % (numrow, allOutputFiles[numrow]))
# read file contents as one string
            try:
                outputFileContents = open(allOutputFiles[numrow],'r').read()
            except:
                if allOutputFiles[numrow] == '':
                    stringError = (
                        'OUTPUT file must be specified.'
                        )
                    print stringError
                    showinfo(
                        'Error: OUTPUT file (save)',
                        stringError
                        )
                    return
                else:
                    stringError = (
                        'Cannot read the OUTPUT file\n\n' +
                        '%s\n\n'
                        ) % (allOutputFiles[numrow])
                    print stringError
                    showinfo(
                        'Error: OUTPUT file (save)',
                        stringError
                        )
                return
            
            if DEBUG_SAVEMYSQLCOMMAND:
                print 'contents of fileOutput =\n',outputFileContents
        
# collect in list the data to send to mysql table; 26 elements in all
# ... these MUST match database table fields!!
            data2send = []
# system data                                           datatype    length
            data2send.append(user)                  #1  char        20
            data2send.append(testerNameFirst)       #2  char        255
            data2send.append(testerNameLast)        #3  char        255
            data2send.append(currentDirectory)      #4  char        60
            data2send.append(hostName)              #5  char        20
# REQUIRED: machine on which executable was run
            data2send.append(machineForExecutable)  #6  char        25
            data2send.append(day_number_since_01jan2011)             #7  int         5
            data2send.append(dayofweek)             #8  char        3
            data2send.append(month)                 #9  char        3
            data2send.append(dayofmonth)            #10 int         2
            data2send.append(year)                  #11 int         6
            data2send.append(dateOfLastSend)        #12 char        15
            data2send.append(timeOfLastSend)        #13 char        15
# input file, dir, and content
            data2send.append(inputFile)             #14 char        50
            data2send.append(inputFileDir)          #15 char        60
            data2send.append(inputFileContents)     #16 text
# REQUIRED: output file, dir, and content
            data2send.append(outputFile)            #17 char        50
            data2send.append(outputFileDir)         #18 char        60
            data2send.append(outputFileContents)    #19 text
#  make file, dir, and content      
            data2send.append(makeFile)              #20 char        50
            data2send.append(makeFileDir)           #21 char        60
            data2send.append(makeFileContents)      #22 text
# source file, dir, and content
            data2send.append(sourceFile)            #23 char        50
            data2send.append(sourceFileDir)         #24 char        60
            data2send.append(sourceFileContents)    #25 text
# executable file and dir (binary content will not be stored)
            data2send.append(executableFile)        #26 char        50
            data2send.append(executableFileDir)     #27 char        60
# qsub file, dir, and content
            data2send.append(qsubFile)              #28 char        50
            data2send.append(qsubFileDir)           #29 char        60
            data2send.append(qsubFileContents)      #30 text
# compile line
            data2send.append(compileLine)           #31 char        200
# execute line
            data2send.append(executeLine)           #32 char        200
# user comments
            data2send.append(userComments)          #33 text
        
# ERROR CHECKING
# ... make sure OUTPUT file is defined -- this is the minimum needed to run Co-PylotDB
            if outputFile == '':
                stringNoOutputFile = (
                    'No OUTPUT file has been specified\n\n' +
                    'An OUTPUT must be specified for this program to run.\n\n' +
                    'Specify an OUTPUT file and try again.'
                    )
                print stringNoOutputFile
                showinfo(
                    'Error: no OUTPUT file specified',
                    stringNoOutputFile
                    )
                return

                
            numfieldsData2Send = len(data2send)
            
            if DEBUG_SAVEMYSQLCOMMAND:
                print(
                    'Number of data fields (no auto_index included here) to send: %s ' %
                    (numfieldsData2Send)
                    )             

# --- END OF ERROR CHECKING

# form MySQL command
# ... start @ line 10736 in module_accessMySQL.py
            '''
            stringUseDatabase = (
                'USE' + ' ' + database
                )
            self.cursorHandleMySQL.execute(stringUseDatabase)
            '''            
        
# insert co-pylotdb data into database table
# ... form first part of command
            self.myMySQLCommand = (
                'INSERT INTO ' + myDatabase + '.' + myTable + 
                ' (' +
                'user,' +                       # 1
                'tester_name_first,' +          # 2
                'tester_name_last,' +           # 3
                'current_dir,' +                # 4
                'host_name,' +                  # 5
                'target_machine,' +             # 6
                'day_number_since_01jan2011,' + # 7
                'day_of_week,' +                # 8
                'month,' +                      # 9
                'day_of_month,' +               # 10
                'year,' +                       # 11
                'date_of_last_send,' +          # 12
                'time_of_last_send,' +          # 13
                'input_file_name,' +            # 14
                'input_file_dir,' +             # 15
                'input_file_contents,' +        # 16
                'output_file_name,' +           # 17
                'output_file_dir,' +            # 18
                'output_file_contents,' +       # 19
                'makefile_name,' +              # 20
                'makefile_dir,' +               # 21
                'makefile_contents,' +          # 22
                'source_file_name,' +           # 23
                'source_file_dir,' +            # 24
                'source_file_contents,' +       # 25
                'executable_file_name,' +       # 26
                'executable_file_dir,' +        # 27
                'qsub_file_name,' +             # 28
                'qsub_file_dir,' +              # 29
                'qsub_file_contents,' +         # 30
                'compile_line,' +               # 31
                'execute_line,' +               # 32
                'user_comments' +               # 33
                ')' +
                ' VALUES ('
                )

# ... form format of insert command
            for numField in range(numfieldsData2Send):
# without auto_index
#            if numField < numfieldsData2Send - 1:
# with auto_index
# ... write all data to first fields in table

                if numField < numfieldsData2Send - 1:
                    self.myMySQLCommand += "(\"" + str(data2send[numField]) + "\")" + ', '
                    if DEBUG_SAVEMYSQLCOMMAND:
                        print(
                            '\n' + str(numField + 1) + ". " + "\"" + str(data2send[numField]) + "\""
                            )
                else:
# if last row of last command, do NOT include end comma
#                    if numrow < (len(rangeLenAllOutputFiles) - 1):
#                        self.myMySQLCommand += "(\"" + data2send[numField] + "\")" + ' )\','
 #                   else:
                    self.myMySQLCommand += "(\"" + str(data2send[numField]) + "\")" + " )" 
                    if DEBUG_SAVEMYSQLCOMMAND:
                        print( 
                            '\n' + str(numField + 1) + ". " + "\"" + str(data2send[numField]) + "\"\n\n"
                            )

# see the whole command
            if DEBUG_SAVEMYSQLCOMMAND:
                print(' \n***** self.myMySQLCommand =\n%s\n\n' % (self.myMySQLCommand))       
            
# add command to list of lists
            saveMySQLCommand.append([self.myMySQLCommand])
            
            if DEBUG_SAVEMYSQLCOMMAND:
                print '\nbefore success, saveMySQLCommand =\n', saveMySQLCommand

# write entire command to a file; use extension 'cop', short for co-pylot
        success = self.saveMySQLCommandToFileUsingCPickle(saveMySQLCommand)
        
        if DEBUG_SAVEMYSQLCOMMAND:
            print('\n***** success = %s' % success)
#
        if success:
            stringSuccess = (
                'Co-PYLOT data successfully saved to file\n\n' +
                '"' + self.filenameMySQLOutputFile + '"\n\n'
                'Number of MySQL INSERT commands saved to file: ' + str(len(allOutputFiles))
                )
            print('\n' + stringSuccess)
            showinfo(
                'Success: data inserted',
                stringSuccess
                )

        return


    def mysql_ComboDatabases(self):
        '''
        graph combobox for DATABASES
        
        Inputs: 
            self.myDatabases
            
        Outputs:
            self.comboboxDbSelect(.set()/.get())  
            self.varDbTotal(.set()/.get())
            
        '''

# top label
        labelDbSelect = Label(
            self.frameMySQL_31_00,
            text='DATABASES\n(select to show Tables ->)',
            bg=self.colorbg,
            )
        labelDbSelect.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=0,
            pady=2,
            )
# combobox            
        self.comboboxDbSelect = Pmw.ComboBox(
            self.frameMySQL_31_00,
            scrolledlist_items=self.myDatabases,
            dropdown=0,
            entry_state='disabled',
            entry_disabledbackground='white',
            entry_disabledforeground='black',
            selectioncommand=self.handler_ComboDatabases,
            scrolledlist_hull_width=500
            )
        self.comboboxDbSelect.grid(
            row=1,
            column=0,
            columnspan=2,
            pady=2,
            )
        self.comboboxDbSelect.component('scrolledlist').configure(
            hscrollmode='static'
            )
        self.comboboxDbSelect.component('scrolledlist').configure(
            vscrollmode='static'
            )
# could also have used...
#        self.comboboxDbSelect.configure(scrolledlist_hscrollmode = 'static')
#        self.comboboxDbSelect.configure(scrolledlist_vscrollmode = 'static')
        
# 'total' label               
        labelDbTotal = Label(
            self.frameMySQL_31_00,
            text='Databases: ',
            bg=self.colorbg,
            )
        labelDbTotal.grid(
            row=2,
            column=0,
            pady=2,
            sticky=E,
            )
            
# 'entry' for total # of databases            
        self.varDbTotal=StringVar()
        self.varDbTotal.set(len(self.myDatabases))
        self.entryDbTotal = Entry(
            self.frameMySQL_31_00,
            bg=self.colorbg,
            relief=FLAT,
            textvariable=self.varDbTotal,
            width=5,
            )
        self.entryDbTotal.grid(
            row=2,
            column=1,
            pady=2,
            sticky=W,
            )
            
    def mysql_ComboDatabaseTables(self):
        '''
        graph combobox for DATABASE TABLES
        
        Inputs: 
            self.myDatabaseTables
            
        Outputs:
            self.comboboxDbTableSelect(.set()/.get())
            self.varDbTablesTotal(.set()/.get())
            
        '''
        if DEBUG_PRINTMETHODNAME:
            print( 
                '\n** In mysql_ComboDatabaseTables\n'
                )

# ... top label
        labelTables = Label(
            self.frameMySQL_32_00,
            text='TABLES IN DATABASE\n(select target table)',
            bg=self.colorbg,
            )
        labelTables.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=0,
            pady=2,
            )
# ... combobox for Database TABLES               
        self.comboboxDbTableSelect = Pmw.ComboBox(
            self.frameMySQL_32_00,
            scrolledlist_items=self.myDatabaseTables,
            dropdown=0,
            entry_state='disabled',
            entry_disabledbackground='white',
            entry_disabledforeground='black',
            selectioncommand=self.handler_ComboDatabaseTables,
            scrolledlist_hull_width=500
            )
        self.comboboxDbTableSelect.grid(
            row=1,
            column=0,
            columnspan=2,
            pady=2,
            )
# ... affix scrollbars
        self.comboboxDbTableSelect.configure(scrolledlist_hscrollmode = 'static')
        self.comboboxDbTableSelect.configure(scrolledlist_vscrollmode = 'static')

# ... label for total            
        labelDbTablesTotal = Label(
            self.frameMySQL_32_00,
            text='Tables: ',
            bg=self.colorbg,
            )
        labelDbTablesTotal.grid(
            row=2,
            column=0,
            pady=2,
            sticky=E,
            )
# ... total # of tables          
        self.varDbTablesTotal = StringVar()
        self.varDbTablesTotal.set(len(self.myDatabaseTables))
        self.entryDbTablesTotal = Entry(
            self.frameMySQL_32_00,
            bg=self.colorbg,
            relief=FLAT,
            textvariable=self.varDbTablesTotal,
            width=5,
            )
        self.entryDbTablesTotal.grid(
            row=2,
            column=1,
            pady=2,
            sticky=W,
            ) 
            
        return

            
    def clearDbTables(self):
        '''
        reset Tables combobox and totals
        '''

# clear Tables combobox
        self.comboboxDbTableSelect.clear()
# reset total to zero
        self.varDbTablesTotal.set(0)
        
    def methodRadiobutton_ThatBeginWith(self):
        '''
        Purpose:
            fill entry field with first 5 letters of 'Output file' filename if
            filename is greater than 5 characters; otherwise, fill entry field
            with entire filename which is 5 chars or less.
            
            User can always add other chars, but the first letters must always 
            match the first letters in the entry for OUTPUT file, as checked for
        
        Called by:
            def handlerBrowseForOutputFile
        '''
        if DEBUG_PRINTMETHODNAME:
            print('\n\n** In handlerRadiobutton_ThatBeginWith\n')
            
        filename = self.scrolledtextOutputFile.get().strip()
        fnNoExtension, extension = os.path.splitext(filename)
        outputfileEntry = self.scrolledtextOutputFile.get()
        if DEBUG:
            print('  > fnNoExtension = %s' % fnNoExtension)
            print('  > extension = %s' % extension)
#        entryMachineForExecutable = self.varMachineOnWhichExecutableWasRun.get().strip()
        stringNoOutputFile = ''
        if fnNoExtension == '': 
            stringNoOutputFile += (
                '\n> No entry in field for "OUTPUT file".\n\n' +
                'This is a REQUIRED field and must be selected first.\n\n' +
                'Select an output file and try again.\n'
                )
            print(stringNoOutputFile)
            showinfo(
                'Error: no OUTPUT file',
                stringNoOutputFile
                )
            return
            
        length = self.lengthBeginningFileNameLettersToMatch
        if DEBUG:
            print('length = %s' % length)
        if len(fnNoExtension) > length:
            firstCharactersOfFileName = fnNoExtension[0:length]
            if DEBUG:
                print('firstCharactersOfFileName = %s' % firstCharactersOfFileName)
            self.varEntry_ThatBeginWith.set(firstCharactersOfFileName)
        elif len(outputfileEntry) == 0:
            stringNoOutputFile = (
                'No output file has been selected.\n\n' +
                'Select an output file and try again.'
                )
            print(stringNoOutputFile)
            showinfo(
                'Error: no output file',
                stringNoOutputFile
                )
            return 1 # no output file selected
        else:
# fnNoExtension is less than length, so just output fnNoExtension
            if DEBUG:
                print('else: fnNoExtension = %s' % fnNoExtension)
            self.varEntry_ThatBeginWith.set(fnNoExtension)
        
        return 0
        
        
    def handlerRadiobutton_ContainsThePhrase(self):
        '''
        Purpose:
            checks for errors:
                1. OUTPUT file must be specified before 
                    this option is selected
                2. phrase must be specified before this 
                    option is selected
                3. matching phrase must match somewhere
                    in the OUTPUT file; if not, select
                    another OUTPUT file or enter another
                    phrase
            
        Called by:
            createWidgets
        '''
        if DEBUG_PRINTMETHODNAME:
            print('\n\n** In handlerRadiobutton_ContainsThePhrase\n')
        
# zero out the entry
        self.radiobutton_ContainsThePhrase.configure(
            text=('all 00/00 files that contain the phrase')
            )
        
        nameOutputFile = self.scrolledtextOutputFile.get().strip()
        phrase = self.varEntry_ContainsThePhrase.get().strip()

# ----- error checks
# if OUTPUT file field is empty, say so and return
        stringError = ''
        if nameOutputFile == '':
            stringError = (
                'No OUTPUT file has been selected.\n\n' +
                'An OUTPUT file must be selected before this\n' +
                'option can be selected.\n\n' +
                'Select an OUTPUT file and try again.'
                )
            print(stringError)
            showinfo(
                'Error: no OUTPUT file',
                stringError
                )
            self.radiobutton_ContainsThePhrase.deselect()
            return


# if the phrase field is empty, say so and return
        stringError = ''
        if phrase == '':
            stringError = (
                'No phrase has been entered.\n\n' +
                'Enter a phrase before selecting this option,\n' +
                'and try again.'
                )
            print(stringError)
            showinfo(
                'Error: no phrase',
                stringError
                )
            self.radiobutton_ContainsThePhrase.deselect()
            return

# phrase must match something in the specified "OUTPUT file"
        stringError = ''
        if phrase not in nameOutputFile:
            stringError = (
                'The phrase is not part of the current OUTPUT file,\n' +
                'even though it may be contained in a file in the directory.'
                'The phrase must be part of the current OUTPUT filename to\n' +
                'ensure a valid phrase has been entered.\n\n' +
                'Select another OUTPUT file that has the given phrase, or\n' +
                'make sure the phrase is found in the selected OUTPUT file.\n\n' +
                'Enter a proper phrase or select another OUTPUT file\n' +
                'and try again.'
                )
            print(stringError)
            showinfo(
                'Error: no phrase',
                stringError
                )
            self.radiobutton_ContainsThePhrase.deselect()
            return
            
# ----- end of error checks

# total number of files in directory

# calculate number of files that have a matching phrase
        dirname, filename = os.path.split(self.filepathOutput)
#        dirname = self.scrolledtextOutputFileDirectory.get()
        numberOfFilesAffected_ContainsThePhrase = 0
        numberOfFilesTotal = 0
        for myfile in os.listdir(dirname):
            numberOfFilesTotal += 1
            if phrase in myfile:
                numberOfFilesAffected_ContainsThePhrase += 1
                
        if numberOfFilesAffected_ContainsThePhrase <> 0:
            self.radiobutton_ContainsThePhrase.configure(
            text=('all %s/%s files that contain the phrase' %
            (numberOfFilesAffected_ContainsThePhrase,numberOfFilesTotal) )
            )
        return
        
        
    def handlerClearMachineOnWhichExecutableWasRun(self):
        '''
        Purpose:
            clear the entry field for 'Machine on which executable was run'
        '''
        self.varMachineOnWhichExecutableWasRun.set('')

    def refreshTables(self):
        '''
        Purpose:
            refresh tables list            
        '''

# check if connected to a MySQL server
        self.checkMySQLConnection()
        if self.connectionFlag == 0: return           
        
# define current database
        myDatabase = self.comboboxDbSelect.get().lstrip()
        if not myDatabase:
            showinfo(
                'Error: no database specified',
                '\nNo database has been specified. Please\n' +
                'select a database and try again.\n\n'
                )
            return
        
#        self.cursorHandleMySQL.execute('USE' + ' ' + myDatabase)

# clear table list
        self.myDatabaseTables = []
# get database tables
        if DEBUG:
            print(
                'self.cursorHandleMySQL.execute("SHOW TABLES FROM ' + myDatabase + '")'
                )
        start = time.time()
        self.cursorHandleMySQL.execute("SHOW TABLES FROM " + myDatabase)
        tables = self.cursorHandleMySQL.fetchall()
        finish = time.time()
        delta_t = finish - start
        if DEBUG:
            print(
                '  (Time: %-7.4f secs)' % delta_t
                )

        i=0
        for table in tables:
            i+=1
            self.myDatabaseTables.append(table[0]) 
            
        self.myDatabaseTables.sort()
              
        return  

    def checkMySQLConnection_fromMainWindow(self):
        '''
        checks connection to MySQL server from Main Window
        
        '''
        if DEBUG_PRINTMETHODNAME:
            print(
                '** In module_accessMySQL/checkMySQLConnection_fromMainWindow'
                )
        
# check if connected to a MySQL server
        self.connectionFlag = 1
#        if not self.myDbConnection:
# try any always-true command; if valid, we are still connected       
        try:
            self.cursorHandleMySQL.execute('show engines')
        except:
            self.connectionFlag = 0
        return  

    def mysql_GetDatabases(self):
        '''
        gets list of databases from MySQL server
        
        inputs:
            
        outputs:
            self.myDatabases
        '''
# clear database list
        self.myDatabases = []
# get databases
        if DEBUG:
            print(
                'self.cursorHandleMySQL.execute("SHOW DATABASES")'
                )
        start=time.time()
        self.cursorHandleMySQL.execute("SHOW DATABASES")
        databases = self.cursorHandleMySQL.fetchall()
        finish=time.time()
        delta_t = finish - start
        if DEBUG:
            print(
                '  (Time: %-7.4f secs)' % delta_t
                )
        if DEBUG:
            print(
                'MySQL Databases:'
                )
        i=0
        printString=''
        for database in databases:
            i+=1
            printString+=('%2s. ' % i  + database[0] + '\n')
# assemble string for combobox
            self.myDatabases.append(database[0]) 
            
        self.myDatabases.sort()
        
        if DEBUG:
            print(
                printString
                )
            
            
    def mysql_GetDatabaseTables(self):
        '''
        gets list of database tables from MySQL server
        
        inputs:
            
        outputs:
            self.myDatabaseTables
        '''
# get current database
        databaseCurrent = self.comboboxDbSelect.get().lstrip()
        if databaseCurrent == '' or databaseCurrent == None:
            print(
                'No database has been specified.'
                )
            showinfo(
                'Error: no database',
                'No database has been chosen for this\n' +
                'operation.\n\n' +
                'Please choose a database.'
                )
            return
        for database in self.myDatabases:
            if database == databaseCurrent:
                self.refreshTables()
                return
                
# if we get this far, no database match
        print(
            '\nDatabase is not in current list.'
            )
        showinfo(
            'Error: database does not exist.',
            'The database for which you are trying to generate\n' +
            'a table does not exist in the current list of\n' +
            'databases.\n\n' +
            'Please create the database before trying to add\n' +
            'a table to it.'
            )
            
        return
        
    def checkMySQLConnection(self):
        '''
        checks connection to MySQL server and switches STATUS lights
            depending on status
            
        Connection indicators:
            self.checkbuttonStatusDbNotConnected.configure(state='normal')
            self.checkbuttonStatusDbAttemptConnect.configure(state='disabled')
            self.checkbuttonStatusDbConnected.configure(state='disabled')
        
        '''
        if DEBUG_PRINTMETHODNAME:
            print('** In module_accessMySQL/checkMySQLConnection')
        
# check if connected to a MySQL server
        self.connectionFlag = 1
#        if not self.myDbConnection:
# try any always-true command; if valid, we are still connected       
        try:
            self.cursorHandleMySQL.execute('show engines')
        except:
            self.checkbuttonStatusDbNotConnected.configure(state='normal')
            self.checkbuttonStatusDbAttemptConnect.configure(state='disabled')
            self.checkbuttonStatusDbConnected.configure(state='disabled')
            print(
                'Not connected to database server!'
                )
            showinfo(
                'Error: not connected',
                'No connection to a database server.\n'
                )
            self.connectionFlag = 0
            return

        return
                
        

# ============= HANDLERS ===============================

    def handlerClearExecutableFile(self):
        '''
        Purpose:
            clear the file and dir enries for the EXECUTABLE file
        '''
        if DEBUG_PRINTMETHODNAME:
            print('\nClear Executable file and directory entries')
        self.entryExecutableFile.setvalue('')
        self.entryExecutableFileDirectory.setvalue('')
        return
        
    def handlerClearQsubFile(self):
        '''
        Purpose:
            clear the file and dir entries for the QSUB file
        '''
        if DEBUG_PRINTMETHODNAME:
            print('\nClear Qsub file and directory entries')
        self.entryQsubFile.setvalue('')
        self.entryQsubFileDirectory.setvalue('')
        self.fileQsub = ''
        
    def handlerClearInputFile(self):
        '''
        Purpose:
            clear the file and dir entries for the INPUT file
        '''
        if DEBUG_PRINTMETHODNAME:
            print('\nClear input file and directory entries')
#        self.varInputFile.set('')
        self.entryInputFile.setvalue('')
        self.entryInputFileDirectory.setvalue('')  
        self.fileInput = ''
        return
    
    def handlerClearOutputFile(self):
        '''
        Purpose:
            clear the file and dir entries for the OUTPUT file;
            also clear the entry field for 'all files that begin with'
        '''
        if DEBUG_PRINTMETHODNAME:
            print('\nClear OUTPUT file and directory entries')
#        self.varOutputFile.set('')
        self.scrolledtextOutputFile.setvalue('')
        self.scrolledtextOutputFileDirectory.setvalue('')
        self.filepathOutput = ''
        self.varEntry_ThatBeginWith.set('')
        self.varEntry_ContainsThePhrase.set('')
        self.varEntry_WithThisExtension.set('')
        self.radiobutton_WithThisExtension.configure(
            text=('all 00/00 files with this extension')
            )
        self.radiobutton_ThatBeginWith.configure(
            text=('all 00/00 files that begin with')
            )
        self.radiobutton_ContainsThePhrase.configure(
            text=('all 00/00 files that contain the phrase')
            )
        self.radiobutton_InThisDirectory.configure(
            text=('all 0 files in this directory')
            )
        
        return

    def handlerClearMakeFile(self):
        '''
        Purpose:
            clear the file and dir entries for the MAKE file
        '''
        if DEBUG_PRINTMETHODNAME:
            print('\nClear MAKE file and directory entries')
#        self.varMakeFile.set('')
        self.entryMakeFile.setvalue('')
        self.entryMakeFileDirectory.setvalue('') 
        self.fileMake = ''
        return

    def handlerClearSourceFile(self):
        '''
        Purpose:
            clear the file and dir entries for the SOURCE file
        '''
        if DEBUG_PRINTMETHODNAME:
            print('\nClear SOURCE file and directory entries')
            
#        self.varSourceFile.set('')
        self.entrySourceFile.setvalue('')
        self.entrySourceFileDirectory.setvalue('') 
        self.fileSource = ''
        return
        
    def handlerClearCompileLine(self):
        '''
        Purpose:
            clear compile line
        '''
        if DEBUG_PRINTMETHODNAME:
            print('\nClear COMPILE line entry')
        self.entryCompileLine.setvalue('')
        return
        
    def handlerClearExecuteLine(self):
        '''
        Purpose:
            clear execute line
        '''
        if DEBUG_PRINTMETHODNAME:
            print('\nClear EXECUTE line entry')
        self.entryExecuteLine.setvalue('')
        return
    
    def handlerClearUserComment(self):
        '''
        Purpose:
            clear 'User comments' text box
        '''
        ans = askokcancel(
            'Clear text...',
            'Clear the text box?\n'
            )
        if ans:
            self.scrolledtextUserComment.clear()
        
        return
        

    def handlerConnectAfterPassword(self, event):
        '''
        Purpose:
            Connect to MySQL server after entering password just by
        hitting Enter
        '''
        self.buttonConnectToMySQL.invoke()
        
        return
                
            
    def handler_ComboDatabases(self, myDatabase):
        '''
        handles selection from DATABASE combobox
        '''        
# get the current selection for Database
        self.use_Database = myDatabase
        
# clear Tables and total
        self.clearDbTables()
# refresh table list
        self.refreshTables() 
            
# show tables in Tables combobox
        self.mysql_ComboDatabaseTables()
                
        return
        
    def handlerResetValuesMySQL(self):
        '''
        reset MySQL server values
        
        Inputs:
            
        '''
        if DEBUG_PRINTMETHODNAME:
            print('** In handlerResetValuesMySQL')

# clear password            
        self.varPasswordMySQL.set('')

# arbitrarily select server to display
        self.comboServerMySQL.selectitem(self.servers[0])
        
# pick port
        if self.co-pylotDotConf_Exists:
            self.varPortMySQL.set(
                self.portForRemoteServer
                )
        else:
            self.varPortMySQL.set('3306')
        
# pick username based on selected server
        if self.comboServerMySQL.get().strip() == 'localhost':
#            self.varUserMySQL.set('root')
            self.varUserMySQL.set(self.usernameForLocalServer)
        else:
            self.varUserMySQL.set(self.usernameForRemoteServer)
        
        return
        
                
    def handlerClearValuesMySQL(self):
        '''
        reset MySQL server values
        
        Inputs:
            
        '''
        if DEBUG_PRINTMETHODNAME:
            print('** In handlerClearValuesMySQL')
# use if fields are to be cleared        
        self.varUserMySQL.set('')
        self.varPasswordMySQL.set('')
        self.comboServerMySQL.setentry('')
        self.varPortMySQL.set('')
        
        return
        
    def handlerMySQLConnect(self):
        '''
        connects to MySQL server and extracts database names
        
        Inputs:
            username:   self.varUserMySQL
            password:   self.varPasswordMySQL
            server:     self.comboServerMySQL
            port:       self.varPortMySQL
            
            Databases and Tables lists:
                self.myDatabases
                self.myDatabaseTables

        Connection indicators:
            self.checkbuttonStatusDbNotConnected.configure(state='normal')
            self.checkbuttonStatusDbAttemptConnect.configure(state='disabled')
            self.checkbuttonStatusDbConnected.configure(state='disabled')
            
        '''
            
        self.checkMySQLConnection_fromMainWindow()
            
        if self.connectionFlag:
            stringConnected = (
                'You are already connected to a MySQL server.\n\n' +
                'Disconnect first, then connect to desired server.'
                )
            showinfo(
                'Info: connected',
                stringConnected
                )
# clear password field
            self.varPasswordMySQL.set('')
            return
        
        self.checkbuttonStatusDbNotConnected.configure(state='disabled')
        self.checkbuttonStatusDbAttemptConnect.configure(state='normal')
        self.checkbuttonStatusDbConnected.configure(state='disabled')    
        
# check if all values are present
        un=self.varUserMySQL.get()
        pw=self.varPasswordMySQL.get()
        svr=self.comboServerMySQL.get()
        prt=self.varPortMySQL.get()
        
        valuePresent=1
        valueString=''
        
        if un == '':
            valuePresent=0
            print(
                ' Username is blank.'
                )
            valueString=' Username is blank\n'
        if pw == '':
            valuePresent=0
            print(
                ' Password is blank.'
                )
            valueString+=' Password is blank.\n'
        if svr == '':
            valuePresent=0
            print(
                ' Server is not specified.'
                )
            valueString+=' Server is not specified.\n'
        if prt == '':
            valuePresent=0
            print(
                ' Port is blank; try 3306'
                )
            valueString+=' Port is blank.\n'
        
        if not valuePresent:
            print(
                ' Following errors occurred:\n' + valueString
                )
            showinfo(
            'ERROR in input',
            'Please correct the following errors:\n\n' +
            valueString
            )
            self.checkbuttonStatusDbNotConnected.configure(state='normal')
            self.checkbuttonStatusDbAttemptConnect.configure(state='disabled')
            
            self.checkbuttonStatusDbConnected.configure(state='disabled')   
            return
        
        if DEBUG:
            print(
                '     user = ' + un + '\n' +
                '     host = ' + svr + '\n' +
                '     port = ' + prt 
                )
                   
# now connect to server
        try:
            self.myDbConnection = MySQLdb.connect(
                user=un,
                passwd=pw,
                host=svr,
                port=eval(prt)
                )            
        except:
            stringErrorServerNotAvailable = (
                'Could not connect to database.\n\n' + 
                'Possible reasons:\n' +
                '  - Invalid username, password, or server name\n' +
                '  - Check if "Caps Lock" has been pressed\n' +
                '  - Server timeout (log back in)\n' +
                '  - Server not available at this time\n\n' +
                'Check input fields and try again.'
                )
            print(
                stringErrorServerNotAvailable
                )
            showinfo(
                'ERROR',
                stringErrorServerNotAvailable
                )
            self.checkbuttonStatusDbNotConnected.configure(state='normal')
            self.checkbuttonStatusDbAttemptConnect.configure(state='disabled')
            self.checkbuttonStatusDbConnected.configure(state='disabled') 
            return    

# At this point, connection is successful
        if DEBUG:
            print(
                ' Connected to MySQL database\n'
                )
# ... show status indicators
        self.checkbuttonStatusDbNotConnected.configure(state='disabled')
        self.checkbuttonStatusDbAttemptConnect.configure(state='disabled')
        self.checkbuttonStatusDbConnected.configure(state='normal')
        
# store values  for use in inserting data into database
        self._userMySQL_Save = un
        self._passwdMySQL_Save = pw
        self._hostMySQL_Save = svr
        self._portMySQL_Save = prt
        
# reset password field for security purposes
        self.varPasswordMySQL.set('')

# get a cursor handle for executing SQL commands
        self.cursorHandleMySQL = self.myDbConnection.cursor()
# turn on autocommit; else, database will not update when you want
        self.cursorHandleMySQL.execute("set autocommit = 1")     
# get database list
        self.mysql_GetDatabases()
        
# graph combobox for Databases
        self.mysql_ComboDatabases()
        
        return
        
    def handlerMySQLDisconnect(self):
        '''
        disconnects from MySQL database
        '''
# check if connected to a MySQL server
        self.checkMySQLConnection()
        if self.connectionFlag == 0: return
        
        ans=askokcancel(
            'Disconnect...',
            'You are about to disconnect\n' +
            'from the MySQL database.\n\n' + 
            'Click OK to continue, or CANCEL to\n' +
            'quit this process.'
            )
        if ans:
            try:
                self.myDbConnection.close()  
                
            except:
                showinfo(
                    'Info...',
                    'No database is opened.'
                    )
                return
                
            print(
                '\nDisconnected from MySQL database.'
                )
        else:
            print(
                'Disconnect process canceled.'
                )
            return
            
# clear 'Select a Database' combobox
        if DEBUG_PRINTDISCONNECT:
            print(
                '\nClearing all combo boxes...'
                )
        self.comboboxDbSelect.clear()
        self.comboboxDbTableSelect.clear()
        
# reset password
        if DEBUG_PRINTDISCONNECT:
            print(
                '\nReset password field.'
                )
        self.varPasswordMySQL.set('')
        
# reset totals
        if DEBUG_PRINTDISCONNECT:
            print(
                '\nReset totals.'
                )
        self.varDbTotal.set(0)
        self.varDbTablesTotal.set(0)

# set indicators
        if DEBUG_PRINTDISCONNECT:
            print(
                '\nReset Status indicators.'
                )
        self.checkbuttonStatusDbNotConnected.configure(state='normal')
        self.checkbuttonStatusDbAttemptConnect.configure(state='disabled')
        self.checkbuttonStatusDbConnected.configure(state='disabled')
        
# set server connection to false  
        if DEBUG_PRINTDISCONNECT:
            print(
                'Set server connection to false.'
                )
        self.myDbConnection = 0
        
        return
                
    def handler_ComboDatabaseTables(self, myTable):
        '''
        handles selection from TABLES combobox
        '''
        
# get the current selection for Database
#        self.use_Database = self.comboboxDbSelect.get()
#        print '  ... use database:',self.use_Database
        
# get the current selection for Database
        self.use_DatabaseTable = myTable
        if DEBUG:
            print(
                '  ... use database table:' + self.use_DatabaseTable
                )
        
# if 'Table Functions' window exists, refresh the 'Table:' field
        try:
            mapped = self.toplevelTableFunctions.winfo_exists()
        except:
            mapped = False 

        if mapped:            
            self.varEntrySelectTable.set(
                self.comboboxDbTableSelect.get().lstrip()
                ) 

        return
        
        
    def saveMySQLCommandToFileUsingCPickle(self, saveContents):
        '''
        Purpose:
            Search for and select the output file for
            the MySQL commands; to be read in to PylotDB and
            executed so that the data is inserted into the
            selected database table
        '''
        if DEBUG_PRINTMETHODNAME:
            print('\n** In saveMySQLCommandToFileUsingCPickle **')
        
        if DEBUG:
            print('\nsaveContents:\n%s' % (saveContents))
# define dictionary of options for askopenfilename()
        options = {}
        options = {
#            'defaultextension' : '.',
            'defaultextension' : '.cop',
#            'filetypes' : [('Comma-Separated Values','.csv'),('All files','.*')],
            'filetypes' : [('cop','.cop')],  # ,('All files','*')
#            'initialdir' : '.',
#            'initialdir' : self.initialDir,
            'initialdir' : os.getcwd(),
            'initialfile' : '',
            'parent' : self.frameParent,
            'title' : 'Save MySQL command to file'
            } 
            
# full filepath
        try:
            self.filepathMySQLCommandOutput = tkFileDialog.asksaveasfilename(**options)
        except:
            stringError = (
                'Cannot save file for the MySQL commands'
                )
            print stringError
            showinfo(
                'Error saving file',
                stringError
                )
            return 0
# split into directory name and filename
        dirname, self.filenameMySQLOutputFile = os.path.split(self.filepathMySQLCommandOutput)

# Error check            
        if self.filenameMySQLOutputFile == '':
            print '   No output filename chosen!'
            '''
            showinfo(
                'No output filename chosen...',
                'You must enter a filename for the file to be read'
                )
            '''
            return 0
        else:
            if DEBUG:
                print '\n    Output dirname =',dirname
                print '    Output filename =',self.filenameMySQLOutputFile
# end of Error check

# open the file 
        try:
            outFile = open(self.filepathMySQLCommandOutput,'w')
        except:
            errorOutFileOpen = (
                'Could not open the output file\n\n' +
                self.filenameMySQLOutputFile + '\n\n' +
                'in directory\n\n' + 
                dirname
                )
            print(errorOutFile)
            showinfo(
                'Error: cannot open file',
                errorOutFile
                )
            return 0
# create a pickler object
        objectPickler = cPickle.Pickler(outFile)

# write file
        try:
# write lines to file (NOT the way to do this and preserve the object to be written!!)
#            outFile.writelines(saveContents)
# pickle data to the file; to read back in with PylotDB, use 'load' instead of 'dump';  
            objectPickler.dump(saveContents)
        except:
            errorOutFileWrite = (
                'Could not write the MySQL command file\n\n' + 
                self.filenameMySQLOutputFile + '\n\n' +
                'to directory\n\n' +
                dirname
                )
            print(errorOutFileWrite)
            showinfo(
                'Error: cannot write file',
                errorOutFileWrite
                )
            return 0
            
# close the file; always good practice
        outFile.close()
            
        return 1
        
        
# ======= threads handlers =========

    def threadSendUsage_Co_PylotDB(threadName,*vars):
        '''
        Purpose:
        store usage stats in a database table
        '''
        
        if DEBUG_THREAD_STATS:
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
        day_number_since_01jan2011 = vars[7]
        dayOfWeek = vars[8]
        month = vars[9]
        dayOfMonth = vars[10]
        year = vars[11]
        time = vars[12]
        hostName = vars[13]
        co_pylotdb_stats_server_valid = vars[14]
        co_pylotdb_stats_server_username = vars[15]
        co_pylotdb_stats_server_password = vars[16]
        co_pylotdb_stats_server = vars[17]
        co_pylotdb_stats_server_port = vars[18]
        co_pylotdb_stats_database = vars[19]
        co_pylotdb_stats_table = vars[20]

# connect to stats server
        myDbConnection_Track_Co_PylotDB = ''
        if co_pylotdb_stats_server_valid:
            try:
                myDbConnection_Track_Co_PylotDB = MySQLdb.connect(
                    user=co_pylotdb_stats_server_username,
                    passwd=co_pylotdb_stats_server_password,
                    host=co_pylotdb_stats_server,
                    port=co_pylotdb_stats_server_port
                    )
            except:
                if DEBUG_THREAD_STATS:
                    stringNoConnect = (
                        'Cannot connect to Co_PylotDB stats database due to invalid\n' +
                        'values in the co-pylotdb.conf file.'
                        )
                    print('\n' + stringNoConnect)
                    return        
        else:
# if values are not valid for server, just return and continue;
#   we don't want co-pylotdb stopped just because we can't capture stats
            if DEBUG_THREAD_STATS:
                stringNoConnect = (
                    'Cannot connect to Co-PylotDB stats database due to blank\n' +
                    'or missing values in the co-pylotdb.conf file.'
                    )
                print('\n' + stringNoConnect)
            return
            
# ... if value is still blank, just return
        if myDbConnection_Track_Co_PylotDB == '':
            stringNoConnect2 = (
                'Cannot connect to Co-PylotDB stats database.\n' +
                ' Value for "myDbConnection_Track_Co_PylotDB" is blank.\n' +
                ' Check "co_pylotdb_stats..." values in co-pylotdb.conf'
                )
            print('\n' + stringNoConnect2 + '\n')
            return
            
# ... if we make it this far, connection to stats database and table is good
        stringConnectSuccess = (
            'Connected to Co-PylotDB stats database server: %s'
            ) % (
                co_pylotdb_stats_server
                )
        print('\n' +stringConnectSuccess)
            
# get a cursor handle for executing SQL commands
        cursorHandleMySQL_Track_Co_PylotDB = myDbConnection_Track_Co_PylotDB.cursor()
# turn on autocommit; else, database will not update when you want
        cursorHandleMySQL_Track_Co_PylotDB.execute("set autocommit = 1")  
        
# check for stats database; if it does not exist, create it
        statDatabases = []
        try:
            cursorHandleMySQL_Track_Co_PylotDB.execute("SHOW DATABASES")
            statDatabases = cursorHandleMySQL_Track_Co_PylotDB.fetchall() # tuple of tuples
            statDatabases_List = [item[0] for item in statDatabases]
        except:
            stringCannotShowDatabases = (
                'Unable to "SHOW DATABASES" for Co-PylotDB stats.'
                )
            print('\n' + stringCannotShowDatabases)
            myDbConnection_Track_Co_PylotDB.close()
            return
            
        if DEBUG_THREAD_STATS:
            print('\nCo-PylotDB statDatabases_List:')
            print(statDatabases_List)
            
        if co_pylotdb_stats_database not in statDatabases_List:
            stringCreateDatabase = "CREATE DATABASE " + co_pylotdb_stats_database
            if DEBUG_THREAD_STATS:
                print('\nstringCreateDatabase = %s' % stringCreateDatabase)
                print('\nco_pylotdb_stats_database = %s' % co_pylotdb_stats_database)
                print('\nstatDatabases = ')
                print(statDatabases)
            
            try:
                cursorHandleMySQL_Track_Co_PylotDB.execute(stringCreateDatabase)
            except:
                stringCannotCreateStatsDatabase = (
                    'Unable to create Co-PylotDB stats database\n' +
                    '   %s\n' 
                    ) % (
                        co_pylotdb_stats_database
                        )
                print('\n' + stringCannotCreateStatsDatabase)
                myDbConnection_Track_Co_PylotDB.close()
                return
# 
            stringSuccess_CreateStatsDatabase = (
                'Created Co-PylotDB stats database: %s'
                ) % (
                co_pylotdb_stats_database
                )
            print('\n' + stringSuccess_CreateStatsDatabase)
            
# check for stats database table; if it does not exist, create it
        statDatabaseTables = []
        tableStats_DatabaseDotTable = co_pylotdb_stats_database + '.' + co_pylotdb_stats_table
        
        try:
            cursorHandleMySQL_Track_Co_PylotDB.execute(
                "SHOW TABLES FROM " + co_pylotdb_stats_database
                )
            statDatabaseTables = cursorHandleMySQL_Track_Co_PylotDB.fetchall()
            statDatabase_Tables_List = [item[0] for item in statDatabaseTables]
            if DEBUG_THREAD_STATS:
                print('\nCo-PylotDB statDatabaseTables =')
                print(statDatabaseTables)
                print('\nCo-PylotDB statDatabase_Tables_List')
                print(statDatabase_Tables_List)
        except:
                stringCannotCreateStatsDatabase = (
                    'Unable to "SHOW TABLES" from Co-PylotDB stats database.' 
                    ) 
                print('\n' + stringCannotCreateStatsDatabase)
                myDbConnection_Track_Co_PylotDB.close()
                return
                
        if co_pylotdb_stats_table not in statDatabase_Tables_List:
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
            
            if DEBUG_THREAD_STATS:
                print('Co-PylotDB commandCreateTable = \n')
                print(commandCreateTable)
            
            try:
                cursorHandleMySQL_Track_Co_PylotDB.execute(commandCreateTable)
            except:
                stringCannotCreateStatsTable = (
                    'Unable to create Co-PylotDB stats table\n' +
                    '   %s\n' 
                    ) % (
                        co_pylotdb_stats_table
                        )
                print('\n' + stringCannotCreateStatsTable)
                myDbConnection_Track_Co_PylotDB.close()
                return   

            stringSuccess_CreateStatsTable = (
                'Created Co-PylotDB stats table: %s'
                ) % (
                co_pylotdb_stats_table
                )
            print('\n' + stringSuccess_CreateStatsTable)

# insert data into database
        if DEBUG_THREAD_STATS:
            print(' >>>>> INSERTing into Co-PylotDB stats table')
        stringInsert = (
            "INSERT INTO " + 
            co_pylotdb_stats_database + 
            "." + 
            co_pylotdb_stats_table +
            " (user,name_first,name_last,code,python_version,os,os_name," +
            "day_number_since_01jan2011,day_of_week,month,day_of_month,year,time,host_name)" +                      
            " VALUES" +
            " ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," +
            " '%s')"  
            ) % (
            userName,
            name_first,
            name_last,
            codeName,
            versionPython,
            operatingSystem,
            osName,
            day_number_since_01jan2011,
            dayOfWeek,
            month,
            dayOfMonth,
            year,
            time,
            hostName
            )
            
        if DEBUG_THREAD_STATS:
            print('\n' + stringInsert)
            
        try:
            cursorHandleMySQL_Track_Co_PylotDB.execute(
                stringInsert
                )
        except:
            if DEBUG_THREAD_STATS:
                currentModule = 'co-pylotdb.py'
                currentMethod = 'threadSendUsage_Co_PylotDB'
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
                    co_pylotdb_stats_database,
                    co_pylotdb_stats_table,
                    currentModule,
                    currentMethod
                    )
                print('\n' + stringDatabaseProblem)   
            return
            
# disconnect from database server
        if DEBUG_THREAD_STATS:
            print(' >>>>> closing Co-PylotDB stats server connection\n')
            
        print('\nCo-PylotDB stats submitted')
        
        stringFlushPrivileges = (
            'FLUSH PRIVILEGES'
            )
        cursorHandleMySQL_Track_Co_PylotDB.execute(stringFlushPrivileges)
        
        myDbConnection_Track_Co_PylotDB.close()
        
        return                        
        
# ======================= main ============================ # 
if __name__ == '__main__':
    root = Tk()
    root.geometry(
        '+%d+%d' % (x_Windows, y_Windows) 
        )
    colorbg = 'gray'
#    colorbg = 'tan'
#    app = AccessMySQL(root,'tan')
    app = AccessMySQL(root,colorbg)
    app.master.title(
       'Co-PylotDB: Transfer user files/data to MySQL database table'
        )
    app.master.configure(
#        bg='tan',
        bg=colorbg
        )
    app.mainloop()      
            