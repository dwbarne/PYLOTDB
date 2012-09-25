##!/usr/bin/python # do not use; use my local Python which
#                     has proper libraries installed

# Filename: module_emailParser.py
#
# Methods:
# 1. parse                          parses a MIME email
# 2. send2db                        sends parsed info to a database
# 3. email2user                     sends status email back to sender
# 4. trackUsage                     sends info to database to keep track of users
# 5. readConfigureFileForEcoPylot   reads parameters from user-modified input file
# 6. mySQLConnect                   connects to database; sets up cursor

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


# ===== global imports =====
# ... python modules
import sys                                      # retrieves command line arguments;
                                                #   do NOT use < or > to redirect input or output
import re                                       # regular expressions
from email.mime.multipart import MIMEMultipart  # to handler web-based email msgs using MIME
import base64                                   # for decoding attachments sent in base64
from email.parser import Parser                 # for parsing emails
import platform                                 # for system characteristics
import os                                       # "
import sys                                      # "
import time                                     # for time calculations
import yaml                                     # for reading in eco_pylot.conf configure file
import MySQLdb                                  # for accessing database server
# ... external modules
stringCannotImport = ''
try:
    import MySQLdb                              # for MySQL database access
except:
    stringCannotImport += (
        '- Cannot import MySQLdb for accessing MySQL databases:\n' +
        '  http://sourceforge.net/projects/mysql-python\n\n'
        )
    
if stringCannotImport <> '':
    print(
        '\nError: import problem',
        stringCannotImport +
        'Install missing module(s).\n\n' +
        'PYLOT must exit.\n\n'
        )
    sys.exit()

# ===== end of global imports =====

# ===== global constants =====
# ... name of this module
MODULE = 'module_emailParser.py'
DEBUG_MODULES = 1                               # prints which module is being executed
DEBUG_PRINT_EMAIL = 1                           # prints email msg
DEBUG_PRINT_OUTPUT = 1                          # prints general output
DEBUG_PYLOT_CONF_FILE = 1                       # prints debug info when reading conf file
DEBUG_YAML_INPUT_FILE = 1                       # prints YAML input file parameters
DEBUG_PRINT_METHOD = 1                          # print name of method currently executing
PRINT_STATS = 1                                 # print output for usage

# ===== end of global constants =====

# = = = = = = = = = = = =  class EmailParser = = = = = = = = = = = = = 

class EmailParser():
    def __init__(
        self, 
        msg, 
        eco_pylot_dot_conf_file, 
        eco_pylot_dot_conf_template_file
        ):
    
        self.msg = msg
        self.location_eco_pylot_dot_conf_file = eco_pylot_dot_conf_file
        self.location_eco_pylot_dot_conf_template_file = eco_pylot_dot_conf_template_file
        
# ===== ERROR CHECK ON self.msg =====

# set default values
#        self.msgOk = True
        self.yamlFileOk = True
# define empty strings for attributes
        self.msgErrorString = ''
        self.hasAttachments = ''
        self.myDatabase = ''
        self.myTable = ''
        mailProtocol = ''
        self.userEmailBody = ''

# error check on email message        
# ... check if msg has any length
        if len(self.msg) == 0:
#            self.msgOk = False
            self.msgErrorString += (
                '\nERROR: length of message is zero.\n' +
                ' No message is available for parsing. This is probably\n' +
                ' a coding error between the calling program and the\n' +
                ' constructor for module "module_emailParser.py".\n\n'
                )
            if DEBUG_PRINT_OUTPUT:
                print('\n' + self.msgErrorString)
            return
            
# ... determine if mail is MIME; if SMTP or UNKNOWN, return
        if(
        self.msg.count('MIME-Version') > 0 
        or 
        self.msg.count('MIME_VERSION') > 0
        or
        self.msg.count('MIME-VERSION') > 0
        ):
            mailProtocol = 'MIME'
        else:
            mailProtocol = 'SMTP or UNKNOWN'
#            self.msgOk = False
            self.msgErrorString += (
                '\nERROR: email protocol is unknown\n' +
                ' Email protocol is SMTP or UNKNOWN. However, eCo-Pylot is\n' +
                ' written for MIME email protocol only.\n\n'
                )
    
        if DEBUG_PRINT_OUTPUT:
            if len(mailProtocol) > 0:
                print('\nProtocol of email: %s\n' % mailProtocol)

# parse email for headers; datatype = dict; if no headers found, we cannot
# determine current user or much of anything else
        try:
            self.headers = Parser().parsestr(self.msg) # creates an instance!
        except:
#            self.msgOk = False
            if len(self.headers) <> 0:
                self.msgErrorString += (
                    '\nERROR: headers could not be properly parsed\n' +
                    ' Email headers could not be properly parsed from the\n' +
                    ' the email message using internal module "email.parser".'
                    )
            else:
                self.msgErrorString += (
                    '\nERROR: headers not found\n' +
                    ' At least one of the typically-found header was not\n' +
                    ' found in the current message.' 
                    )
# can't go on if we don't have header info
            return

# extract username
        userName = self.headers['from'].split(' <')[1].split('@')[0]
            
# open output file; overwritten for each email
# ... provides the latest output for verifying all is working like expected
        self.opsys = sys.platform[:3]    # first 3 characters
        
        if self.opsys == 'win':
            fileName = './tempfileFromParserModuleOnWinPlatform_' + userName + '.out'
        else:
            fileName = './tempfileFromParserModuleOnPosixPlatform_' + userName + '.out'

# open output file; if an error occurs, print it, but don't quit program
        try:
            self.fout = open(fileName,'w') 
        except:
            stringCannotOpenFile = (
                '\nERROR: cannot open file\n' +
                ' Unable to open file\n' +
                '   %s\n' +
                ' Check permissions to write to current directory.'
                ) % (
                fileName
                )
            print(stringCannotOpenFile)

        if self.fout:
# write fileName
            self.fout.write('filename: %s\n\n' % fileName)
#  Now the header items can be accessed as a dictionary:
            self.fout.write('Headers from parsing email:\n')
            self.fout.write('  To: %s\n' % self.headers['to'])
            self.fout.write('  From: %s\n' % self.headers['from'])
            self.fout.write('  Subject: %s\n' % self.headers['subject'])
            self.fout.write('  Date/Time(UTC): %s\n' % self.headers['date'])
            self.fout.write('  Mail protocol: %s\n' % mailProtocol)
        
# extract server name
#        self.myDatabaseServer = self.headers['to'].split('@')[1]
        extractServer = []
        extractServer = re.findall(
#            '"(\w+_\w+@\w+.\w+.\w+)"', self.headers['to']
            '".+@(.+)"', self.headers['to']
            )
        self.myDatabaseServer = extractServer[0]
        if DEBUG_PRINT_OUTPUT:
            print('\nself.headers[\'to\'] = %s' % self.headers['to'])
            print('\nserver = %s' % self.myDatabaseServer)
        
# error check on individual headers:
        if self.headers['subject'] == None or self.headers['subject'] == '':
#            self.msgOk = False
            self.msgErrorString += (
                '\nERROR: no value in field "Subject:"\n' +
                ' This is used to determine the database table name.\n' +
                ' Insert desired table name into the Subject field and try again.'
                )
        else:
            self.myTable = self.headers['subject']
        
#        if not self.msgOk:
#            if self.fout:
#                self.fout.write('\nFAILED:\n%s' % self.msgErrorString)
#            return

# ===== END ERROR CHECK =====

# ... print email
        if DEBUG_PRINT_EMAIL:
            print('\n\n>> email looks like:\n\n%s\n\n' % self.msg)
            
        return  # __init__
        
        
    def readConfigureFileForEcoPylot(self):
        '''
        Purpose:
            read in parameters for database server and tracking server,
            among other things
        '''
        if DEBUG_MODULES:
            print('\n>> in module ' + MODULE + '/readConfigureFileForEcoPylot <<\n')
        
# define servers from conf file it conf file exists;
#  otherwise, default to blank entries and user has to input values
        eco_pylotDotConf_Exists = 0
        
        try:
#            if self.opsys == 'win':
#                eco_pylotDotConf = open('./eco_pylot.conf','r')
#            else:
#                eco_pylotDotConf = open('/home/dwbarne/Parser/Modules/eco_pylot.conf','r')
#            eco_pylotDotConf_Exists = 1
            eco_pylotDotConf = open(self.location_eco_pylot_dot_conf_file,'r')
            eco_pylotDotConf_Exists = 1
        except:
            stringNoConfFile = (
                'Method: readConfigureFileForEcoPylot\n' +
                'The file "eco_pylot.conf" could not be found or cannot be opened.\n\n' +
                '"eco_pylot.conf" allows the user to define parameters like username\n' +
                'and server names that would otherwise need to be manually entered\n' +
                'each time Pylot is run.\n\n' +
                'eco_pylot will generate a generic template, save it as "eco_pylot.conf_template",'
                'and exit. Next, edit the file to define appropriate parameters so these will' +
                'not have to be entered every time eco_pylot is run, then copy the file to\n' +
                '"eco_pylot.conf" in the Modules directory under the directory for "eco_pylot.py"\n' +
                'so that it will be read by "eco_pylot.py" next time it is executed.\n\n' +
                'MAKE SURE PERMISSIONS ARE SET SO NO ONE ELSE BUT OWNER CAN LOOK AT FILE,\n' +
                'AS IT WILL CONTAIN AT LEAST ONE PASSWORD!!' 
                )
