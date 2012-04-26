# email 'from' and 'text' box
#
# from Programming Python, p. 314, highly modified
#  date: 062608

import sys
from Tkinter import *
import tkFont
from tkMessageBox import *
import smtplib      # for sending emails
import time         # for putting date & time on emails
import string       # to clean up emailTo list
import os           # to get username
import socket       # for error msg if server cannot connect
import Pmw          # for comboboxes, etc.
import yaml         # for reading list of mail servers

# debugging
DEBUG = 0       # for printing selected variables
DEBUG_SERVERS = 0   # = 1 prints list of servers defined in email_dialog.conf file

# list of mail servers;
#   most mail servers will require authentication via login, unless user
#   is already logged in to the domain

# environment parameters
if os.name == 'nt':
    userName = os.environ['USERNAME']
elif os.name == 'posix':
    userName = os.environ['USER']
else:
    try:
        userName = os.environ['USER']
    except:
        userName = 'UNK'
        
if userName == 'UNK':
    print('\nself.userName = %s' % userName)
    print(
        'This is not an acceptable username for PylotDB to continue.\n\n' +
        'Check coding in module "email_dialog.py".\n\n' +
        'PylotDB must quit.\n\n'
        )
    sys.exit()

# if posix (any *nix version), find which directory pylot.py is in, so that
#   the email ".conf" file can be written to the subdirectory "Modules"  
if os.name == 'posix':
    pylotdbHomeDir = ''
    homeDir = '/home/' + userName
    file2find = 'pylotdb.py'
    foundPylotDB = 0
# do a directory tree walk, starting in home directory
    for root, dirs, files in os.walk(homeDir):
            for file in files:
                if file2find == file:
                    pylotdbHomeDir = root + '/'
                    foundPylotDB = 1
                    break
            if foundPylotDB:
                break

# for windows, just use current directory; will be ok most of the time, unless
#   an alias is used for "pylot.py"
else:
    pylotdbHomeDir = './'
            
if pylotdbHomeDir == '':
    stringNoPylotDBHomeDir = (
        'No home directory was found for pylotdb.py\n\n' + 
        'This should not have happened, since pylotdb is running!\n\n' +
        'Please contact code administrator with this error.'
        )
    print(stringNoPylotDBHomeDir)
    self.MySQL_Output(
        0,
        stringNoPylotDBHomeDir
        )
    showerror(
        'PylotDB home dir not found',
        stringNoPylotDBHomeDir
        )
    sys.exit()
               
else:
    print('\nOS type: '),
    print(os.name)
    print('pylotdbHomeDir: '),
    print(pylotdbHomeDir)

# read list of mail servers from file email_dialog.conf
email_dialogDotconf = pylotdbHomeDir + 'Modules/email_dialog.conf'
try:
    fileConf = open(email_dialogDotconf,'r')
    fileConfExists = 1
except: # email_dialogDotconf does not exist
    try:
        fileConf = open(email_dialogDotconf,'w')
    except:
# if file does not exist, define empty list of mail servers
        stringFileNotFound = (
            '\nFile %s for defining parameters for help email sent\n' +
            'using PylotDB was not found and/or could not be written.\n\n' +
            'Hence, the list of help-email mail servers is empty. User\n' +
            'will need to manually input an available mail server.'
            ) % (
            email_dialogDotconf
            )
        print(stringFileNotFound)
        fileConfExists = 0
        mailServers = []
    else:
# write generic mail servers to file so we'll have something to work with;
#  these will be in yaml format for a list
        fileConf.write(
            '# file: email_dialog.conf\n' +
            '# called by: email_dialog.py\n' +
            '# author: Daniel W. Barnette, dwbarne@sandia.gov\n' +
            '# date created: May 2011 with modifications made afterward\n' +
            '\n' +
            '# COMMENTS\n' +
            '# 1. email servers for program "email_dialog.py" that is called\n' +
            '#    by "pylotdb.py"; used when users want to send email to \'help administrator\'.\n' +
            '# 2. Format:\n' +
            '#    " - domain/name_of_mail_server:port"  (without quotes, of course;\n' +
            '#          see examples below)\n' +
            '# 3. MySQL\'s "port" defaults to the number 25.\n' +
            '# 4. a) Place the mail server you want as default at the top of the list.\n' +
            '#     b) The top value will be the default server value displayed\n' +
            '#       in the email window in pylotdb.py.\n' +
            '#    c) If you are on a company network, for example, this will\n' +
            '#       typically be your local email server.\n' +
            '#    Example:\n' +
            '#    email_servers:\n'+
            '#      - gmail.com/smtp.gmail.com:25\n' +
            '#      - earthlink.net/smtp.gmail.com:25\n' +
            '#      - microsoft.com/smtp.live.com:25\n' +
            '#      - yahoo.com/smtp.mail.yahoo.com:25\n' +
            '\n' +
            '# PYLOTDB\'s HELP EMAIL ADDRESS\n' +
            '\n' +
            'email_for_help:\n' +
            '- pylotdb-help@sandia.gov\n' +
            '\n' +
            '# MAIL SERVER LIST - SOME VALUES MIGHT BE SITE DEPENDENT\n' +
            '\n' +
            'email_servers:\n' +
            ' - sandia.gov/mail.sandia.gov:25\n' +
            ' - earthlink.net/smtp.earthlink.net:25\n' +
            ' - gmail.com/smtp.gmail.com:25\n' +
            ' - microsoft.com/smtp.live.com:25\n' +
            ' - yahoo.com/smtp.mail.yahoo.com:25'
            )
        fileConf.close()
        fileConf = open(email_dialogDotconf,'r')
        fileConfExists = 1

