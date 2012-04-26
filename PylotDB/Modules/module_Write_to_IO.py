#! /usr/local/bin/python     # for *nix runs
# ===== Header =====
# Filename: module_Write_to_IO.py
# Author: dwbarne
# Creation date: Fri, 01-16-2009

# use this file to extract methods to put in other modules for
#  writing to I/O windows

# Purpose:
"""
methods for writing to pylot's i/o windows

Use the following statements to access:

prefix = '>$ '
.
.
import module_Write_to_IO as write
.
.
.
    write.MySQL_Output(
        1,
        '** this is a msg'
        )
"""

# ----- PRINT methods -----

# Host Info
def HostInfo_Commands(self,prepend,msg):
    """
    Purpose:
    print to special I/O Windows if they exist; otherwise,
    print to standard output; can prepend prefix if desired.
    
    Inputs: 
    prepend
    msg
    Window: self.textHostInfoCommandsWindows_IO
    """
    if prepend != 0 and prepend != 1:
        self.wrongPrependValue(prepend,'Commands','module_accessMySQL.py')
        return
    
    if self.textMySQLCommandsWindows_IO:
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
    
def HostInfo_Output(self,prepend,msg):
    """
    Purpose:
    print to special I/O Windows if they exist; otherwise,
    print to standard output; can prepend prefix if desired.
    
    Inputs: 
    prepend
    msg
    Window: self.textHostInfoOutputWindows_IO
    """
    if prepend != 0 and prepend != 1:
        self.wrongPrependValue(prepend,'Output','module_accessMySQL.py')
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
        print msg
        
    self.textHostInfoOutputWindows_IO.update_idletasks()
    
    
# CVS/SVN Access
def CvsSvnAccess_Commands(self,prepend,msg):
    """
    Purpose:
    print to special I/O Windows if they exist; otherwise,
    print to standard output; can prepend prefix if desired.
    
    Inputs: 
    prepend
    msg
    Window: self.textCvsSvnAccessCommandsWindows_IO
    """
    if prepend != 0 and prepend != 1:
        self.wrongPrependValue(prepend,'Commands','module_accessMySQL.py')
        return
    
    if self.textCvsSvnAccessCommandsWindows_IO:
# windows IO exist, so display there instead of stdout
        if prepend:
# use prefix         
            try:
                self.textCvsSvnAccessCommandsWindows_IO.insert(
                    END,
                    prefix + msg + '\n'
                    )
            except:
# separate since cannot combine list and tuple in one command
                self.textCvsSvnAccessCommandsWindows_IO.insert(
                    END,
                    prefix + ' '
                    )
                self.textCvsSvnAccessCommandsWindows_IO.insert(
                    END,
                    msg
                    )
                self.textCvsSvnAccessCommandsWindows_IO.insert(
                    END,
                    '\n'
                    )
                    
        else:
# do not use prefix
            try:
                self.textCvsSvnAccessCommandsWindows_IO.insert(
                    END,
                    msg + '\n'
                    )
            except:
                self.textCvsSvnAccessCommandsWindows_IO.insert(
                    END,
                    msg
                    )
                self.textCvsSvnAccessCommandsWindows_IO.insert(
                    END,
                    ' ' + '\n'
                    )
        self.textCvsSvnAccessCommandsWindows_IO.see(
            END
            )
    else:
        print msg
        
    self.textCvsSvnAccessCommandsWindows_IO.update_idletasks()
    
def CvsSvnAccess_Output(self,prepend,msg):
    """
    Purpose:
    print to special I/O Windows if they exist; otherwise,
    print to standard output; can prepend prefix if desired.
    
    Inputs: 
    prepend
    msg
    Window: self.textCvsSvnAccessOutputWindows_IO
    """
    if prepend != 0 and prepend != 1:
        self.wrongPrependValue(prepend,'Output','module_accessMySQL.py')
        return
        
    if self.textCvsSvnAccessOutputWindows_IO:
