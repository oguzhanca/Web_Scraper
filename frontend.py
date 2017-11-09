from tkinter import *
from tkinter import messagebox
import backend



def getUrlFromTextBar():
    if title_text.get() != "":
        global url
        url = title_text.get()
        printText()
        backend.requestPage(url)

    else:
        messagebox.showwarning("", "This URL is not valid!!")


def printText(): #For testing purposes!!
    list1.insert(END, "Ifin ici: " + url)

def changeFrame():
    #fr = Frame()
	print("hello_world")

def donothing():
    filewin = Toplevel(window)
    filewin.geometry("150x150")
    button = Button(filewin, text="Do nothing button")#, command=changeFrame)
    button.pack()

window=Tk()

################################################################################
menubar = Menu(window,bg='#1877a3')
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=donothing)
filemenu.add_command(label="Save", command=donothing)
filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_command(label="Close", command=donothing)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)
savemenu = Menu(menubar, tearoff=0)
savemenu.add_command(label="csv file", command=donothing)

savemenu.add_separator()

savemenu.add_command(label="xlsx file", command=donothing)
savemenu.add_command(label="database file", command=donothing)
savemenu.add_command(label="json file", command=donothing)

menubar.add_cascade(label="Save As", menu=savemenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)


window.config(menu=menubar)
################################################################################

window.wm_title("Data Scrapper")
window.geometry("700x400")
window.resizable(width=False, height=False)
window.configure(background='#44b5ea')

l1=Label(window,text="URL: ", bg='#44b5ea')
l1.grid(row=0,column=0, pady=8)

title_text=StringVar()
Url_Bar=Entry(window, width=90, bg='#1877a3', textvariable=title_text)
Url_Bar.grid(row=0,column=1, rowspan=2, columnspan=4, pady=8)

list1=Listbox(window, height=20,width=90, bg='#1877a3')
list1.grid(row=3,column=1,rowspan=10,columnspan=4, pady=2)

sb1=Scrollbar(window)
sb1.grid(row=2,column=5,rowspan=12)

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

b1=Button(window,text="Start", width=12, command=getUrlFromTextBar)
b1.grid(row=3,column=8)

window.mainloop()