#            self.fout.write('\n' + stringNoConfFile + '\n')
            self.msgErrorString += stringNoConfFile
            string_eCo_PylotDotConf_Template = (
                '# file: eco_pylot.conf\n' +
                '# called by: module_emailParser.py\n' +
                '\n' +
                '# COMMENTS\n' +
                '# 1. If not done already, rename this file from "eco_pylot.conf_template"\n' +
                '#    to "eco_pylot.conf" after filling in data below.\n' +
                '# 2. This file is used to define various parameters for eco_pylot.\n' +
                '# 3. File is read in and used as object self.yamlDotLoad[<key>] where <key>\n' +
                '#    is "main_database_servers", for example, to access list of servers.\n' +
                '# 4. Leave database_server info blank unless you want to use localhost db server\n' +
                '# 5. Example of names for common email servers:\n' +
                '#     Gmail: smtp.gmail.com:25\n' +
                '\n' +
                '# DATABASE SERVER (if blank, use values parsed from email\n' +
                'database_server:\n' +
                '    - servername\n' +
                'database_server_username:\n' +
                '    - username\n' +
                'database_server_password:\n' +
                '    - password\n' +
                'database_server_port:\n' +
                '    - 3306\n' +
                '\n' +
                '# TRACKING SERVER\n' +
                'tracking_server:\n' +
                '    - trackingservername\n' +
                'tracking_server_username:\n' +
                '    - username\n' +
                'tracking_server_password:\n' +
                '    - password\n' +
                'tracking_server_port:\n' +
                '    - port_number\n' +
                'tracking_database:\n' +
                '    - database\n' +
                'tracking_database_table:\n' +
                '    - table\n' +
                '\n' +
                '# MAIL SERVER\n' +
                'mail_server:\n' +
                '    - mail.domain\n' +
                'username_for_mail_server:\n' +
                '    - mymailserverusername\n' +
                'password_for_mail_server:\n' +
                '    - mymailserverpasswordifneeded\n' +
                '\n' +
                '# ADMINISTRATOR INFO\n' +
                'code_administrator_name:\n' +
                '    - "firstName lastName"\n' +
                'code_administrator_mail_server:\n' +
                '    - mailserver:port\n' +
                'code_administrator_email:\n' +
                '    - codeadminemailaddress@domain\n'
                )
            stringWriteTemplate = (
                '\nWriting following to "eco_pylot.conf_template" as template\n' +
                'for file "eco_pylot.conf":\n%s\n' 
                )
#            self.fout.write(
            self.msgErrorString += (
                stringWriteTemplate % string_eCo_PylotDotConf_Template
                )
                
            if self.fout:
                self.fout.write(self.msgErrorString)

            self.yamlFileOk = True

            try:
#                if self.opsys == 'win':
#                    fileConf = open('./eco_pylot.conf_template','w')
#                else:
#                    fileConf = open('/home/dwbarne/Parser/Modules/eco_pylot.conf_template','w')
                fileConf = open(self.location_eco_pylot_dot_conf_template_file,'w')
                fileConf.write(string_eCo_PylotDotConf_Template)
                fileConf.close()
            except:
                stringCantOpenConfFile = (
                    'Method: readConfigureFileForEcoPylot\n' +
                    '\nCan\'t open "eco_pylot.conf_template" file to write template.\n\n' +
                    'Likely reason is you don\'t have permission to write\n' +
                    'the file to this directory.\n\n'
                    )
#            self.fout.write('\n' + stringCantOpenConfFile + '\n')
                self.msgErrorString += stringCantOpenConfFile
                self.yamlFileOk = False

            else:
                stringConfFileWritten = (
                    'Method: readConfigureFileForEcoPylot\n' +
                    'A configuration template has been written to file "eco_pylot.conf_template".\n\n' +
                    'Edit this file to fill in data specific to your environment, then\n' +
                    'copy the file to "eco_pylot.conf" which will be read by eco-ylot the next\n' +
                    'the next time it\'s run.\n\n' +
                    'Program exiting'
                    )
#                self.fout.write('\n' + stringConfFileWritten + '\n')
                self.msgErrorString += stringConfFileWritten
                self.yamlFileOk = False
                
            return
                
# pylotDotConf does exist
        if eco_pylotDotConf_Exists:
# ... load YAML input file
            self.yamlDotLoad = yaml.load(eco_pylotDotConf)
            if DEBUG_PYLOT_CONF_FILE:
                print('\nself.yamlDotLoad:\n%s\n' % self.yamlDotLoad)
                
# yaml file parameters for local database
# ... if databaseServer exists, it overides the one read in via email;
# ... this feature is mainly for debugging or trying out new features on a local database
            try:
                self.databaseServerFromConfFile = \
                    str(self.yamlDotLoad['database_server'][0])
            except:
                self.databaseServerFromConfFile = ''
                
            try:
                self.databaseServerUserNameFromConfFile = \
                    str(self.yamlDotLoad['database_server_username'][0])
            except:
                self.databaseServerUserNameFromConfFile = ''
                
            try:
                self.databaseServerPasswordFromConfFile = \
                    str(self.yamlDotLoad['database_server_password'][0])
            except:
                self.databaseServerPasswordFromConfFile = ''
                
# if at least one of the above parameters is not blank but another is, then we 
#   have a conflict in how the logic is to be handles; notify user

            if self.fout:
                self.fout.write('\nFrom method "readConfigureFileFromEcoPylot":\n')
                self.fout.write('   self.databaseServerFromConfFile =\n')
#                self.fout.write(str(type(self.databaseServerFromConfFile)))
                self.fout.write(str(self.databaseServerFromConfFile))
                self.fout.write('\n   self.databaseServerUserNameFromConfFile =\n')
#                self.fout.write(str(type(self.databaseServerUserNameFromConfFile)))
                self.fout.write(str(self.databaseServerUserNameFromConfFile))
                self.fout.write('\n   self.databaseServerPasswordFromConfFile =\n')
#                self.fout.write(str(type(self.databaseServerPasswordFromConfFile)))
                self.fout.write(str(self.databaseServerPasswordFromConfFile))
                self.fout.write('')

            if(
            (self.databaseServerFromConfFile == 'None' or self.databaseServerFromConfFile == '')
            and
            (self.databaseServerUserNameFromConfFile == 'None' or self.databaseServerUserNameFromConfFile == '')
            and
            (self.databaseServerPasswordFromConfFile == 'None' or self.databaseServerPasswordFromConfFile == '')
            ):
                self.useYamlServerValues = False
            elif (
            (self.databaseServerFromConfFile <> 'None' and self.databaseServerFromConfFile <> '')
            and
            (self.databaseServerUserNameFromConfFile <> 'None' and self.databaseServerUserNameFromConfFile <> '')
            and
            (self.databaseServerPasswordFromConfFile <> 'None' and self.databaseServerPasswordFromConfFile <> '')
            ):
                self.useYamlServerValues = True
            else:
# at least one of the database parameters from eco_pylotDotConf file is blank and others are not
                self.yamlFileOk = False
                stringErrorInYamlDotConfFile = (
                    'Method: readConfigureFileForEcoPylot\n' +
                    'At least one of the following values is blank, when either\n' +
                    'all should be blank, indicating database server values are\n' +
                    'taken from email files, or they should all have values, indicating\n' +
                    'database server values are taken from "eco_pylot.conf" file.\n\n' +
                    ' - database_server: %s\n' +
                    ' - database_server_username: %s\n' +
                    ' - database_server_password: %s\n\n' +
                    'Enter valid values in "eco_pylot.conf" and try again.'
                    ) % (
                    self.databaseServerFromConfFile,
                    self.databaseServerUserNameFromConfFile,
                    self.databaseServerPasswordFromConfFile
                    )
                    
                self.msgErrorString += stringErrorInYamlDotConfFile
                return
                
# read in other yaml parameters               
            self.databaseServerPort = self.yamlDotLoad['database_server_port'][0]
# ... tracking server
            self.trackingServer = self.yamlDotLoad['tracking_server'][0]
            self.trackingServerUserName = self.yamlDotLoad['tracking_server_username'][0]
            self.trackingServerPassword = self.yamlDotLoad['tracking_server_password'][0]
            self.trackingServerPort = self.yamlDotLoad['tracking_server_port'][0]
            self.trackingDatabase = self.yamlDotLoad['tracking_database'][0]
            self.trackingDatabaseTable = self.yamlDotLoad['tracking_database_table'][0]
# ... mail server
            self.mailServer = self.yamlDotLoad['mail_server'][0]
            self.usernameForMailServer = self.yamlDotLoad['username_for_mail_server'][0]
            self.passwordForMailServer = self.yamlDotLoad['password_for_mail_server'][0]
# ... admin info
            self.nameForCodeAdministrator = self.yamlDotLoad['code_administrator_name'][0]
            self.mailServerForCodeAdministrator = self.yamlDotLoad['code_administrator_mail_server'][0]
            self.emailAddressForCodeAdministrator = self.yamlDotLoad['code_administrator_email'][0]
             
# write to file
            if DEBUG_YAML_INPUT_FILE and self.fout:
                self.fout.write('\nYAML INPUT FILE PARAMETERS:\n')
                self.fout.write('self.useYamlServerValues = %s\n' % self.useYamlServerValues)
                self.fout.write('  1. self.databaseServerFromConfFile: %s\n' % self.databaseServerFromConfFile)
                self.fout.write('  2. self.databaseServerUserNameFromConfFile: %s\n' % self.databaseServerUserNameFromConfFile)
                self.fout.write('  3. self.databaseServerPasswordFromConfFile: %s\n' % self.databaseServerPasswordFromConfFile)
                self.fout.write('  4. self.databaseServerPort: %s\n' % self.databaseServerPort)
                self.fout.write('  5. self.trackingServer: %s\n' % self.trackingServer)
                self.fout.write('  6. self.trackingServerUserName: %s\n' % self.trackingServerUserName)
                self.fout.write('  7. self.trackingServerPassword: %s\n' % self.trackingServerPassword)
                self.fout.write('  8. self.trackingServerPort: %s\n' % self.trackingServerPort)
                self.fout.write('  9. self.trackingDatabase: %s\n' % self.trackingDatabase)
                self.fout.write(' 10. self.trackingDatabaseTable: %s\n' % self.trackingDatabaseTable)
                self.fout.write(' 11. self.mailServer: %s\n' % self.mailServer)
                self.fout.write(' 12. self.usernameForMailServer: %s\n' % self.usernameForMailServer)
                self.fout.write(' 13. self.passwordForMailServer: %s\n' % self.passwordForMailServer)
                self.fout.write(' 14. self.nameForCodeAdministrator: %s\n' % self.nameForCodeAdministrator)
                self.fout.write(' 15. self.emailAddressForCodeAdministrator: %s\n' % self.emailAddressForCodeAdministrator)
                self.fout.write('\n')

            return  # readConfigureFileForEcoPylot


    def parse(self):
        '''
        Purpose:
            parse a MIME email msg, detach attachments + body + subject + destination +
                other items; prepare all data for submission to a database
        '''
        if DEBUG_MODULES:
            print('\n>> in module ' + MODULE + '/parse <<\n')
            
# define month:number dict
        dictMonth = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',
             'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
        
            
        ''' 
# use if input is from command line:   
if len(sys.argv) == 1:
    self.fout.write('\nYou must include a filename on the command line!')
    self.fout.write('')
    sys.exit()
        '''
        '''
self.fout.write('\nsys.argv[0] = %s' % sys.argv[0])
len_sys = len(sys.argv) - 1
self.fout.write('You have %s other parameters:' % len_sys)
if len_sys > 0:
    for arg in sys.argv[1:]:
        self.fout.write('   arg = %s' % arg)
else:
    self.fout.write('\n -- END --')
    sys.exit()
        '''
    
        '''
f = open(sys.argv[1])
fin = sys.stdin.read()
        '''
        
        '''
        self.fout.write('\n\n----start of email message------\n')
        self.fout.write('\nContents of file:\n%s' % self.msg)
        self.fout.write('\n\n----end of email message------\n\n')
        '''