# check if file is in yaml format
if fileConfExists:
    try:
        mailConfData = yaml.load(fileConf)
    except:
        mailConfData = ''
        stringNotYamlFile = (
            'The file %s was found for reading in the help email address\n'
            'and the list of mail servers, but it is apparently not in\n' +
            'yaml format.\n\n' +
            'Yaml format requires lines like this:\n' +
            'email_servers:\n' +
            ' - gmail.com/smtp.gmail.com:25\n\n' +
            'Since PylotDB will not overwrite the existing file, and\n' +
            'since the file contents are not in the proper format\n' + 
            'the list of mail servers will be empty. User will need\n' +
            'to input desired server if sending help email from PylotDB.'
            ) % (
            email_dialogDotconf
            )
        print(stringNotYamlFile)
        showinfo(
            'Info: improperly formatted input file -- non-fatal',
            stringNotYamlFile
            )
# file was not in yaml format, so just define empty list of mail servers
        mailServers = []
        emailForHelp = 'pylotdb-help@sandia.gov'
        
else:
    mailConfData = ''
    mailServers = []
    emailForHelp = 'pylotdb-help@sandia.gov'
        
# if fileConf is open, close it
try:
    fileConf.close()
except:
    pass

# extract email server names and email address for help
if mailConfData:
    for (key,value) in mailConfData.iteritems():
        if key == 'email_servers':
            mailServers = value
        if key == 'email_for_help':
            emailForHelp = value[0]
        
if DEBUG_SERVERS:
    stringServers = (
        '\nList of mail servers from file "Modules/email_dialog.conf":\n%s'
        ) % (
        mailServers
        )
    print(stringServers)
    stringHelpFile = (
        '\nEmail address for help: %s'
        ) % (
        emailForHelp
        )
    print(stringHelpFile)

#makemodal = (len(sys.argv) > 1)
#print "len(sys.argv) =",len(sys.argv)

class SendEmail(Frame):
    def __init__(self, windowEmail):
        self.windowEmail = windowEmail
        Frame.__init__(self,self.windowEmail)
        self.grid(columnspan=10)
        if os.name == 'nt':
            self.userName = os.environ['USERNAME']
        elif os.name == 'posix':
            self.userName = os.environ['USER']
        else:
            try:
                self.userName = os.environ['USER']
            except:
                self.userName = 'UNK'
                
# define mail servers
        self.listMailServers = mailServers
# define email address for help
        self.emailForHelp = emailForHelp
        
# define data font
        self.dataFont = tkFont.Font(
            family="Arial",
            size="8",
            weight='normal'
            )
# define button font
        self.buttonFont = tkFont.Font( 
            family="Arial",
            size="8",
            weight='normal'
            )
# define entry font			
        self.entryFont = tkFont.Font( 
            family="Arial",
            size="10",
            weight='normal'
            )
# define label font 
        self.labelFont = tkFont.Font(
            family='Courier',
            size='8',
            weight='normal'
            )
# define small button font
        self.buttonFontSmall = tkFont.Font(
            family='arial',
            size='8',
            )
# start making widgets!
        self.createEmailWidgets()  

# ===== end of __init__  =====   


    def createEmailWidgets(self):  
        '''
        Purpose:
            Create all the email widgets
        '''
        
# = = = = FRAMES = = = =

# create frame for TOP widgets  
        rowCount = 0
        self.frameTopEmail=Frame(
            self.windowEmail,
            )
        self.frameTopEmail.grid(
            row=0,
            column=0,
            padx=10,
            pady=5,
            sticky=W,
            )
            
# frame for mail server selection and login
        rowCount += 1
        self.frameMailServer = Frame(
            self.windowEmail,
            )
        self.frameMailServer.grid(
            row=rowCount,
            column=0,
            padx=10,
            pady=5,
            sticky=W,
            )
        
# create frame for MIDDLE widgets
        rowCount += 1
        self.frameMiddleEmail=Frame(
            self.windowEmail,
            )
        self.frameMiddleEmail.grid(
            row=rowCount,
            column=0,
            padx=10,
            pady=5,
            sticky=W,
            )
            
# create separate frame for CHECKBUTTON
        rowCount += 1
        self.frameCheckButton=Frame(
            self.windowEmail,
            )
        self.frameCheckButton.grid(
            row=rowCount,
            column=0,
            padx=10,
            pady=5,
            sticky=W,
            )
        
# create frame for BOTTOM widgets
        self.frameBottomEmail=Frame(
            self.windowEmail,
            )
        self.frameBottomEmail.grid(
            row=99,
            column=0,
            padx=10,
            pady=5,
            sticky=W,
            )
            
            
# = = = = WIDGETS = = = =
# TOP FRAME
       
# FROM, TO, and SUBJECT text box
#    From
        self.labelFromBox=Label(
            self.frameTopEmail,
            text="From: ",
            font=self.dataFont,
            justify=RIGHT
            )
        self.labelFromBox.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky=E,
            )
#   To
        self.labelToBox=Label(
            self.frameTopEmail,
            text="To: ",
            font=self.dataFont,
            height=3,
            )
        self.labelToBox.grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky=E,
            )
#    Subject           
        self.labelSubjectBox=Label(
            self.frameTopEmail,
            text="Subject: ",
            font=self.dataFont,
            )
        self.labelSubjectBox.grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky=E,
            )
            

# Create entry fields      
#    From     
        self.entryFromBox=Entry(
            self.frameTopEmail,
            width=45,
            )
        self.entryFromBox.grid(
            row=0,
            column=1,
            sticky=W,
            padx=5,
            pady=5,
            )
        self.entryFromBox.insert(
            INSERT,
            self.userName
            )

# To
        self.textToBox=Text(
            self.frameTopEmail,
            width=45,
            height=3
            )
        self.textToBox.grid(
            row=1,
            column=1,
            sticky=W,
            padx=5,
            pady=5,
            )
        self.textToBox.insert(
            INSERT,
#            "pylotdb-help@sandia.gov,"
            self.emailForHelp,
            )         
# Label for additional email addresses
        self.labelToAdditionsBox=Label(
            self.frameTopEmail,
            text=(
                "Separate additional\n"
                +"email addresses\n"
                +"by commas"
                ),
            font=self.dataFont,
            justify=LEFT
            )
        self.labelToAdditionsBox.grid(
            row=1,
            column=2,
            padx=0,
            pady=0,
            sticky=W,
            )
            
