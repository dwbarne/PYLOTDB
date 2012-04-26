#!/usr/local/bin/python     # for *nix runs
# ===== Header =====
# Filename: module_leadingSpaces.py
# author: dwbarne
# creation date: Thu, 10-29-2008

# Purpose:
"""
creates a frame for choosing parameters to add or
delete leading spaces in a file

"""


from Tkinter import *
from tkMessageBox import *
import Pmw
#import module_spawnprogram
from tkMessageBox import *
import tkFont
import os
from tkFileDialog import *

# Define globals
# ... Text frame width and height
w_frameText = 75        # default: 75
h_frameText = 30        # default: 30

#  ... main Window placement relative to top left of screen
x_Windows = 25
y_Windows = 0

# width of frame for line numbers in text box
widthLineNumbersFrame = 6
widthLineNumbers = widthLineNumbersFrame - 0
# put together format string used in handlerTextLineNumbers; numbers are right justified
stringLineNumberFormat = '%' + str(widthLineNumbers) + 'd'

#   ... current directory
currentDirectory = os.getcwd().split('\\').pop()
currentDirectoryFullPath = os.getcwd()

colorbg='lightgreen'


def leadingSpaces(self,parentFrame):
    """
    displays widgets in the parent frame;
    also provides for choosing and saving 
    the target file,
    """
    
    self.parentFrame = parentFrame
    
# ... button
    buttonFontFamily = 'helvetica'
    buttonFontSize = '6'
    # define button font
    self.buttonFont = tkFont.Font(
        family=buttonFontFamily,
        size=buttonFontSize,
        )

# FRAMES with parentFrame: frameEditor     
#   ... for label
    frame0 = Frame(
        parentFrame,
        bg=colorbg,
#        relief=RIDGE,
#        borderwidth=2,
        )
    frame0.grid(
        row=0,
        column=0,
        )
#   ... for editor        
    frame1 = Frame(
        parentFrame,
        bg=colorbg,
        )
    frame1.grid(
        row=1,
        column=0,
        )
        
    frame2 = Frame(
        parentFrame,
        bg=colorbg,
        )
    frame2.grid(
        row=2,
        column=0,
        )
 
# ============widgets ==============================

# FRAME 0:
    frame00 = Frame(
        frame0,
        bg=colorbg,
        )
    frame00.grid(
        row=0,
        column=0
        )
    frame01 = Frame(
        frame0,
        bg=colorbg,
        )
    frame01.grid(
        row=1,
        column=0,
        )
    labelTop0 = Label(
        frame00,
        text='ADD / DELETE LEADING SPACES IN A FILE',
        bg=colorbg,
        fg='black',
        font=self.titleFont,
        justify=CENTER
        )
    labelTop0.grid(
        row=0,
        column=0,
        columnspan=2,
        pady=5,
        )
        
    labelTop1 = Label(
        frame00,
        text='- Have file opened in favorite editor to choose line\n' + 
          '  numbers, if needed.\n\n' +
          '- Original file is never modified until "Save file" button\n' +
          '  is pressed and then only if file is saved as original.\n'
          ,
        bg=colorbg,
        fg='black',
        font=self.titleFont,
        justify=LEFT
        )
    labelTop1.grid(
        row=1,
        column=0,
        columnspan=2,
        pady=5,
        )
 
# checkbutton to ADD spaces 
    self.varCheckbuttonSpacesAdd = IntVar()
    self.checkbuttonSpacesAdd = Checkbutton(
        frame00,
        text='Add',
        bg=colorbg,
        variable=self.varCheckbuttonSpacesAdd,
        command=handlerCheckbuttonSpacesAdd(self),
        )
    self.checkbuttonSpacesAdd.grid(
        row=2,
        column=0,
        pady=5,
        )
    self.checkbuttonSpacesAdd.select()
        
# checkbutton to DELETE spaces
    self.varCheckbuttonSpacesDelete = IntVar()
    self.checkbuttonSpacesDelete = Checkbutton(
        frame00,
        text='Delete',
        bg=colorbg,
        variable=self.varCheckbuttonSpacesDelete,
        command=handlerCheckbuttonSpacesDelete(self),
        )
    self.checkbuttonSpacesDelete.grid(
        row=2,
        column=0,
        pady=5,
        sticky=E
        )

# 'ADD' label        
    self.labelNumSpacesAdd = Label(
        frame01,
        text='Number of spaces to ADD: ',
        bg=colorbg,
        )
    self.labelNumSpacesAdd.grid(
        row=3,
        column=0,
        pady=5
        )