# now parse self.msg

#  If the e-mail headers are in a file, uncomment this line:
#headers = Parser().parse(open(messagefile, 'r'))

#  Or for parsing headers in a string, use:
        '''
# use for testing
        headers = Parser().parsestr(
            'From: <user@example.com>\n'
            'To: <someone_else@example.com>\n'
            'Subject: Test message\n'
            '\n'
            'Body would go here\n'
            )
        '''
# split email into lines        
        msgNew = self.msg.split('\n')
        if self.fout:
            self.fout.write('\nlen(msgNew) = %s\n\n' % len(msgNew))
            self.fout.write('\n\nmsgNew = \n%s\n' % msgNew)
        
        
# for UTC time (not corrected for local time:
# ... format:  Thu, 2 Jun 2011 19:24:09 +0000
#        dateSubmitted = self.headers['date'].split()
# for local time
# ... format: Thu Jun  2 13:24:11 2011
        dateSubmitted = msgNew[0]
#        self.fout.write('\n1. dateSubmitted = %s' % dateSubmitted)
        dateSubmitted = dateSubmitted.split()
#        self.fout.write('\n2. dateSubmitted = %s' % dateSubmitted)
        dateSubmitted = dateSubmitted[2:]
#        self.fout.write('\n3. dateSubmitted = %s' % dateSubmitted)
# now looks like: ['Thu', 'June', '2', '13:24:11', '2011']
        
        if DEBUG_PRINT_OUTPUT:
            print('dateSubmitted = %s' % dateSubmitted)

# for UTC
#        day = dateSubmitted[0][:3]
# for local
        day = dateSubmitted[0]
        
# extract database and table; their existence is verified later
# ... database
        self.myDatabase = self.headers['to'].split('@')[0][1:]
        if '-' in self.myDatabase:
            self.myDatase.replace('-','_')
# ... table
        self.myTable = self.headers['subject'].split(',')[0]
# replace any dashes with underscores; do nothing if string has no dashes
        self.myTable.replace('-','_')
        
        '''
# extract server name
#        self.myDatabaseServer = self.headers['to'].split('@')[1]
        extractServer = []
        extractServer = re.findall(
#            '"(\w+_\w+@\w+.\w+.\w+)"', self.headers['to']
            '".+@(.+)"', self.headers['to']
            )
        self.myDatabaseServer = extractServer[0]
        if DEBUG_PRINT_OUTPUT:
            print('\nself.headers[\'to\'] = %s' % self.headers['to'])
            print('\nserver = %s' % self.myDatabaseServer)
        '''

# date: ddMonyyyy
# for UTC:
#        date = dateSubmitted[1] + dateSubmitted[2] + dateSubmitted[3]
# for local
        date = dateSubmitted[2] + dateSubmitted[1] + dateSubmitted[4]
# date2: yyyy/mm/dd
        date2 = dateSubmitted[4] + '/' + dictMonth[dateSubmitted[1]] + '/' + dateSubmitted[2]
        timeSubmitted = dateSubmitted[3]
        frm = self.headers['from']
        
# replace extraneous chars put in by mail server for line continuation
#        msgNew = self.msg.replace('=\n','') 

# extract body of email; will be user_comments in table
#  (tried regular expressions to do this, without success; just use string methods)
        mailBody = ''
        icount = 0
        for line in msgNew:
# start
            if line.count('quoted-printable'):
                icount += 1
                continue
# end
            if(
            icount >= 1
            and
            line.count('--_0')
            ):
                icount -= 1
                break
# increment
            if icount >= 1:
                mailBody += line + '\n'
                icount += 1
                
# strip leading whitespace
        mailBody = mailBody.strip()
        if self.fout:
            self.fout.write('\nmailBody = \n%s\n' % mailBody)
            if ( 
            (mailBody.count('\n') > 0 and len(mailBody) >= 1)
            or
            (len(mailBody) >= 1)
            ):
                self.fout.write(
                    '\nNumber of lines in mailBody (includes blank lines): %s\n' 
                    % (mailBody.count('\n') + 1)
                    )
            else:
                self.fout.write(
                    '\nNumber of lines in mailBody (includes blank lines): 0\n' 
                    )

# get rid of '-', as the msgBoundary has extraneous ones in the file's last line
# ... line designating email content boundaries
        msgBoundary = re.findall(r'boundary="([A-Za-z0-9_]+)',self.headers['content-type'])[0] 
        msgBoundaryCount = self.msg.count(msgBoundary)
        # decode attachments
        self.hasAttachments = self.headers['x-ms-has-attach']  
        
# date in format yyyy/mm/dd; this is the date-stamp on the email
        self.date2db = date2
# other params
        fromName = self.headers['from'].split(' <')[0][1:-1]
        fromNameSplit = fromName.split(',')
        nameLast = fromNameSplit[0].strip()
        nameFirst = fromNameSplit[1].strip() 
        fromEmailAddress = self.headers['from'].split(' <')[1][0:-1]
        to = self.headers['to'].split(' <')[1][:-1]
# get database username and password from email 'to' value
        myDbUserAndPassword = to.split('_')
        self.myDatabaseServerUserName = myDbUserAndPassword[0]
        self.myDatabaseServerPassword = myDbUserAndPassword[1].split('@')[0]
# other parameters
        subject = ' '.join(self.headers['subject'].split())
        self.hasAttachments = self.headers['x-ms-has-attach']
        content_type = self.headers['content-type']
        mime_version = self.headers['mime-version']
        x_pmx_version = self.headers['x-pmx-version']
        content_language = self.headers['content-language']
        self.userEmailBody = mailBody
        
# time now; slice out of date/time string
        self.timeRightNow = time.ctime(time.time())[11:19]
        
        stringEmailParsingResults = (
            '\n=== EMAIL PARSING RESULTS ===\n' +
            '  frm: %s\n' +
            '  day: %s\n' +
            '  date: %s\n' + 
            '  date2: %s\n' +
            '  timeSubmitted: %s\n' + 
            '  database_server: %s\n' +
            '  database_server_username: %s\n' +
            '  database_server_password: %s\n' +
            '  fromName: %s\n' +
            '  fromEmailAddress: %s\n' +
            '  to: %s\n' +
            '  subject: %s\n' +
            '  self.hasAttachments: %s\n' +
            '  content-type: %s\n' +
            '  mime-version: %s\n' +
            '  x-pmx-version: %s\n' +
            '  content-language: %s\n' +
            '  body:\n%s\n' +
            '  msgBoundary = %s\n' +
            '  msgBoundaryCount = %s\n\n'
            ) % (
            frm,
            day,
            date,
            date2,
            timeSubmitted,
            self.myDatabaseServer,
            self.myDatabaseServerUserName,
            self.myDatabaseServerPassword,
            fromName,
            fromEmailAddress,
            to,
            subject,
            self.hasAttachments,
            content_type,
            mime_version,
            x_pmx_version,
            content_language,
            self.userEmailBody,
            msgBoundary,
            msgBoundaryCount
            )
       
        if DEBUG_PRINT_OUTPUT:
            print(stringEmailParsingResults)
        if self.fout:
            self.fout.write(stringEmailParsingResults)            

# extract all attachments, if present; decode using base64
        if self.hasAttachments == 'yes':
            msgLines = self.msg.split('\n')
            if DEBUG_PRINT_OUTPUT:
                print('\nnumber of lines in message = %s\n' % len(msgLines))
            self.dictAttachmentsInfo = {}
            icount = 0
            attachedName = attachedEncoding = attachedBody = False
            attachmentBody = ''
            for numberLine,line in enumerate(msgLines):
                if 'Content-Description' in line:
                    if DEBUG_PRINT_OUTPUT:
                        print('\n\nfound Content-Description in Line #%s' % numberLine)
                    lineSplit = line.split()
                    attachmentFilename = lineSplit[len(lineSplit) - 1]
                    if DEBUG_PRINT_OUTPUT:
                        print('    attachmentFilename = %s' % attachmentFilename)
                    attachedName = True
                    continue
                if attachedName and ('Content-Transfer-Encoding' in line):
                    if DEBUG_PRINT_OUTPUT:
                        print('found Content-Transfer-Encoding in Line #%s' % numberLine)
                    lineSplit = line.split()
                    attachmentEncoding = lineSplit[len(lineSplit) - 1]
                    if DEBUG_PRINT_OUTPUT:
                        print('    attachmentEncoding = %s' % attachmentEncoding)
                    attachedEncoding = True
                    continue
                if attachedName and attachedEncoding:
                    lineModified = line
                    if line.count('--_'):  # occurs in intermediate msg boundaries
                        lineModified = lineModified.replace('--_','_')
                    if line.count('_--'):   # occurs in last msg boundary
                        lineModified = lineModified.replace('_--','_')
                    if DEBUG_PRINT_OUTPUT:
                        print('lineModified, msgBoundary = \n%s\n%s' %
                            (lineModified, msgBoundary)
                            )
                    if lineModified == '\n':
                        continue
                    elif lineModified == msgBoundary:    # end of msg; collect all info and move on
                        attachedName = attachedEncoding = attachedBody = False
                        if DEBUG_PRINT_OUTPUT:
                            print('\n\n   >>> attachmentBody (not decoded) =\n%s\n\n' % attachmentBody)
# decode attached file so humans can read it
                        attachmentBodyDecoded = base64.decodestring(attachmentBody)
                        self.dictAttachmentsInfo['file' + str(icount)] = [
#                    attachmentFilename,attachmentEncoding,attachmentBodyDecoded
                            attachmentFilename,attachmentBodyDecoded
                            ]
                        if DEBUG_PRINT_OUTPUT:
                            print('\n\n    >>>> self.dictAttachmentsInfo = \n%s\n\n' % self.dictAttachmentsInfo)
                        attachmentBody = ''
                        icount += 1 
                        continue
                    else:
                        attachmentBody += lineModified + '\n'
                        if DEBUG_PRINT_OUTPUT:
                            print('>> numberLine, attachmentBody = %s. %s' % (numberLine,attachmentBody))

# there are no attachments -- so no data files
        else:
#            self.msgOk = False
            self.msgErrorString += '\nERROR: no data files are attached to email.'
            return
        
#        if DEBUG_PRINT_OUTPUT:
#            print('\n\nlen(self.dictAttachmentsInfo) = %s' % len(self.dictAttachmentsInfo))
#            print('\n\nself.dictAttachmentsInfo =\n%s\n\n' % self.dictAttachmentsInfo)
#            print('\n'*3)

