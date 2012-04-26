#!/usr/local/bin/python     # for *nix runs
# ===== Header =====
# Filename: module_Editor.py
# author: dwbarne
# creation date: Thu, 10-29-2008

# Purpose:
"""
creates a basic editing packing in a frame

"""


from Tkinter import *
from tkMessageBox import *
import Pmw
import module_spawnprogram
from tkMessageBox import *
import tkFont
import os
from tkFileDialog import *

# Define globals
# ... Text frame width and height
w_frameText = 55        # default: 75
h_frameText = 20        # default: 30

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


def my_Editor(self,parentFrame0,parentFrame1,bgcolor,labelMain):
    """
    displays text box, used as an editor, in the parent frame;
    also provides for reading and saving files,
    executing a file, and a limited set of
    buttons for manipulating text.
    """
    self.parentFrame0=parentFrame0
    self.parentFrame1=parentFrame1
    
# FRAMES with widgets:
#   ... for read/save
    self.frameEditor00 = Frame(
        self.parentFrame0,
        bg=bgcolor,
        )
    self.frameEditor00.grid(
        row=0,
        column=0,
        pady=10,
        )
#   ... for search      
    self.frameEditor01 = Frame(
        self.parentFrame0,
        bg=bgcolor,
        )
    self.frameEditor01.grid(
        row=1,
        column=0,
        pady=10,
        )
#   ... for modifying input file
    self.frameEditor02 = Frame(
        self.parentFrame0,
        bg=bgcolor,
        )
    self.frameEditor02.grid(
        row=2,
        column=0,
        pady=10,
        )        

# FRAMES with parentFrame1:   
#   ... for editor
    self.frameEditor10 = Frame(
        self.parentFrame1,
        bg=bgcolor,
        )
    self.frameEditor10.grid(
        row=0,
        column=0,
        )
#   ... for editor's buttons        
    self.frameEditor11 = Frame(
        self.parentFrame1,
        bg=bgcolor,
        )
    self.frameEditor11.grid(
        row=1,
        column=0,
        )
        
    self.frameEditor12 = Frame(
        self.parentFrame1,
        bg=bgcolor,
        )
    self.frameEditor12.grid(
        row=2,
        column=0,
        )

 # ========= widgets =============================
 
# FRAME 0:
    label00 = Label(
        self.frameEditor00,
        text=labelMain + '\n',
        bg=bgcolor,
        font=self.titleFont,
        )
    label00.grid(
        row=0,
        column=0,
        columnspan=99,
        )
        
# button to Read code into Text Box
    buttonRead = Button(
#        self.frameSave,
        self.frameEditor00,
        text='READ from file',
        bg='white',
        fg='blue',
        justify=CENTER,
        borderwidth=5,
        relief=RAISED,
        command=handlerReadCode(self,labelMain),
        )
    buttonRead.grid(
        row=1,
        column=0,
        padx=5,
        pady=5,
        )

# button to Save code into a file
    buttonSave = Button(
#        self.frameSave,
        self.frameEditor00,
        text='SAVE to file',
        bg='white',
        fg='blue',
        justify=CENTER,
        borderwidth=5,
        relief=RAISED,
        command=handlerSaveCode(self),
        )
    buttonSave.grid(
        row=1,
        column=1,
        padx=5,
        pady=5,
        )
        
    self.buttonSearchText = Button(
#        self.frameTextSearch,
        self.frameEditor01,
        text='Search ',
        justify=CENTER,
#        width=6,
        borderwidth=5,
        relief=RAISED,
        command=handlerTextBox_Search(self),
        )
    self.buttonSearchText.grid(
        row=0,
        column=0,
        padx=2,
        pady=2,
        sticky=E,
        )
        
    self.entrySearchTextVar = StringVar()
    self.entrySearchText = Entry(
        self.frameEditor01,
        width=25,
        justify=LEFT,
        textvariable=self.entrySearchTextVar,
        )
    self.entrySearchText.grid(
        row=0,
        column=1,
        columnspan=2,
        padx=0,
        pady=0,
        )
            
    self.varCheckbuttonSearchTextUp = IntVar()
    self.checkbuttonSearchTextUp = Checkbutton(
        self.frameEditor01,
        text='Up',
        bg=bgcolor,
        variable=self.varCheckbuttonSearchTextUp,
#        command=self.handlerTextBox_UpSearch,
        )
# do not grid yet
    self.checkbuttonSearchTextUp.grid(
        row=1,
        column=1,
        padx=0,
        pady=0,
        sticky=NE,
        )
    
    self.varCheckbuttonSearchText = IntVar()
    self.checkbuttonSearchText = Checkbutton(
        self.frameEditor01,
        text='Match case',
        bg=bgcolor,
        variable=self.varCheckbuttonSearchText,
#        command=self.handlerTextBox_MatchCase,
        )
    self.checkbuttonSearchText.grid(
        row=1,
        column=2,
        padx=0,
        pady=0,
        sticky=NW,
        )
        
        
             
        