# Subject
        self.entrySubjectBox=Entry(
            self.frameTopEmail,
            width=45,
            )
        self.entrySubjectBox.grid(
            row=2,
            column=1,
            padx=5,
            pady=5,
            sticky=W,
            )
        self.entrySubjectBox.insert(
            0,
            "PYLOTDB problems, concerns and/or comments"
            )
            
# MAIL SERVER FRAME
# ... label for selecting/entering server
        label = Label(
            self.frameMailServer,
            text=(
                '   Select/enter mail server:\n' +
                '(format: domain/server:port)'
                ),
            justify=RIGHT,
            )
        label.grid(
            row=0,
            column=0,
            pady=5,
            padx=2,
            sticky=E,
            )
# ... combobox for selecting/entering server
        self.comboboxSelectMailServer = Pmw.ComboBox(
            self.frameMailServer,
            scrolledlist_items=self.listMailServers,
            listheight=100,
            entry_state='normal',
            entry_width=30,
            entry_background='white',
            entry_foreground='black',
            entry_relief=FLAT,
            scrolledlist_hull_width=500,
            )
        self.comboboxSelectMailServer.grid(
            row=0,
            column=1,
            pady=5,
            padx=2,
            sticky=W,
            )
        if self.listMailServers <> []:
            self.comboboxSelectMailServer.selectitem(0)
        else:
            self.comboboxSelectMailServer.setentry('')
            
# clear MailServer  
        buttonClearSelectMailServer = Button(
            self.frameMailServer,
            text='Clear',
            font=self.buttonFontSmall,
            borderwidth=3,
            relief=RAISED,
            width=8,
            background='white',
            foreground='blue',
            command=self.handlerClearSelectMailServer,
            )
        buttonClearSelectMailServer.grid(
            row=0,
            column=2,
            padx=5,
            pady=0,
            sticky=W,
            )         
     
# ... label for user entry
        label = Label(
            self.frameMailServer,
            text=' username for mail server:\n(if needed)',
            justify=RIGHT,
            )
        label.grid(
            row=1,
            column=0,
            pady=5,
            padx=2,
            sticky=E,
            )
# user entry for mail server
        self.varEntryMailServerUserName = StringVar()
        self.entryMailServerUserName = Entry(
            self.frameMailServer,
            textvariable=self.varEntryMailServerUserName,
            width=15,
            )
        self.entryMailServerUserName.grid(
            row=1,
            column=1,
            padx=0,
            pady=5,
            sticky=W,
            )
        '''
        self.entrySubjectBox.insert(
            0,
            "PYLOT concerns"
            )
        '''
# ... label for password entry
        label = Label(
            self.frameMailServer,
            text=(
                'password for mail server:\n(if username needed)'
                ),
            justify=RIGHT,
            )
        label.grid(
            row=2,
            column=0,
            pady=5,
            padx=2,
            sticky=E,
            )
# password entry for mail server
        self.varEntryMailServerPassWord = StringVar()
        self.entryMailServerPassWord = Entry(
            self.frameMailServer,
            textvariable=self.varEntryMailServerPassWord,
            width=15,
            show='*'
            )
        self.entryMailServerPassWord.grid(
            row=2,
            column=1,
            padx=0,
            pady=5,
            sticky=W,
            ) 

# MIDDLE FRAME

# MESSAGE box 
        label = Label(
            self.frameMiddleEmail,
            text='Message:',
            )
        label.grid(
            row=0,
            column=0,
            padx=0,
            pady=0,
            sticky=W,
            )
# set up scroll bars
        yScroll=Scrollbar(
            self.frameMiddleEmail,
            orient=VERTICAL
            )
        yScroll.grid(
            row=1,  
            column=1,
            sticky='NS',
            pady=5,
            padx=1,
            ) 
        self.textMessageBox=Text(
            self.frameMiddleEmail,
            font=self.entryFont,
            borderwidth=5,
            relief=RIDGE,
            wrap=WORD,
            height=15,
            width=80,
            bg='white',
            yscrollcommand=yScroll.set
            )
        self.textMessageBox.grid(
            row=1, 
            column=0, 
            padx=5,
            pady=5,
            sticky=NSEW,
            )
 
#        yScroll["command"]=self.textMessageBox.yview
        yScroll.configure(command=self.textMessageBox.yview)
        '''
        self.textMessageBox.insert(
            INSERT,
            "<Enter email message here; \nalso change above email address to pylotdb-help.sandia.gov> "
            )
        '''
            
# CHECKBUTTON FRAME

# copy of email is sent to sender unless following box is checked 
        msgCheckButton='Do NOT send this email to me'
        self.varCheckButton = IntVar()
        self.checkButtonNotMe=Checkbutton(
            self.frameCheckButton, 
            text=msgCheckButton,
            variable=self.varCheckButton,
            command=self.handlerCheckButton,
            justify=LEFT,
            font=self.dataFont,
            padx=5,
            pady=5,
            )
        self.checkButtonNotMe.grid(
            row=0,
            column=0,
            padx=15,
            pady=2,
            )

# BOTTOM FRAME            
                    
# SEND email button
        self.sendEmailButton = Button(
            self.frameBottomEmail,
            font=self.dataFont,
            text='SEND EMAIL',
            command=self.handlerEmailSendButton,
            relief=RAISED,
            borderwidth=5,
            )
        self.sendEmailButton.grid(
            row=0, 
            column=0,
            padx=5,
            pady=2,
            )
#QUIT email button
        self.cancelEmailButton = Button(
            self.frameBottomEmail, 
            font=self.dataFont,
            text='Quit email', 
            command=self.handlerQuit,
            relief=RAISED,
            borderwidth=5,
            )
        self.cancelEmailButton.grid(
            row=0, 
            column=1,
            padx=20,
            pady=2,
            )
        
# place focus on the 'win' window
#        self.focus_set()
#        self.grab_set()
#        self.wait_window()

        return