# 'DELETE' label - do not grid yet
    self.labelNumSpacesDelete = Label(
        frame01,
        text='Number of spaces to DELETE: ',
        bg=colorbg,
        )
    self.labelNumSpacesDelete.grid(
        row=3,
        column=0,
        pady=5
        )
    self.labelNumSpacesDelete.grid_remove()
        
    self.spaces=('4','8','12','16','20')
    self.comboNumSpaces = Pmw.ComboBox(
        frame01,
        scrolledlist_items=self.spaces,
        entry_background='white',
        entry_width=4,
        listheight=100,
        scrolledlist_hull_width=10,
        )
    self.comboNumSpaces.selectitem(self.spaces[0])
    self.comboNumSpaces.grid(
        row=3,
        column=1,
        pady=5,
        sticky=W,
        )
    

# FRAME 1:
    labelPathName = Label(
        frame1,
        text='Path:',
        bg=colorbg,
        justify=RIGHT,
        )
    labelPathName.grid(
        row=0,
        column=0,
        sticky=E,
        pady=5,
        )
        
    self.entryPathName = Pmw.ScrolledText(
        frame1,
        text_padx=3,
        text_pady=3,
        vscrollmode='static',
        usehullsize=1,
        hull_width=225,
        hull_height=60,
        )

#    self.entryPathName = Pmw.EntryField(
#        frame1,
#        validate=None,
#        entry_width=30,
#        )
    self.entryPathName.grid(
        row=0,
        column=1,
        padx=5,
        pady=5,
        sticky=W,
        )
        
    labelFileName = Label(
        frame1,
        text='File: ',
        bg=colorbg,
        justify=RIGHT,
        )
    labelFileName.grid(
        row=1,
        column=0,
        sticky=E,
        pady=5
        )
        
    self.entryFileName = Pmw.EntryField(
        frame1,
        validate=None,
        entry_width=30,
        )
    self.entryFileName.grid(
        row=1,
        column=1,
        padx=5,
        pady=5,
        sticky=W,
        )
        
# button for file        
    buttonFileName = Button(
        frame1,
        text='Browse',
        width=6,
        borderwidth=5,
        bg='white',
        fg='blue',
        relief=RAISED,
        font=self.buttonFont,
        command=handlerReadCode(self)
        )
    buttonFileName.grid(
        row=2,
        column=1,
        sticky=N
        )
        
    labelTotalLines = Label(
        frame1,
        text='Lines read: ',
        bg=colorbg,
        )
    labelTotalLines.grid(
        row=2,
        column=0,
        sticky=E,
        )
        
    self.entryTotalLines = Entry(
        frame1,
        width=8,
        bg=colorbg,
        justify=LEFT,
        )
    self.entryTotalLines.grid(
        row=2,
        column=1,
        sticky=W,
        )
    self.entryTotalLines.insert(0,'0')
    self.entryTotalLines.configure(
        background=colorbg,
        foreground='black'
        )
    self.entryTotalLines.configure(state=DISABLED)
        
# entry for starting line number
    labelStart = Label(
        frame1,
        text='Starting line number: ',
        bg=colorbg,
        justify=RIGHT,
        )
    labelStart.grid(
        row=3,
        column=0,
        sticky=E,
        padx=5,
        pady=5,
        )
        
    self.entryStart = Entry(
        frame1,
        width=10,
        justify=LEFT,
        )
    self.entryStart.grid(
        row=3,
        column=1,
        sticky=W,
        )

# entry for ending line number        
    labelEnd = Label(
        frame1,
        text='Ending line number: ',
        bg=colorbg,
        justify=RIGHT
        )
    labelEnd.grid(
        row=4,
        column=0,
        sticky=E,
        padx=5,
        pady=5,
        )
        
    self.entryEnd = Entry(
        frame1,
        width=10,
        justify=LEFT,
        )
    self.entryEnd.grid(
        row=4,
        column=1,
        sticky=W,
        )
    