# FRAME 1:
# Construct text box frame and line numbered frame with scrollbars      
# ... x (horizontal) scrollbar
    self.xScrollMyCode=Scrollbar(
        self.frameEditor10,
        orient=HORIZONTAL,
        )
    self.xScrollMyCode.grid(
        row=1,
        column=1,
        columnspan=1,
        sticky=E+W,
        padx=0,
        pady=0,
        )
# ... y (vertical) scrollbar
    self.yScrollMyCode=Scrollbar(
        self.frameEditor10,
        orient=VERTICAL,
        )
    self.yScrollMyCode.grid(
        row=0,
        column=2,
        sticky=N+S,
        padx=0,
        pady=2
        )
        
# ... construct line number text box
# ... text box with numbers
    self.textLineNumbers = Text(
        self.frameEditor10,
        bg='lightgray',
        fg='black',
        width=widthLineNumbersFrame,
        height=h_frameText,
        font=self.dataFont,
        wrap=NONE,
        takefocus=0,
        )
    self.textLineNumbers.grid(
        row=0,
        column=0,
        padx=0,
        pady=2,
        sticky=W,
        )
    self.textLineNumbers.insert(
        1.0,
        (stringLineNumberFormat % 1)
        )
    self.indexLineNumberSave = '1.' + str(widthLineNumbers)


    print ' ***** Line number index:',self.textLineNumbers.index(INSERT)
    print ' ***** END index:',self.textLineNumbers.index(END)
    print
        
# ... construct the text box        
    self.textMyCode = Text(
#        self.frameRightColumn,
        self.frameEditor10,
        bg='white',
        fg='black',
        width=w_frameText,
        height=h_frameText,
        font=self.dataFont,
        wrap=NONE,
        xscrollcommand=self.xScrollMyCode.set,
        yscrollcommand=self.yScrollMyCode.set,
        )
    self.textMyCode.grid(
        row=0,
        column=1,
        padx=2,
        pady=2,
#        sticky=NSEW,
        )
# ... couple scrollbars to text box
    self.xScrollMyCode.configure(
        command=self.textMyCode.xview,
        )
    self.yScrollMyCode.configure(
        command=handlerScrollTwoTextFrames(self),
        )
        
# set bindings for updating line numbers
    self.textMyCode.bind(
        "<KeyPress-Return>",
#        handlerTextLineNumbersReturn(self,' ')
        handlerTextLineNumbersReturn(self,' ')
        )
    self.textMyCode.bind(
        "<KeyPress-Up>",
        handlerTextLineNumbersUpArrow(self,' ')
        )
    self.textMyCode.bind(
        "<KeyPress-Down>",
        handlerTextLineNumbersDownArrow(self,' ')
        )
    self.textMyCode.bind(
        "<KeyPress-BackSpace>",
        handlerTextLineNumbersDelete(self,' ')
        )
    self.textMyCode.bind(
        "<Leave>",
        handlerTextLineNumbersHilite(self,' ')
        )
    self.textMyCode.bind(
        "<Enter>",
#        self.handlerTextLineNumbersUnhilite
        handlerTextLineNumbersHilite(self,' ')
        )
    self.textMyCode.bind(
        "<ButtonRelease-1>",
        handlerTextLineNumbersHilite(self,' ')
        )
    self.textMyCode.bind(
        "<KeyRelease-Tab>",
        handlerTextMyCodeTab(self,' ')
        )

# enable/disable line numbers as needed
    self.textLineNumbers['state']='disabled'

        
# set tags to format inserts to text box
    self.textMyCode.tag_config(
        'comment',
        foreground='red',
        font=('lucida',8,'bold')
        )
        
    self.textMyCode.grid_propagate(0)
    
# FRAME: frameEditor1

        
# wrap/don't-wrap button
    self.checkWrapOff = StringVar()
    self.checkWrapOff.set('Wrap text')
    self.checkWrap = IntVar()
    self.checkWrap.set(0)
    self.checkbuttonWrap = Checkbutton(
#    self.frameTextButtons,
        self.frameEditor11,
        selectcolor='darkgray',
        borderwidth=5,
        relief=RAISED,
        indicatoron=0,
        width=10,
        command=handlerCheckButtonWrap(self),
        variable=self.checkWrap,
        textvariable=self.checkWrapOff,
        )
# DWB - WRAP does not work correctly yet, so do not grid
#    self.checkbuttonWrap.grid(
#        row=2,
#        column=0,
#        padx=2,
#        pady=5,
#        )
        
    self.buttonClear = Button(
        self.frameEditor11,
        text='Clear all text',
        font=self.dataFont,
        width=10,
        borderwidth=5,
        justify=CENTER,
        relief=RAISED,
        command=handlerClearTextField(self),
        )
    self.buttonClear.grid(
        row=0,
# DWB - Move to column 1 when wrap/unwrap is restored
        column=0,
        padx=5,
        pady=5,
        )
        
    self.buttonAddRemoveSpaces = Button(
        self.frameEditor11,
        text='+/- leading spaces...',
        borderwidth=5,
        relief=RAISED,
        command=handlerPlusMinusLeadingSpaces(self),
        )
    self.buttonAddRemoveSpaces.grid(
        row=0,
        column=1,
        padx=5,
        pady=5,
        columnspan=1,
        )
                   
    self.buttonClearSelection = Button(
        self.frameEditor11,
        text='Clear selection',
        font=self.dataFont,
        borderwidth=5,
        width=10,
        justify=CENTER,
        relief=RAISED,
        command=handlerTextBox_ClearSelection(self),
        )