# ===== end of createEmailWidgets =====

    
    def handlerClearSelectMailServer(self):
        '''
        Purpose:
            clear the mail server entry widget
        '''
        self.comboboxSelectMailServer.setentry('')
        
        return
    

    def handlerCheckButton(self):
        '''
        Purpose:
            if checkbutton is checked, do not
            send a copy of the email to user.
        '''
        
        self.doNotSend=self.varCheckButton.get()
        
        if self.doNotSend:
            print "\nINFO: email will NOT be sent to your inbox"
        else:
            print "\nINFO: email will be sent to your inbox"
            
        return
        
    
    def handlerEmailSendButton(self):
        '''
        Purpose:
            check email list; check mail server
        '''
        if DEBUG:
            print " *** method: handlerEmailSendButton ***"
# define servers in dictionary(key,value) to search for and attempt login if found
# Reference:
#   http://www.realifewebdesigns.com/web-resources/pop3-smtp.html
            
# repair email headers
        success = self.formatEmail()
        if not success: 
            return
        
# at this point, all necessary fields have values except 
#   possibly the mail server username and password
        '''
        try:
            (self.key,self.server) = self.searchEmailServer()
        except ValueError:
            print '\n>>> No email servers found!'   
            print '    ... Could be servers are too slow to respond, or' 
            print '    ... maybe just a bad connection.'
            print '    ... Try again.\n'
            showerror(
                'No servers found...', \
                'No servers found\n' +
                'Could be servers are too slow to respond, or\n' +
                'maybe just a bad connection.\n' +
                'Try again...'
                )
            return
        '''
        
# clean up email addresses as required by the server
#        self.cleanupEmailAddresses()

# join email list with semi-colons; if this does not work,
#  try joining them with commas; it's usually one or the other
#        self.emailToJoinedWithSemicolon = ';'.join(self.emailTo)
        if self.emailFrom[0].count('@') == 0:
            self.entryFromBox.delete(0,END)
            self.entryFromBox.insert(
                INSERT,
                self.userName + '@' + 
                self.comboboxSelectMailServer.get().split('/')[0]
                )
            self.emailFrom = self.entryFromBox.get()
            
        successfulSend = self.sendEmail(self.emailTo)
        
        return
           
# ===== end of handlerEmailSend =====
        
        
    def formatEmail(self):
        '''
        Purpose:
            get values from entry window and modify according to some 
            canonical form
        '''
        self.emailFrom = self.entryFromBox.get()
        self.emailTo = self.textToBox.get(1.0,END)
        self.emailSubject = self.entrySubjectBox.get()
        self.emailMessage = self.textMessageBox.get(1.0,END)
        self.emailDate = time.ctime(time.time())
        
        self.myMailServer = self.comboboxSelectMailServer.get().strip()
# these can be blank if already auto-logged-in to a local server
        self.myMailServerUserName = self.entryMailServerUserName.get().strip()
        self.myMailServerPasWord = self.entryMailServerPassWord
        
        stringEmptyFields = ''
        
        if(
        self.emailFrom == ''
        or
        self.emailTo == ''
        or
        self.emailSubject == ''
        or 
        self.emailMessage == ''
        or
        self.myMailServer == ''
        ):
            if self.emailFrom == '':
                stringEmptyFields += (
                    '\n - From:'
                    )
            if self.emailTo == '':
                stringEmptyFields += (
                    '\n - To:'
                    )
            if self.emailSubject == '':
                stringEmptyFields += (
                    '\n - Subject'
                    )
            if self.emailMessage == '':
                stringEmptyFields += (
                    '\n - Message'
                    )
            if self.myMailServer == '':
                stringEmptyFields += (
                    '\n - Mail server'
                    )
                    
        if stringEmptyFields <> '':
            stringFieldsToCorrect = (
                'The following empty fields need attention:\n\n' +
                stringEmptyFields
                )
            print(stringFieldsToCorrect)
            showerror(
                'Error: empty fields',
                stringEmptyFields
                )
            return 0    # failed
            
# determine how many email addresses based on separator being 
#  whitespace, commas, or semicolons
        lenDueToWhiteSpace=len(self.emailTo.split())
        lenDueToComma=len(self.emailTo.split(','))
        lenDueToSemiColon=len(self.emailTo.split(';'))
        self.emailEntries=max(lenDueToWhiteSpace,lenDueToComma,lenDueToSemiColon)
# save separator
        separator=1   # default to whitespace
        if lenDueToComma > lenDueToWhiteSpace: separator=2
        if lenDueToSemiColon > max(lenDueToComma,lenDueToWhiteSpace): separator=3
        
# split email address list
        if separator==1:
            print "\n INFO: separate email addresses based on whitespace..."
            self.emailTo=self.emailTo.split()
        elif separator==2:
            print "\n INFO: separate email addresses based on commas..."
            self.emailTo=self.emailTo.split(',')
        elif separator==3:
            print "\n INFO: separate email addresses based on semicolons..."
            self.emailTo=self.emailTo.split(';')
        else:
            stringCheckSeparator = (
                "\n ** Fatal Error in email address list - check separator!\n"
                )
            print(stringCheckSeparator)
            showerror(
                'Error: check separator',
                stringCheckSeparator
                )
            return 0    # failed

#Debug
        if DEBUG:
            print("\nbefore filtering - self.emailTo = %s" % self.emailTo)
            print("         len(emailTo) = %s" % len(self.emailTo))
        
# remove blank email addresses
        indexToRemoveBlankAddresses = []
        for index in range(len(self.emailTo)):
            if self.emailTo[index] == '':
                indexToRemoveBlankAddresses.append(index)
                
        if len(indexToRemoveBlankAddresses) > 0:
            for index in indexToRemoveBlankAddresses:
                self.emailTo.remove(self.emailTo[index])
            
#Debug
        if DEBUG:
            print("\nafter filtering - self.emailTo = %s" % self.emailTo)
            print("  len(emailTo) = %s" % len(self.emailTo))
        
