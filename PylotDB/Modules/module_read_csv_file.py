# filename: read_csv_file.py
# Author: Shai Vaingast, from book "Beginning Python Visualization"
# Revised by: Daniel Barnette
# date: April 2009

import csv
import tkFont
import MySQLdb
from Tkinter import *
from tkFileDialog import *
from tkMessageBox import *  # askokcancel, showinfo, showerror, etc.
import Pmw
import sys

# module name
MODULE = 'module_read_csv_file.py'

# for debugging
DEBUG_CSV = 0           # if 1 or True, print variables for debugging
DEBUG_PRINT_METHOD = 0  # print method name every time the method is entered

class ReadCSVFile(Frame):
    def __init__(self,
        parent,
        colorbg,
        MySQL_Commands,
        MySQL_Output,
        myDatabase,
        myTable,
        myTableStructure,
        handlerDisplayAllFields,
        _user,
        _passwd,
        _host,
        _port,
        statusDbConnection,
        cursorHandleMySQL,
        ):
        
        Frame.__init__(self)
  
        self.frameParent = parent
        self.MySQL_Commands = MySQL_Commands
        self.MySQL_Output = MySQL_Output
        self.colorbg = colorbg
        self.myDatabase = myDatabase.lstrip()
        self.myTable = myTable.lstrip()
        self.myTableStructure = myTableStructure
        self.handlerDisplayAllFields = handlerDisplayAllFields
        self._userMySQL_Save = _user
        self._passwdMySQL_Save = _passwd
        self._hostMySQL_Save = _host
        self._portMySQL_Save = _port
        self.myDbConnection = statusDbConnection
        self.cursorHandleMySQL = cursorHandleMySQL

#        self.shell=shell
        
        if DEBUG_PRINT_METHOD:
            print('\n***** Welcome to ReadCSVFile *****\n')
        self.MySQL_Output(
            1,
            '***** Welcome to ReadCSVFile *****'
            )
            
# header input file lines begins with one of these characters
        self.headerFirstChar = [
            '#','c','C','>','*','&','%','@','!','+'
            ]
# list of how many lines to skip in header of input file
        self.headerLinesToSkip = [
        '1','2','3','4','5','6','7','8','9','10'
        ]
        
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
# define header font
        self.headerFont = tkFont.Font(
            family='arial',
            size='10',
            weight='bold',
            )
# define header font small
        self.headerFontSmall = tkFont.Font(
            family='arial',
            size='8',
            weight='bold',
            )
# define small button font
        self.buttonFontSmall = tkFont.Font(
            family='arial',
            size='7',
            )
# define smallest button font
        self.buttonFontSmallest = tkFont.Font(
            family='arial',
            size='6',
            )
# define data font
        self.dataFont = tkFont.Font(
            family='lucida console',
            size='10',
            )
# define table font
        self.tableFont = tkFont.Font(
            family='terminal',
            size='9',
            )
# ... button
        buttonFontFamily = 'helvetica'
        buttonFontSize = '8'
# define button font
        self.buttonFont = tkFont.Font(
            family=buttonFontFamily,
            size=buttonFontSize,
            )
            
# define toplevel
# destroy any old toplevel frames
        try:
            self.toplevelFindCsvFile.destroy()
            self.MySQL_Output(
            1,
            'Previous toplevel widget removed from screen.'
            )
        except: 
            self.MySQL_Output(
            1,
            'No previous toplevel widget to remove from screen.'
            )
                    
# open Toplevel frame for entering database name
        self.toplevelFindCsvFile = Toplevel(
            self.frameParent,
            bg=self.colorbg
            )
        self.toplevelFindCsvFile.title(
            'Add to database...'
            )
            
        self.toplevelFindCsvFile.transient(self.frameParent)
# place the top window
        x_Windows=400
        y_Windows=80
        self.toplevelFindCsvFile.geometry(
            '+%d+%d' % (x_Windows, y_Windows)
            )   
            
# call def to create widgets
        self.createWidgets()

# create widgets
    def createWidgets(self,):
        '''
        Create widgets for reading CSV data
        '''
        if DEBUG_PRINT_METHOD:
            print(
                '\n** In ' + MODULE + '/' + 
                'createWidgets'
                )
        self.MySQL_Output(
            1,
            '** In ' + MODULE + '/' + 'createWidgets'
            )    
# define frames
        frame_00 = Frame(
            self.toplevelFindCsvFile,
            bg=self.colorbg,
            )
        frame_00.grid(
            row=0,
            column=0,
            padx=0,
            pady=0,
            )
        
        frame_10 = Frame(
            self.toplevelFindCsvFile,
            bg=self.colorbg,
            )
        frame_10.grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky=W,
            )
            
        frame_15 = Frame(
            self.toplevelFindCsvFile,
            bg=self.colorbg,
            )
        frame_15.grid(
            row=2,
            column=0,
            padx=15,
            pady=0,
            sticky=W,
            )
        
        frame_20 = Frame(
            self.toplevelFindCsvFile,
            bg=self.colorbg,
            )
        frame_20.grid(
            row=3,
            column=0,
            padx=5,
            pady=5,
            sticky=W,
            )
            
        frame_25 = Frame(
            self.toplevelFindCsvFile,
            bg=self.colorbg,
            )
        frame_25.grid(
            row=4,
            column=0,
            padx=15,
            pady=0,
            sticky=W,
            )
        
        frame_30 = Frame(
            self.toplevelFindCsvFile,
            bg=self.colorbg,
            )
        frame_30.grid(
            row=5,
            column=0,
            padx=5,
            pady=0,
            sticky=W,
            )
            
        frame_35 = Frame(
            self.toplevelFindCsvFile,
            bg=self.colorbg,
            )
        frame_35.grid(
            row=6,
            column=0,
            padx=5,
            pady=5,
            sticky=W,
            )
        
        frame_40 = Frame(
            self.toplevelFindCsvFile,
            bg=self.colorbg,
            )
        frame_40.grid(
            row=7,
            column=0,
            padx=0,
            pady=5,
            )            

# Widgets
# FRAME 00
        
        labelReadCsvFile = Label(
            frame_00,
            text='READ DATA FROM FILE',
            font=self.titleFontBig,
            bg=self.colorbg
            )
        labelReadCsvFile.grid(
            row=0,
            column=0,
            columnspan=99,
            pady=5,
            )
            
# FRAME 10
        labelHeaderFiles = Label(
            frame_10,
            text='Header lines:',
            bg=self.colorbg,
            font=self.headerFontSmall,
            )
        labelHeaderFiles.grid(
            row=0,
            column=0,
            padx=0,
            pady=0,
            sticky=W,
            )
# FRAME 15
        self.var_radiobuttonSkipHeaderLines = StringVar()
        self.radiobuttonNoHeaderLines = Radiobutton(
            frame_15,
            variable=self.var_radiobuttonSkipHeaderLines,
            value='none',
            text='No header lines; read entire file',
            bg=self.colorbg,
#            command=self.handlerHeaderLines,
            )
        self.radiobuttonNoHeaderLines.grid(
            row=0,
            column=0,
            padx=0,
            pady=0,
            sticky=W,
            )

# set as default
        self.var_radiobuttonSkipHeaderLines.set('none')
            
        self.radiobuttonHeaderLines = Radiobutton(
            frame_15,
            variable=self.var_radiobuttonSkipHeaderLines,
            value='skip',
            text='Number of header lines to skip',
            bg=self.colorbg,
#            command=self.handlerHeaderLines,
            )
        self.radiobuttonHeaderLines.grid(
            row=1,
            column=0,
            padx=0,
            pady=0,
            sticky=W,
            )
            
        self.comboboxNumberOfHeaderLinesToSkip = Pmw.ComboBox(
            frame_15,
            scrolledlist_items=self.headerLinesToSkip,
            listheight=200,
            entry_width=3,
            sticky='w',
            scrolledlist_hull_width=10,
            )
        self.comboboxNumberOfHeaderLinesToSkip.grid(
            row=1,
            column=1,
            padx=0,
            pady=0,
            sticky=W,
            )
        self.comboboxNumberOfHeaderLinesToSkip.component('entryfield').setvalue(
            self.headerLinesToSkip[0]
            )
            
        self.radiobuttonLinesBeginWith = Radiobutton(
            frame_15,
            variable=self.var_radiobuttonSkipHeaderLines,
            value='begin_with',
            text='Ignore lines beginning with',
            bg=self.colorbg,
#            command=self.handlerHeaderLines,
            )
        self.radiobuttonLinesBeginWith.grid(
            row=2,
            column=0,
            padx=0,
            pady=0,
            sticky=W,
            )

        self.comboboxLinesBeginWith = Pmw.ComboBox(
            frame_15,
            scrolledlist_items=self.headerFirstChar,
            listheight=200,
            entry_width=3,
            sticky='w',
            scrolledlist_hull_width=10,
            )
        self.comboboxLinesBeginWith.grid(
            row=2,
            column=1,
            padx=0,
            pady=0,
            sticky=W,
            )
        self.comboboxLinesBeginWith.component('entryfield').setvalue(
            self.headerFirstChar[0]
            )
            