# FRAME 2:
        
    self.buttonClear = Button(
        frame2,
        text='Clear all fields',
        width=12,
        borderwidth=5,
        justify=CENTER,
        relief=RAISED,
        bg='white',
        fg='blue',
        font=self.buttonFont,
        command=handlerClearAllFields(self),
        )
    self.buttonClear.grid(
        row=0,
        column=0,
        columnspan=99,
        padx=5,
        pady=10,
        )
        
    self.buttonProcess = Button(
        frame2,
        text='Process file',
        width=10,
        borderwidth=5,
        relief=RAISED,
        command=handlerProcessCode(self),
        )
    self.buttonProcess.grid(
        row=1,
        column=0,
        padx=10,
        pady=10,
        )
        
    self.buttonFileSave = Button(
        frame2,
        text='Save file',
        width=10,
        borderwidth=5,
        relief=RAISED,
        command=handlerSaveCode(self),
        )
    self.buttonFileSave.grid(
        row=1,
        column=1,
        padx=10,
        pady=10,
        )
    
    self.buttonQuit = Button(
        frame2,
        text='Quit',
        justify=CENTER,
        width=5,
        borderwidth=5,
        relief=RAISED,
        command=handlerQuit(self),
        )
    self.buttonQuit.grid(
        row=1,
        column=2,
        padx=10,
        pady=10,
        )
        
# HANDLERS

# ===== handlerCheckbuttonSpacesAdd =====
def handlerCheckbuttonSpacesAdd(self):
    """
    deselects 'Delete' checkbutton
    
    Checkbutton variable:
        self.checkbuttonSpacesAdd
        self.checkbuttonSpacesDelete
    Grids:
        self.labelNumSpacesAdd.grid
        self.labelNumSpacesDelete.grid
        
    """
    def tempDef():
        print '\n** In handlerSpacesAdd'
        self.checkbuttonSpacesDelete.deselect()
        self.checkbuttonSpacesAdd.select()
        self.labelNumSpacesDelete.grid_remove()
        self.labelNumSpacesAdd.grid()
        
    return tempDef
    
# ===== handlerCheckbuttonSpacesAdd =====

# ===== handlerCheckbuttonSpacesDelete =====
def handlerCheckbuttonSpacesDelete(self):
    """
    deselects 'Add' checkbutton
    
    Checkbutton variable:
        self.checkbuttonSpacesAdd
        self.checkbuttonSpacesDelete
    Grids:
        self.labelNumSpacesAdd.grid
        self.labelNumSpacesDelete.grid
        
    """
    def tempDef():
        print '\n** In handlerSpacesDelete'
        self.checkbuttonSpacesAdd.deselect()
        self.checkbuttonSpacesDelete.select()
        self.labelNumSpacesAdd.grid_remove()
        self.labelNumSpacesDelete.grid()
        
    return tempDef
    
# ===== end of handlerCheckbuttonSpacesDelete =====

# ==== handlerReadCode =====

def handlerReadCode(self):
    """
    Purpose:
        read python code from a file
    """
    
    def tempDef():
        global currentDirectory
        
        print '\n** In handlerReadCode'
        
        self.indicatorProcessed = 0

# clear all fields
        """
        self.checkbuttonSpacesAdd.select()
        self.checkbuttonSpacesDelete.deselect()
        self.labelNumSpacesAdd.grid()
        self.labelNumSpacesDelete.grid_remove()
        self.comboNumSpaces.selectitem(self.spaces[0])
        """
        self.entryPathName.clear()
        self.entryFileName.clear()
        self.entryTotalLines.configure(state=NORMAL)
        self.entryTotalLines.delete(0,END)
        self.entryTotalLines.insert(0,'0')
        self.entryTotalLines.configure(state=DISABLED)
        self.entryStart.delete(0,END)
        self.entryEnd.delete(0,END)
    
# define dictionary of options
        options = {}
        options = {
            'defaultextension' : '.*',
            'filetypes' : [('All files','.*'),('python','.py')],
            'initialdir' : currentDirectory,
            'initialfile' : '',
            'parent' : self.parentFrame,
            'title' : 'Read file'
            }      
        
# get filename
#    dirname, filename = os.path.split(askopenfilename(**options))
        inputFile = askopenfilename(**options)
        tempPath, tempFile = os.path.split(inputFile)
        if inputFile == '': return
        print '\n    File opened:',inputFile
        self.filename=open(inputFile,'rU').readlines()
        lenFile=len(self.filename)
        print '\nInput file has %s lines.' % len(self.filename)

# display filename
        self.entryPathName.clear()
        self.entryPathName.setvalue(tempPath)
        self.entryFileName.clear()
        self.entryFileName.setentry(tempFile)
# display number of lines
        self.entryTotalLines.configure(state=NORMAL)
        self.entryTotalLines.delete(0,END)
        self.entryTotalLines.insert(0,lenFile)
        self.entryTotalLines.configure(state=DISABLED)
# set start and ending line numbers to 1 and max, respectively, as default values
        self.entryStart.insert(0,'1')
        self.entryEnd.insert(0,str(lenFile))
        
    return tempDef
    
# ===== end of handlerReadCode =====

