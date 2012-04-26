#!/usr/bin/env python
#================================================================

from Tkinter import *
import tkFont

class Flasher(Frame):
    def __init__(self, parent, master=None):
        Frame.__init__(self, master)
        self.grid()
        
        self.frameParent = parent
        
        self.stringRepeat = '.'
        self.repeat = ''
        self.timesRepeat = 10
        self.timeDelay = 500   #msecs

        self.buttonFont = tkFont.Font ( 
            family="Helvetica",
            size="12",
            )
        self.createWidgets()

    def createWidgets(self):
    
# open Toplevel frame for entering database name
        self.toplevelEntryFlash = Toplevel(
            self.frameParent,
            bg='white',
            )
        self.toplevelEntryFlash.title(
            ''
            )
            
        self.toplevelEntryFlash.transient(self.frameParent)
# place the top window
        x_Windows=self.frameParent.winfo_rootx() + 600
        y_Windows=self.frameParent.winfo_rooty() + 400
        self.toplevelEntryFlash.geometry(
            '+%d+%d' % (x_Windows, y_Windows)
            )
        '''
# add frames to toplevel            
        frame_00 = Frame(
            self.toplevelEnterDatabaseNameAdd,
            bg='tan',
            )
        frame_00.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            )
        '''
    
        self.varPanicButton = StringVar()
        self.varPanicButton.set('     Please wait')
        self.panicButton = Entry ( 
#            self,
            self.toplevelEntryFlash,
            width=20,
            textvariable=self.varPanicButton,
            background="white",
            foreground="blue",
            font=self.buttonFont, 
            justify=LEFT,
            )
        self.panicButton.grid(
            row=0,
            column=0,
            sticky=E+W+N+S,
            )
        self.flash()
        
        return
        
    def flash(self):
        if len(self.repeat) <= self.timesRepeat:
            self.varPanicButton.set('     Please wait' + self.repeat)
            self.panicButton.after(self.timeDelay, self.flash)
            self.repeat += self.stringRepeat
        else:
            self.repeat = ''
#            self.toplevelEntryFlash.destroy()
#            self.panicButton.after(self.timeDelay, self.flash)

        return

    def stop(self):
        self.toplevelEntryFlash.destroy()
        
        return

if __name__ == '__main__':
    root=Tk()
    app = Flasher(root)
#    app.master.title("Sample application")
    app.mainloop()