# windows IO exist, so display there instead of stdout
        if prepend:
# use prefix
            try:
                self.textCvsSvnAccessOutputWindows_IO.insert(
                    END,
                    prefix + msg + '\n'
                    )
            except:
# separate since cannot combine list and tuple in one command
                self.textCvsSvnAccessOutputWindows_IO.insert(
                    END,
                    prefix + ' '
                    )
                self.textCvsSvnAccessOutputWindows_IO.insert(
                    END,
                    '\n'
                    )
        else:
# do not use prefix
            try:
                self.textCvsSvnAccessOutputWindows_IO.insert(
                    END,
                    msg + '\n'
                    )
            except:
                self.textCvsSvnAccessOutputWindows_IO.insert(
                    END,
                    msg
                    )
                self.textCvsSvnAccessOutputWindows_IO.insert(
                    END,
                    ' ' + '\n'
                    )
        self.textCvsSvnAccessOutputWindows_IO.see(
            END
            )            
    else:
        print msg
        
    self.textCvsSvnAccessOutputWindows_IO.update_idletasks()
    

# Compile
def Compile_Commands(self,prepend,msg):
    """
    Purpose:
    print to special I/O Windows if they exist; otherwise,
    print to standard output; can prepend prefix if desired.
    
    Inputs: 
    prepend
    msg
    Window: self.textCompileCommandsWindows_IO
    """
    if prepend != 0 and prepend != 1:
        self.wrongPrependValue(prepend,'Commands','module_accessMySQL.py')
        return
    
    if self.textCompileCommandsWindows_IO:
# windows IO exist, so display there instead of stdout
        if prepend:
# use prefix         
            try:
                self.textCompileCommandsWindows_IO.insert(
                    END,
                    prefix + msg + '\n'
                    )
            except:
# separate since cannot combine list and tuple in one command
                self.textCompileCommandsWindows_IO.insert(
                    END,
                    prefix + ' '
                    )
                self.textCompileCommandsWindows_IO.insert(
                    END,
                    msg
                    )
                self.textCompileCommandsWindows_IO.insert(
                    END,
                    '\n'
                    )
                    
        else:
# do not use prefix
            try:
                self.textCompileCommandsWindows_IO.insert(
                    END,
                    msg + '\n'
                    )
            except:
                self.textCompileCommandsWindows_IO.insert(
                    END,
                    msg
                    )
                self.textCompileCommandsWindows_IO.insert(
                    END,
                    ' ' + '\n'
                    )
        self.textCompileCommandsWindows_IO.see(
            END
            )
    else:
        print msg
        
    self.textCompileCommandsWindows_IO.update_idletasks()
    
def Compile_Output(self,prepend,msg):
    """
    Purpose:
    print to special I/O Windows if they exist; otherwise,
    print to standard output; can prepend prefix if desired.
    
    Inputs: 
    prepend
    msg
    Window: self.textCompileOutputWindows_IO
    """
    if prepend != 0 and prepend != 1:
        self.wrongPrependValue(prepend,'Output','module_accessMySQL.py')
        return
        
    if self.textCompileOutputWindows_IO:
# windows IO exist, so display there instead of stdout
        if prepend:
# use prefix
            try:
                self.textCompileOutputWindows_IO.insert(
                    END,
                    prefix + msg + '\n'
                    )
            except:
# separate since cannot combine list and tuple in one command
                self.textCompileOutputWindows_IO.insert(
                    END,
                    prefix + ' '
                    )
                self.textCompileOutputWindows_IO.insert(
                    END,
                    '\n'
                    )
        else:
# do not use prefix
            try:
                self.textCompileOutputWindows_IO.insert(
                    END,
                    msg + '\n'
                    )
            except:
                self.textCompileOutputWindows_IO.insert(
                    END,
                    msg
                    )
                self.textCompileOutputWindows_IO.insert(
                    END,
                    ' ' + '\n'
                    )
        self.textCompileOutputWindows_IO.see(
            END
            )            
    else:
        print msg
        
    self.textCompileOutputWindows_IO.update_idletasks()
    