# variables now defined (example values):
#   1. day (Sat)
#   2. date (19Feb2011)
#   3. date2 (2011-02-19)
#   4. timeSubmitted (09:05:38)
#   5. fromName (Barnette, Daniel W)
#   6. fromEmailAddress (dwbarne@sandia.gov)
#   7. to (mantevo-data@oso.sandia.gov)
#   8. subject (attachment test 021911 9:06am)  
#   9. self.hasAttachments (yes)
#   10. content-type 
#   11. mime-version
#   12. x-pmx-version
#   13. content-language (en-US)
#   14. mailbody (body text)    -- Database field: 'user_comments'
#   15. self.dictAttachmentsInfo{'file0':[attachmentFilename,attachmentBodyDecoded],...}  

# print attachments; shows how to print 
# ... sort keys
        keyOrder = self.dictAttachmentsInfo.keys()
        keyOrder.sort()
# ... cycle thru and print each attachment
        for key in keyOrder:
#            print('>> %s: attachment name: %s' % (key,self.dictAttachmentsInfo[key][0]) )
#            print(self.dictAttachmentsInfo[key][1])
#            print('\n==============================\n')
            stringKeyOrder = (
                '>> %s: attachment name: %s\n' +
                '%s\n' +
                '\n=======================================\n'
                ) % (
                key, self.dictAttachmentsInfo[key][0], self.dictAttachmentsInfo[key][1]
                )
            if DEBUG_PRINT_OUTPUT:
                print(stringKeyOrder)
            self.fout.write(stringKeyOrder)  
            
# days since my arbitrary start date
# ... timeStartDate = (yr, month, day, hr, min, sec, day of week, day of year, daylight savings flag)
# ...       start at Jan 1, 2011, Saturday (day 5 of week), with no DST at this date            
        timeStartDate = (2011,1,1,0,0,0,5,1,0)
        timeStartDateSinceEpoch_Seconds = time.mktime(timeStartDate)
        timeNow_Seconds = time.time()
        timeNowSinceStartDate_Days = \
            (timeNow_Seconds - timeStartDateSinceEpoch_Seconds)/3600./24. + 1

# error check all input for invalid values or for blanks;
# ... if invalid or has blank fields, send email back to user stating what went wrong;
# ... include attachments
# ... send blind copy to dwbarne@sandia.gov
# ... 

        stringParsedEmailElements = (
            '\nParsed email elements will be sent to:\n' +
            '     DatabaseServer: %s' +
            '     Database: %s' +
            '     Table: %s\n'
            ) % (
            self.myDatabaseServer,
            self.myDatabase,
            self.myTable
            )

        if DEBUG_PRINT_OUTPUT:
            print(stringParsedEmailElements)
        if self.fout:
            self.fout.write(stringParsedEmailElements)
            
        self.userName = fromEmailAddress.strip().split('@')[0]
        self.codeName = 'eco_pylot'
        self.versionPython = platform.python_version()
        self.operatingSystem = platform.system()
        self.dayNumber = int(timeNowSinceStartDate_Days)
        self.dayOfWeek,self.month,self.day,self.time,self.year = time.ctime().split()
        self.osName = os.name 
        '''
        if self.osName == 'nt':
            computerName = os.environ['COMPUTERNAME']
        elif self.osName == 'posix':
            computerName = os.environ['HOSTNAME']
        else:
            try:
                computerName = os.environ['HOSTNAME']
            except:
                computerName = 'unknown'
        '''
        computerName = platform.uname()[1]
        self.hostName = computerName
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
# list of variables to be transferred to database, in order
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  1. user                          char    (20)
#  2. tester_name_first             char    (255)
#  3. tester_name_last              char    (255)
#  4. current_dir                   char    (60)
#  5. host_name                     char    (20)
#  6. target_machine                char    (25)
#  7. day_number_since_01jan2011    int     (12)
#  8. day_of_week                   char    (5)
#  9. month                         char    (5)
# 10. day_of_month                  int     (5)
# 11. year                          int     (12)
# 12. date_of_last_send             char    (15)
# 13. time_of_last_send             char    (15)
# 14. input_file_name               char    (50)
# 15. input_file_dir                char    (60)
# 16. input_file_contents           text
# 17. output_file_name              char    (50)
# 18. output_file_dir               char    (60)
# 19. output_file_contents          text
# 20. makefile_name                 char    (50)
# 21. make_file_dir                 char    (60)
# 22. makefile_contents             text
# 23. source_file_name              char    (50)
# 24. source_file_dir               char    (60)
# 25. source_file_contents          text
# 26. executable_file_name          char    (50)
# 27. executable_file_dir           char    (60)
# 28. qsub_file_name                char    (50)
# 29. qsub_file_dir                 char    (60)
# 30. qsub_file_contents            text
# 31. compile_line                  char    (200)
# 32. execute_line                  char    (200)
# 33. user_comments                 text
    
        if self.fout:
            self.fout.write('\nself.dictParams (unordered):\n')

        self.dictParams = {}
        self.dictParams = {
        'user' : self.userName,
        'tester_name_first' : nameFirst,
        'tester_name_last' : nameLast,
        'current_directory' : '',
        'host_name' : '',
        'target_machine' : '',
        'day_number_since_01jan2011' : self.dayNumber,
        'day_of_week' : self.dayOfWeek,
        'month' : self.month,
        'day_of_month' : self.day,
        'year' : self.year,
        'date_of_last_send' : date2,
        'time_of_last_send' : timeSubmitted,
        'input_file_name' : '',
        'input_file_dir' : '',
        'input_file_contents' : '' ,
        'output_file_name' : '',
        'output_file_dir' : '',
        'output_file_contents' : 'file attachments will go here',
        'makefile_name' : '',
        'make_file_dir' : '',
        'makefile_contents' : '',
        'source_file_name' : '',
        'source_file_dir' : '',
        'source_file_contents' : '',
        'executable_file_name' : '',
        'executable_file_dir' : '',
        'qsub_file_name' : '',
        'qsub_file_dir' : '',
        'qsub_file_contents' : '',
        'compile_line' : '',
        'execute_line' : '',
        'user_comments' : self.userEmailBody,
        }
        
        icount = 1
        for key,value in self.dictParams.iteritems():
            stringDictParams = (
                '%s. %s : %s' 
                ) % (
                icount,
                key,
                value
                )
            if DEBUG_PRINT_OUTPUT:
                print(stringDictParams)
            if self.fout:
                self.fout.write(stringDictParams)
            icount += 1
        if DEBUG_PRINT_OUTPUT:
            print('\n')
        if self.fout:
            self.fout.write('\n')
        