#    self.buttonClearSelection.grid(
#        row=2,
#        column=2,
#        padx=2,
#        pady=5,
#        )
    


    self.buttonRefreshLineNumbers = Button(
        self.frameEditor11,
        text='Refresh line numbers',
        borderwidth=5,
        relief=RAISED,
        command=refreshLineNumbers(self),
        )
    self.buttonRefreshLineNumbers.grid(
        row=0,
        column=2,
        padx=5,
        pady=5,
        )
        

# button to execute python code
    """
    buttonExecute = Button(
        self.frameEditor11,
        text='EXECUTE Python file',
        bg='white',
        fg='blue',
        justify=CENTER,
        borderwidth=5,
        relief=RAISED,
        command=handlerExecuteCode(self),
        )
    buttonExecute.grid(
        row=2,
        column=4,
        padx=5,
        pady=5,
        )
    """
    
# ... quit button on right side
    """
    labelMyCode = Label(
        self.frameEditor12,
        bg=bgcolor,
        width=60,
        )
    labelMyCode.grid(
        row=0,
        column=0,
        )  

    self.buttonQuitRight = Button(
        self.frameEditor12,
        text='Quit',
        font=self.buttonQuitFont,
        borderwidth=5,
        relief=RAISED,
        width=10,
        command=handlerQuit(self),
        )
    
    self.buttonQuitRight.grid(
        row=0,
        column=1,
        padx=0,
        pady=2,
        sticky=E,
        ) 
    """

# ===== handlerScrollTwoTextFrames =====
def handlerScrollTwoTextFrames(self,*args):
    """
    allows synchronized scrolling of two frames
    """
    
    def tempDef(*args):
# old way
#    apply(self.textLineNumbers.yview,args)
#    apply(self.textMyCode.yview,args)
#
# new way
        self.textLineNumbers.yview(*args)
        self.textMyCode.yview(*args)
    return tempDef
    
# ===== end of handlerScrollTwoTextFrames =====
    
# ===== handlerTextLineNumbersReturn =====

def handlerTextLineNumbersReturn(self,event):
    """
    Add line number at bottom when 'return' is pressed,
    or when lines are inserted. Each line inserted must end
    with a '\n' (carriage return).
    """
    
    global stringLineNumberFormat
    
    def tempDef(event):
    
        print '\n** In handlerTextLineNumbersReturn'
#    print ' raw index =',eval(self.textMyCode.index(END))
    
        self.textLineNumbers['state']='normal'
    
# these values are strings
        indexCurrentLine, indexCurrentChar = self.textMyCode.index(INSERT).split('.')
        print 'Current line number, char = ',indexCurrentLine, indexCurrentChar
        indexEnd = self.textMyCode.index(END)
    
# these values are ints    
        indexCurrentLineInt = eval(indexCurrentLine)  
        indexDummy, lengthCurrentLine = self.textMyCode.index(indexCurrentLine + '.end').split('.')
        lengthCurrentLine = int(lengthCurrentLine)
        indexEndInt = eval(self.textMyCode.index(END))        
        print ' indexCurrentInt:',indexCurrentLineInt
        print ' indexEndInt:',indexEndInt
        print ' length of current line:',lengthCurrentLine
    
        index=str(float(indexEndInt))
        format=stringLineNumberFormat % (indexEndInt)
        
        print '*********'
        print 'indexEndInt =',indexEndInt
        print 'format =',format
        print 'self.textMyCode.index(END) =',self.textMyCode.index(END)
        print 'length of current line:',lengthCurrentLine
        print '*********'
     
# if wrap is turned on and line length exceeds text box width, then print the line number AND a carriage return    
        if self.checkWrap.get() and lengthCurrentLine > w_frameText:
            print "\nWrap is turned on."
            numNewLines = lengthCurrentLine / w_frameText
            print 'number of newLines =',numNewLines
            
            self.refreshLineNumbers()
            
            """
            
            for numNewLine in range(numNewLines):
                self.textLineNumbers.insert(
                    str(eval(self.textMyCode.index(INSERT)) + 1) ,
                    '\n'
                    )
                    
            self.textLineNumbers.insert(
                END,
#            self.textMyCode.index(END),
                '\n' + format       # line numbers right justified
                )
            """
                    
        else:
            self.textLineNumbers.insert(
                END,
#            self.textMyCode.index(END),
                '\n' + format      # line numbers right justified
                ) 
    
# make sure the current line we just moved to is visible
        self.textLineNumbers.see(str(float(indexCurrentLineInt+1)))
        self.textMyCode.see(str(float(indexCurrentLineInt+1)))
        print ' "SEE" line number index:',str(float(indexCurrentLineInt+1))
        print
        
        self.textLineNumbers['state']='disabled'
    
    return tempDef
    
    