# Setup
def Setup_Commands(self,prepend,msg):
    """
    Purpose:
    print to special I/O Windows if they exist; otherwise,
    print to standard output; can prepend prefix if desired.
    
    Inputs: 
    prepend
    msg
    Window: self.textSetupCommandsWindows_IO
    """
    if prepend != 0 and prepend != 1:
        self.wrongPrependValue(prepend,'Commands','module_accessMySQL.py')
        return
    
    if self.textSetupCommandsWindows_IO:
# windows IO exist, so display there instead of stdout
        if prepend:
# use prefix         
            try:
                self.textSetupCommandsWindows_IO.insert(
                    END,
                    prefix + msg + '\n'
                    )
            except:
# separate since cannot combine list and tuple in one command
                self.textSetupCommandsWindows_IO.insert(
                    END,
                    prefix + ' '
                    )
                self.textSetupCommandsWindows_IO.insert(
                    END,
                    msg
                    )
                self.textSetupCommandsWindows_IO.insert(
                    END,
                    '\n'
                    )
                    
        else:
# do not use prefix
            try:
                self.textSetupCommandsWindows_IO.insert(
                    END,
                    msg + '\n'
                    )
            except:
                self.textSetupCommandsWindows_IO.insert(
                    END,
                    msg
                    )
                self.textSetupCommandsWindows_IO.insert(
                    END,
                    ' ' + '\n'
                    )
        self.textSetupCommandsWindows_IO.see(
            END
            )
    else:
        print msg
        
    self.textSetupCommandsWindows_IO.update_idletasks()
    
def Setup_Output(self,prepend,msg):
    """
    Purpose:
    print to special I/O Windows if they exist; otherwise,
    print to standard output; can prepend prefix if desired.
    
    Inputs: 
    prepend
    msg
    Window: self.textSetupOutputWindows_IO
    """
    if prepend != 0 and prepend != 1:
        self.wrongPrependValue(prepend,'Output','module_accessMySQL.py')
        return
        
    if self.textSetupOutputWindows_IO:
# windows IO exist, so display there instead of stdout
        if prepend:
# use prefix
            try:
                self.textSetupOutputWindows_IO.insert(
                    END,
                    prefix + msg + '\n'
                    )
            except:
# separate since cannot combine list and tuple in one command
                self.textSetupOutputWindows_IO.insert(
                    END,
                    prefix + ' '
                    )
                self.textSetupOutputWindows_IO.insert(
                    END,
                    '\n'
                    )
        else:
# do not use prefix
            try:
                self.textSetupOutputWindows_IO.insert(
                    END,
                    msg + '\n'
                    )
            except:
                self.textSetupOutputWindows_IO.insert(
                    END,
                    msg
                    )
                self.textSetupOutputWindows_IO.insert(
                    END,
                    ' ' + '\n'
                    )
        self.textSetupOutputWindows_IO.see(
            END
            )            
    else:
        print msg
        
    self.textSetupOutputWindows_IO.update_idletasks()
    

# Run
def Run_Commands(self,prepend,msg):
    """
    Purpose:
    print to special I/O Windows if they exist; otherwise,
    print to standard output; can prepend prefix if desired.
    
    Inputs: 
    prepend
    msg
    Window: self.textRunCommandsWindows_IO
    """
    if prepend != 0 and prepend != 1:
        self.wrongPrependValue(prepend,'Commands','module_accessMySQL.py')
        return
    
    if self.textRunCommandsWindows_IO:
# windows IO exist, so display there instead of stdout
        if prepend:
# use prefix         
            try:
                self.textRunCommandsWindows_IO.insert(
                    END,
                    prefix + msg + '\n'
                    )
            except:
# separate since cannot combine list and tuple in one command
                self.textRunCommandsWindows_IO.insert(
                    END,
                    prefix + ' '
                    )
                self.textRunCommandsWindows_IO.insert(
                    END,
                    msg
                    )
                self.textRunCommandsWindows_IO.insert(
                    END,
                    '\n'
                    )
                    
        else:
# do not use prefix
            try:
                self.textRunCommandsWindows_IO.insert(
                    END,
                    msg + '\n'
                    )
            except:
                self.textRunCommandsWindows_IO.insert(
                    END,
                    msg
                    )
                self.textRunCommandsWindows_IO.insert(
                    END,
                    ' ' + '\n'
                    )
        self.textRunCommandsWindows_IO.see(
            END
            )
    else:
        print msg
        
    self.textRunCommandsWindows_IO.update_idletasks()
    
def Run_Output(self,prepend,msg):
    """
    Purpose:
    print to special I/O Windows if they exist; otherwise,
    print to standard output; can prepend prefix if desired.
    
    Inputs: 
    prepend
    msg
    Window: self.textRunOutputWindows_IO
    """
    if prepend != 0 and prepend != 1:
        self.wrongPrependValue(prepend,'Output','module_accessMySQL.py')
        return
        
    if self.textRunOutputWindows_IO:
# windows IO exist, so display there instead of stdout
        if prepend:
# use prefix
            try:
                self.textRunOutputWindows_IO.insert(
                    END,
                    prefix + msg + '\n'
                    )
            except:
# separate since cannot combine list and tuple in one command
                self.textRunOutputWindows_IO.insert(
                    END,
                    prefix + ' '
                    )
                self.textRunOutputWindows_IO.insert(
                    END,
                    '\n'
                    )
        else:
# do not use prefix
            try:
                self.textRunOutputWindows_IO.insert(
                    END,
                    msg + '\n'
                    )
            except:
                self.textRunOutputWindows_IO.insert(
                    END,
                    msg
                    )
                self.textRunOutputWindows_IO.insert(
                    END,
                    ' ' + '\n'
                    )
        self.textRunOutputWindows_IO.see(
            END
            )            
    else:
        print msg
        
    self.textRunOutputWindows_IO.update_idletasks()
    

# Status
def Status_Commands(self,prepend,msg):
    """
    Purpose:
    print to special I/O Windows if they exist; otherwise,
    print to standard output; can prepend prefix if desired.
    
    Inputs: 
    prepend
    msg
    Window: self.textStatusCommandsWindows_IO
    """
    if prepend != 0 and prepend != 1:
        self.wrongPrependValue(prepend,'Commands','module_accessMySQL.py')
        return
    
    if self.textStatusCommandsWindows_IO:
# windows IO exist, so display there instead of stdout
        if prepend:
# use prefix         
            try:
                self.textStatusCommandsWindows_IO.insert(
                    END,
                    prefix + msg + '\n'
                    )
            except:
# separate since cannot combine list and tuple in one command
                self.textStatusCommandsWindows_IO.insert(
                    END,
                    prefix + ' '
                    )
                self.textStatusCommandsWindows_IO.insert(
                    END,
                    msg
                    )
                self.textStatusCommandsWindows_IO.insert(
                    END,
                    '\n'
                    )
                    
        else:
# do not use prefix
            try:
                self.textStatusCommandsWindows_IO.insert(
                    END,
                    msg + '\n'
                    )
            except:
                self.textStatusCommandsWindows_IO.insert(
                    END,
                    msg
                    )
                self.textStatusCommandsWindows_IO.insert(
                    END,
                    ' ' + '\n'
                    )
        self.textStatusCommandsWindows_IO.see(
            END
            )
    else:
        print msg
        
    self.textStatusCommandsWindows_IO.update_idletasks()
    
def Status_Output(self,prepend,msg):
    """
    Purpose:
    print to special I/O Windows if they exist; otherwise,
    print to standard output; can prepend prefix if desired.
    
    Inputs: 
    prepend
    msg
    Window: self.textStatusOutputWindows_IO
    """
    if prepend != 0 and prepend != 1:
        self.wrongPrependValue(prepend,'Output','module_accessMySQL.py')
        return
        
    if self.textStatusOutputWindows_IO:
# windows IO exist, so display there instead of stdout
        if prepend:
# use prefix
            try:
                self.textStatusOutputWindows_IO.insert(
                    END,
                    prefix + msg + '\n'
                    )
            except:
# separate since cannot combine list and tuple in one command
                self.textStatusOutputWindows_IO.insert(
                    END,
                    prefix + ' '
                    )
                self.textStatusOutputWindows_IO.insert(
                    END,
                    '\n'
                    )
        else:
# do not use prefix
            try:
                self.textStatusOutputWindows_IO.insert(
                    END,
                    msg + '\n'
                    )
            except:
                self.textStatusOutputWindows_IO.insert(
                    END,
                    msg
                    )
                self.textStatusOutputWindows_IO.insert(
                    END,
                    ' ' + '\n'
                    )
        self.textStatusOutputWindows_IO.see(
            END
            )            
    else:
        print msg
        
    self.textStatusOutputWindows_IO.update_idletasks()
    

# Post-Process
def PostProcess_Commands(self,prepend,msg):
    """
    Purpose:
    print to special I/O Windows if they exist; otherwise,
    print to standard output; can prepend prefix if desired.
    
    Inputs: 
    prepend
    msg
    Window: self.textPostProcessCommandsWindows_IO
    """
    if prepend != 0 and prepend != 1:
        self.wrongPrependValue(prepend,'Commands','module_accessMySQL.py')
        return
    
    if self.textPostProcessCommandsWindows_IO:
# windows IO exist, so display there instead of stdout
        if prepend:
# use prefix         
            try:
                self.textPostProcessCommandsWindows_IO.insert(
                    END,
                    prefix + msg + '\n'
                    )
            except:
# separate since cannot combine list and tuple in one command
                self.textPostProcessCommandsWindows_IO.insert(
                    END,
                    prefix + ' '
                    )
                self.textPostProcessCommandsWindows_IO.insert(
                    END,
                    msg
                    )
                self.textPostProcessCommandsWindows_IO.insert(
                    END,
                    '\n'
                    )
                    
        else:
# do not use prefix
            try:
                self.textPostProcessCommandsWindows_IO.insert(
                    END,
                    msg + '\n'
                    )
            except:
                self.textPostProcessCommandsWindows_IO.insert(
                    END,
                    msg
                    )
                self.textPostProcessCommandsWindows_IO.insert(
                    END,
                    ' ' + '\n'
                    )
        self.textPostProcessCommandsWindows_IO.see(
            END
            )
    else:
        print msg
        
    self.textPostProcessCommandsWindows_IO.update_idletasks()
    
def PostProcess_Output(self,prepend,msg):
    """
    Purpose:
    print to special I/O Windows if they exist; otherwise,
    print to standard output; can prepend prefix if desired.
    
    Inputs: 
    prepend
    msg
    Window: self.textPostProcessOutputWindows_IO
    """
    if prepend != 0 and prepend != 1:
        self.wrongPrependValue(prepend,'Output','module_accessMySQL.py')
        return
        
    if self.textPostProcessOutputWindows_IO:
# windows IO exist, so display there instead of stdout
        if prepend:
# use prefix
            try:
                self.textPostProcessOutputWindows_IO.insert(
                    END,
                    prefix + msg + '\n'
                    )
            except:
# separate since cannot combine list and tuple in one command
                self.textPostProcessOutputWindows_IO.insert(
                    END,
                    prefix + ' '
                    )
                self.textPostProcessOutputWindows_IO.insert(
                    END,
                    '\n'
                    )
        else:
# do not use prefix
            try:
                self.textPostProcessOutputWindows_IO.insert(
                    END,
                    msg + '\n'
                    )
            except:
                self.textPostProcessOutputWindows_IO.insert(
                    END,
                    msg
                    )
                self.textPostProcessOutputWindows_IO.insert(
                    END,
                    ' ' + '\n'
                    )
        self.textPostProcessOutputWindows_IO.see(
            END
            )            
    else:
        print msg
        
    self.textPostProcessOutputWindows_IO.update_idletasks()
    
    
# MySQL Access
def MySQL_Commands(self,prepend,msg):
    """
    Purpose:
    print to special I/O Windows if they exist; otherwise,
    print to standard output; can prepend prefix if desired.
    
    Inputs: 
    prepend
    msg
    Window: self.textMySQLCommandsWindows_IO
    """
    if prepend != 0 and prepend != 1:
        self.wrongPrependValue(prepend,'Commands','module_accessMySQL.py')
        return
    
    if self.textMySQLCommandsWindows_IO:
# windows IO exist, so display there instead of stdout
        if prepend:
# use prefix         
            try:
                self.textMySQLCommandsWindows_IO.insert(
                    END,
                    prefix + msg + '\n'
                    )
            except:
# separate since cannot combine list and tuple in one command
                self.textMySQLCommandsWindows_IO.insert(
                    END,
                    prefix + ' '
                    )
                self.textMySQLCommandsWindows_IO.insert(
                    END,
                    msg
                    )
                self.textMySQLCommandsWindows_IO.insert(
                    END,
                    '\n'
                    )
                    
        else:
# do not use prefix
            try:
                self.textMySQLCommandsWindows_IO.insert(
                    END,
                    msg + '\n'
                    )
            except:
                self.textMySQLCommandsWindows_IO.insert(
                    END,
                    msg
                    )
                self.textMySQLCommandsWindows_IO.insert(
                    END,
                    ' ' + '\n'
                    )
        self.textMySQLCommandsWindows_IO.see(
            END
            )
    else:
        print msg
        
    self.textMySQLCommandsWindows_IO.update_idletasks()
        
def MySQL_Output(self,prepend,msg):
    """
    Purpose:
    print to special I/O Windows if they exist; otherwise,
    print to standard output; can prepend prefix if desired.
    
    Inputs: 
    prepend
    msg
    Window: self.textMySQLOutputWindows_IO
    
    """
    if prepend != 0 and prepend != 1:
        self.wrongPrependValue(prepend,'Output','module_accessMySQL.py')
        return
        
    if self.textMySQLOutputWindows_IO:
# windows IO exist, so display there instead of stdout
        if prepend:
# use prefix
            try:
                self.textMySQLOutputWindows_IO.insert(
                    END,
                    prefix + msg + '\n'
                    )
            except:
# separate since cannot combine list and tuple in one command
                self.textMySQLOutputWindows_IO.insert(
                    END,
                    prefix + ' '
                    )
                self.textMySQLOutputWindows_IO.insert(
                    END,
                    '\n'
                    )
        else:
# do not use prefix
            try:
                self.textMySQLOutputWindows_IO.insert(
                    END,
                    msg + '\n'
                    )
            except:
                self.textMySQLOutputWindows_IO.insert(
                    END,
                    msg
                    )
                self.textMySQLOutputWindows_IO.insert(
                    END,
                    ' ' + '\n'
                    )
        self.textMySQLOutputWindows_IO.see(
            END
            )            
    else:
        print msg
        
    self.textMySQLOutputWindows_IO.update_idletasks()
        
        
# ----------------------------------------------------------------------------
# misc defs
def wrongPrependValue(self,value,window,module):
    """
    Purpose:
    tell user that the wrong prepend value was used, and what
    module to check
    """
    showinfo(
        'Error: incorrect prepend value',
        '\nError in determining whether to prepend a\n' +
        'print statement with a prompt. The value must be\n' +
        'either 0 or 1. The current value is\n' +
        '   prepend = ' + value + '\n\n' +
        'Check code in the following file:\n' +
        '   ' + module + ' for the ' + window + ' window.' +  '\n' 
        )
    return