# check for required parameters; if not available, put in error msg
# required values:
#               
        return  # parse
        
      
    def mySQLConnect(self):
        '''
        connects to MySQL server 
        
        Inputs:
            if from yaml file eco_pylot.conf:
                self.databaseServerFromConfFile
                self.databaseServerUserNameFromConfFile
                self.databaseServerPasswordFromConfFile
            or if from email:
                self.myDatabaseServer
                self.myDatabaseServerUserName
                self.myDatabaseServerPassword
                
            Port:
                self.databaseServerPort
            
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'MySQLConnect\n')
            
        connected = self.checkMySQLConnection()  
        
        if connected:
            if DEBUG_PRINT_OUTPUT:
                print('\n -- already connected to database\n')
            if self.fout:
                self.fout.write('\n -- already connected to database\n')
            return
        
        if self.useYamlServerValues:
# determined in method 'readConfigureFileForEcoPylot'
            self.fout.write(
                '\nUsing login parameters determined in method "readConfigureFileForEcoPylot"'
                )
            un = self.databaseServerUserNameFromConfFile
            pw = self.databaseServerPasswordFromConfFile
            svr = self.databaseServerFromConfFile
            prt = self.databaseServerPort
        else:
# determined in method 'parse'
            if self.fout:
                self.fout.write(
                    '\nUsing login parameters determined in method "parse"'
                    )
            un = self.myDatabaseServerUserName
            pw = self.myDatabaseServerPassword
            svr = self.myDatabaseServer
            prt = 3306
        
        valuePresent=1
        valueString=''
        
        if un == '':
            valuePresent=0
            valueString=' Username is blank\n'
        if pw == '':
            valuePresent=0
            valueString+=' Password is blank.\n'
        if svr == '':
            valuePresent=0
            valueString+=' Server is not specified.\n'
        if prt == '':
            valuePresent=0
            valueString+=' Port is blank.\n'
        
        if not valuePresent:
            stringErrorLoginValues = (
                '\nERROR: following errors occurred:\n%s' % valueString
                )
            if DEBUG_PRINT_OUTPUT:
                print(stringErrorLoginValues)
#            self.fout.write('\nFollowing errors occurred:\n%s' % valueString)
            self.msgErrorString += stringErrorLoginValues
            return
            
        if self.fout:
            self.fout.write('\nLogin values:\n')
            self.fout.write('   user: %s\n' % un)
            self.fout.write('   password: %s\n' % pw)
            self.fout.write('   host: %s\n' % svr)
            self.fout.write('   port: %s\n\n' % str(prt))
            
        stringLoginValues = (
            '\nDatabase login values:\n' +
            '     user = ' + un + '\n' +
            '     password = ' + pw + '\n' +
            '     host = ' + svr + '\n' +
            '     port = ' + str(prt) + '\n\n' 
            )
        if DEBUG_PRINT_OUTPUT:
            print(stringLoginValues)
        self.fout.write(stringLoginValues)
        
# now connect to server
        try:
            self.myDbConnection = MySQLdb.connect(
                user=un,
                passwd=pw,
                host=svr,
                port=prt
                )            
        except:
            stringErrorServerNotAvailable = (
                '\nERROR: Could not connect to database.\n\n' + 
                'Possible reasons:\n' +
                '  - Invalid username, password, or server name\n' +
                '  - Check if "Caps Lock" has been pressed\n' +
                '  - Server timeout (log back in)\n' +
                '  - Server not available at this time\n\n' +
                'Check input fields and try again.'
                )
            if DEBUG_PRINT_OUTPUT:
                print('\n' + stringErrorServerNotAvailable)
            self.msgErrorString += stringErrorServerNotAvailable
            return    

# At this point, connection is successful
        stringConnected = (
            '\n  *** Connected to MySQL database ***\n'
            )
        if DEBUG_PRINT_OUTPUT:
            print(stringConnected)
        if self.fout:
            self.fout.write(stringConnected)

# get a cursor handle for executing SQL commands
        self.cursorHandleMySQL = self.myDbConnection.cursor()
# turn on autocommit; else, database will not update when you want
        self.cursorHandleMySQL.execute("set autocommit = 1")
        
        return  # mySQLConnect
        
        
    def send2db(self):
        '''
        Purpose:
            Send parsed info to database
            
        Input:
            self.dictParams
        '''
        if DEBUG_MODULES:
            print('\n>> in module ' + MODULE + '/send2db <<\n')   
        
# print all variables
        stringVariablesToDatabase = (
            '\n----- VARIABLES TO SEND TO DATABASE TABLE -----\n' +
            ' user = %s\n' +
            ' testerNameFirst = %s\n' +
            ' testerNameLast = %s\n' +
            ' currentDirectory = %s\n' +
            ' hostName = %s\n' +
            ' machineForExecutable = %s\n' +
            ' day_number_since_01jan2011 = %s\n' +
            ' day_of_week = %s\n' +
            ' month = %s\n' +
            ' day_of_month = %s\n' +
            ' year = %s\n' +
            ' dateOfLastSend = %s\n' +
            ' timeOfLastSend = %s\n' +
            ' inputFile = %s\n' +
            ' inputFileDir = %s\n' +
#            ' inputFileContents = %s\n' +
            ' outputFile = %s\n' +
            ' outputFileDir = %s\n' +
#            ' outputFileContents = %s\n' +
            ' makeFile = %s\n' +
            ' makeFileDir = %s\n' +
#            ' makeFileContents = %s\n' +
            ' sourceFile = %s\n' +
            ' sourceFileDir = %s\n' +
#            ' sourceFileContents = %s\n' +
            ' executableFile = %s\n' +
            ' executableFileDir = %s\n' +
            ' qsubFile = %s\n' +
            ' qsubFileDir = %s\n' +
#            ' qsubFileContents = %s\n' +
            ' compileLine = %s\n' +
            ' executeLine = %s\n' +
            ' userComments = %s\n'            
            ) % (
            self.dictParams['user'],
            self.dictParams['tester_name_first'],
            self.dictParams['tester_name_last'],
            self.dictParams['current_directory'],
            self.dictParams['host_name'],
            self.dictParams['target_machine'],
            self.dictParams['day_number_since_01jan2011'],
            self.dictParams['day_of_week'],
            self.dictParams['month'],
            self.dictParams['day_of_month'],
            self.dictParams['year'],
            self.dictParams['date_of_last_send'],
            self.dictParams['time_of_last_send'],
            self.dictParams['input_file_name'],
            self.dictParams['input_file_dir'],
#            self.dictParams['input_file_contents'],
            self.dictParams['output_file_name'],
            self.dictParams['output_file_dir'],
#            self.dictParams['output_file_contents'],
            self.dictParams['makefile_name'],
            self.dictParams['make_file_dir'],
#            self.dictParams['makefile_contents'],
            self.dictParams['source_file_name'],
            self.dictParams['source_file_dir'],
#            self.dictParams['source_file_contents']
            self.dictParams['executable_file_name'],
            self.dictParams['executable_file_dir'],
            self.dictParams['qsub_file_name'],
            self.dictParams['qsub_file_dir'],
#            self.dictParams['qsub_file_contents'],
            self.dictParams['compile_line'],
            self.dictParams['execute_line'],
            self.dictParams['user_comments']
            )
            
        if DEBUG_PRINT_OUTPUT:
            print(stringVariablesToDatabase)
        if self.fout:
            self.fout.write(stringVariablesToDatabase)
            
        stringDBParams = (
            '\nmyDatabaseServer = %s\n' +
            'myDatabase = %s\n' +
            'myTable = %s\n'
            ) % (
            self.myDatabaseServer,
            self.myDatabase,
            self.myTable
            )

        if DEBUG_PRINT_OUTPUT:
            print(stringDBParams)
        if self.fout:
            self.fout.write(stringDBParams)
        '''
        if len(self.dictAttachmentsInfo) == 0:
                stringNoOutputFile = (
                    'Specify an OUTPUT file'
                    )
                self.fout.write('\n' + stringNoOutputFile)
                return
        '''
            
# collect in list the data to send to mysql table; 26 elements in all
# ... these MUST match database table fields!!
        data2send = []
# system data                                                               datatype    length
        data2send.append(self.dictParams['user'])                       #1  char        20
        data2send.append(self.dictParams['tester_name_first'])          #2
        data2send.append(self.dictParams['tester_name_last'])           #3
        data2send.append(self.dictParams['current_directory'])          #4  char        60
        data2send.append(self.dictParams['host_name'])                  #5  char        20
# REQUIRED: machine on which executable was run
        data2send.append(self.dictParams['target_machine'])             #6  char        20
        data2send.append(self.dictParams['day_number_since_01jan2011']) #7  int         12
        data2send.append(self.dictParams['day_of_week'])                #8  char        5
        data2send.append(self.dictParams['month'])                      #9  char        5
        data2send.append(self.dictParams['day_of_month'])               #10 int         5
        data2send.append(self.dictParams['year'])                       #11 char        15

        data2send.append(self.dictParams['date_of_last_send'])          #12 char        15
        data2send.append(self.dictParams['time_of_last_send'])          #13 char        15
# input file, dir, and content
        data2send.append(self.dictParams['input_file_name'])            #14 char        50
        data2send.append(self.dictParams['input_file_dir'])             #15 char        60
        data2send.append(self.dictParams['input_file_contents'])        #16 text

# REQUIRED: output file, dir, and content
        data2send.append(self.dictParams['output_file_name'])           #17 char        50
        data2send.append(self.dictParams['output_file_dir'])            #18 char        60
        data2send.append(self.dictParams['output_file_contents'])       #19 text        THIS IS REQUIRED
        indexForAttachments = 18

#  make file, dir, and content      
        data2send.append(self.dictParams['makefile_name'])              #20 char        50
        data2send.append(self.dictParams['make_file_dir'])              #21 char        60
        data2send.append(self.dictParams['makefile_contents'])          #22 text

# source file, dir, and content
        data2send.append(self.dictParams['source_file_name'])           #23 char        50
        data2send.append(self.dictParams['source_file_dir'])            #24 char        60
        data2send.append(self.dictParams['source_file_contents'])       #25 text
            
# executable file and dir (binary content will not be stored)
        data2send.append(self.dictParams['executable_file_name'])       #26 char        50
        data2send.append(self.dictParams['executable_file_dir'])        #27 char        60

# qsub file, dir, and content
        data2send.append(self.dictParams['qsub_file_name'])             #28 char        50
        data2send.append(self.dictParams['qsub_file_dir'])              #29 char        60
        data2send.append(self.dictParams['qsub_file_contents'])         #30 text
            
# compile line
        data2send.append(self.dictParams['compile_line'])               #31 char        200
            
# execute line
        data2send.append(self.dictParams['execute_line'])               #32 char        200
            
# user comments
        data2send.append(self.dictParams['user_comments'])              #33 text
        
# login to database server
        
# ... make sure table has enough fields to handle input; if not, table does not match INSERT command
        commandDescribe = (
            'DESCRIBE %s.%s' % (self.myDatabase, self.myTable)
            )
        try:
            self.cursorHandleMySQL.execute(commandDescribe)
        except:
            stringErrorDescribe = (
                '\nERROR: Cannot execute DESCRIBE command for\n\n' +
                '  database: %s\n' +
                '  table: %s\n\n' +
                'Make sure database and table exist and that you have\n' +
                'permission to access the database and table, and try again.'
                ) % (self.myDatabase, self.myTable)
            if DEBUG_PRINT_OUTPUT:
                print(stringErrorDescribe)
            self.msgErrorString += stringErrorDescribe
            return
            
        tableStructure = self.cursorHandleMySQL.fetchall()
        numfieldsInTable = len(tableStructure) - 1
        numfieldsData2Send = len(data2send)
        
        stringTableStructure = ''
        stringTableStructure += (
            '\ntableStructure for table "%s":' % self.myTable
            )
        for itemNumber, item in enumerate(tableStructure):
            stringTableStructure += (
                '\n  %s. %s' % (itemNumber+1, item)
                )
        if DEBUG_PRINT_OUTPUT:
#            print('\ntableStructure for %s:' % self.myTable)
#            for itemNumber, item in enumerate(tableStructure):
#                print('%s. %s' % (itemNumber+1, item))
            print(stringTableStructure)
        if self.fout:
            self.fout.write(stringTableStructure)
            
        if numfieldsData2Send <> numfieldsInTable:
            stringErrorTableFields = ''
            stringErrorTableFields += (
                '\nNumber of user fields (exclude auto_index) in table %s: %s' % 
                (self.myTable,numfieldsInTable)
                )
            stringErrorTableFields += (
                '\nNumber of data fields (exclude auto_index) to send to table "%s": %s ' %
                (self.myTable, numfieldsData2Send)
                )
            if DEBUG_PRINT_OUTPUT:
                print(stringErrorTableFields)
            self.msgErrorString += stringErrorTableFields
            stringMismatch = (
                '\nNumber of data fields does not match the number of\n' +
                'table fields, indicating a mismatch between data\n' + 
                'and table, or the wrong table has been selected.\n\n' +
                'Verify that correct table has been chosen, or modify\n' +
                'the chosen table to match data fields, and try again.'
                )
            if DEBUG_PRINT_OUTPUT:
                print stringMismatch
            self.msgErrorString += stringMismatch
            return

# ... use following form to enable INSERT of data into select columns; this is needed when
# ...   adding data to an existing table with more fields than the original created for
# ...   co-pylot and the auto-index column field location is not field #29
# ... form first part of command
        self.myMySQLCommand_FirstPart = (
            'INSERT INTO ' + self.myDatabase + '.' + self.myTable + 
            ' (' +
            'user, ' +                          # 1 -- index 0
            'tester_name_first, ' +             # 2
            'tester_name_last, ' +              # 3
            'current_dir, ' +                   # 4
            'host_name, ' +                     # 5
            'target_machine, ' +                # 6
            'day_number_since_01jan2011, ' +    # 7
            'day_of_week, ' +                   # 8
            'month, ' +                         # 9
            'day_of_month, ' +                  # 10
            'year, ' +                          # 11
            'date_of_last_send, ' +             # 12
            'time_of_last_send, ' +             # 13
            'input_file_name, ' +               # 14
            'input_file_dir, ' +                # 15
            'input_file_contents, ' +           # 16
            'output_file_name, ' +              # 17
            'output_file_dir, ' +               # 18 
            'output_file_contents, ' +          # 19 This is required!
            'makefile_name, ' +                 # 20
            'makefile_dir, ' +                  # 21
            'makefile_contents, ' +             # 22
            'source_file_name, ' +              # 23
            'source_file_dir, ' +               # 24
            'source_file_contents, ' +          # 25
            'executable_file_name, ' +          # 26
            'executable_file_dir, ' +           # 27
            'qsub_file_name, ' +                # 28
            'qsub_file_dir, ' +                 # 29
            'qsub_file_contents, ' +            # 30
            'compile_line, ' +                  # 31
            'execute_line, ' +                  # 32
            'user_comments ' +                  # 33
#                'auto_index' +                 # 34 Automatically updated
            ')' +
            ' VALUES ('
            )

# loop over all attached files; other fields always stay same
        for attachedFileNumber in range(len(self.dictAttachmentsInfo)):
            stringHeader = (
                '\n\n========  DATA SET %s of %s TO SEND TO DATABASE =========='
                ) % (
                attachedFileNumber + 1,
                len(self.dictAttachmentsInfo)
                )
            if DEBUG_PRINT_OUTPUT:
                print(stringHeader)
            if self.fout:
                self.fout.write(stringHeader)
            tempAdd2MySQLCommand = ''
            data2send[indexForAttachments] = self.dictAttachmentsInfo['file' + str(attachedFileNumber)]
            stringForAttachments = (
#                '\nattachedFileNumber = %s: data2send[%s] = %s'
                '\nattachedFileNumber = %s:\n'
                ) % (
                str(attachedFileNumber + 1)
#                indexForAttachments,
#                data2send[indexForAttachments]
                )
            if DEBUG_PRINT_OUTPUT:
                print(stringForAttachments)
            if self.fout:
                self.fout.write(stringForAttachments)
            
# ... form format of insert command                
            for numField in range(numfieldsData2Send):
# ... write all data to first fields in table
                if numField < numfieldsData2Send - 1:
# ... include comma if field is not the last
                    tempAdd2MySQLCommand += "(\"" + str(data2send[numField]) + "\")" + ', '                        
                else:
# ... no comma for last field
                    tempAdd2MySQLCommand += "(\"" + str(data2send[numField]) + "\")" + " )" 
#                    self.fout.write('\n\nLOOK:\n%s\n' % tempAdd2MySQLCommand)

# print fields
                stringCommand = (
                    '%s. "%s"'
                    ) % (
                    str(numField + 1),
                    str(data2send[numField])
                    )
                if self.fout:
                    self.fout.write(stringCommand)
                if DEBUG_PRINT_OUTPUT:
                    print(stringCommand)
                        
                        
            self.myMySQLCommand = self.myMySQLCommand_FirstPart + tempAdd2MySQLCommand
                        
# see the whole command before executing
            stringCommand = (
                '\nself.myMySQLCommand = %s\n'
                ) % (
                self.myMySQLCommand
                )
            if DEBUG_PRINT_OUTPUT:
                print(stringCommand)
            if self.fout:
                self.fout.write(stringCommand)
            
            try:
                self.cursorHandleMySQL.execute(self.myMySQLCommand)
            except:
                insertErrorString = (
                    '\n>> Error: Not able to insert data into database.\n\n' +
                    'Check INSERT command for mismatch errors with table.\n\n' + 
                    'INSERT process halted.\n\n'
                    )
                if DEBUG_PRINT_OUTPUT:
                    print(insertErrorString)
                self.msgErrorString += insertErrorString
                return

        stringSuccess = (
            '\neCo-Pylot data export SUCCESSFUL.\n\n' + 
            'Number of rows added to table: ' + str(len(self.dictAttachmentsInfo)) + '\n\n'
            )
        if DEBUG_PRINT_OUTPUT:
            print(stringSuccess)
        self.fout.write(stringSuccess)
        
        return  # send2db

                
    def email2user(self):
        '''
        Purpose:
            Send return email to user re status of attempt to 
            send parsed email to database
            
            Currently, send user email if success or if failure
            
            Send email to code admin if error messages occur
        '''
        import smtplib
        import time
        
        if DEBUG_MODULES:
            print('\n>> in module ' + MODULE + '/email2user <<\n')
            
# return email parameters
        returnEmail_From = self.headers['to']
        returnEmail_To = self.headers['from']
        returnEmail_Date = time.ctime(time.time())
# NOTE: the first line in an email body MUST BE a newline (\n)!!!!
#  ... or else nothing will be part of the body until a blank line is encountered
        returnEmail_Body = ''
        Body = ''
        if self.userEmailBody:
            Body = (
                '\n--- Body of user email ---\n' +
                self.userEmailBody +
                '\n--- End ---\n' 
                )
        
# include error messages if there are any
        if self.msgErrorString <> '':
            '''
            stringAdminEmail = (
                '\nIf you are unable to determine why your submission was not\n' +
                'successful, contact the current code administrator for possible help.' 
                ) 
            self.msgErrorString += stringAdminEmail
            '''
# check if SUBJECT has been included in email; this is the database table  
# we will not know the database if the email has not yet been parsed
            if self.myTable:
                returnEmail_Subject = (
                    'FAILED: entries for table "' + self.myTable + '"\n'
                    )
                if self.myDatabase:
                    Body += (
                        '\nEntries failed for\n' +
                        '   database: %s\n' +
                        '   table: %s\n'
                        ) % (
                        self.myDatabase,
                        self.myTable
                        )
                else:
                    Body += (
                        '\nEntries failed for\n' +
                        '   table: %s\n'
                        ) % (
                        self.myTable
                        )
                    
            else:
                returnEmail_Subject = (
                    'FAILED: entries for table "UNKNOWN"'
                    )
                if self.myDatabase:
                    Body += (
                        '\nEntries failed for\n' +
                        '   database: %s\n' +
                        '   table: UNKNOWN\n'
                        ) % (
                        self.myDatabase,
                        )
                else:
                    pass
                    
        else:
            returnEmail_Subject = (
                'SUCCESS: entries for table "' + self.myTable + '"'
                )
            returnEmail_Body += (
                '\nEntries were successful for\n' +
                '   database: %s\n' +
                '   table: %s\n'
                ) % (
                self.myDatabase,
                self.myTable
                )
        
# include names of attached files
        if self.hasAttachments:
            Body += '\nAttachment filenames:\n'
# ... sort keys
            keyOrder = self.dictAttachmentsInfo.keys()
            keyOrder.sort()
# ... cycle thru and print each attachment
            for number,key in enumerate(keyOrder):
                Body += '  %s. %s\n' % (str(number + 1),self.dictAttachmentsInfo[key][0])
        else:
            Body += (
            '\nERROR: there are no attachments.\n' +
            'At least one file must be attached for eCo-Pylot to work.\n' +
            'Attach at least one file and try again.'
            )
            
        if len(self.msgErrorString) > 0:
            Body = (
                '\nErrors encountered:\n' + 
                self.msgErrorString + Body
                )
                
        returnEmail_Body += Body
        
        try:
            if self.fout:
                self.fout.write('\nreturnEmail_Body = \n%s' % returnEmail_Body)
        except:
            print('\nreturnEmail_Body = \n%s' % returnEmail_Body)
        
        stringReturnEmail = (
            '\nreturnEmail parameters:\n' +
            '  mail server: %s\n' +
            '  returnEmail_From: %s\n' +
            '  returnEmail_To: %s\n' +
            '  returnEmail_Date: %s\n' +
            '  returnEmail_Subject: %s\n' +
            '  returnEmail_Body: %s\n'
            ) % (
            self.mailServer,
            returnEmail_From,
            returnEmail_To,
            returnEmail_Date,
            returnEmail_Subject,
            returnEmail_Body,
            )
        
        if DEBUG_PRINT_OUTPUT:
            print(stringReturnEmail)
        try:
            if self.fout:
                self.fout.write('\n\n>> Error message being sent back to user.\n')  
                self.fout.write(stringReturnEmail)
        except:
            print('\n\n>> Error message being sent back to user.\n')  
            print(stringReturnEmail)
                
# form email structure
        mMessageUser = (
            'From: %s\n' +
            'To: %s\n' +
            'Date: %s\n' +
            'Subject: %s\n' +
            '\n\nThis email originated from server: %s\n%s\n\n' + 
            '==== END ===='
            ) % (
            returnEmail_From, 
            returnEmail_To, 
#            returnEmail_Date, 
            time.ctime(time.time()),
            returnEmail_Subject,
            self.myDatabaseServer,
            returnEmail_Body
            )
            
# send email
# ... connect to mail server
        self.connectMailServer = 0
        try:
            self.connectMailServer = smtplib.SMTP(self.mailServer)
            okConnect = 1
        except: 
            stringNoConnectionToMailServer = (
                '\nCould not connect to mail server\n' +
                '   %s\n' +
                'No mail will be sent to user from this mail server.'
                ) % (
                self.mailServer
                )
            if DEBUG_PRINT_OUTPUT:
                print(stringNoConnectionToMailServer)
            if self.fout:
                self.fout.write(stringNoConnectionToMailServer)
            okConnect = 0
#                return 
        if self.connectMailServer:
# ... login if not a local mailserver; if 0 is returned, no mail will be sent
#            if self.mailServer <> 'mail.sandia.gov':
            okToSendMail = self.handlerLoginToExternalMailServer()
#               if not okToSendMail:
#                    return    # no mail will be sent
        else:
            okToSendMail = 0
                
# ... send mail to user
        mail2UserSuccess = 0
        if okToSendMail:
            try:
                mail2User = self.connectMailServer.sendmail(
                    returnEmail_From, 
                    returnEmail_To,
                    mMessageUser
                    )
                mail2UserSuccess = 1
            except:
                stringNoMail2User = (
                    '\nMail server could not send mail:\n' +
                    '   Mail server: %s\n' +
                    '   From: %s\n' +
                    '   To: %s\n' +
                    'No mail will be sent to user from this mail server.'
                    ) % (
                    self.mailServer,
                    returnEmail_From,
                    returnEmail_To
                    )
                if DEBUG_PRINT_OUTPUT:
                    print(stringNoMail2User)
                self.fout.write(stringNoMail2User)
                mail2UserSuccess = 0
#                    self.connectMailServer.quit()
#                return    # no mail will be sent
            
            self.connectMailServer.quit()
 
# ============================ 
                      
# if errors, send email to database admin
        if len(self.msgErrorString) > 0:
            mMessageAdmin_Body = (
                '\n========= Error messages for admin ==========\n' + 
                '%s\n\n' +
                'This email originated from:\n' +
                '   server: %s\n' +
                '   user: %s\n\n' +
                '%s'
                ) % (
                returnEmail_Date,
                self.myDatabaseServer,
                self.headers['from'],
                returnEmail_Body
                )
        else:
            stringNoErrors = (
                '\nNo errors were found; no email will be sent to code admin\n'
                )
            if DEBUG_PRINT_OUTPUT:
                print(stringNoErrors)
            if self.fout:
                self.fout.write(stringNoErrors)
            return
            
# form email structure
        mMessageAdmin = (
            'From: %s\n' +
            'To: %s\n' +
            'Date: %s\n' +
            'Subject: %s\n' +
            '\n\n%s\n\n' + 
            '==== END of email to admin ===='
            ) % (
            returnEmail_From, 
#            returnEmail_To, 
            self.emailAddressForCodeAdministrator,
            time.ctime(time.time()),
            returnEmail_Subject, 
            mMessageAdmin_Body
            )
                
# ... connect to mail server
        self.connectMailServer = 0
        try:
            self.connectMailServer = smtplib.SMTP(self.mailServerForCodeAdministrator)
#            okConnect = 1
        except: 
            stringNoConnectionToAdminMailServer = (
                '\nCould not connect to admin mail server\n' +
                '   %s\n' +
                'No mail will be sent to user from this mail server.'
                ) % (
                self.mailServerForCodeAdministrator
                )
            if DEBUG_PRINT_OUTPUT:
                print(stringNoConnectionToAdminMailServer)
            if self.fout:
                self.fout.write(stringNoConnectionToAdminMailServer)
#            okConnect = 0
#            return

# ... login if not a local mailserver; if 0 is returned, no mail will be sent
#        if okConnect:
        if self.connectMailServer:
#            if self.mailServer <> 'mail.sandia.gov':
            okToSendMail = self.handlerLoginToExternalMailServer()
#            else:
#                okToSendMail = 1
        else:
            okToSendMail = 0
#            if not okToSendMail:
#                return    # no mail will be sent
                
# ... send mail to code administrator
        mail2AdminSuccess = 0
        if okToSendMail:
            try:
                mail2Admin = self.connectMailServer.sendmail(
                    returnEmail_From, 
                    self.emailAddressForCodeAdministrator, # To:
                    mMessageAdmin
                    )
                mail2AdminSuccess = 1
            except:
                stringNoMail2Admin = (
                    '\nMail server could not send mail:\n' +
                    '   Mail server: %s\n' +
                    '   From: %s\n' +
                    '   To: %s\n' +
                    'No mail will be sent to code administrator from this mail server.'
                    ) % (
                    self.mailServerForCodeAdministrator,
                    returnEmail_From,
                    self.emailAddressForCodeAdministrator
                    )
                if DEBUG_PRINT_OUTPUT:
                    print(stringNoMail2Admin)
                if self.fout:
                    self.fout.write(stringNoMail2Admin)
                mail2AdminSuccess = 0
#                self.connectMailServer.quit()
#                return    # no mail will be sent
            
        if self.connectMailServer:
            self.connectMailServer.quit()
            
        
# check for errors for both user and code admin
# ... to user
        if mail2UserSuccess:
            stringSuccess = '\n\n>> SUCCESS: sent return email to user\n'
            if DEBUG_PRINT_OUTPUT:
                print(stringSuccess)
            try:
                if self.fout:
                    self.fout.write(stringSuccess)
            except:
                if not DEBUG_PRINT_OUTPUT:
                    print(stringSuccess)
        else:
            stringFailure = '\n\n>> ERROR: failure to send return email to user\n'
            if DEBUG_PRINT_OUTPUT:
                print(stringFailure)
            try:
                if self.fout:
                    self.fout.write(stringFailure)
            except:
                if not DEBUG_PRINT_OUTPUT:
                    print(stringFailure)
# ... to code administrator       
        if mail2AdminSuccess:
            stringSuccess = '\n\n>> SUCCESS: sent return email to code administrator\n'
            if DEBUG_PRINT_OUTPUT:
                print(stringSuccess)
            try:
                if self.fout:
                    self.fout.write(stringSuccess)
            except:
                if not DEBUG_PRINT_OUTPUT:
                    print(stringSuccess)
        else:
            stringFailure = '\n\n>> ERROR: failure to send return email to code administrator\n'
            if DEBUG_PRINT_OUTPUT:
                print(stringFailure)
            try:
                if self.fout:
                    self.fout.write(stringFailure)
            except:
                if not DEBUG_PRINT_OUTPUT:
                    print(stringFailure)
            
            
        return  # email2user
                                               
        
    def trackUsage(self):
        '''
        Purpose:
            track usage for eCo-Pylot only if database submission is successful
        '''
        if DEBUG_MODULES:
            print('\n>> in module ' + MODULE + '/trackUsage <<\n')
            
            
        if self.msgErrorString <> '':
            stringNoStats2Database = (
                '\nSince there are errors, no stats will be saved to database'
                )
            if PRINT_STATS:
                print(stringNoStats2Database)
            if self.fout:
                self.fout.write(stringNoStats2Database)                
            return
            
# define connection info for login to MySQL server
        myStatDatabase = self.trackingDatabase
        myStatTable = self.trackingDatabaseTable
        port = self.trackingServerPort
        usr = self.trackingServerUserName
        pw = self.trackingServerPassword
        server = self.trackingServer
            
# define all variables to send to database 'stats-eco_pylot'
        user = usr
        name_first = self.dictParams['tester_name_first']
        name_last = self.dictParams['tester_name_last']
        code = self.codeName
        python_version = self.versionPython        
        os = self.operatingSystem
        os_name = self.osName
        day_number = self.dayNumber # make into 'int' for filtering
        day_of_week = self.dayOfWeek
        month = self.month
        day_of_month = self.day
        year = self.year # make into 'int' for filtering
        time = self.time        
        host_name = self.hostName
        
# make into a list
        stats2db = []
        stats2db = [
            user, name_first, name_last, code, python_version, os, os_name,
            day_number, day_of_week, month, day_of_month, year, time, host_name
            ]
        
# form MySQL insert command
        command_FirstPart = (
                'INSERT INTO ' + myStatDatabase + '.' + myStatTable +
                ' (' +
                'user, ' +                      # 1
                'name_first, ' +                # 2
                'name_last, ' +                 # 3
                'code, ' +                      # 4
                'python_version, ' +            # 5
                'os, ' +                        # 6
                'os_name, ' +                   # 7
                'day_number_since_01jan2011, '+ # 8
                'day_of_week, ' +               # 9
                'month, ' +                     # 10
                'day_of_month, ' +              # 11
                'year, ' +                      # 12
                'time, ' +                      # 13
                'host_name ' +                  # 14
                ')' +
                ' VALUES ('  
                )

        lenStats = len(stats2db)
        tempAdd2Command = ''
        for i in range(lenStats):
            if i < lenStats - 1:
                tempAdd2Command += '\n' + '   \'' + str(stats2db[i]) + '\','
            else:
                tempAdd2Command += '\n' + '   \'' + str(stats2db[i]) + '\')'
                
        if PRINT_STATS:
            print('\n> command_FirstPart =')
            print(command_FirstPart)
            print('type(command_FirstPart) = %s' % type(command_FirstPart))
            print('\n> tempAdd2Command =')
            print(tempAdd2Command)
            print('type(tempAdd2Command) = %s' % type(tempAdd2Command))
                
        command = command_FirstPart + tempAdd2Command
                
        stringConnectToStatsDatabase = (
            '\nMySQL command to insert into stats database table:\n %s'
            ) % command
        if PRINT_STATS:
            print(stringConnectToStatsDatabase)
            print('')
        if self.fout:
            self.fout.write(stringConnectToStatsDatabase + '\n')
        
        
# login to database server; if it fails, then assume server is not reachable and return
        if PRINT_STATS:
            stringStatsConnection = (
                '\nLogin info for stats usage:\n' +
                '  user = %s\n' +
                '  passwd = %s\n' +
                '  host = %s\n' +
                '  port = %d\n' 
                ) % (
                usr,
                pw,
                server,
                port
                )
            print(stringStatsConnection)
        if self.fout:
            self.fout.write(stringStatsConnection)
        
        try:            
            myStatsConnection = MySQLdb.connect(
                user=usr,
                passwd=pw,
                host=server,
                port=port
                )
        except:
            stringNoStatsConnection = (
                'Could not connect to Pylot stats database:\n' +
                '  database: %s\n' +
                '  table: %s\n\n' +
                ' .... continuing ....\n'
                ) % (myStatDatabase, myStatTable)
            if PRINT_STATS:
                print stringNoStatsConnection
            self.msgErrorString += stringNoStatsConnection
            return
            
# get a cursor handle for executing SQL commands
        cursorHandleMySQLStats = myStatsConnection.cursor()
# turn on autocommit; else, database will not update when you want
        cursorHandleMySQLStats.execute("set autocommit = 1")
            
# insert data into database table
        try:
            cursorHandleMySQLStats.execute(command)
        except:
            insertErrorString = (
                '\nERROR:\n' +
                'Not able to insert data into\n' +
                '  database: %s\n' +
                '  table: %s\n' +
                'Check INSERT command for mismatch errors with table.\n\n' + 
                'INSERT process halted.\n\n'
                ) % (
                myStatDatabase,
                myStatTable
                )
            if PRINT_STATS:
                print(insertErrorString)
            if self.fout:
                self.fout.write(insertErrorString)
            myStatsConnection.close()
            self.msgErrorString += insertErrorString
            return
            
        myStatsConnection.close()
            
        stringSuccess = (
            '>> SUCCESS: Database insertion for eco_pylot usage stats.\n'
            )
        if PRINT_STATS:
            print('\n%s' % stringSuccess)
        if self.fout:
            self.fout.write(stringSuccess)
            
        return  # trackUsage
        
        
    def exit_eCo_Pylot(self,methodLastCalled):
        '''
        Purpose:
            exit on errors, printing msgErrorString and which method was last called
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'exit_eCo_Pylot\n')
            
        if self.msgErrorString <> '':
            print('\nself.msgErrorString = \n')
            print(self.msgErrorString)
            try:
                if self.fout:
                    self.fout.write('\n\n============ Error Messages ===============\n\n')
                stringAdminEmail = (
                    '\n\nIf you are unable to determine why your submission was not\n' +
                    'successful, contact the current code administrator for possible help.' +
                    '\n\nCurrent code administrator:\n' +
                    '    Name: %s\n' +
                    '    email: %s\n'
                    ) % (
                        self.nameForCodeAdministrator,
                        self.emailAddressForCodeAdministrator
                        )
                self.msgErrorString += stringAdminEmail
                if self.fout:
                    self.fout.write(self.msgErrorString)
                    self.fout.write('\nLast method called: %s\n' % methodLastCalled)