# ===== end of handlerTextLineNumbersReturn =====
    
# ===== handlerTextLineNumbersUpArrow =====
def handlerTextLineNumbersUpArrow(self,event):
    """
    Purpose:
    makes sure the displayed line number matches with the text line properly;
    used with the up and down arrow keys
    """
    print '\n** In handlerSeeTextLineNumbersUpArrow'
    print ' current index:',self.textMyCode.index(INSERT)
    
    def tempDef(event):
 
        self.textLineNumbers['state']='normal' 
        index, char=self.textMyCode.index(INSERT).split('.')
# want to display line we are going to, not from whence we came
        indexFloat = float(eval(index)-1)
        index = str(indexFloat)
# never less than 1
        if indexFloat < 1.0 : 
            index='1.0'
        print ' --- Final index (up arrow) =',index        
        self.textLineNumbers.see(
            index
            )
        self.textLineNumbers['state']='disabled'
    
    return tempDef
        
# ===== end of handlerTextLineNumbersUpArrow =====        

# ===== handlerTextLineNumbersDownArrow =====
def handlerTextLineNumbersDownArrow(self,event):
    """
    Purpose:
    makes sure the displayed line number matches with the text line properly;
    used with the up and down arrow keys
    """

    def tempDef(event):
    
        print '\n** In handlerSeeTextLineNumbersDownArrow'
        print ' current index:',self.textMyCode.index(INSERT)
    
    
        self.textLineNumbers['state']='normal'
    
        indexCurrent, charCurrent = self.textMyCode.index(INSERT).split('.')
        indexEND, charEND = self.textMyCode.index(END).split('.')
        
        if (int(eval(indexCurrent))) == (int(eval(indexEND))-1):
            self.textLineNumbers.see(
                str(float(int(eval(self.textMyCode.index(END))) - 1))
                )
            print ' At end of file.'
            print '   cursor location at end of last line - index:',int(eval(self.textMyCode.index(END))) 
            self.textLineNumbers['state']='disabled'
            return
# we are at end of file, so behavior is to move cursor to end of line
# first, determine length of last line
# assemble the correct index
# move cursor to that location
# return
        print ' indexEND =',indexEND
# want to display line we are going to, not from whence we came
        indexCurrentFloat = float(eval(indexCurrent)+1)
        index = str(indexCurrentFloat)
        indexEndFloat = float(eval(indexEND))
# never greater than END
#    if indexFloat > indexFloatEND:
#        index = str(indexFloatEND)
        print ' --- Final index (down arrow) =',index
        self.textLineNumbers.see(
            index
            )
        self.textLineNumbers['state']='disabled'
        
    return tempDef
     
# ===== end of handlerTextLineNumbersDownArrow =====

# ===== handlerTempInsert =====
def handlerTempInsert(self):
    """
    inserts line and end number at current cursor location
    """
    def tempDef():
        indexCurrentLineNumber = self.textMyCode.index(INSERT)
        indexEndLineNumber = self.textMyCode.index(END)
        self.textMyCode.insert(
            INSERT,
#        'This is line ' + indexCurrentLineNumber + ', the end is located at ' + indexEndLineNumber
            'This is a line with a carriage return\n'
            )
    return tempDef

# ===== end of handlerTempInsert =====

# ===== handler TempDelete =====
def handlerTempDelete(self):
    """
    deletes end of lines
    """
    print '** In handlerTempDelete'
    self.textMyCode.insert(END,'This is the end line')
    raw_input()
    self.textMyCode.delete(END)
    self.textLineNumbers.delete(END)
    

# ===== handlerTextLineNumbersDelete =====
def handlerTextLineNumbersDelete(self,event):
    """
    Delete line number at bottom when 'delete' is pressed.
    """
    
    def tempDef(event):
        
        global widthLineNumbers
    
        print '\n** In handlerTextLineNumbersDelete'
#    print ' raw index =',eval(self.textMyCode.index(END))
    
        self.textLineNumbers['state']='normal'
    
# first check is there is a selection-delete
        try:
            print 'Checking for "Selection Delete"...'
            indexFirstLine, indexFirstChar = self.textMyCode.index(SEL_FIRST).split('.')
            indexLastLine, indexLastChar = self.textMyCode.index(SEL_LAST).split('.')
            print '\n SELECTION DELETE found:'
            print ' indexFirstLine, indexFirstChar =',indexFirstLine, indexFirstChar
            print ' indexLastLine, indexLastChar =', indexLastLine, indexLastChar
#        print ' WARNING: no selection-delete has been implemented yet.'
#        print '    delete operation halted.'
            
            diffLines = eval(indexLastLine) - eval(indexFirstLine)
            print ' Number of line numbers to selectively deleted =',diffLines
            
            for line in range(diffLines):
                indexBeginDelete = str(eval(self.textLineNumbers.index(END))-1)
                indexEndDelete = self.textLineNumbers.index(END)
                self.textLineNumbers.delete(indexBeginDelete,indexEndDelete)
                print ' .... deleted line',indexBeginDelete
                
            self.textLineNumbers['state']='disabled'
            
            return
            