# FRAME 20
        labelFileFormat = Label(
            frame_20,
            text='File format:',
            background=self.colorbg,
            font=self.headerFontSmall,
            )
        labelFileFormat.grid(
            row=0,
            column=0,
            padx=0,
            pady=0,
            sticky=W,
            )
# FRAME 25    
        self.var_radiobuttonFileFormat = StringVar()
        self.radiobuttonFileFormatCsv = Radiobutton(
            frame_25,
            variable=self.var_radiobuttonFileFormat,
            value='csv',
            text='CSV (comma-separated values]',
            bg=self.colorbg,
            )
        self.radiobuttonFileFormatCsv.grid(
            row=0,
            column=0,
            padx=0,
            pady=0,
            sticky=W,
            )
            
        self.radiobuttonFileFormatYaml = Radiobutton(
            frame_25,
            variable=self.var_radiobuttonFileFormat,
            value='yaml',
            text='YAML',
            bg=self.colorbg,
            )
        self.radiobuttonFileFormatYaml.grid(
            row=1,
            column=0,
            padx=0,
            pady=0,
            sticky=W,
            )  
# set default to CSV
        self.var_radiobuttonFileFormat.set('csv')

# FRAME 30:
        labelFileFormat = Label(
            frame_30,
            text='Select INPUT file:',
            background=self.colorbg,
            font=self.headerFontSmall,
            )
        labelFileFormat.grid(
            row=0,
            column=0,
            padx=0,
            pady=0,
            sticky=W,
            )
# FRAME 35:
# open file and display full path and filename in boxes
        labelPathName = Label(
            frame_35,
            text='Path:',
            bg=self.colorbg,
            justify=RIGHT,
            )
        labelPathName.grid(
            row=0,
            column=0,
            sticky=E,
            padx=0,
            pady=5,
            )
        
        self.entryPathName = Pmw.ScrolledText(
            frame_35,
            text_padx=3,
            text_pady=3,
            vscrollmode='static',
            text_font=self.buttonFontSmall,
            usehullsize=1,
            hull_width=225,
            hull_height=60,
            )
        self.entryPathName.grid(
            row=0,
            column=1,
            padx=5,
            pady=0,
            sticky=W,
            )
        
        labelFileName = Label(
            frame_35,
            text='File: ',
            bg=self.colorbg,
            justify=RIGHT,
            )
        labelFileName.grid(
            row=1,
            column=0,
            sticky=E,
            padx=0,
            pady=5
            )
        
        self.entryFileName = Pmw.EntryField(
            frame_35,
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
            frame_35,
            text='Browse',
            width=6,
            borderwidth=5,
            bg='white',
            fg='blue',
            relief=RAISED,
            font=self.buttonFont,
            command=self.askOpenFilename,
#            command=handlerReadCode(self)
            )
        buttonFileName.grid(
            row=2,
            column=1,
            sticky=N,
            padx=0,
            pady=0,
            )
        
        labelTotalLines = Label(
            frame_35,
            text='Lines in file: ',
            bg=self.colorbg,
            )
        labelTotalLines.grid(
            row=2,
            column=0,
            sticky=E,
            padx=5,
            pady=1,
            )
        
        self.entryTotalLines = Entry(
            frame_35,
            width=8,
            bg='white',
            fg='black',
            justify=LEFT,
            disabledbackground='white',
            disabledforeground='black',
            )
        self.entryTotalLines.grid(
            row=2,
            column=1,
            sticky=W,
            padx=0,
            pady=1,
            )
        self.entryTotalLines.insert(0,'')
        self.entryTotalLines.configure(state=DISABLED)

# FRAME 40
# Read data button
# ... command opens up another window which displays results before inserting into table
        self.buttonReadCsvFile = Button(
            frame_40,
            text='Read Datafile...',
#            bg=self.colorbg,
            borderwidth=5,
            relief=RAISED,
            justify=CENTER,
            width=12,
            command=self.handlerReadCsvFile,
            )
        self.buttonReadCsvFile.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            )
        self.buttonReadCsvFile.configure(state='disabled')

# cancel button
        buttonCancelReadCsvFile = Button(
            frame_40,
            text='Cancel',
#            bg=self.colorbg,
            borderwidth=5,
            relief=RAISED,
            justify=CENTER,
            width=6,
            command=(lambda: self.toplevelFindCsvFile.destroy())
            )
        buttonCancelReadCsvFile.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            )
            
        return

      
# def to handle csv files
    def handlerReadCsvFile(self):
        '''
        Reads a CSV file and returns it as a list of rows.
        
        File has been opened in 'def askOpenFilename(self):'
        
        Input attributes:
            self.myOpenCsvFile                  CSV file, opened
            self.rowCount_MyOpenCsvFile         number of lines in CSV file
            self.elementsPerRow_MyOpenCsvFile   number of elements per row
        '''
        if DEBUG_PRINT_METHOD:
            print(
                '\n** In ' + MODULE + '/' + 
                'handlerReadCsvFile'
                )
        self.MySQL_Output(
            1,
            '** In ' + MODULE + '/' + 'handlerReadCsvFile'
            ) 
        if not self.entryFileName.getvalue():
            print '\nNo filename is available. Check input and try again.'
            self.MySQL_Output(
                1,
                '  ... No filename is available. Check input and try again.'
                )
            try:
                showinfo(
                    'Error: no filename',
                    '\nNo filename is available.' + '\n\n' +
                    'Check input and try again.',
                    parent=self.toplevelFindCsvFile
                    )
            except:
                showinfo(
                    'Error: no filename',
                    '\nNo filename is available.' + '\n\n' +
                    'Check input and try again.',
                    )
            return
            
# rewind file
        try:
            self.myOpenCsvFile.seek(0,0)
        except:
            stringOpenCsvError = (
                'For some reason, file\n' +
                '%s\n' +
                'cannot be rewound to be read.\n\n' +
                'This process cannot continue.'
                )
            print('\n' + stringOpenCsvError)
            self.MySQL_Output(
                0,
                stringOpenCsvError
                )
            try:
                showerror(
                    'Error: cannot rewind csv file',
                    stringOpenCsvError,
                    parent=self.toplevelReadCsvFile
                    )
            except:
                showerror(
                    'Error: cannot rewind csv file',
                    stringOpenCsvError
                    )
            return
        
# initialize
        rowsOfData = 0
        rowsSkipped = 0
        rowsTotal = 0
       
# do some error checks
        if self.var_radiobuttonSkipHeaderLines.get() == 'none':
            rowsSkipped = 0
            
        if self.var_radiobuttonSkipHeaderLines.get() == 'skip':
            try:
                rowsSkipped = int(self.comboboxNumberOfHeaderLinesToSkip.get())
            except:
                errorSkip1 = (
                    'Number of lines to skip is not an integer.\n\n' +
                    ' Enter a valid integer and try again.\n\n'
                    )
                print (
                    '\n' + errorSkip1
                    )
                try:
                    showinfo(
                        'Error: not an integer',
                        errorSkip1,
                        parent=self.toplevelFindCsvFile
                        )
                except:
                    showinfo(
                        'Error: not an integer',
                        errorSkip1
                        )
                return
                
            print '\n>> Rows skipped = %s' % rowsSkipped
            print 'total lines = %s' % self.entryTotalLines.get()
        
            if rowsSkipped < 0:
                errorSkip2 = (
                    'Number of header lines to skip must be a\n' + 
                    'positive integer.\n\n' + 
                    'Enter a positive integer and try again.\n\n'
                    )
                print (
                    '\n' + errorSkip2
                    )
                try:
                    showinfo(
                        'Error: invalid value',
                        errorSkip2,
                        parent=self.toplevelFindCsvFile
                        )
                except:
                    showinfo(
                        'Error: invalid value',
                        errorSkip2
                        )
                return
            if rowsSkipped >= self.entryTotalLines.get():
                errorSkip3 = (
                    'Number of header lines to skip must be\n' +
                    ' less than total lines in the input file.\n\n' +
                    'Adjust number of header lines to skip and\n' + 
                    ' try again.\n\n'
                    )
                print(
                    '\n' + errorSkip3
                    )
                try:
                    showinfo(
                        'Error: invalid value',
                        errorSkip3,
                        parent=self.toplevelFindCsvFile
                        )
                except:
                    showinfo(
                        'Error: invalid value',
                        errorSkip3
                        )
                return
# get symbol to determine what lines to skip
        if self.var_radiobuttonSkipHeaderLines.get() == 'begin_with':
            symbolToSkip = self.comboboxLinesBeginWith.get()
            if symbolToSkip == '':
                errorstringSymbolToSkip = (
                    'No symbol has been specified.\n\n' +
                    'Select a symbol and try again.\n\n'
                    )
                print(
                    '\n' + errorstringSymbolToSkip
                    )
                try:
                    showinfo(
                        'Error: no symbol',
                        '\n' + errorstringSymbolToSkip,
                        parent=self.toplevelFindCsvFile
                        )
                except:
                    showinfo(
                        'Error: no symbol',
                        '\n' + errorstringSymbolToSkip
                        )
                return
                
# csv.reader returns a list of lists, where each list contains individual string elements        

# check each row for validity        
        for row in csv.reader(self.myOpenCsvFile):
            rowsTotal += 1