# how many @'s in emailTo
        self.atCount=0
        for index in range(len(self.emailTo)):
            self.atCount+=self.emailTo[index].count('@')
            
#DEBUG
        if DEBUG:
            print("\nself.emailTo, atCount = %s, %s" % (self.emailTo,self.atCount))
        
# check if any special characters in email list elements, 
#   including separators used above (the one used will not 
#   show up in the individual entries).
# This implies that the same separator must be used to 
#   separate all email addresses in the main entry window!
        charList1=[ '#', ',', '!', '$', '^', '&', '*', '(', ')', '+', '=', '{']
        charList2=['}', '[', ']', '|', '\\', '/', ":", "?", '>', "<", "`", " ","\n"]
        charList=charList1 + charList2
        
# remove any special characters, but we will later check for them again
        icount = 0
        for index in range(len(self.emailTo)):
            for char in charList:
                if self.emailTo[index].count(char) > 0:
                    self.emailTo[index] = self.emailTo[index].replace(char,'')
                    if DEBUG:
                        icount += 1
                        print('\n%s. replaced character \'%s\' in email address %s' 
                            % (
                            icount,
                            char,
                            self.emailTo[index]
                            )
                            )
            
        specialCharactersInEmailAddresses=0
        
#Debug
        if DEBUG:
            print("\nself.emailTo = %s" % self.emailTo)

# if any special characters found now, email process stops for user to correct addresses            
        for index in range(len(self.emailTo)):
            specialCharacterCount=0
            for char in charList:
                specialCharacterCount=self.emailTo[index].count(char)
                if specialCharacterCount != 0:
                    print "\n >> There are %s special characters ( %s ) in %s\n" % \
                        (specialCharacterCount,char,self.emailTo[index])
                    specialCharactersInEmailAddresses+=specialCharacterCount
                
        if specialCharactersInEmailAddresses != 0:    
            print(
                "\n ERROR: A total of %s special characters were found\n" +
                "in the email addresses."
                ) % (
                specialCharactersInEmailAddresses
                )
            print "\n   Please correct these before continuing...\n"
            showerror(
                'Error: special characters in email addresses',
                'Special or extraneous characters in email addresses\n' +
                'are not allowed!\n' +
                'Please re-enter the "To:" email address(es)'
                )
# we don't know how to handle special characters embedded in an email address, so just return and let user take care of problem
            return 0    # failed
                

# check input
        if not self.emailFrom:
            print(
                "The 'From:' field is empty!\n" +
                "Please enter your email address and try again."
                )
            showerror(
                'No "From:" email address',
                'The "From:" field is empty!\n' +
                'Please enter your email address and try again.'
                )
        elif not self.emailTo:
            print(
                "The 'To:' field is empty!\n" +
                "Please enter the recipient's email address"
                )
            showerror(
                'No "To:" email address',
                'The "To:" field is empty!\n' +
                'Please enter the recipient\'s email address.'
                )
        elif not self.emailSubject:
            print(
                "The 'Subject:' field is empty!\n" + 
                "Please enter the relevant subject."
                )
            showerror(
                'No "Subject:" entry',
                'The "Subject:" field is empty!\n' +
                'Please enter the relevant subject.'
                )
# check for @ count in emailTo
        elif self.atCount == 0:
            print(
                "No '@' in any address!\n" +
                "Please re-enter email address(es) separated by commas,\n" +
                "semicolons, or spaces."
                )
            showerror(
                'Invalid "To:" email address(es)',
                'No "@" in any address!\n' +
                'Please re-enter email address(es) separated by commas,\n' +
                'semicolons, or spaces.'
                )
#        elif len(emailTo.split()) == 1:
# make sure @ counts match number of email entries
        elif self.atCount != self.emailEntries:
            print(
                "Number of '@'s don't match number of email address!\n" +
                "Please re-enter email address(es)."
                )
            showerror(
                'Invalid "To:" email address(es)',
                'Number of "@"s don\'t match number of email addresses!\n' +
                'Please re-enter email address(es).'
                )
            if DEBUG:
                print "    *** Number of @'s =",self.atCount
                print "         Number of emailEntries =",self.emailEntries

        else:
# first, cleanup emailTo in case of multiple recipients
#   no matter what separator is used, use semi-colons as universal separators

# check for invalid email entries, but try to save others in the list
            indexToRemove = []
            for index in range(len(self.emailTo)):
# check for length of each entry
                if len(self.emailTo[index]) <= 5:
                    print(
                        "\n  > Removing invalid email address from list - too short:\n%s"
                        % self.emailTo[index]
                        )
                    indexToRemove.append(index)
#                    self.emailTo.remove(self.emailTo[index])
# check for too many @s in each entry
                elif self.emailTo[index].count('@') > 1:
                    print(
                        "\n > Removing invalid email address from list - too many '@'s:\n%s" 
                        % self.emailTo[index]
                        )
                    indexToRemove.append(index)
#                    self.emailTo.remove(self.emailTo[index])
# check for whitespace in each entry
                elif self.emailTo[index].count(' ',1,len(self.emailTo[index])-1) > 0:
                    print(
                        "\n > Removing invalid email address from list - invalid whitespace:\n%s"
                        % self.emailTo[index]
                        )
                    indexToRemove.append(index)
#                    self.emailTo.remove(self.emailTo[index])
# can also just remove white space
#                    self.emailTo.replace[' ','']
                else:
                    print(
                        "\n > #%s. Email address appears to be valid:\n%s" 
                        % (index+1,self.emailTo[index])
                        )
                
# in the unlikely event all email addresses have been removed...                
            if len(self.emailTo) == 0:
                print "\nThere are no valid email addresses!"
                print "\n  Try again..."
                showerror(
                    'No valid email addresses',
                     'There are no valid email addresses!\n\n' +
                     'Please try again.'
                     )
                return 0
                
# remove any bad addresses so we can keep going
            if len(indexToRemove) > 0:
                for index in indexToRemove:
                    self.emailTo.remove(self.emailTo[index])
                