# no selection, so come here for single character delete       
        except TclError:           
# these values are strings
            indexCurrentLine, indexCurrentChar = self.textMyCode.index(INSERT).split('.')
            print 'Current line number, char = ',indexCurrentLine, indexCurrentChar
            indexEnd = self.textMyCode.index(END)
    
# these values are ints   
            indexCurrentCharInt = int(eval(indexCurrentChar))
            if indexCurrentCharInt > 0:
                print ' Cursor is not at beginning of line.'
                print '   No line deletion yet, just character deletion.'
                return
            
            indexCurrentLineInt = int(eval(indexCurrentLine))
            if indexCurrentLineInt == 1 and indexCurrentCharInt == 0:
                print ' Cursor is at the beginning of line 1.'
                print '   No deletions allowed at this cursor location.'
                print
                self.textLineNumbers['state']='disabled'
                return
            
            indexBeginDelete = str(eval(self.textLineNumbers.index(END))-1)
            indexEndDelete= self.textLineNumbers.index(END)
            self.textLineNumbers.delete(indexBeginDelete,indexEndDelete)
    
            print ' Deleting from %s to %s in textLineNumbers' % (indexBeginDelete, indexEndDelete)
        
# line numbers take up 'widthLineNumbers' spaces
#        End=str(eval(indexEnd))
#        self.textLineNumbers.delete(End) 
#        newEnd = self.textMyCode.index(END)
#        self.textLineNumbers.delete(str(float(eval(newEnd))),str(float(eval(newEnd)+0.5)))
    
            self.textLineNumbers.delete(indexBeginDelete,indexEndDelete)
    
    
# plus values scroll line numbers up; neg values scroll down    
#    scrollLines = -5
#    self.textLineNumbers.yview_scroll(scrollLines,UNITS)
#    print ' Scroll line numbers in y direction:',scrollLines
    
# make sure the current line we just moved to is visible
            var=self.textMyCode.index(INSERT)
            self.textLineNumbers.see(var)
#        self.textLineNumbers.see(var)
#        self.textMyCode.see(var)
            print ' "SEE" line number index:',str(var)
            print
            
            self.textLineNumbers['state']='disabled'
            
    return tempDef

# ===== end of handlerTextLineNumbersDelete =====

# ===== handlerTextLineNumbersHilite =====
def handlerTextLineNumbersHilite(self,event):
    """ 
    hilight the current line when the cursor leaves or enters the window
    """
    
    def tempDef(event):
        
        print '\n** In handlerTextLineNumbersHilite'
        
        self.textLineNumbers['state']='normal'
        
# delete the hilite in the previous location    
        self.textLineNumbers.delete(
            self.indexLineNumberSave
            )
            
        print ' deleted indexLineNumberSave =',self.indexLineNumberSave
    
# determine current location        
        indexLineNumber, indexChar = self.textMyCode.index(INSERT).split('.')
        
        print 'Current indexLineNumber:',indexLineNumber
        
#   save the indexLine Number for unhiliting next time
        self.indexLineNumberSave = indexLineNumber + '.' + str(widthLineNumbers)
        
        self.textLineNumbers.insert(
            self.indexLineNumberSave,
            '>'
            )       
       
#    self.textLineNumbers.configure(bg='yellow').insert(indexLineNumber + '.' + str(widthLineNumbers))
    
        self.textLineNumbers['state']='disabled'
        
    return tempDef

# ===== end of handlerTextLineNumbersHilite =====

# ===== handlerTextLineNumbersUnhilite =====
def handlerTextLineNumbersUnhilite(self,event):
    """ 
    remove the hilight the current line when the cursor enters the window
    """
    
    def tempDef(event):
        
        print '\n** In handlerTextLineNumbersUnhilite'
        
        self.textLineNumbers['state']='normal'
        
        indexLineNumber, indexChar = self.textMyCode.index(INSERT).split('.')
        
        print 'indexLineNumber for hilite to be removed:', self.indexLineNumberSave
        
# indexLineNumber = eval(indexLineNumber)
        
        self.textLineNumbers.delete(
#        indexLineNumber + '.' + str(widthLineNumbers)
            self.indexLineNumberSave
            )
                
        self.textLineNumbers['state']='disabled'
        
    return tempDef
    
# ===== end of handlerTextLineNumbersUnhilite =====   

# ===== handlerTextMyCodeTab =====
def handlerTextMyCodeTab(self,event):
    """ 
    make sure a tab results in 4 spaces at a time,
    not a typical tab
    """
    
    def tempDef(event):
        print '\n** In handlerTextMyCodeTab'

        self.textMyCode.delete("%s-1c" % INSERT, INSERT)
        
        self.textMyCode.insert(
            INSERT,
            '    '
            )
    return tempDef
        
# ===== end of handlerTextMyCodeTab =====    

# ===== insertStringsIntoTextBox =====