#            if DEBUG_CSV:
#                print '  Row %s (len %s): %s' % (rowsTotal, len(row), row)
            
# check for empty row
            if row == '':
                errorstringEmptyRow = (
                    'Row %s is empty.\n\n' +
                    'Empty rows are not allowed.\n\n' +
                    'Check row values in file and try again.\n\n' +
                    'Operation halted.\n\n'
                    ) % rowsTotal
                print(
                    '\n' + errorstringEmptyRow
                    )
                try:
                    showinfo(
                        'Error: empty row',
                        '\n' + errorstringEmptyRow,
                        parent=self.toplevelFindCsvFile
                        )
                except:
                    showinfo(
                        'Error: empty row',
                        '\n' + errorstringEmptyRow
                        )
                return
#        for row in csv.reader(open(self.filename)):
            if self.var_radiobuttonSkipHeaderLines.get() == 'none':
                rowsOfData += 1
#                self.dataCsv.append(row)
            elif self.var_radiobuttonSkipHeaderLines.get() == 'skip':
                if rowsTotal > rowsSkipped:
                    rowsOfData += 1
#                    self.dataCsv.append(row)
            elif self.var_radiobuttonSkipHeaderLines.get() == 'begin_with':
                if row[0][0:1] <> symbolToSkip:
                    rowsOfData += 1
                else:
                    rowsSkipped += 1
#                    self.dataCsv.append(row)
            else:
                errorHeaderLines = (
                    'Internal Error: Header lines have been incorrectly\n' + 
                    ' specified by code logic.\n\n' + 
                    'Contact code administrator about this problem.\n\n' +
                    'This operation is canceled.\n\n' 
                    )
                print (
                    '\n' + errorHeaderLines
                    )
                try:
                    showinfo(
                        'Internal error',
                        '\n' + errorHeaderLines,
                        parent=self.toplevelFindCsvFile
                        )
                except:
                    showinfo(
                        'Internal error',
                        '\n' + errorHeaderLines
                        )
                return

# check for proper number of elements per row, internal to input file
            if rowsOfData == 1:
                self.elementsPerRow_MyOpenCsvFile = len(row)
# store first data row for output in window
                rowDisplayForComparison = row
# 'rowsOfData' can be zero, so have to use the following statement, not just 'else'
            elif rowsOfData > 1:
                elementsPerRow = len(row)
                if elementsPerRow != self.elementsPerRow_MyOpenCsvFile:
                    print '\nError in element count:'
                    print '  Row 1 element count: %s' % self.elementsPerRow_MyOpenCsvFile
                    print '  Row %s element count: %s' % (rowsTotal, elementsPerRow)
                    stringElementCountError = (
                        'Error in element count:' + '\n' +
                        '  Row 1 element count: %s \n' +
                        '  Row  %s element count: %s' + '\n\n' +
                        'Row element counts must be the same.\n\n' +
                        'Check "Header lines" selection in "Read Data\n' +
                        '  From File" to make sure correct option has\n' +
                        '  been selected, then try again.\n\n' +
                        'Otherwise, the file format may be incorrect\n' +
                        '  due to an unknown reason.\n\n'
                        )
                    self.MySQL_Output(
                        1,
                        (stringElementCountError
                        )
                        % (self.elementsPerRow_MyOpenCsvFile,rowsTotal,elementsPerRow)
                        )
                    try:
                        showinfo(
                            'Error: wrong element count',
                            (stringElementCountError
                            )
                            % (self.elementsPerRow_MyOpenCsvFile,rowsTotal,elementsPerRow),
                            parent=self.toplevelFindCsvFile
                            )
                    except:
                        showinfo(
                            'Error: wrong element count',
                            (stringElementCountError
                            )
                            % (self.elementsPerRow_MyOpenCsvFile,rowsTotal,elementsPerRow)
                            )
                    return
                    
# error if no data
        if rowsOfData == 0:
            stringNoData = (
                'Data cannot be read based on parameters\n' +
                ' specified by user.\n\n' +
                'Example: perhaps the lines to be skipped\n' +
                ' are equal to or greater than the total\n' +
                ' number of lines in the file.\n\n' +
                'Specify new values and try again.\n\n'
                )
            print(
                stringNoData
                )
            try:
                showinfo(
                    'Warning: no data to read',
                    stringNoData,
                    parent=self.toplevelFindCsvFile
                    )
            except:
                showinfo(
                    'Warning: no data to read',
                    stringNoData
                    )
            return
            
        print('\n' + '-'*40 + '\n')
        
        '''
        Another way to read the file, but elements are not output as strings:
        # open the file and store contents in myfileContents; however, this
        #   is not a good idea for large files
        myfileContents = open(self.filename,'r').readlines()
        lenMyFileContents = len(myfileContents)
        print '\nInput file has %s lines.' % len(myfileContents)
        '''
        
# data seems ok at this point
                            
# specify background color of window
        colorbg='lightgreen'
# define toplevel
# destroy any old toplevel frames
        try:
            self.toplevelReadCsvFile.destroy()
            self.MySQL_Output(
            1,
            'Previous toplevel widget removed from screen.'
            )
        except: 
            self.MySQL_Output(
            1,
            'No previous toplevel widget to remove from screen.'
            )
                    
# open Toplevel frame for entering database name
        self.toplevelReadCsvFile = Toplevel(
            self.toplevelFindCsvFile,
            bg=colorbg,
            )
        self.toplevelReadCsvFile.title(
            'Import CSV data ...'
            )
            
        self.toplevelReadCsvFile.transient(self.frameParent)
# place the top window
        x_Windows=750
        y_Windows=20
        self.toplevelReadCsvFile.geometry(
            '+%d+%d' % (x_Windows, y_Windows)
            )

# remember, rows are not stored, so have to read file again with parameters from 'IMPORT CSV DATA' window to determine
#    which lines will be inserted into database directly from file; this reduces storage and increases speed, especially for 
#    really large tables!!!!
# once data is successfully read, print 'do you wish to refresh table?' but must invoke 'Refresh complete table" button

#  several checks on bounds and proper values
# frames
        frame_00 = Frame(
            self.toplevelReadCsvFile,
            bg=colorbg,
            )
        frame_00.grid(
            row=0,
            column=0,
            pady=5,
            )
            
        frame_10 = Frame(
            self.toplevelReadCsvFile,
            bg=colorbg,
            )
        frame_10.grid(
            row=1,
            column=0,
            pady=5,
            )
            
        frame_15 = Frame(
            self.toplevelReadCsvFile,
            bg=colorbg,
            )
        frame_15.grid(
            row=2,
            column=0,
            pady=5,
            )
            
        frame_20 = Frame(
            self.toplevelReadCsvFile,
            bg=colorbg,
            )
        frame_20.grid(
            row=3,
            column=0,
            pady=5,
            )
            
        frame_25 = Frame(
            self.toplevelReadCsvFile,
            bg=colorbg,
            )
        frame_25.grid(
            row=4,
            column=0,
            pady=5,
            )
        
# frame_00 widgets
# ... title
        labelTitle = Label(
            frame_00,
            text=('IMPORT CSV DATA\nfile: %s' % self.entryFileName.get()),
            font=self.titleFontBig,
            bg=colorbg,
            )
        labelTitle.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=5,
            )
# ... database          
        labelDatabase = Label(
            frame_00,
            text='Database:',
            bg=colorbg,
            )
        labelDatabase.grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky=E,
            )
            
        entryDatabase = Entry(
            frame_00,
            disabledbackground='white',
            disabledforeground='black',
            )
        entryDatabase.grid(
            row=1,
            column=1,
            padx=5,
            pady=5,
            sticky=W,
            )
        entryDatabase.configure(state=NORMAL)
        entryDatabase.insert(0,self.myDatabase)
        entryDatabase.configure(state=DISABLED)
# ... table
        labelTable = Label(
            frame_00,
            text='Table:',
            bg=colorbg,
            )
        labelTable.grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky=E,
            )
            
        entryTable = Entry(
            frame_00,
            disabledbackground='white',
            disabledforeground='black',
            )
        entryTable.grid(
            row=2,
            column=1,
            padx=5,
            pady=5,
            sticky=W,
            )
        entryTable.configure(state=NORMAL)
        entryTable.insert(0,self.myTable)
        entryTable.configure(state=DISABLED)
        
# ... table columns
        labelTableColumns = Label(
            frame_00,
            text='Table fields per row:',
            bg=colorbg,
            )
        labelTableColumns.grid(
            row=3,
            column=0,
            padx=5,
            pady=5,
            sticky=E,
            )
            
        entryTableColumns = Entry(
            frame_00,
            disabledbackground='white',
            disabledforeground='black',
            )
        entryTableColumns.grid(
            row=3,
            column=1,
            padx=5,
            pady=5,
            sticky=W,
            ) 
        entryTableColumns.configure(state=NORMAL)
        entryTableColumns.insert(0,len(self.myTableStructure))
        entryTableColumns.configure(state=DISABLED)
        