# ===== handlerSaveCode =====

def handlerSaveCode(self):
    """
    Purpose:
        save the code generated thus far to a file
    """
    
    def tempDef():
    
        global currentDirectory
        
        print '\n** In handlerSaveCode'
        
        if self.indicatorProcessed == 0:
            print '\nWARNING: file has not been processed, so no need to save.'
            showinfo(
                'Warning...',
                'File has not been processed, so no need to save!\n'
                )
            return

        
        options = {}
        options = {
            'defaultextension' : '.*',
            'filetypes' : [('All files','.*'),('python','.py')],
            'initialdir' : currentDirectory,
            'initialfile' : '',
            'parent' : self.frameParent,
            'title' : 'Save file'
            }      
        
# get filename
#    dirname, filename = os.path.split(asksaveasfilename(**options))
        filename = asksaveasfilename(**options)
        
        print '\n     filename to save: ',filename
# open the filename
        if filename:
#        self.fileInitial=filename
            myfile=open(filename,'w')
        else:
            print '\n>>ERROR: file not found.'
            print '     filename =',filename
            print 
            return
            
#    print '\n   Text to save:'
#    print self.textMyCode.get(1.0, END)
#    print
            
        myfile.writelines(self.filename)
        myfile.close()
        print '\n     file %s has been written' % filename
        print 
# reset Process Indicator to zero        
        self.indicatorProcessed = 0
        
    return tempDef
        
    
# ===== end of handlerSaveCode ====

# ===== handlerProcessCode =====
def handlerProcessCode(self):
    """
    Purpose:
        to add or delete spaces from input file
    """
    def tempDef():
        print '\n** In handlerProcessCode'
        if not self.entryFileName.get():
            print '\n No filename has been selected.'
            print '  Check input and try again.'
            showinfo(
                'ERROR...',
                'No filename has been selected.\n\n' +
                'Check input and try again.'
                )
            return
        lineStart = int(self.entryStart.get())
        lineEnd = int(self.entryEnd.get())
        numSpaces = int(self.comboNumSpaces.get())
        lenFile = len(self.filename)
        print '  Starting line:',lineStart
        print '  Ending line:',lineEnd
        print '  Spaces:',numSpaces
        print '  Length of file:',lenFile

        """        
        if self.varCheckbuttonSpacesAdd.get():
            print '  Checkbutton-add value is TRUE'
        else:
            print '  Checkbutton-add value is FALSE'
            
        if self.varCheckbuttonSpacesDelete.get():
            print '  Checkbutton-delete value is TRUE'
        else:
            print '  Checkbutton-delete value is FALSE'
        sys.exit()
        """
# bounds checking
        if lineStart > lineEnd:
            print '\nWARNING - "Ending line" cannot be less than "Starting line" '
            print '\n   Starting line =',lineStart
            print '   Ending line =',lineEnd
            print '     Check your input and try again.\n'
            showinfo(
                'ERROR...',
                'Ending line cannot be less than\n' +
                '  starting line!\n\n' +
                'Check input and try again.\n'
                )
            return
    
        if ( 
            lineStart > lenFile or 
            lineEnd > lenFile or
            lineStart < 1 or 
            lineEnd < 1 
            ):
            print 'type: lineStart =',type(lineStart)
            print 'type: lenFile =',type(lenFile)
            print '\nWARNING - Starting or Ending line number out of range'
            print '   Max line number:',lenFile
            print '   Your starting line:',lineStart
            print '   Your ending line:',lineEnd
            print '     Check your input and try again.\n'
            showinfo(
                'ERROR...',
                'Starting or ending line number\n' +
                '  out of range.\n\n' +
                'Check input and try again.\n'
                )
            return
        if (
            numSpaces < 1 or
            numSpaces > 24
            ):
            print '\nWARNING - number of spaces to ADD or DELETE is out of range.'
            print '  numSpaces must be greater than 0 and '
            print '    less than or equal to 24!'
            print ''
            print ' Check input and try again.'
            showinfo (
                'ERROR...',
                'Number of spaces to ADD or DELETE\n' +
                '  is out of range.\n\n' +
                'Check input and try again\n'
                )
            return
        

# which one: add or delete?
        if self.varCheckbuttonSpacesAdd.get():