def insertStringsIntoTextBox(self,tag,strings):
    """
    Purpose:
    - insert code blocks into PyRite code editor
    - checks strings for tags; if a tag is present, separate tag from string and insert string;
    - if no tag is present, just insert string
    
    Called by:
        handlerHeader_Insert
        handlerGeometry_Insert
        
    """
    
    def tempDef(tag,strings):
        
        global stringLineNumberFormat
        
        print '\n**In insertStringsIntoTextBox'
#    print '    You pushed the "Insert code" button'
        print '\n Insert tag value =',tag
        print 'Number of strings to insert:',len(strings)
        print
        
        import module_utilities_insertStringsIntoTextBox
        
        module_utilities_insertStringsIntoTextBox.insertStringsIntoTextBox(self,tag,strings,stringLineNumberFormat)
        
    return tempDef
    
# ===== end of insertStringsIntoTextBox =====

# ===== handlerCheckButtonWrap =====

def handlerCheckButtonWrap(self):
    """
    Purpose:
    determines in text wraps or not
    
    Called by:
    createWidgets
    
    Calls:
    None
    
    """
    
    def tempDef():
    
        global stringLineNumberFormat
    
        print '\n** In handlerCheckButtonWrap'
        print '     You clicked the "Wrap text" button'
        print '     self.checkWrap =',self.checkWrap
    
        if self.checkWrap.get():
# wrap is on
            self.textMyCode.configure(wrap=CHAR)
            print '   wrap is set to CHAR'
            self.checkWrapOff.set('Unwrap text')


        else:
# wrap is off
            self.textMyCode.configure(wrap=NONE)
            print '  wrap is set to NONE'
            self.checkWrapOff.set('Wrap text')
        
        refreshLineNumbers(self)
    return tempDef
    
# ===== end of handlerCheckButtonWrap =====

# ===== refreshLineNumbers =====
    
def refreshLineNumbers(self):
    """
    Refresh all line numbers when wrap is turned on or off,
    or when return in pressed and wrap is turned on,
    or when text is inserted and wrap is turned on
    """
    
    def tempDef():
        
        print '\n** In refreshLineNumbers'
        
        self.textLineNumbers['state']='normal'
# get current location
        currentLocation = self.textMyCode.index(INSERT)
            
# refresh all line numbers
# check if wrap is on
        wrapTrue = self.checkWrap.get()
        wrapTrue = 0
#  delete all line numbers
        self.textLineNumbers.delete(1.0,END)
# format line number
        format=stringLineNumberFormat % 1
#  start with first line
        self.textLineNumbers.insert(
            1.0,
            format
            )
        lengthCurrentLine = len(self.textMyCode.get(1.0,'1.end'))
        if wrapTrue and lengthCurrentLine > w_frameText:
            numNewLines = lengthCurrentLine / w_frameText
            for numNewLine in range(numNewLines):
                self.textLineNumbers.insert(
                    END,
                    '\n'
                    )
# return if only one line
        if int(eval(self.textMyCode.index(END))) == 1: 
            self.textLineNumbers.insert(
                self.indexLineNumberSave,
                '>'
                )
            self.textLineNumbers['state']='disabled'    
            return
        
# now for the others
        indexStart = 2
        indexEnd = int(eval(self.textMyCode.index(END)))
# check rest of lines in text files
        for line in range(indexStart,indexEnd):
            indexCurrentLineStart = float(line)
            indexCurrentLine, lengthCurrentLine = self.textMyCode.index(
                str(int(indexCurrentLineStart)) + '.end' 
                ) \
                .split('.')
            indexCurrentLine = int(indexCurrentLine)
            lengthCurrentLine = int(lengthCurrentLine)
            
            format = stringLineNumberFormat % line
            
            print '\nFor line %s:' % line
            print '   indexCurrentLineStart =',indexCurrentLineStart
            print '   indexCurrentLine =',indexCurrentLine
            print '   lengthCurrentLine =',lengthCurrentLine
# increase line number
# if wrap is turned on and line length exceeds text box width, then print the line number AND a carriage return    
            if wrapTrue and lengthCurrentLine > w_frameText:
                print "\nWrap is turned on and line length exceeds text box width."
                numNewLines = lengthCurrentLine / w_frameText
                print '   number of newLines =',numNewLines
            
                self.textLineNumbers.insert(
                    END,
                    '\n' + format       # line numbers right justified
                    )
                    
                for numNewLine in range(numNewLines):
                    self.textLineNumbers.insert(
                        END,
                        '\n'
                        )
                    
            else:
                self.textLineNumbers.insert(
                    END,
                    '\n' + format      # line numbers right justified
                    ) 
                    
# return to current location
        self.textLineNumbers.see(currentLocation)
        self.textMyCode.see(currentLocation)
        
        self.textLineNumbers.insert(
            self.indexLineNumberSave,
            '>'
            )
                    
        self.textLineNumbers['state']='disabled'
        
    return tempDef
        
# ===== end of refreshLineNumbers =====   

# ===== handlerPlusMinusLeadingSpaces =====