# ... data elements per row
        labelDataElementsPerRow = Label(
            frame_00,
            text='Import-data-fields per row\n(excludes auto_index field):',
            bg=colorbg,
            )
        labelDataElementsPerRow.grid(
            row=4,
            column=0,
            padx=5,
            pady=5,
            sticky=E,
            )
            
        entryDataElementsPerRow = Entry(
            frame_00,
            disabledbackground='white',
            disabledforeground='black',
            )
        entryDataElementsPerRow.grid(
            row=4,
            column=1,
            padx=5,
            pady=5,
            sticky=W,
            )
        entryDataElementsPerRow.configure(state=NORMAL)
        entryDataElementsPerRow.insert(0,self.elementsPerRow_MyOpenCsvFile)
        entryDataElementsPerRow.configure(state=DISABLED)

# ... data rows
        labelDataRows = Label(
            frame_00,
            text='Input-file rows total:',
            bg=colorbg,
            )
        labelDataRows.grid(
            row=5,
            column=0,
            padx=5,
            pady=5,
            sticky=E,
            )
            
        entryDataRows = Entry(
            frame_00,
            disabledbackground='white',
            disabledforeground='black',
            )
        entryDataRows.grid(
            row=5,
            column=1,
            padx=5,
            pady=5,
            sticky=W,
            ) 
        entryDataRows.configure(state=NORMAL)
        entryDataRows.insert(0,rowsTotal)
        entryDataRows.configure(state=DISABLED)
        
# frame_10 widgets
# ... title
        labelTableComparisons = Label(
            frame_10,
            text='    Comparisons of 1st Data Row with Table Datatypes    ',
            bg=colorbg,
            font=self.titleFontBig,
            )
        labelTableComparisons.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            sticky=E,
            ) 
# ... scrollable box     
        fixedFont = Pmw.logicalfont('Fixed')
        scrolledtextSummary = Pmw.ScrolledText(
            frame_10,
            columnheader=1,
            rowheader=1,
            rowcolumnheader=1,
            usehullsize=1,
            hull_width=425,
            hull_height=300,
            text_wrap='none',
            text_font=fixedFont,
            Header_font=fixedFont,
            Header_foreground='black',
            Header_background='lightgreen',
            rowheader_width=3,
            rowheader_font=fixedFont,
            rowcolumnheader_width=3,
            text_padx=3,
            text_pady=3,
            Header_padx=3,
            rowheader_pady=0,
            hscrollmode='static',
            vscrollmode='static',
            )
        scrolledtextSummary.grid(
            row=1,
            column=0,
            sticky='e' + 'w',
            )
# create row header from list of field names
        headerFieldNames = ['1st_Data_Row','Column_Name','Datatype']
        scrolledtextSummary.component('rowcolumnheader').insert('end','No.')
        
# count number of entries; put numbers under 'No.'
        for count in range(len(self.myTableStructure)):
            count+=1
            scrolledtextSummary.component('rowheader').insert('end','%3u\n' % count )
      
# create column headers
        headerLine = '%12s  %-12s  %-12s' % ('1st_Data_Row','Column_Name','Datatype') 
        scrolledtextSummary.component('columnheader').insert('0.0',headerLine)
        countTotal = 0
        mismatch=0
        for struct in self.myTableStructure:
            countTotal+=1
# ignore auto_index column
            if struct[0][0:12] == 'auto_index':
                continue
            else:
                try:
                    dataLine = '%12s  %-12s  %-12s\n' % (
                        rowDisplayForComparison[countTotal-1][0:12],
                        struct[0][0:12],
                        struct[1]
                        )
                except:
                    mismatch=1
                    dataLine = '%12s  %-12s  %-12s\n' %(
                        '???',
                        struct[0][0:12],
                        struct[1]
                        )
            scrolledtextSummary.insert('end',dataLine)
# simple check for errors
#        print ('>> Number of data elements per row = %s' % (len(self.myTableStructure)))
# frame _15 widgets
# ... header lines skipped
        labelHeaderLinesSkipped = Label(
            frame_15,
            text='Header lines skipped:',
            bg=colorbg,
            )
        labelHeaderLinesSkipped.grid(
            row=0,
            column=0,
            padx=5,
            pady=2,
            sticky=E,
            )
        self.varEntryheaderLinesSkipped = StringVar()
        self.entryHeaderLinesSkipped = Entry(
            frame_15,
            width=8,
            textvariable=self.varEntryheaderLinesSkipped,
            disabledbackground = 'white',
            disabledforeground = 'black',
            )
        self.entryHeaderLinesSkipped.grid(
            row=0,
            column=1,
            padx=0,
            pady=2,
            sticky=W,
            )
        self.varEntryheaderLinesSkipped.set(rowsSkipped)
        self.entryHeaderLinesSkipped.configure(state='disabled')
            
# ... header lines read
        labelLinesWithValidData = Label(
            frame_15,
            text='Lines containing valid data:',
            bg=colorbg,
            )
        labelLinesWithValidData.grid(
            row=1,
            column=0,
            padx=5,
            pady=2,
            sticky=E,
            )
        self.varEntryLinesWithValidData = StringVar()    
        self.entryLinesWithValidData = Entry(
            frame_15,
            width=8,
            textvariable=self.varEntryLinesWithValidData,
            disabledbackground='white',
            disabledforeground='black',
            )
        self.entryLinesWithValidData.grid(
            row=1,
            column=1,
            padx=0,
            pady=2,
            sticky=W,
            ) 
        self.varEntryLinesWithValidData.set(rowsOfData)
        self.entryLinesWithValidData.configure(state='disabled')
# frame_20 widgets
# ... start importing at line #
        labelLineStart = Label(
            frame_20,
            text='Begin importing at line\n(editable):',
            bg=colorbg,
            justify=RIGHT,
            )
        labelLineStart.grid(
            row=0,
            column=0,
            padx=5,
            pady=2,
            sticky=E,
            )
            
        rowStart = rowsSkipped + 1
        self.varEntryLineStart = StringVar()
        self.entryLineStart = Entry(
            frame_20,
            width=8,
            textvariable=self.varEntryLineStart,
            )
        self.entryLineStart.grid(
            row=0,
            column=1,
            padx=0,
            pady=2,
            sticky=W,
            ) 
        self.varEntryLineStart.set(rowStart)
        self.entryLineStart.bind(
            "<Any-KeyRelease>",
            self.handlerUpdateBeginningNumberOfLinesToImport
            )
# ... end importing at line #
        labelLineEnd = Label(
            frame_20,
            text=' and end at line\n(editable):',
            bg=colorbg,
            justify=RIGHT,
            )
        labelLineEnd.grid(
            row=0,
            column=2,
            padx=0,
            pady=2,
            sticky=W,
            )
        rowEnd = rowsTotal
        self.varEntryLineEnd = StringVar()
        self.entryLineEnd = Entry(
            frame_20,
            width=8,
            textvariable=self.varEntryLineEnd,
            )
        self.entryLineEnd.grid(
            row=0,
            column=3,
            padx=0,
            pady=2,
            sticky=W,
            ) 
        self.varEntryLineEnd.set(rowEnd)
        self.entryLineEnd.bind(
            "<Any-KeyRelease>",
            self.handlerUpdateEndingNumberOfLinesToImport
            )
            
# need to be able to refer back to these values, so attach to instance using self
# ... begin importing at line:
        self.rowStart = rowStart
# ... and end at line:
        self.rowsTotal = rowsTotal # used in other methods
# ... lines containing valid data
        self.rowsOfData = rowsOfData
# ... header lines skipped:
        self.rowsSkipped = rowsSkipped # used in other methods
# ... number of lines to import:
        self.rowsToBeImported = rowEnd - rowStart + 1

# ... total lines to import
        labelLinesToImport = Label(
            frame_20,
            text='Number of lines to import:',
            bg=colorbg,
            )
        labelLinesToImport.grid(
            row=1,
            column=0,
            padx=5,
            pady=2,
            sticky=E,
            )
            
        self.varEntryLinesToImport = StringVar()
        self.entryLinesToImport = Entry(
            frame_20,
            width=8,
            textvariable=self.varEntryLinesToImport,
            disabledbackground='white',
            disabledforeground='black',
            )
        self.entryLinesToImport.grid(
            row=1,
            column=1,
            padx=0,
            pady=2,
            sticky=W,
            ) 
        self.varEntryLinesToImport.set(self.rowsToBeImported)
        self.entryLinesToImport.configure(state='disabled')
        
# line counter
        labelLinesImportedCounter = Label(
            frame_20,
            text=' Number of lines\nimported:',
            bg=colorbg,
            justify=RIGHT,
            )
        labelLinesImportedCounter.grid(
            row=1,
            column=2,
            padx=0,
            pady=2,
            sticky=W,
            )
        self.varEntryLinesImportedCounter = StringVar()
        self.entryLinesImportedCounter = Entry(
            frame_20,
            width=8,
            textvariable=self.varEntryLinesImportedCounter,
            disabledbackground='white',
            disabledforeground='black',
            )
        self.entryLinesImportedCounter.grid(
            row=1,
            column=3,
            padx=0,
            pady=2,
            sticky=W,
            ) 
        self.varEntryLinesImportedCounter.set(0)
        self.entryLinesImportedCounter.configure(state='disabled')
        