# ... add spaces
            print '\n** In handlerProcessCode: add leading spaces'
            diff = lineEnd - lineStart + 1
            print
            for i in range(diff):
                lineNumber=lineStart+i
                line = self.filename[lineNumber-1]
                print '\n----------------------------'
                print 'Before change ...'
                print '%s. %s' % (lineNumber,line)
                if line[0] <> '#' and len(line) > 1:
                    lineNew=' '*numSpaces + line
                    print ' After change ...'
                    print '%s. %s' % (lineNumber,lineNew)
                    self.filename[lineNumber-1]=lineNew
                else:
                    print ' Comment - no change'
                    
                    
# ... delete spaces                
        elif self.varCheckbuttonSpacesDelete.get():
            print '\n** In handlerProcessCode: delete leading spaces'

            diff = lineEnd - lineStart + 1
            print
            for i in range(diff):
                lineNumber=lineStart+i
                line = self.filename[lineNumber-1]
                print '\n--------------------------------'
                print 'Before change ...'
                print '%s. %s' % (lineNumber,line)
                lineNew=line
                if len(lineNew) > 1 and lineNew[0] == ' ':
                    for char in range(numSpaces):
                        print ' char =',char
                        print '   len(lineNew) =',len(lineNew)
                        if lineNew[0] == ' ':
                            lineNew=lineNew.replace(' ','',1) 
                        else:
# no more leading spaces
                            break

                print ' After change ...'
                print '%s. %s' % (lineNumber,lineNew)
                self.filename[lineNumber-1]=lineNew
        else:
            print '\n ERROR: handlerProcessCode'
            print '  Problem with checkbuttons being checked'
            print '  This error is fatal.'
            print '  Program is halted.'
            sys.exit()

# indicate the file has been processed            
        self.indicatorProcessed = 1
    
    return tempDef

# ===== end of handlerProcessCode =====

# ==== handlerExecuteCode =====

def handlerExecuteCode(self):
    """
    Purpose:
        execute python code from a file
    """
    
    def tempDef():
        global currentDirectoryFullPath
    
        print '\n** In handlerExecuteCode'

        import module_spawnprogram
    
# instantiate class Spawn
        spawn=module_spawnprogram.Spawn() 
# run spawn method
        spawn.spawn(
            'python',
            self.frameParent,
            currentDirectoryFullPath,
            fileInitial = '',
            )
        
    return tempDef
    
# ===== end of handlerReadCode =====



# ===== handlerClearTextField =====

def handlerClearAllFields(self):
    """
    Purpose:
        give option to clear the entire text field
        
    Variables to reset:
        self.checkbuttonSpacesAdd
        self.checkbuttonSpacesDelete
        self.labelNumSpacesAdd.grid
        self.labelNumSpacesDelete.grid
        self.comboNumSpaces.selectitem(self.spaces[0])
        self.entryPathName
        self.entryFileName
        self.entryTotalLines (use enable, disable)
        self.entryStart
        self.entryEnd
        
    """
    def tempDef():
        print '\n** In handlerClearAllFields'
        ans=askokcancel(
            'Clear fields',
            'This will clear all fields and\n' + 
            ' and set the "Add spaces" checkbutton.\n\n' + 
            'Continue?'
            )
        
        if ans:
            self.checkbuttonSpacesAdd.select()
            self.checkbuttonSpacesDelete.deselect()
            self.labelNumSpacesAdd.grid()
            self.labelNumSpacesDelete.grid_remove()
            self.comboNumSpaces.selectitem(self.spaces[0])
            self.entryPathName.clear()
            self.entryFileName.clear()
            self.entryTotalLines.configure(state=NORMAL)
            self.entryTotalLines.delete(0,END)
            self.entryTotalLines.insert(0,'0')
            self.entryTotalLines.configure(state=DISABLED)
            self.entryStart.delete(0,END)
            self.entryEnd.delete(0,END)
                        
        else:
            print '     Canceled'
        
    return tempDef
        
# ===== end of handlerClearTextField =====

# ===== handlerQuit =====

def handlerQuit(self):
    """
    Purpose:
        give option to quit the program
    """
    
    def tempDef():
    
        print '\n** In handler Quit'
#        ans=askokcancel(
#            'Quit...',
#            'Really quit?'
#            )
#        if ans:
#            sys.exit()
        self.parentFrame.destroy()
#        else:
#            print '          Canceled'
            
    return tempDef
            
            
# ===== end of handlerQuit =====


# ===== main =====

if __name__ == '__main__':
    root=Tk()
    my_Editor(self,root)
    root.mainloop()
    
    
#    app=CreateWidgets(root)
#    app.master.title(
#        'PyCADD - Python Code Analysis, Design, and Development'
#        )
#    app.master.configure(bg='lightblue')
#    app.tk_focusFollowsMouse()
#    app.mainloop()

             