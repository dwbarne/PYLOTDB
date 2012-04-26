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

# debugging
DEBUG = 1       # for printing selected variables

# list of mail servers;
#   most mail servers will require authentication via login   
mailServers = {
    'earthlink':'smtp.earthlink.net:25',
    'microsoft':'smtp.live.com:25',
    'gmail':'smtp.gmail.com:25',
    'yahoo':'smtp.mail.yahoo.com:25'
    }


#makemodal = (len(sys.argv) > 1)
#print "len(sys.argv) =",len(sys.argv)

class SendEmail(Frame):
    def __init__(self, windowEmail):
        self.windowEmail=windowEmail
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
        self.dictMailServers = mailServers
        self.listMailServers = self.dictMailServers.keys()
        
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
#            "pylot-help@sandia.gov,"
            "dwbarne@gmail.com"
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
            "PYLOT problems, concerns and/or comments"
            )
            
# MAIL SERVER FRAME
# ... label for selecting/entering server
        label = Label(
            self.frameMailServer,
            text=(
                'Select/enter mail server:\n' +
                ' Ex: smtp.gmail.com:25 '
                ),
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
            entry_width=20,
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
# ... label for user entry
        label = Label(
            self.frameMailServer,
            text=' username:',
            )
        label.grid(
            row=0,
            column=2,
            pady=5,
            padx=2,
            sticky=E,
            )
# user entry for mail server
        self.entryMailServerUserName = Entry(
            self.frameMailServer,
            width=15,
            )
        self.entryMailServerUserName.grid(
            row=0,
            column=3,
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
            text=' password:',
            )
        label.grid(
            row=0,
            column=4,
            pady=5,
            padx=2,
            sticky=E,
            )
# password entry for mail server
        self.entryMailServerPassWord = Entry(
            self.frameMailServer,
            width=15,
            show='*'
            )
        self.entryMailServerPassWord.grid(
            row=0,
            column=5,
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
            "<Enter email message here; \nalso change above email address to pylot-help.sandia.gov> "
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
        if not success: return
        
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
            showerror('No servers found...', \
              'No servers found\n  Could be servers are too slow to respond, or\n  maybe just a bad connection.\n   Try again...')
            return
        '''
        
# clean up email addresses as required by the server
??        self.cleanupEmailAddresses()
        
# for those servers requiring explicit username and password to login...     
        self.loginRequired=0
        if self.key == 'Earthlink':
            self.loginRequired = 1
            self.boxLogin()
        elif self.key == 'Gmail':
            self.loginRequired = 1
            self.boxLogin()
# and for those NOT requiring explicit login...        
        elif self.key == 'Sandia':
            self.sendEmail()
        else:
            print "\n ERROR: no server found in method handlerEmailSend!\n"
            showerror('No Server Found','No email server found to send email!')
           
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
            
# determine how many email addresses based on separator being whitespace, commas, or semicolons
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
            print "DEBUG: before filtering - emailTo = ",self.emailTo
            print "         len(emailTo) = ",len(self.emailTo)
        
# remove blank email addresses
        blankEmailCount=self.emailTo.count('')
        for count in range(blankEmailCount):
            self.emailTo.remove('')
            
# remove any newline \n characters
        newlineEmailCount=self.emailTo.count('\n')
        for count in range(newlineEmailCount):
            self.emailTo.remove('\n')
            
#Debug
        if DEBUG:
            print "DEBUG: after filtering - emailTo = ",self.emailTo
            print "         len(emailTo) = ",len(self.emailTo)
        
# how many @'s in emailTo
        self.atCount=0
        for index in range(len(self.emailTo)):
            self.atCount+=self.emailTo[index].count('@')
            
#DEBUG
        if DEBUG:
            print "DEBUG: emailTo, atCount = ",(self.emailTo,self.atCount)
        
# check if any special characters in email list elements, 
#   including separators used above (the one used will not 
#   show up in the individual entries).
# This implies that the same separator must be used to 
#   separate all email addresses in the main entry window!
        charList1=[ '#', ',', '!', '$', '^', '&', '*', '(', ')', '+', '=', '{']
        charList2=['}', '[', ']', '|', '\\', '/', ":", "?", '>', "<", "`", " "]
        charList=charList1 + charList2
            
        specialCharactersInEmailAddresses=0
        
#Debug
        if DEBUG:
            print "\nDebug: emailTo = ",self.emailTo
 
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
                "\n ERROR: A total of %s special characters were found\n' +
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
            for index in range(len(self.emailTo)):
# check for length of each entry
                if len(self.emailTo[index]) <= 5:
                    print(
                        "\n  > Removing invalid email address from list - too short:\n%s"
                        % self.emailTo[index]
                        )
                    self.emailTo.remove(self.emailTo[index])
# check for too many @s in each entry
                elif self.emailTo[index].count('@') > 1:
                    print(
                        "\n > Removing invalid email address from list - too many '@'s:\n%s" 
                        % self.emailTo[index]
                        )
                    self.emailTo.remove(self.emailTo[index])
# check for whitespace in each entry
                elif self.emailTo[index].count(' ',1,len(self.emailTo[index])-1) > 0:
                    print(
                        "\n > Removing invalid email address from list - invalid whitespace:\n%s"
                        % self.emailTo[index]
                        )
                    self.emailTo.remove(self.emailTo[index])
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
                
# see how many email addresses after cleaning out junk
            print(
                "\nNumber of email addresses that appear valid: %s\n" 
                % len(self.emailTo)
                )
            
# join all email addresses as one string separated by semicolons, regardless of what separator was used by user
#   depends on server!
            if len(self.emailTo) > 1:
                self.emailTo=';'.join(self.emailTo)

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

# example for smtp.gmail.com mail server
# >>> import smtplib
# >>> s = smtplib.SMTP('smtp.gmail.com:25')
# >>> s.starttls()
# >>> s.login('dwbarne@gmail.com','pw')
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
        for key,server in self.emailServers.iteritems():
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

def sendEmail(self):
# form msg body to print in email; insert blank line at top of msg body as required by some servers (like Sandia's for example!)
        self.emailMessageFinal="\n" + \
            "From: %s\n" % self.emailFrom + \
            "To: %s\n" % self.emailTo + \
            "Date: %s\n" % self.emailDate + \
            "Subject: %s\n\n" % self.emailSubject + \
            "%s\n" % self.emailMessage + \
            " -- end of message --\n\n"
#                        % (emailFrom,emailTo,emailDate,emailSubject,emailMessage)
        print "\n >> emailMessageFinal\n %s" % self.emailMessageFinal
        
        try:
#                        showinfo('Sending ...','Email being sent - please wait..')
            winInfo1=Toplevel(borderwidth=5, bg='lightblue')
            waitLabel=Label(winInfo1,
                text='Attempting to send email - please wait...',
                font=self.labelFont
                )
            waitLabel.grid(padx=10,pady=10,row=0,column=0)

            email=self.emailServer.sendmail(self.emailFrom,self.emailTo,self.emailMessageFinal)
        except smtplib.SMTPServerDisconnected:
            print " >>> ..... Email server timed out or disconnected.\n" + \
                "  You may have entered wrong Username and/or Password,\n" + \
                "  or you may not have an account on this particular server,\n" + \
                "  or server timed out.\n\n"
            showinfo(
                'Timeout occurred...',
                'Email server timed out or disconnected.\n\n' + 
                'You may have entered username/password incorrectly')
            winInfo1.destroy()
            if self.loginRequired:
                self.winLoginBox.destroy()
            self.emailServer.quit()
            return
        except smtplib.SMTPRecipientsRefused:
            print 
            print ">>> You have been denied access to the %s email server\n" % key + \
                 "     because your login username and/or password was not accepted.\n\n"
            print " >>>         Unable to send email.\n"
            print 
            showinfo('ERROR...','Login username and/or password not accepted.\nUnable to send email to %s server' % self.key)
            winInfo1.destroy()
            if self.loginRequired:
                self.winLoginBox.destroy()
            self.emailServer.quit()
            return
        except (socket.gaierror, socket.error, socket.herror),error:
            print ">>> ... Your message may not have been sent!"
            print " >>>         Unable to send email.\n"
            print error
            showinfo('ERROR...','Socket error.\nUnable to send email to %s server' % self.key)
            winInfo1.destroy()
            if self.loginRequired:
                self.winLoginBox.destroy()
            self.emailServer.quit()
            return
        except:
            print " >>> ..... disconnected -- reason unknown."
            print " >>>         Unable to send email.\n"
            print
            showinfo('ERROR...','Unable to send email to %s server.\nReason unknown.' % self.key)
            winInfo1.destroy()
            if self.loginRequired:
                self.winLoginBox.destroy()
            self.emailServer.quit()
            return
        else:
            print "\nEmail successfully sent to %s server\n" % self.key
            showinfo('Email sent..','Email Successfully sent to %s server' % self.key)
            winInfo1.destroy()
            if self.loginRequired:
                self.winLoginBox.destroy()
            self.emailServer.quit()

# ===== end of sendEmail =====
            
# Handlers
    def handlerQuit(self):
        ans=askokcancel('Verify exit from email','Really quit email?')
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
        self.emailServer.quit()

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
    email.master.title("PYLOT: send email to pylot-help.sandia.gov")
    email.mainloop()
    
    
    
# questions
# 1. how to get 'send email' to generate only one login window before returning
# 2. how to get checkbox working correctly with proper frame (don't have to call Frame.__init__ twice?
# 3. why does checkbox not follow the grid's row-column numbering? It seems to see the whole box as row=col=0
# 4. after clicking 'send email', the login box for earthlink/gmail needs to take focus
# 5. why won't the login window come up before the countdown happens??