# reset button
        self.buttonEntryLinesReset = Button(
            frame_20,
            text='Reset all',
            width=10,
            borderwidth=3,
            relief=RAISED,
            justify=CENTER,
            command=self.handlerButtonEntryLinesReset,
            background='white',
            foreground='blue',
            )
        self.buttonEntryLinesReset.grid(
            row=2,
            column=0,
            columnspan=99,
            padx=0,
            pady=0,
            )
        
# ... command opens up another window before inserting into table
        self.varTextForReadCsvFileImport = StringVar()
        self.varTextForReadCsvFileImport.set('Import to table')
        self.varStartStopCsvFileImport = IntVar()
        self.checkbuttonReadCsvFileImport = Checkbutton(
            frame_25,
            indicatoron=0,
            textvariable=self.varTextForReadCsvFileImport,
            variable=self.varStartStopCsvFileImport,
            borderwidth=5,
            relief=RAISED,
            justify=CENTER,
            width=30,
            background='white',
            foreground='blue',
            selectcolor='yellow',
            command=self.handlerImportToDatabase,
            )
        self.checkbuttonReadCsvFileImport.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            )
        
# cancel button
        buttonCancelReadCsvFileImport = Button(
            frame_25,
            text='Cancel',
            borderwidth=5,
            relief=RAISED,
            justify=CENTER,
            width=10,
#            command=(lambda: self.toplevelReadCsvFile.destroy())
            command=self.handlerCancelReadCsvFileImport,
            )
        buttonCancelReadCsvFileImport.grid(
            row=1,
            column=0,
            columnspan=99,
            padx=5,
            pady=5,
            )

# ... prevent users from modifying text and headers
        scrolledtextSummary.configure(
            text_state='disabled',
            Header_state='disabled'
            )            
# checks
# ... if number of data elements and number of table columns don't agree
        if mismatch:

# ... define error string
            stringError = (
                'Error: total number of data elements does' + '\n' +
                '  NOT match number of table columns.' + '\n\n' + 
                'Check that correct CSV file is being imported.' + '\n'
                )
# ... output error
            self.MySQL_Output(
                0,
                stringError
                )
            try:
                showinfo(
                    'Error: data mismatch',
                    stringError + '\n',
                    parent=self.toplevelReadCsvFile
                    )
            except:
                showinfo(
                    'Error: data mismatch',
                    stringError + '\n'
                    )
            return  
        else:
# ... if number of data elements and number of table columns agree
            printString = (
#                '-------------------' + '\n' +
                'Number of data elements per row and' + '\n' + 
                ' number of column names match.' + '\n\n' + 
                'Please check "IMPORT CSV DATA" window\n' +
                ' to ensure that Data and Datatype' + '\n' +
                ' columns correspond, then click on' + '\n' +
                ' "Import to table" to import data to table.\n\n'
                )

            self.MySQL_Output(
                0,
                printString
                )
            try:
                showinfo(
                    'SUCCESS: data match',
                    '\n' + printString,
                    self.toplevelReadCsvFile
                    )
            except:
                showinfo(
                    'SUCCESS: data match',
                    '\n' + printString
                    )
# everything ok to this point; enable button to import data to table            
#            self.buttonReadCsvFileImport.configure(state=NORMAL)
            
        return
        
        
    def handlerButtonEntryLinesReset(self):
        '''
        Purpose:
            reset all entries in IMPORT CSV DATA window to original values
        '''
        if DEBUG_PRINT_METHOD:
            print(
                '\n** In ' + MODULE + '/' + 
                'handlerButtonEntryLinesReset'
                )
        self.MySQL_Output(
            1,
            '** In ' + MODULE + '/' + 
            'handlerButtonEntryLinesReset'
            )
# reset 'begin importing at line'
        self.varEntryLineStart.set(self.rowStart)
# reset 'and end at line'
        self.varEntryLineEnd.set(self.rowsTotal)
# reset 'number of lines to import'
        self.varEntryLinesToImport.set(self.rowsToBeImported)
# reset 'number of lines imported'
        self.varEntryLinesImportedCounter.set(0)
        self.entryLinesToImport.configure(disabledbackground='white')
        
        return
        
    def handlerUpdateBeginningNumberOfLinesToImport(self,event):
        '''
        Purpose:
            updates the 'number of lines to import' field when the
            beginning number of lines to read is changed.
            
        Checks for the following input errors:
        1. entry must be an integer
        2. input must not be a negative number
        3. start line cannot be less than the number of header lines skipped
        4. start line must not be greater than total number of lines
        '''
        if DEBUG_PRINT_METHOD:
            print(
                '\n** In ' + MODULE + '/' + 
                'handlerUpdateBeginningNumberOfLinesToImport'
                )
        self.MySQL_Output(
            1,
            '** In ' + MODULE + '/' + 
            'handlerUpdateBeginningNumberOfLinesToImport'
            )        
        
# reset 'number of lines imported' field:
        self.varEntryLinesImportedCounter.set(0)
        
# 1. entry must be an integer
        try:
            lineStartForImport = int(self.varEntryLineStart.get().strip())
        except:
# if blank, just return
            if self.varEntryLineStart.get().strip() == '':
                self.varEntryLinesToImport.set('')
                self.entryLinesToImport.configure(disabledbackground='red')
                return
            errorLineStart = (
                'Beginning line number must be a positive integer.\n\n' +
                'Enter a valid integer value and try again.\n\n'
                )
            self.varEntryLinesToImport.set('')
            self.entryLinesToImport.configure(disabledbackground='red')
            print(
                '\n' + errorLineStart
                )
            try:
                showinfo(
                    'Error: beginning line number',
                    '\n' + errorLineStart,
                    parent=self.toplevelReadCsvFile
                    )
            except:
                showinfo(
                    'Error: beginning line number',
                    '\n' + errorLineStart
                    )            
            
            return
            
       
# 2. input must not be a negative number
        if lineStartForImport < 0:
            errorNegativeValue = (
                'Invalid value for beginning line number.\n\n' +
                'Enter valid value and try again.\n\n'
                )
            self.varEntryLinesToImport.set('')
            self.entryLinesToImport.configure(disabledbackground='red')
            print(
                '\n' + errorNegativeValue
                )
            try:
                showinfo(   
                    'Error: negative value',
                    '\n' + errorNegativeValue,
                    parent=self.toplevelReadCsvFile
                    )
            except:
                showinfo(   
                    'Error: negative value',
                    '\n' + errorNegativeValue
                    )

            return
            
            
# 3. beginning line cannot be less than the number of header lines skipped
        if (
            lineStartForImport <= self.rowsSkipped
            ):
            errorLineTooSmall = (
                'Beginning line number for import cannot be less than\n' + 
                ' or equal to number of header lines skipped.\n\n' +
                'Enter a valid starting value and try again.\n\n'
                )
            self.varEntryLinesToImport.set('')
            self.entryLinesToImport.configure(disabledbackground='red')
            print(
                '\n' + errorLineTooSmall
                )
            try:
                showinfo(
                    'Error: invalid starting value',
                    '\n' + errorLineTooSmall,
                    parent=self.toplevelReadCsvFile
                    )
            except:
                showinfo(
                    'Error: invalid starting value',
                    '\n' + errorLineTooSmall
                    )

            return
            
            
# 4. start line must not be greater than ending line
        if (
#            lineStartForImport > self.rowsTotal
            lineStartForImport > eval(self.varEntryLineEnd.get())
            ):
            errorLineTooBig = (
                'Starting line number for import cannot be larger than\n' +
                ' the ending line shown.\n\n' +
                'Enter a valid starting value and try again.\n\n'
                )
            self.varEntryLinesToImport.set('')
            self.entryLinesToImport.configure(disabledbackground='red')
            print(
                '\n' + errorLineTooBig
                )
            try:
                showinfo(
                    'Error: invalid starting value',
                    '\n' + errorLineTooBig,
                    parent=self.toplevelReadCsvFile
                    )
            except:
                showinfo(
                    'Error: invalid starting value',
                    '\n' + errorLineTooBig
                    )

            return
      
            
# update number of lines to import
        numberOfLinesToImport = eval(self.varEntryLineEnd.get()) - eval(self.varEntryLineStart.get()) + 1
        self.varEntryLinesToImport.set(numberOfLinesToImport)
        self.entryLinesToImport.configure(disabledbackground='white')
            
        return

        
        
    def handlerUpdateEndingNumberOfLinesToImport(self,event):
        '''
        Purpose:
            updates the 'number of lines to import' field when the
            ending number of lines to read is changed.
            
        Checks for the following input errors:
        1. entry must be an integer
        2. input must not be a negative number
        3. end line cannot be less than the number of header lines skipped
        4. end line must not be greater than total number of lines
        5. end line must not be be less than beginning line
        '''
        if DEBUG_PRINT_METHOD:
            print(
                '\n** In ' + MODULE + '/' + 
                'handlerUpdateBeginningNumberOfLinesToImport'
                )
        self.MySQL_Output(
            1,
            '** In ' + MODULE + '/' + 
            'handlerUpdateBeginningNumberOfLinesToImport'
            )
            
# reset 'number of lines imported' field:
        self.varEntryLinesImportedCounter.set(0)
            