# see how many email addresses after cleaning out junk
            print(
                "\nAfter filtering, number of email addresses that appear valid: %s\n" 
                % len(self.emailTo)
                )
                
            print('\nFinal email list:\n%s\nType(self.emailTo) = %s' 
                % (
                self.emailTo,
                type(self.emailTo)
                )
                )
            
# join all email addresses as one string separated by semicolons, 
#   regardless of what separator was used by user
#   depends on server!
# DON'T USE THIS APPROACH -- turns list into a string, and sendmail wants a list for mailing addresses
#            if len(self.emailTo) > 1:
#                self.emailTo=';'.join(self.emailTo)

# print headers as they will 'almost' appear in email     
#   have left to do:
#         1. append email domain to user name in emailFrom; have to determine which server will login to first, though.     
            print " From:",self.emailFrom
            print " To:",self.emailTo
            print " Date:",self.emailDate
            print " Subject:",self.emailSubject
            print " Message:\n",self.emailMessage
            print " -- end of Message -- \n"
            print "\n >>> email input is ready\n"
            
# indicate email address ready
            return 1
           
# ===== end of formatEmail =====

# example for "smtp.gmail.com" gmail server
# >>> import smtplib
# >>> s = smtplib.SMTP('smtp.gmail.com:25')
# >>> s.starttls()
# >>> s.login('user@gmail.com','pw')
# >>> msg = """\
# ... From: dwbarne@gmail.com
# ... To: dwbarne@sandia.gov
# ... Subject: test
# ...
# ... this is a test @ 1247 on Tue
# ... """
# >>> s.sendmail('dwbarne@gmail.com','dwbarne@sandia.gov', msg)
# {}
# >>> s.quit()

          
            
    def searchEmailServer(self):
        '''
        Purpose:
            cycles through email servers until one is found;
            this is not currently used since a connection can
            be made to some servers requiring authentication or
            to a local server for which the user has already
            been authenticated; user can also connect to a 
            server for which no account exists which is determined
            later. All of this implies messy logic.
        '''
# search for email server 
        success=0
        for serverTemp in self.listMailServers:
            server = serverTemp.split('/')[1]
            try:
                print "\n\n>>> Trying to connect to email server for",key
                print "         Server name:",server
                self.emailServer=smtplib.SMTP(server)
            except smtplib.SMTPConnectError:   
                print ">>>   .... SMTPConnectError - server not available."
                print ">>>          server = ",server
                print ""
            except smtplib.SMTPServerDisconnected:
                print ">>>   .... SMTPServerDisconnected - could not connect."
            except (socket.gaierror, socket.error, socket.herror, \
                    smtplib.SMTPException), e:
                print ">>> ... socket error -- may be bad connection\n>>> ......continuing"
            except:
                print ">>> ... unknown connection error -- continuing" 
            else:
                success=1
# no exceptions have occurred, so try to login to emailServer
                if key == 'Earthlink':
                    self.emailServer.ehlo(server)
                elif key == 'Gmail':
                    self.emailServer.starttls()
                break

        if success:
            print "\n>>> CONNECT_SUCCESS: you are connected to the %s email server" % key
            return (key,server)
        else:
            print "\n ERROR: cannot find any email server!"
            return ''

# ===== end of searchEmailServer =====                

                        
    def boxLogin(self):
        '''
        Purpose:
            login window; not used
        '''
# popup login box
        self.winLoginBox=Toplevel(takefocus=1)
        self.winLoginBox.title(self.key + ' Login Box')
        self.winLoginBox.grid()
        self.winLoginBox.transient(self.frameTopEmail)
        x_Windows=100
        y_Windows=200
        self.winLoginBox.geometry(
            '+%d+%d' % (x_Windows, y_Windows)
            )
# Username box
        rowx=0
#
        self.loginboxTopLable=Label(
            self.winLoginBox,
            text="Login to " + self.key,
            font=self.labelFont
            )
        self.loginboxTopLable.grid(
            row=rowx,
            column=1,
            padx=5,
            pady=5,
            sticky=W
            )
        
        rowx+=1
        self.loginboxLabelUser=Label(
            self.winLoginBox,
            text="   User:",
            font=self.labelFont,
            )
        self.loginboxLabelUser.grid(
            row=rowx,
            column=0,
            padx=5,
            pady=5,
            sticky=E,
            )

        self.loginboxEntryUser=Entry(
            self.winLoginBox,
            width=30,
            font=self.labelFont
            )
        self.loginboxEntryUser.grid(
            row=rowx,
            column=1,
            sticky=W,
            padx=5,
            pady=5,
            )

# PW box 
        rowx+=1
        self.loginboxLabelPW=Label(
            self.winLoginBox,
            text=" Password: ",
            font=self.labelFont
            )
        self.loginboxLabelPW.grid(
            row=rowx,
            column=0,
            padx=5,
            pady=5,
            sticky=E,
            )

        self.loginboxEntryPW=Entry(
            self.winLoginBox,
            width=30,
            font=self.labelFont,
            show='*'
            )
        self.loginboxEntryPW.grid(
            row=rowx,
            column=1,
            sticky=W,
            padx=5,
            pady=5,
            )

# OK login button
        rowx+=1
        self.loginboxOkLoginButton = Button(
            self.winLoginBox,
            font=self.buttonFont,
            text='OK',
            command=self.handlerLoginBoxOK
            )
        self.loginboxOkLoginButton.grid(
            row=rowx, 
            column=0,
            padx=5,
            pady=5,
            sticky='E',
            )
#CANCEL login button
        self.loginboxCancelLoginButton = Button(
            self.winLoginBox, 
            font=self.buttonFont,
            text='Cancel', 
            command=self.handlerLoginBoxCancel
            )
        self.loginboxCancelLoginButton.grid(
            row=rowx, 
            column=1,
#                            sticky='E',
            )
                            