def handlerPlusMinusLeadingSpaces(self):
    """
    Purpose:
        Add or delete leading spaces as needed
    """
    import module_leadingSpaces
    
    print '\n** In handlerPlusMinusLeadingSpaces'
    
    def tempDef():
    
        myFrame = Toplevel(
            self.parentFrame0,
            background='lightgreen'
            )   
        myFrame.title('Add/Delete Leading Spaces')
        module_leadingSpaces.leadingSpaces(self,myFrame)  
        
    return tempDef

# ===== end of handlerPlusMinusLeadingSpaces =====

# ===== handlerSaveCode =====

def handlerSaveCode(self):
    """
    Purpose:
        save the code generated thus far to a file
    """
    
    def tempDef():
    
        global currentDirectory
        
        print '\n** In handlerSaveCode'
        
        options = {}
        options = {
            'defaultextension' : '.*',
            'filetypes' : [('All files','.*')],
            'initialdir' : currentDirectory,
            'initialfile' : '',
            'parent' : self.parentFrame0,
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
            
        myfile.write(self.textMyCode.get(1.0,END))
        myfile.close()
        print '\n     file %s has been written' % filename
        print 
        
    return tempDef
        
    
# ===== end of handlerSaveCode ====

# ==== handlerReadCode =====

def handlerReadCode(self,labelMain):
    """
    Purpose:
        read python code from a file
    """
    
    def tempDef():
        global currentDirectory
        
        print '\n** In handlerReadCode'
    
# define dictionary of options
        options = {}
        if labelMain == 'INPUT FILE':
            options = {
                'defaultextension' : '.inp',
                'filetypes' : [('input','.inp'),('All files','.*')],
                'initialdir' : currentDirectory,
                'initialfile' : '',
                'parent' : self.parentFrame0,
                'title' : 'Read input file'
                }  

        elif labelMain == 'PLOT FILE':
            options = {
                'defaultextension' : '.plt',
                'filetypes' : [('plot','.plt'),('All files','.*')],
                'initialdir' : currentDirectory,
                'initialfile' : '',
                'parent' : self.parentFrame0,
                'title' : 'Read plot file'
                }  
        else:
            options = {
                'defaultextension' : '.*',
                'filetypes' : [('All files','.*')],
                'initialdir' : currentDirectory,
                'initialfile' : '',
                'parent' : self.parentFrame0,
                'title' : 'Read file'
                }  
        
# get filename
#    dirname, filename = os.path.split(askopenfilename(**options))
        filename = askopenfilename(**options)
        print '\n    File opened:',filename
        myfileContents = ''
        myfileContents += open(filename,'r').read()
    
# clear text box 
# DWB - may want to check with user if this is ok, or may want to append or insert a file's code into present code
        ans=askyesno(
            'Clear text',
            'Clear text box before inserting file?'
            )
        if ans:    
            self.textMyCode.delete(1.0,END)
        
# read lines from filename and insert into text box self.textMyCode
        self.textMyCode.insert(
        1.0,
        myfileContents
        )       
        print '\n     file %s has been read' % filename
        print 
        
    return tempDef
    
# ===== end of handlerReadCode =====

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

# ===== handlerTextBox_Search =====
def handlerTextBox_Search(self):
    """
    Purpose:
    search for pattern in text box
    
    Called by:
    createWidgets
    
    Calls:
    None
    
    """
    
    def tempDef():
    
        print '\n** In handlerTextBox_Search'

# remove any tags
        print ' clearing tag "hilite" '
        self.textMyCode.tag_delete(
            'hilite'
            )
    
        pattern=self.entrySearchText.get()
        lengthPattern=len(pattern)
        currentIndex=self.textMyCode.index(INSERT)
        print ' pattern =',pattern
        print ' pattern length =',lengthPattern
        print ' currentIndex =',currentIndex


# match case
        if self.varCheckbuttonSearchText.get():
            ignoreCase=0    # do NOT ignore case
        else:
            ignoreCase=1    # ignore case
        print ' ignoreCase (0, ignore; 1, do not) =',ignoreCase
    
# search up
        if self.varCheckbuttonSearchTextUp.get():
            print ' ** Search direction: up'
            try:
                print ' patternSave = ',self.patternSave
                print ' pattern = ',pattern
                if pattern == self.patternSave:
                    goback=1
                    print 'patterns match; searching backwards'
                    print ' &&& self.indexSave =',self.indexSave
                    print ' &&& ignoreCase =',ignoreCase
                    print ' &&& goback =', goback
# start search at indexSave
                    indexFound=self.textMyCode.search(
                        pattern,
                        self.indexSave,
#                    stopindex=1.0,  # to prevent wrapping
                        nocase=ignoreCase,
                        backwards=goback,
                        )     
                else:
# if patterns do not match, start at INSERT
                    goback=1
                    print 'patterns DONT match; searching backwards'
                    indexFound=self.textMyCode.search(
                        pattern,
                        INSERT,
#                        stopindex=END, # to prevent wrapping
                        nocase=ignoreCase,
                        backwards=goback,
                        )                
            except (NameError, AttributeError):
# since patternSave does not exist, start at INSERT
                goback=1
                print 'patterns DONT match; no patternSave; searching backwards'
                indexFound=self.textMyCode.search(
                    pattern,
                    INSERT,
#                    stopindex=END, # to prevent wrapping
                    nocase=ignoreCase,
                    backwards=goback,
                    )
            
# search down
        else:
            print ' Search direction: down'
# move cursor past the current found word if search pattern is same as before    
            try:
                print ' patternSave = ',self.patternSave
                print ' pattern = ',pattern
                if pattern == self.patternSave:
                    print 'patterns match; searching forward'
#                    currentLine, currentChar = currentIndex.split('.')
                    currentLine, currentChar = self.indexSave.split('.')
                    newLine = currentLine
                    newChar = str(eval(currentChar) + lengthPattern)
                    indexNew = str(float(self.indexSave) + lengthPattern)
                    indexNew = newLine + '.' + newChar
                    self.textMyCode.insert(indexNew,'')
                    print ' old index =',currentLine
                    print ' indexNew after moving index =',indexNew
# patterns match, so start at indexSave from last time, plus a correction to get past the previous word
                    goback=0
                    indexFound=self.textMyCode.search(
                        pattern,
                        indexNew,
#                        stopindex=END, # to prevent wrapping
                        nocase=ignoreCase,
                        backwards=goback,
                        )
                else:
                    print 'patterns DONT match; searching forward'
# if patterns do not match, start at INSERT
                    goback=0
                    indexFound=self.textMyCode.search(
                        pattern,
                        INSERT,
#                        stopindex=END, # to prevent wrapping
                        nocase=ignoreCase,
                        backwards=goback,
                        )                
            except (NameError, AttributeError):
                print 'patterns DONT match; no patternSave; searching forward'
# since patternSave does not exist, start at INSERT
                goback=0
                indexFound=self.textMyCode.search(
                    pattern,
                    INSERT,
#                    stopindex=END, # to prevent wrapping
                    nocase=ignoreCase,
                    backwards=goback,
                    )
            

            
        print '  backwards (0=no, 1=yes) =',goback
        print '  indexFound =',indexFound
        
# return if nothing found    
        if indexFound == '':
            showinfo(
                'Not found',
                'Pattern \'' + pattern + '\' was not found.'
                )
            self.patternSave=''
            self.indexSave=''
            return
        else:
# place cursor at new word and make sure line is displayed in window
            self.textMyCode.see(indexFound)

#        
        indexLine, indexChar = indexFound.split('.')
        
        self.textLineNumbers.see(float(eval(indexLine)))
        
        self.textMyCode.tag_config(
            'hilite',
            background = 'lightgreen'
            )
        self.textMyCode.tag_add(
            'hilite',
            indexLine + '.' + indexChar,
            indexLine + '.' + str(eval(indexChar) + lengthPattern)
            )

            
# save pattern for next search
        self.patternSave=pattern
        self.indexSave=indexFound
        
    return tempDef
    
    

# ===== end of handlerTextBox_Search =====

# ===== handlerTextBox_MatchCase =====
def handlerTextBox_MatchCase(self):
    """
    Purpose:
    searches will depend on case
    
    Called by:
    createWidgets
    
    Calls:
    None
    
    """
    def tempDef():
        print '\n** In handlerTextBox_MatchCase'
        print '     You clicked the "Match case" button'
    return tempDef
# ===== end of handlerTextBox_MatchCase =====

# ===== handlerTextBox_ClearSelection =====
def handlerTextBox_ClearSelection(self):
    """
    Purpose:
    clear the text selection from text box
    
    Called by:
    createWidgets
    
    Calls:
    None
    
    """
    def tempDef():
        print '\n** In handlerTextBox_ClearSelection'
    
        ans=askokcancel(
            'Delete selection',
            'Do you really want to\ndelete this selection?'
            )
        if ans:        
            self.textMyCode.selection_clear()

            print '     Selection deleted.\n'
    
    return tempDef
    
# ===== end of handlerTextBox_ClearSelection =====

# ===== handlerClearTextField =====

def handlerClearTextField(self):
    """
    Purpose:
        give option to clear the entire text field
    """
    def tempDef():
        print '\n** In handlerClearTextField'
        print '     You have clicked "Clear all text" '
        ans=askokcancel(
            'Clear...',
            'This will clear the entire text box!\nAll unsaved data will be lost.\nContinue?'
            )
        
        if ans:
            self.textMyCode.delete(1.0,END) 
            print '   All text deleted.'
  
            self.textLineNumbers['state']='normal'
            self.textLineNumbers.delete(1.0,END)
# start numbering all over again
            self.textLineNumbers.insert(
            1.0,
            (stringLineNumberFormat % 1)
            )
            self.textLineNumbers['state']='disabled' 
            
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
        ans=askokcancel(
            'Quit...',
            'Quit PyCADD?\nBe sure to save your file before quitting!'
            )
        if ans:
            sys.exit()
        else:
            print '          Canceled'
            
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

             