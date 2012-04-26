# checkbutton frame using python & Tkinter
#   date: 070808

# This file sets a variable to true or false, depending on whether the box is checked or not, respectively

from Tkinter import *
import tkFont
import string

win=Tk()
#root.title=("Send email to me?")

class CheckButton_2(Frame):
    def __init__(self,windowEmail):
        self.windowEmail=windowEmail
        Frame.__init__(self,self.windowEmail)
        self.dataFont = tkFont.Font(
            family="Helvetica",
            size="8"
            )

#
    def createCheckButtonLabel(self,msg,rowx,coly):
        # a generic text label at first; reset later
        self.cbLabel=Label(
            self.windowEmail,
            text=msg,
            font=self.dataFont,
            )
        self.cbLabel.grid(
            columnspan=2,
            row=rowx,
            column=coly,
#            sticky=E
            )
        
    def createCheckButton(self,msg,rowx,coly):               
        self.var = IntVar()
        self.msg=msg
        Checkbutton(
            self.windowEmail, 
            text=self.msg,
            variable=self.var,
            command=self.checkButtonHandler,
#            relief=RIDGE,
            justify=CENTER,
            borderwidth=5,
            font=self.dataFont,
            padx=5,
            pady=5,
            ).grid(
#            row=self.rowx, 
#            column=self.coly,
            row=rowx,
            column=coly,
            rowspan=1,
            columnspan=2,
            sticky=S+E,
            padx=10,
            pady=10,
            )

    def checkButtonHandler(self):
        import string
        self.doNotSend=self.var.get()
        if self.doNotSend:
            print "\nINFO: email will NOT be sent to your inbox"
            show
        else:
            print "\nINFO: email will be sent to your inbox"
    
if __name__ == "__main__":
# set up the main window called 'root'
#    root=Tk()
    win.title("Checkbutton test")
#instantiate
    check=CheckButton_2()
# set up the basic frame
#    base=Frame(root)
#    base.grid()
# set up labels
#    msgLabel='Opt Out of Receiving Email'
    msgButton='If checked, do NOT send me a copy of this email'
#    check.createCheckButtonLabel(msgLabel,0,0)
    check.createCheckButton(msgButton,1,0)
    check.mainloop()