# ===== end of boxLogin =====

    def cleanupEmailAddresses(self):
        '''
        Purpose:
            NOT USED
            join email list together, with separator determined by server
        '''
        if self.key == 'Sandia': 
            ';'.join(self.emailTo)
# attach extension to username now that server is known, if not done already
            if self.emailFrom[0].count('@') == 0:
                self.entryFromBox.delete(0,END)
                self.entryFromBox.insert(
                    INSERT,
                    self.userName + '@sandia.gov'
                    )
                self.emailFrom=self.entryFromBox.get()
                
        elif self.key == 'Earthlink':
            ','.join(self.emailTo)
# attach extension to username now that server is known, if not done already
            if self.emailFrom[0].count('@') == 0:
                self.entryFromBox.delete(0,END)
                self.entryFromBox.insert(
                    0,
                    self.userName + '@earthlink.net'
                    )
                self.emailFrom=self.entryFromBox.get()
                
        elif self.key == 'Gmail':
            ','.join(self.emailTo)
# attach extension to username now that server is known, if not done already
            if self.emailFrom[0].count('@') == 0:
                self.entryFromBox.delete(0,END)
                self.entryFromBox.insert(
                    0,
                    self.userName + '@gmail.com'
                    )
                self.emailFrom=self.entryFromBox.get()
                
        else:
            print "\n FATALERROR: unknown key when trying to attach extension to userName"
            print "\n      method: cleanupEmailAddresses"
            print "\n      key =",self.key

# ===== end of cleanupEmailAddresses =====

    def sendEmail(self,emailTo):
        '''
        Purpose: 
            login if username/password provided; else send mail
        '''
# form msg body to print in email; insert blank line at top of msg body as required by some servers (like Sandia's for example!)
        self.emailMessageFinal = (
            "From: %s\n" % self.emailFrom +
            "To: %s\n" % emailTo +
            "Date: %s\n" % self.emailDate +
            "Subject: %s\n\n" % self.emailSubject +
            "%s\n" % self.emailMessage +
            " -- end of message --\n\n"
            )

        if DEBUG:
            print "\n >> emailMessageFinal:\n %s" % self.emailMessageFinal
        
        myMailServerAddress = self.comboboxSelectMailServer.get().split('/')[1]
        myMailServer = self.comboboxSelectMailServer.get().split('/')[0]
        myMailServerUserName = self.varEntryMailServerUserName.get().strip()
        myMailServerPassWord = self.varEntryMailServerPassWord.get().strip()
        
        if DEBUG:
            stringPrint = (
                '\nmyMailServerAddress = %s\n' +
                'myMailServer = %s\n' +
                'myMailServerUserName = %s\n'
                ) % (
                self.comboboxSelectMailServer.get().split('/')[1],
                self.comboboxSelectMailServer.get().split('/')[0],
                self.varEntryMailServerUserName.get().strip()
                )
        
        if(
        myMailServerUserName == ''
        and
        myMailServerPassWord == ''
        ) or (
        myMailServerUserName <> ''
        and
        myMailServerPassWord <> ''
        ):
# pass
            pass
        elif myMailServerUserName == '':
# error - user left off username
            stringNoMailServerUserName = (
                'Mail server username is missing.'
                )
            print(stringNoMailServerUserName)
            showerror(
                'Error: no username',
                '\n' + stringNoMailServerUserName
                )
            return 0
        elif myMailServerPassWord == '':
# error - user left off password
            stringNoMailServerPassWord = (
                'Mail server password is missing.'
                )
            print(stringNoMailServerPassWord)
            showerror(
                'Error: no password',
                '\n' + stringNoMailServerPassword
                )
            return 0  
        

# toplevel - "attempting to send email"
        bgColor = 'lightblue'
        
        winInfo1 = Toplevel(
            borderwidth=5, 
            bg=bgColor
            )
        winInfo1.title(
            'ATTEMPTING TO SEND EMAIL'
            )
        winInfo1.transient(self.windowEmail)
        # place the top window
        xWindow = self.windowEmail.winfo_rootx() + 150
        yWindow = self.windowEmail.winfo_rooty() + 300
        winInfo1.geometry(
            '+%d+%d' % (
            xWindow, 
            yWindow
              )
            )
# widgets
        waitLabel = Label(
            winInfo1,
            text='Attempting to send email - please wait...',
            bg=bgColor,
            font=self.labelFont,
            )
        waitLabel.grid(
            row=0,
            column=0,
            padx=10,
            pady=0,
            )
        winInfo1.update_idletasks()
                
# connect to mail server
        stringConnectionError = ''
        stringTryToConnect = (
            '\n\n>>> Trying to connect to email server: %s/%s\n' +
            '   This may take awhile. Please be patient.'
            ) % (
            myMailServer,
            myMailServerAddress
            )
        print(stringTryToConnect)
            
        try:
            self.emailServer = smtplib.SMTP(myMailServerAddress)  
        except smtplib.SMTPConnectError: 
            stringConnectionError += (
                'SMTPConnectError\n' +
                ' Server %s not available.\n'
                ) % (
                myMailServer
                )
        except smtplib.SMTPServerDisconnected:
            stringConnectionError += (
                'SMTPServerDisconnected\n' +
                ' could not connect to server %s.'
                ) % (
                myMailServer
                )
        except (socket.gaierror, socket.error, socket.herror, \
                smtplib.SMTPException), e:
            stringConnectionError += (
                'socket.error\n' +
                ' may be bad connection to %s,\n' +
                ' or a firewall is preventing access'
                ) % (
                myMailServer
                )
        except:
            stringConnectionError += (
                'Unknown connection error.\n' +
                ' Server %s is not accessible.\n' +
                ' Reason is unknown.'
                ) % (
                myMailServer
                )

        if stringConnectionError <> '':
            print('\n' + stringConnectionError)
            winInfo1.destroy()
            showerror(
                'Error: mail server connection',
                stringConnectionError
                )
            return 0
                
# no exceptions have occurred, so try to login to emailServer
        if myMailServer == 'earthlink.net':
            self.emailServer.ehlo(myMailServerAddress)