# 1. entry must be an integer
        try:
            lineEndForImport = int(self.varEntryLineEnd.get().strip())
        except:
            if self.varEntryLineEnd.get().strip() == '':
                self.varEntryLinesToImport.set('')
                self.entryLinesToImport.configure(disabledbackground='red')
                return
            errorLineEnd = (
                'Ending line number is an invalid value.\n\n' +
                'Enter a valid integer value and try again.\n\n'
                )
            self.varEntryLinesToImport.set('')
            self.entryLinesToImport.configure(disabledbackground='red')
            print(
                '\n' + errorLineEnd
                )
            try:
                showinfo(
                    'Error: ending line number',
                    '\n' + errorLineEnd,
                    parent=self.toplevelReadCsvFile
                    )
            except:
                showinfo(
                    'Error: ending line number',
                    '\n' + errorLineEnd
                    )

            return        

            
# 2. input must not be a negative number
        if lineEndForImport < 0:
            errorNegativeValue = (
                'Invalid value for ending line number.\n\n' +
                'Enter valid value and try again.\n\n'
                )
            self.varEntryLinesToImport.set('')
            self.entryLinesToImport.configure(disabledbackground='red')
            print(
                '\n' + errorNegativeValue
                )
            try:
                showinfo(   
                    'Error: negative value',
                    '\n' + errorNegativeValue,
                    parent=self.toplevelReadCsvFile
                    )
            except:
                showinfo(   
                    'Error: negative value',
                    '\n' + errorNegativeValue
                    )                   
                        
            return
            
            
# 3. end line cannot be less than the number of header lines skipped
        if (
            lineEndForImport <= self.rowsSkipped
            ):
            errorLineTooSmall = (
                'Ending line number for import cannot be less than\n' + 
                ' or equal to number of header lines skipped.\n\n' +
                'Enter a valid starting value and try again.\n\n'
                )
            self.varEntryLinesToImport.set('')
            self.entryLinesToImport.configure(disabledbackground='red')
            print(
                '\n' + errorLineTooSmall
                )
            try:
                showinfo(
                    'Error: invalid starting value',
                    '\n' + errorLineTooSmall,
                    parent=self.toplevelReadCsvFile
                    )
            except:
                showinfo(
                    'Error: invalid starting value',
                    '\n' + errorLineTooSmall
                    )
            
            return 
            
            
# 4. end line must not be greater than total number of lines
        if (
            lineEndForImport > self.rowsTotal
            ):
            errorLineTooBig = (
                'Line numbers for import cannot be more than\n' +
                ' the number of lines in the data file.\n\n' +
                'Enter a valid starting value and try again.\n\n'
                )
            print(
                '\n' + errorLineTooBig
                )
            self.varEntryLinesToImport.set('')
            self.entryLinesToImport.configure(disabledbackground='red')
            try:
                showinfo(
                    'Error: invalid starting value',
                    '\n' + errorLineTooBig,
                    parent=self.toplevelReadCsvFile
                    )
            except:
                showinfo(
                    'Error: invalid starting value',
                    '\n' + errorLineTooBig
                    )
            
            return
            
            
# 5. end line must not be be less than beginning line
        if (
            lineEndForImport < eval(self.varEntryLineStart.get())
            ):
            errorLineEndTooSmall = (
                'Ending line number for import cannot be less than\n' +
                ' the beginning line number.\n\n' +
                'Enter a valid ending value and try again.\n\n'
                )
            print(
                '\n' + errorLineEndTooSmall
                )
            self.varEntryLinesToImport.set('')
            self.entryLinesToImport.configure(disabledbackground='red')
            try:
                showinfo(
                    'Error: invalid starting value',
                    '\n' + errorLineEndTooSmall,
                    parent=self.toplevelReadCsvFile
                    )
            except:
                showinfo(
                    'Error: invalid starting value',
                    '\n' + errorLineEndTooSmall
                    )
            
            return

           
# update number of lines to import
        numberOfLinesToImport = eval(self.varEntryLineEnd.get()) - eval(self.varEntryLineStart.get()) + 1
        self.varEntryLinesToImport.set(numberOfLinesToImport)
        self.entryLinesToImport.configure(disabledbackground='white')
            
        return
        
        
    def handlerCancelReadCsvFileImport(self):
        '''
        Purpose:
            kill the toplevel window associated with reading a CSV file
        '''
        if DEBUG_PRINT_METHOD:
            print(
                '\n** In ' + MODULE + '/' + 
                'handlerCancelReadCsvFileImport'
                )
        self.MySQL_Output(
            1,
            '** In ' + MODULE + '/' + 'handlerCancelReadCsvFileImport'
            )  
# kill the toplevel
        self.toplevelReadCsvFile.destroy()
        
        return
    
                
    def handlerImportToDatabase(self):
        '''
        Purpose:
            Import CSV data to user-selected 'database.table'
            
        Called by:
            handlerReadCsvFile
            
        Calls:
        
        Variables:
            self.elementsPerRow_MyOpenCsvFile
            self.myTableStructure
        '''
        if DEBUG_PRINT_METHOD:
            print(
                '\n** In ' + MODULE + '/' + 
                'handlerImportToDatabase'
                )
        self.MySQL_Output(
            1,
            '** In ' + MODULE + '/' + 'handlerImportToDatabase'
            )          

# ... if elements per row and table columns don't match, print error and return without import
        errString = ''
#        print '\nself.elementsPerRow_MyOpenCsvFile = %s' % self.elementsPerRow_MyOpenCsvFile
#        print '\ntype(self.elementsPerRow_MyOpenCsvFile) = %s' % type(self.elementsPerRow_MyOpenCsvFile)
#        print 'len(self.myTableStructure) = %s' % len(self.myTableStructure)
        if DEBUG_CSV:
            print('\nstr(self.elementsPerRow_MyOpenCsvFile) = %s' % str(self.elementsPerRow_MyOpenCsvFile))
            print('\nstr(len(self.myTableStructure) - 1) = %s' % str(len(self.myTableStructure) - 1))
        if str(self.elementsPerRow_MyOpenCsvFile) != str(len(self.myTableStructure) - 1): # account for 'auto_index' column!
            errString += (
                'Number of elements per row in file do not match number of table columns:' + '\n' +
                '  elements per row = ' + str(self.elementsPerRow_MyOpenCsvFile) + '\n' +
                '  number of table columns = ' + str(len(self.myTableStructure)) + '\n\n' +
                'Operation canceled.\n\n'
                )
            print errString
            self.MySQL_Output(
                1,
                errString
                )
            try:
                showinfo(
                    'Error: cannot import data',
                    '\n' + errString + '\n',
                    self.toplevelReadCsvFile
                    )
            except:
                showinfo(
                    'Error: cannot import data',
                    '\n' + errString + '\n'
                    )
            return
            
# prepare button for stopping import
#        self.varTextForReadCsvFileImport.set('Stop importing to table')

# if no errors, import data to table, one line at a time            
        self.send_to_MySQL(
            self._userMySQL_Save,
            self._passwdMySQL_Save,
            self._hostMySQL_Save,
            self._portMySQL_Save
            )
            
        return
        

# send data to database
    def send_to_MySQL(self, stringUser, stringPW, stringHost, numPort):
        '''
        Purpose:
        Connects to 'database.table'; sends data to the table.
        Refreshes table display.
        '''
        if DEBUG_PRINT_METHOD:
            print(
                '\n** In ' + MODULE + '/' + 
                'send_to_MySQL'
                )
        self.MySQL_Output(
            1,
            '** In ' + MODULE + '/' + 'send_to_MySQL'
            )
            
        myTable = self.myTable
        myDatabase = self.myDatabase
        
# reset number of lines imported to zero
        self.varEntryLinesImportedCounter.set(0)
        
# check if important fields are blank
# ... start and end lines
        if self.varEntryLineStart.get() == '' or self.varEntryLineEnd.get() == '':
            stringBlankFields = (
                'The following fields are blank and need values:\n'
                )
            if self.varEntryLineStart.get() == '':
                stringBlankFields += '\n - "Begin importing at line:"'
            if self.varEntryLineEnd.get() == '':
                stringBlankFields += '\n - "and end at line:"'
            stringBlankFields += '\n\nInsert appropriate values and try again.'
            print('\n' + stringBlankFields)
            self.MySQL_Output(
                0,
                stringBlankFields
                )
            showerror(
                'Error: blank field(s)',
                stringBlankFields,
                parent=self.toplevelReadCsvFile
                )
            return
# ... number of lines to import
        if self.varEntryLinesToImport.get() == '':
            stringBlankLinesToImport = (
                'There\'s an error in either the beginning or ending\n' +
                '  line number.\n\n' +
                'Enter valid numbers for both fields and try again.'
                )
            print('\n' + stringBlankLinesToImport)
            self.MySQL_Output(
                0,
                stringBlankLinesToImport
                )
            showerror(
                'Error: invalid line number',
                stringBlankLinesToImport,
                parent=self.toplevelReadCsvFile
                )
            return
            