# if an error message is encountered before yaml file is read, there will be no admin listed
                    self.fout.write(
                        '\nCurrent code administrator: %s, %s\n' % (
                            self.nameForCodeAdministrator,
                            self.emailAddressForCodeAdministrator
                            )
                            )
                    self.fout.write('\nProgram exiting with errors.\n\n')
            except:
                print('\nProgram exiting with errors.\n\n')
# email user
#            self.readConfigureFileForEcoPylot()
            self.email2user()
            sys.exit()

            
        if methodLastCalled == 'finished':
            try:
                self.fout.write('\nLast method called: %s\n\n' % methodLastCalled)
                self.fout.write(
                    '\nCurrent code administrator: %s, %s' % (
                        self.nameForCodeAdministrator,
                        self.emailAddressForCodeAdministrator
                        )
                        )
                self.fout.write('\nProgram exiting without errors')
            except:
                print('\nLast method called: %s\n\n' % methodLastCalled)
                print('\nProgram exiting without errors')
            sys.exit()
        
        return  # exit_eCo_Pylot
        
        
    def checkMySQLConnection(self):
        '''
        Purpose:
            checks connection to MySQL server and switches STATUS lights
            depending on status
        
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'checkMySQLConnection')
        
# check if connected to a MySQL server

# set flag
        connectionFlag = 1
        
# try any always-true command; if valid, we are still connected  
#        self.cursorHandleMySQL.execute('show databases')
#        return
        try:
            self.cursorHandleMySQL.execute('show engines')
        except:             
            connectionFlag = 0

        return connectionFlag   # checkMySQLConnection
        
        
    def handlerLoginToExternalMailServer(self):
        '''
        Purpose:
            called only when the email server needs authentication
        '''
        if DEBUG_PRINT_METHOD:
            print('\n** In ' + MODULE + '/' + 'handlerLoginToExternalMailServer\n')
        
        user = self.usernameForMailServer
        pw = self.passwordForMailServer     # is blank for local mail server
        
        if user == '' and pw == '':
# assumed if user and pw are blank, user is already authenticated on a local mail server
            return
        
        '''
        if (
        self.mailServer == 'smtp.gmail.com:25'
        or
        self.mailServer == 'smtp.gmail.com'
        ):
        '''
# launch tls (Transport Layer Security) -- required by gmail, and ok to use with 
#   other mail servers;
#    tls: upgrades a plain text connection to a secure (TLS or SSL) connection
        try:
            self.connectMailServer.starttls()
        except:
            stringNoStartTls = (
                '\nCould not start TLS encryption on mail server:\n' +
                '  %s\n' +
                'Will still try to send email to user with this server.\n\n'
                )
            if DEBUG_PRINT_OUTPUT:
                print(stringNoStartTls)
            if self.fout:
                self.fout.write(stringNoStartTls)
# uncomment following only if it is desired NOT to send email when TLS encryption 
#   cannot be started
#            self.msgErrorString += stringNoSTartTls
#            return 1
     
# if we have a user and pw, try logging in.
# we may be already authenticated if this is a local mail server, so no need to login;
#   if this is true, we will not need a user and pw from the eCo-Pylot conf file
        if(
        (user <> '') 
        and 
        (pw <> '' and pw <> None)
        ):
            try:
                self.connectMailServer.login(user,pw)
                return 1
            except:
                stringFailureToAuthenticate = (
                    '\n>>> ERROR: Authentication to mail server %s failed.\n' +
                    '      user: %s\n' +
                    '      pw: %s\n'
                    ) % (
                    self.mailServer,
                    user,
                    pw
                    )
                if DEBUG_PRINT_OUTPUT:
                    print(stringFailureToAuthenticate)
                if self.fout:
                    self.fout.write(stringFailureToAuthenticate)
                self.msgErrorString += stringFailureToAuthenticate
                return 0

# return 1 for all other cases                
        return 1    # handlerLoginToExternalMailServer
                
        
# ===== main ===== # 
if __name__ == '__main__':

# define an actual email for 'practice' when this module is run in stand-alone mode
    msg_3_attachments = '''From dwbarne@sandia.gov  Sat Feb 19 09:07:06 2011