# encrypt connection
        self.emailServer.starttls()
# authenticate if username and password are provided
        if myMailServerUserName <> '' and myMailServerPassWord <> '':
            try:
                self.emailServer.login(
                    myMailServerUserName,
                    myMailServerPassWord
                    )
            except:
                stringNoLogin = (
                    'Not able to login to mail server\n\n' +
                    '  %s\n\n' +
                    'Check username and password and try again.'
                    ) % (
                    myMailServer
                    )
                print('\n' + stringNoLogin)
                winInfo1.destroy()
                showerror(
                    'Error: cannot login',
                    stringNoLogin
                    )
                return 0
                    
                
        try:
            email=self.emailServer.sendmail(self.emailFrom,self.emailTo,self.emailMessageFinal)
        except smtplib.SMTPServerDisconnected:
            stringErrorTimeOut = (
                ' Email server timed out or disconnected.\n' + 
                '  You may have entered wrong Username and/or Password,\n' + 
                '  (if needed), or you may not have an account on this\n' +
                '  particular server, or server timed out.\n\n'
                )
            print('\n' + stringErrorTimeOut)
            showinfo(
                'Timeout occurred...',
                stringErrorTimeOut
                )
            winInfo1.destroy()
#            if self.loginRequired:
#                self.winLoginBox.destroy()
            try:
                self.emailServer.quit()
            except:
                pass
            return 0
            
        except smtplib.SMTPRecipientsRefused:
            stringErrorDenied = (
                'You have been denied access to the %s email server\n' +
                ' because your login username and/or password was not accepted.\n\n'
                'Unable to send email.\n\n'
                ) % (
                myMailServer
                )
            showinfo(
                'ERROR...',
                stringErrorDenied
                )
            winInfo1.destroy()
#            if self.loginRequired:
#                self.winLoginBox.destroy()
            try:
                self.emailServer.quit()
            except:
                pass
            return 0
            
        except (socket.gaierror, socket.error, socket.herror),error:
            stringErrorSocket = (
                '>>> Socket error -- your message may not have been sent!\n\n' +
                '>>> Unable to send email to %s server.\n'
                ) % (
                myMailServer
                )
            showinfo(
                'ERROR...',
                stringErrorSocket
                )
            winInfo1.destroy()
#            if self.loginRequired:
#                self.winLoginBox.destroy()
            try:
                self.emailServer.quit()
            except:
                pass
            return 0
            
        except:
            stringErrorUnknown = (
                '>>> ..... disconnected -- reason unknown.\n\n' +
                '>>> Unable to send email to %s server.\n'
                ) % (
                myMailServer
                )
            showinfo(
                'ERROR...',
                stringErrorUnknown
                )
            winInfo1.destroy()
#            if self.loginRequired:
#                self.winLoginBox.destroy()
            try:
                self.emailServer.quit()
            except:
                pass
            return 0
            
        else:
            stringSuccess = (
                "\nEmail successfully sent using %s server\n"
                ) % (
                myMailServer
                )
            print(stringSuccess)
            winInfo1.destroy()
            showinfo(
                'Email sent..',
                stringSuccess
                )
            try:
                self.emailServer.quit()
            except:
                pass
            
        return 1

# ===== end of sendEmail =====
            
# Handlers
    def handlerQuit(self):
        ans=askokcancel(
            'Verify exit from email',
            'Really quit email?'
            )
        if ans: 
            self.windowEmail.withdraw()
        
# ===== end of handlerQuit =====
        
    def handlerLoginBoxOK(self):
# called only when the email server needs authentication
        print "\n >>> handlerLoginBoxOK"
        self.username=self.loginboxEntryUser.get()
        self.password=self.loginboxEntryPW.get()
        print " XXX username = %s" % self.username
#        print " XXX pw = %s" % self.password
        if self.username and self.password:
#            self.winLoginBox.quit()
# authenticate
            try:
                self.emailServer.login(self.username,self.password)
            except smtplib.SMTPException, e:
                print '>>> ERROR: Authentication failed!'
                print '            Try logging in again.'
                showerror('Authentication failed','Login failed due to bad username or password.\nTry SENDing again.')
                self.handlerLoginBoxCancel()
                              
            else:
# after authenticating, send the email            
                self.sendEmail()
        else:
            if not self.username and not self.password:
                print "\n WARNING: Username and password have not been specified in the login box!"
                print "\n            Try SENDing again."
                showerror('No Username or Password','Neither Username nor Password has been specified.\nTry SENDing again.')
                self.handlerLoginBoxCancel()
            elif not self.username:
                print "\n WARNING: No username has been specified in the login box!"
                print "\n            Try SENDing again."
                showerror('No Username','No username specified.\nTry SENDing again.')
                self.handlerLoginBoxCancel()
            elif not self.password:
                print "\n WARNING: No password has been specified in the login box!"
                print "\n            Try SENDing again."
                showerror('No Password','No password specified.\nTry SENDing again.')
                
# ===== end of handlerLoginBoxOK =====    
         
    def handlerLoginBoxCancel(self):
        print "\n >>> handlerLoginBoxCancel"
        self.username=''
        self.password=''
        self.winLoginBox.withdraw()
        try:
            self.emailServer.quit()
        except:
            pass

# ===== end of handlerLoginBoxCancel =====
            
#root=Tk()
#Button(
#    root, 
#    text='popup', 
#    command=dialog
#    ).pack()
#root.mainloop()
if __name__=='__main__':
    email=SendEmail()
    email.master.title("PYLOTDB: send email to pylotdb-help.sandia.gov")
    email.mainloop()
    
    
    
# questions
# 1. how to get 'send email' to generate only one login window before returning
# 2. how to get checkbox working correctly with proper frame (don't have to call Frame.__init__ twice?
# 3. why does checkbox not follow the grid's row-column numbering? It seems to see the whole box as row=col=0
# 4. after clicking 'send email', the login box for earthlink/gmail needs to take focus
# 5. why won't the login window come up before the countdown happens??