# get table structure
        stringTableStructure = (
            "SHOW COLUMNS FROM " + myDatabase + "." + myTable
            )
        try:
            self.cursorHandleMySQL.execute(
                stringTableStructure
                )
        except:
            stringErrorShowColumns = (
                'Cannot show columns from\n\n' +
                '  table: %s\n' +
                '  database: %s\n\n' +
                'Possible reasons:\n' +
                '  - database server may be down\n' +
                '  - table or database no longer exists\n' +
                '  - an unknown event\n\n' +
                'This process cannot continue.'
                )
            print('\n' + stringErrorShowColumns)
            self.MySQL_Output(
                0,
                stringErrorShowColumns
                )
            try:
                showerror(
                    'Error: cannot show table columns',
                    stringErrorShowColumns,
                    parent=self.toplevelReadCsvFile
                    )
            except:
                showerror(
                    'Error: cannot show table columns',
                    stringErrorShowColumns
                    )
            return
            
        myTableStructure = self.cursorHandleMySQL.fetchall()
        
# get field names, field types from table
        fieldNames = []
        fieldTypes = []
        for fields in myTableStructure:
            fieldNames.append(fields[0])
            fieldTypes.append(fields[1]) # to get first two characters, add [0:2] to end
        if DEBUG_CSV:
            print('\nField names from table %s' % myTable)
            print('-'*40)
            for (number,field) in enumerate(fieldNames):
                print('%s. %s of type %s' % (str(number + 1), field, fieldTypes[number]))

# determine formatted print string for command
        if DEBUG_CSV:
            print('\nstringUser = %s' % stringUser)
            print('stringHost = %s' % stringHost)
            print('\ndatabase = %s' % myDatabase)
            print('\ntable = %s' % myTable)
            print('\nnumber of fields (including auto_index) = %s' % len(fieldNames))
            print('\nmyTableStructure = \n') 
            print(myTableStructure)
            print(' ')

# rewind file, for we will read it again 
#   (actually, just move pointer to beginning of file)
        try:
            self.myOpenCsvFile.seek(0,0)
        except:
            stringOpenCsvError = (
                'For some reason, file\n' +
                '%s\n' +
                'cannot be rewound to be read.\n\n' +
                'This process cannot continue.'
                )
            print('\n' + stringOpenCsvError)
            self.MySQL_Output(
                0,
                stringOpenCsvError
                )
            try:
                showerror(
                    'Error: cannot rewind csv file',
                    stringOpenCsvError,
                    parent=self.toplevelReadCsvFile
                    )
            except:
                showerror(
                    'Error: cannot rewind csv file',
                    stringOpenCsvError
                    )
            return
            
# beginning line for valid data, obtained from 'IMPORT CSV DATA' window
        lineStart = int(self.varEntryLineStart.get().strip())
# ending line for valid data, obtained from 'IMPORT CSV DATA' window
        lineEnd = int(self.varEntryLineEnd.get().strip())
# total rows to update
        numberOfRowsToUpdate = (lineEnd - lineStart) + 1
# total rows in file
        numberOfValidDataRowsInTable = self.varEntryLinesWithValidData.get().strip()            

# insert data:
# for each line read from file, we insert a blank row in the database table,
#  then fill in each field individually, rather than with a bulk update. This way,
#  we can isolate the row and field if there is an error in the update. This
#  approach may be slower, but it is much more user friendly in case of an error.
        i=0
        icountData = 0
        rowsFullyUpdated = 0
        rowsPartiallyUpdated = 0
        rowsNotUpdated = 0
#        self.buttonStopCsvFileImport.configure(state=NORMAL)

        for line in csv.reader(self.myOpenCsvFile):
            i+=1
            if i > lineEnd: break
# make sure we only go from lineStart to lineEnd, in case we want to extract
#  only a small portion of the CSV data.
            if i >= lineStart and i <= lineEnd:
# line count of lines inserted into table
                icountData += 1
# get number of fields from CSV data; compare against number of fields in database, 
#  but have to subtract 1 from database fields since we add auto_index                
                if icountData == 1:
                    numFieldsInCsvFile = len(line)
                    
                if DEBUG_CSV:
                    print('\n\nWorking on line # %d' % i )

# insert a blank line in database table
                command = (
                    'INSERT INTO ' + myDatabase + '.' + myTable + ' VALUES()'
                    )
                if DEBUG_CSV:
                    print('\n  Insert blank line with command:\n%s\n' % command)
                try:
                    self.cursorHandleMySQL.execute(command)
                except:
                    stringInsertError = (
                        'Not able to insert blank line into\n\n' +
                        ' database: %s\n' +
                        ' table: %s\n\n' +
                        'Possible reasons:\n' +
                        ' - user does not have proper permissions\n' +
                        ' - database server is down\n' +
                        ' - an unknown event\n\n' +
                        'This process cannot continue.'
                        ) % (
                        myDatabase,
                        myTable
                        )
                    print('\n' + stringInsertError)
                    self.MySQL_Output(
                        0,
                        stringInsertError
                        )
                    try:
                        showerror(
                            'Error: not able to insert blank line',
                            stringInsertError,
                            self.toplevelReadCsvFile
                            )
                    except:
                        showerror(
                            'Error: not able to insert blank line',
                            stringInsertError
                            )
                    return

# get auto_index value, which should correspond to the auto_index value of the
#  blank line just inserted
                command = (
                    'SELECT MAX(auto_index) from ' + myDatabase + '.' +myTable
                    )
                try:
                    self.cursorHandleMySQL.execute(command)
                    maxAutoIndex_Temp = str(self.cursorHandleMySQL.fetchall()[0]) # RHS is a tuple, like '(12L,)'
                    if DEBUG_CSV:
                        print('\nmaxAutoIndex_Temp = %s' % maxAutoIndex_Temp)
                        print('\n  type() = %s' % type(maxAutoIndex_Temp))
                    maxAutoIndex = maxAutoIndex_Temp[1:-3] # RHS appears as '12L'
                    if DEBUG_CSV:
                        print('\nmaxAutoIndex = %s' % maxAutoIndex)
                except:
                    stringInsertError = (
                        'Not able to determine max value for auto_index from\n\n' +
                        ' database: %s\n' +
                        ' table: %s\n\n' +
                        'Possible reasons:\n' +
                        ' - user does not have proper permissions\n' +
                        ' - database server is down\n' +
                        ' - an unknown event\n\n' +
                        'This process cannot continue.'
                        ) % (
                        myDatabase,
                        myTable
                        )
                    print('\n' + stringInsertError)
                    self.MySQL_Output(
                        0,
                        stringInsertError
                        )
                    try:
                        showerror(
                            'Error: unable to determine maxAutoIndex',
                            stringInsertError,
                            self.toplevelReadCsvFile
                            )
                    except:
                        showerror(
                            'Error: unable to determine maxAutoIndex',
                            stringInsertError
                            )
                    return
                    
# setup part of UPDATE command that will not change
                command0 = (
                    'UPDATE ' + myDatabase + '.' + myTable + ' SET '
                    )
                    
# keep track if all fields are updated, or only some fields, in any one row
                ifieldsUpdated = 0
                ifieldsNotUpdated = 0
                    
# now insert csv data into database table, one field at at a time, corresponding to
#  the value for maxAutoIndex
                for (fieldNumber,field) in enumerate(fieldNames):
# no update needed for auto_index field
                    if field == 'auto_index':
                        continue

# prepare rest of command
                    if DEBUG_CSV:
                        print('\n  %s. field: %s, field type: %s' 
                            % (
                            fieldNumber + 1,
                            field,
                            fieldTypes[fieldNumber]
                            ) 
                            )

# if field is blank, insert 'default' whether string, number, or key. Otherwise,
#   the MySQL command will not execute and an error will be printed
                    if line[fieldNumber] == '':
                        command1 = field + ' = default'

                    else:
# all lines read by csv.reader() are typed as strings; we must eval(line) to see if
#   it's a number or a string; if a string, must put quotes around it; if a number,
#   leave it alone and just insert
# also, note that ',NULL' is added in the 'else' logic to account for the
#   added 'auto-index' field
                        try:
                            temp = eval(line[fieldNumber])
                            fieldIsNumber = True
                        except:
                            fieldIsNumber = False
                            
                        if fieldIsNumber:
                            command1 = field + '=' + str(line[fieldNumber])

                        else:
# replace any double quotes with single quotes to avoid confusion in command
                            tempValue = line[fieldNumber].replace('"',"'")
                            command1 = field + '="' + str(tempValue) + '"'

                                
# command for auto_index
                    command2 = ' where auto_index = ' + maxAutoIndex
                    
# assemble command
                    command = command0 + command1 + command2
                    
                    if DEBUG_CSV:
                        print(' \nupdate command: %s' % command)      
            
                    try:
                        self.cursorHandleMySQL.execute(command)
                        ifieldsUpdated += 1
                    except:
                        ifieldsNotUpdated += 1
                        insertErrorString = (
                            'Not able to insert data into\n\n' +
                            ' database: %s\n' +
                            ' table: %s\n' +
                            ' table row: %s\n' +
                            ' field column #: %s\n' +
                            ' field name: %s\n\n' +
                            'Check table structure and datatype of input\n' +
                            'for errors.\n\n' +
                            'Click YES to continue trying to insert data.\n' +
                            'Click NO to cancel the current operation.'
                            ) % (
                            myDatabase,
                            myTable,
                            i,
                            fieldNumber + 1,
                            field,
                            )
                        print('\n' + insertErrorString)
                        self.MySQL_Output(
                            0,
                            insertErrorString
                            )
                        ans = askyesno(
                            'Error: not able to insert data',
                            insertErrorString,
                            parent=self.toplevelReadCsvFile
                            )
                        if not ans:
# give status report to this point
                            if ifieldsNotUpdated == 1:
                                rowsNotUpdated += 1
                            else:
                                rowsPartiallyUpdated += 1
                            stringStatusReport = (
                                'Status report thus far:\n\n' +
                                ' - Number of rows in file: %s\n' +
                                ' - Number of rows to update: %s\n' +
                                ' - Number of rows fully updated: %s\n' +
                                ' - Number of rows partially updated: %s\n' +
                                ' - Number of rows not updated: %s\n\n' +
                                'Importing data to table has been canceled before\n' +
                                'the requested number of rows has been processed.'
                                ) % (
                                numberOfValidDataRowsInTable,
                                numberOfRowsToUpdate,
                                rowsFullyUpdated,
                                rowsPartiallyUpdated,
                                rowsNotUpdated,
                                )
                            print('\n' + stringStatusReport)
                            self.MySQL_Output(
                                0,
                                stringStatusReport
                                )
                            try:    
                                showinfo(
                                    'Info: import canceled',
                                    stringStatusReport,
                                    parent= self.toplevelReadCsvFile
                                    )
                            except:
                                showinfo(
                                    'Info: import canceled',
                                    stringStatusReport
                                    )
# reset import to table button
                            self.varStartStopCsvFileImport.set(0)
#                            self.varTextForReadCsvFileImport.set('Import to table')
                            return
            
                            
                if ifieldsUpdated == numFieldsInCsvFile:
                    rowsFullyUpdated += 1
                elif ifieldsUpdated < numFieldsInCsvFile and ifieldsUpdated <> 0:
                    rowsPartiallyUpdated += 1
                else:
                    rowsNotUpdated += 1
# display lines imported thus far
                self.varEntryLinesImportedCounter.set(
                    eval(self.varEntryLinesImportedCounter.get().strip()) + 1
                    )
# update the 'number of lines imported' field:
                self.toplevelFindCsvFile.update_idletasks()

        
        stringStatusReport = (
            'Final status report on CSV import:\n\n' +
            ' - Number of rows in file: %s\n' +
            ' - Number of rows to update: %s\n' +
            ' - Number of rows fully updated: %s\n' +
            ' - Number of rows partially updated: %s\n' +
            ' - Number of rows not updated: %s\n\n' +
            'Importing data to table has been canceled before\n' +
            'the requested number of rows has been processed.'
            ) % (
            numberOfValidDataRowsInTable,
            numberOfRowsToUpdate,
            rowsFullyUpdated,
            rowsPartiallyUpdated,
            rowsNotUpdated,
            )
        print('\n' + stringStatusReport)
        self.MySQL_Output(
            0,
            stringStatusReport
            )
        try:    
            showinfo(
            'Info: import canceled',
            stringStatusReport,
            parent= self.toplevelReadCsvFile
            )
        except:
            showinfo(
            'Info: import canceled',
            stringStatusReport
            )
            
# reset 'import to table' button
        self.varStartStopCsvFileImport.set(0)
#        self.varTextForReadCsvFileImport.set('Import to table')
        
        return
        

    def askOpenFilename(self):
        '''
        Purpose:
          open a file and print first 5 lines
        
        Author:
          dwbarne
        
        Date:
          Mon, 04-06-2009
        
        Called by:
          main
          
        Attributes:
            self.myOpenCsvFile             CSV file, opened
            self.rowCount_MyOpenCsvFile    number of lines in CSV file
        '''
        if DEBUG_PRINT_METHOD:
            print(
                '\n** In ' + MODULE + '/' + 
                'askOpenFilename'
                )
        self.MySQL_Output(
            1,
            '** In ' + MODULE + '/' + 'askOpenFilename'
            )
            
        import os
        currentDirectory = os.getcwd()

# define dictionary of options
        options = {
            'defaultextension' : '.csv',
            'filetypes' : [('csv','.csv'),('All files','*')],
            'initialdir' : currentDirectory,
            'parent' : self.toplevelFindCsvFile,
            'title' : 'Read file'
            }

# get full pathname
        self.filenameCsv = askopenfilename(**options)             
        dirnameCsv, filenameShortCsv = os.path.split(self.filenameCsv)
        if self.filenameCsv == '': return
        try:
            self.myOpenCsvFile = open(self.filenameCsv,'r')
        except:
            stringErrorOpeningCsvFile = (
                'For some unknown reason, the file\n' +
                'cannot be opened.\n\n' +
                'This process cannot continue.'
                )
            print('\n' + stringErrorOpeningCsvFile)
            self.MySQL_Output(
                0,
                stringErrorOpeningCsvFile
                )
            try:
                showerror(
                    'Error: cannot open file',
                    stringErrorOpeningCsvFile,
                    parent=self.toplevelFindCsvFile
                    )
            except:
                showerror(
                    'Error: cannot open file',
                    stringErrorOpeningCsvFile
                    )
            return
        print('\nFile opened (full pathname): %s\n' % self.filenameCsv)
        self.MySQL_Output(
            1,
            'CSV file opened (full pathname):\n' +  self.filenameCsv
            )
# determine line count
        self.rowCount_MyOpenCsvFile = len(self.myOpenCsvFile.readlines())

# display filename
        self.entryPathName.clear()
        self.entryPathName.setvalue(dirnameCsv)
        self.entryFileName.clear()
        self.entryFileName.setentry(filenameShortCsv)
# display number of lines
        self.entryTotalLines.configure(state=NORMAL)
        self.entryTotalLines.delete(0,END)
        self.entryTotalLines.insert(0,self.rowCount_MyOpenCsvFile)
        self.entryTotalLines.configure(state=DISABLED)
# print total lines
        print (
            "\nThere are %i lines in file %s \n" % (self.rowCount_MyOpenCsvFile,filenameShortCsv)
            )
        self.MySQL_Output(
            1,
            'There are %i lines in file %s ' % (self.rowCount_MyOpenCsvFile,filenameShortCsv)
            )
# print first 5 lines of the file
        rowcountMax = 5
        if self.rowCount_MyOpenCsvFile < 5:
            firstlines = self.rowCount_MyOpenCsvFile
        else:
            firstlines = rowcountMax
        print(
            'First %i lines of file %s:' % (firstlines,filenameShortCsv)
            )
        self.MySQL_Output(
            1,
            'First %i lines of file %s:' % (firstlines, filenameShortCsv))
            
# rewind file
        try:
            self.myOpenCsvFile.seek(0,0)
        except:
            stringOpenCsvError = (
                'For some reason, file\n' +
                '%s\n' +
                'cannot be rewound to be read.\n\n' +
                'This process cannot continue.'
                )
            print('\n' + stringOpenCsvError)
            self.MySQL_Output(
                0,
                stringOpenCsvError
                )
            try:
                showerror(
                    'Error: cannot rewind csv file',
                    stringOpenCsvError,
                    parent=self.toplevelReadCsvFile
                    )
            except:
                showerror(
                    'Error: cannot rewind csv file',
                    stringOpenCsvError,
                    )
            return
# enable 'Read Datafile...' button
        self.buttonReadCsvFile.configure(state='normal')
            
        return
        
        
# ===== main =====
if __name__ == '__main__':
    root=Tk()
# connect to database 
    stringConnect = ''
    stringUser = 'd'
    stringHost = 'localhost'
    numPort=3306
    stringConnect = (
        'User: ' + stringUser + '\n' +
        'Host: ' + stringHost + '\n' +
#            'Passwd: ' + stringPW + '\n' +
        'Port: ' + str(numPort)
        )
    print (
        'Connecting to database...' + '\n' + stringConnect
        )

    myDbConnection = ''
# see if already connected
    print '\nConnection check:'
    print '    myDbConnection =',myDbConnection
    
    if not myDbConnection:
# try to connect; if cannot, print error, show window with error, and return    
        try:
            myDbConnection = MySQLdb.connect(
                user=stringUser,
                passwd=stringPW,
                host=stringHost,
                port=numPort
                )
# cursor
            cursorHandleMySQL = myDbConnection.cursor()
        except:
            print (
                '  Could not connect to database\n' +
                '  Invalid username, password, server or port.\n' +
                '  Could also be due to a simple timeout.\n' +
                '  Check input and try again.'
                )
            showinfo(
                'ERROR',
                'Could not connect - possible invalid username,\n' +
                '  password, server, or port.\n' +
                'Could also be due to a simple timeout.\n' +
                'Check input and try again.'
                )
            sys.exit()
            
# if we get here, connection is successful
    print ('\nConnected to MySQL database\n')
# get CSV filename
    fn=askOpenFilename(root)
# read it
    final_output = read_csv_file(fn)
# print
    print ('\nfinal_output:\n%s' % final_output)
    print ('\nfinal_output[0]:\n%s' % final_output[0])
    print('\nfinal_output[1]:\n%s' % final_output[1])
    print('\nfinal_output[1][4]:\n%s' % final_output[1][4])
# send to database
    answer = askyesno(
        'Send to database?',
        'Do you wish to send data to database?'
        )
    if answer:
        send_to_MySQL('root', 'd', 'localhost', 3306, final_output)