Return-Path: <dwbarne@sandia.gov>
Received: from mailgate.sandia.gov (mailgate.sandia.gov [132.175.109.1])
        by oso.sandia.gov (8.13.1/8.13.1) with ESMTP id p1JG76ZL000389
        for <mantevo-data@oso.sandia.gov>; Sat, 19 Feb 2011 09:07:06 -0700
Received: from mail.sandia.gov (cas2.sandia.gov [134.253.165.160])
        by mailgate.sandia.gov (8.14.4/8.14.4) with ESMTP id p1JG6rBB000554
        for <mantevo-data@oso.sandia.gov>; Sat, 19 Feb 2011 09:06:53 -0700
Received: from ES02SNLNT.srn.sandia.gov ([134.253.165.152]) by
 Cas2.srn.sandia.gov ([134.253.165.160]) with mapi; Sat, 19 Feb 2011 09:07:05
 -0700
From: "Barnette, Daniel W" <dwbarne@sandia.gov>
To: "mantevo_data@face.sandia.gov" <mantevo_data@face.sandia.gov>
Date: Sat, 19 Feb 2011 09:05:38 -0700
Subject: sandbox, attachment test 021911 9:06am
Thread-Topic: attachment test 021911 9:06am
Thread-Index: AQHL0E8MngVctp6F0ki6Ff6H4qHIYw==
Message-ID: <A4E091907CA41449A319E59C0F63A61221F940626E@ES02SNLNT.srn.sandia.gov>
Accept-Language: en-US
Content-Language: en-US
X-MS-Has-Attach: yes
X-MS-TNEF-Correlator:
acceptlanguage: en-US
Content-Type: multipart/mixed;
        boundary="_004_A4E091907CA41449A319E59C0F63A61221F940626EES02SNLNTsrns_"
