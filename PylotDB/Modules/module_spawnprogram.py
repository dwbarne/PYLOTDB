# module_spawnprogram.py
# run a python program from this script
# runs on windows or *nix

import os                   # to get current directory, etc.
import string               # filenames are strings
from tkFileDialog import *  # for 'askopenfilename()', etc
from Tkinter import *       # to inherit from Frame
import sys                  # for sys.exit()
    
    
class Spawn(Frame):
    def __init__(self ):
        print '\n** class Spawn from module_spawnprogram.py'
        
# ========= end of class Spawn ============= #
        
# ========== spawn =========================#
    def spawn(self, runFile, parent, currentDirectory, fileInitial):    
        """
        Purpose:
        spawn a process containing an executable and an input file;
        immediately return to calling program (unblocked call)
        """
        print '\n** In def spawn from module_spawnprogram.py'
        
#        self.frameParent=parent
        
# determine if running in Windows
        if os.name in ("nt", "dos"):
            exefile = ".exe"
            envWindows=1
            print '\n >> Environment: Windows'
        else:
            exefile = ""
            envWindows=0
            print '\n >> Environment: *nix'
            
        print '\n  currentDirectory:',currentDirectory
        print '  fileInitial:',fileInitial
        
# DETERMINE FILENAME TO RUN

# define current directory to use as initial directory in options below
#        currentDirectory = os.getcwd().split('\\').pop()

        if not fileInitial:
            fileInitial=''
       
# define dictionary of options for askopenfilename(); open only python extensions initially
        options = {}
        options = {
            'defaultextension' : '.py',
            'filetypes' : [('python','.py'),('All files','.*')],
            'initialdir' : currentDirectory,
            'initialfile' : fileInitial,
            'parent' : parent,
            'title' : 'Open a Python source file only'
            }      
        
# get filename
#        dirname, filename = os.path.split(askopenfilename(**options))
        inputFile = str(askopenfilename(**options))
        
        print '\nFile opened:',inputFile
            
# if Windows, put double-quotes around filename so that it can be executed properly by spawn
        if envWindows:
            inputFile='"' + inputFile + '"'        
        
        
# SETUP TO SPAWN A PROCESS 
    
        print '\n executable file: %s' % (runFile + exefile)
        print '\n input filename: %s' % inputFile
        
        try:
# check if the os module provides a shortcut
            return os.spawnvp(runFile, (runFile,) + (inputFile,) )
            
        except AttributeError:
            pass
# darn; it doesn't
        try:
            spawnv = os.spawnv
            
        except AttributeError:
# assume it's unix
            pid = os.fork()
            if not pid:
                os.execvp(program, (runFile,) + (inputFile,) )
            return os.wait()[0]
# must be windows
        else:
        
# got spawnv but no spawnp: go look for an executable
# ... construct a list of path names
            paths=string.split(os.environ["PATH"], os.pathsep)
# ... include current directory up front, just in case executable exists there
            paths.insert(0,'.')
# ... determine number of path names            
            length_paths=len(paths)
# ... use counter to see when at end
            icount=0
# ... search thru pathnames to find where runFile exists           
            for path in paths:
                icount+=1
                print '\n %s/%s. path = %s' % (icount,length_paths,path)
                print ' executable =',( runFile + exefile)
                file = os.path.join(path, runFile) + exefile
                print ' - checking whether executable exists in this path...'
                
                try:
# ... (file,) is a one-item tuple; the comma MUST be there!
# ... spawn process returns immediately; it does not wait for other script to finish!
                    spawnv(os.P_NOWAIT, file, (file,) + (inputFile,) )
                    return
                except os.error:
                    if icount == length_paths:
                        print '\nCannot find executable\'s pathname!'
                        print ( 
                            '     executable: ' + runFile + exefile
                            )
# print all pathnames
                        jcount=0
                        print '\nThese paths were searched: '
                        for jpath in paths:
                            jcount+=1
                            print '%s/%s. %s' % (jcount,length_paths,jpath)
                        print '\n' + '---- program terminated ----' + '\n'
                        sys.exit()
                    else:
                        print ' No - try next path in list.\n'
                        

# ========== end of spawn ===================#

# ========== main ===========================#
if __name__ == '__main__':
    root=Tk()
    app=Spawn()
    app.spawn('python',root)

# ========== end of main ======================#

    