MIME-Version: 1.0
X-PMX-Version: 5.6.0.2009776, Antispam-Engine: 2.7.2.376379, Antispam-Data: 2011.2.19.160019
X-PMX-Spam: Gauge=X, Probability=10%, Report='
 BASE64_ENC_TEXT 0.5, MIME_TEXT_ONLY_MP_MIXED 0.05, BODYTEXTP_SIZE_3000_LESS 0, BODY_SIZE_1900_1999 0, BODY_SIZE_2000_LESS 0, BODY_SIZE_5000_LESS 0, BODY_SIZE_7000_LESS 0, DATE_TZ_NA 0, FROM_NAME_PHRASE 0, TXT_ATTACHED 0, __CT 0, __CTYPE_HAS_BOUNDARY 0, __CTYPE_MULTIPART 0, __CTYPE_MULTIPART_MIXED 0, __HAS_MSGID 0, __MIME_TEXT_ONLY 0, __MIME_VERSION 0, __SANE_MSGID 0, __TO_MALFORMED_2 0, __TO_NO_NAME 0'

--_004_A4E091907CA41449A319E59C0F63A61221F940626EES02SNLNTsrns_
Content-Type: text/plain; charset="us-ascii"
Content-Transfer-Encoding: quoted-printable

body of attachment test 021911 9:06am for testing purposes of extracting at=
tached files.

line 2.

Line 3.=

--_004_A4E091907CA41449A319E59C0F63A61221F940626EES02SNLNTsrns_
Content-Type: text/plain; name="attach_1.txt"
Content-Description: attach_1.txt
Content-Disposition: attachment; filename="attach_1.txt"; size=118;
        creation-date="Sat, 19 Feb 2011 09:05:49 GMT";
        modification-date="Sat, 19 Feb 2011 09:05:49 GMT"
Content-Transfer-Encoding: base64

TGluZSAwDQphdHRhY2htZW50IGZpbGU6IGF0dGFjaF8xLnR4dA0KVGhpcyBpcyBhIHRlc3QgZmls
ZSBmb3IgYXR0YWNobWVudDogTGluZSAxDQpMaW5lIDINCg0KTGluZSAzDQoNCkxpbmU0DQoNCkxp
bmUgNQ==

--_004_A4E091907CA41449A319E59C0F63A61221F940626EES02SNLNTsrns_
Content-Type: text/plain; name="attach_2.txt"
Content-Description: attach_2.txt
Content-Disposition: attachment; filename="attach_2.txt"; size=118;
        creation-date="Sat, 19 Feb 2011 09:05:56 GMT";
        modification-date="Sat, 19 Feb 2011 09:05:56 GMT"
Content-Transfer-Encoding: base64

TGluZSAwDQphdHRhY2htZW50IGZpbGU6IGF0dGFjaF8yLnR4dA0KVGhpcyBpcyBhIHRlc3QgZmls
ZSBmb3IgYXR0YWNobWVudDogTGluZSAxDQpMaW5lIDINCg0KTGluZSAzDQoNCkxpbmU0DQoNCkxp
bmUgNQ==

--_004_A4E091907CA41449A319E59C0F63A61221F940626EES02SNLNTsrns_
Content-Type: text/plain; name="attach_1.txt"
Content-Description: attach_1.txt
Content-Disposition: attachment; filename="attach_1.txt"; size=118;
        creation-date="Sat, 19 Feb 2011 09:06:04 GMT";
        modification-date="Sat, 19 Feb 2011 09:06:04 GMT"
Content-Transfer-Encoding: base64

TGluZSAwDQphdHRhY2htZW50IGZpbGU6IGF0dGFjaF8xLnR4dA0KVGhpcyBpcyBhIHRlc3QgZmls
ZSBmb3IgYXR0YWNobWVudDogTGluZSAxDQpMaW5lIDINCg0KTGluZSAzDQoNCkxpbmU0DQoNCkxp
bmUgNQ==

--_004_A4E091907CA41449A319E59C0F63A61221F940626EES02SNLNTsrns_--
    '''
    
# choose which msg, if there are more than one
    msg = msg_3_attachments
# instantiate class
    app = EmailParser(msg)
    app.exit_eCo_Pylot('EmailParser')
    
    app.readConfigureFileForEcoPylot()
    app.exit_eCo_Pylot('readConfigureFileForEcoPylot')
    
    app.mySQLConnect()
    app.exit_eCo_Pylot('mySQLConnect')
    
    app.parse()
    app.exit_eCo_Pylot('parse')
    
    app.send2db()
    app.exit_eCo_Pylot('send2db')
    
    app.email2user()
    app.exit_eCo_Pylot('email2user')
    
    app.trackUsage()
    app.exit_eCo_Pylot('trackUsage')
    
    app.exit_eCo_Pylot('finished')
    

