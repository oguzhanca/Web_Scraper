from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import backend, threading
from multiprocessing import Queue
import time

queue = Queue()
def foo():
    print("Beginning of foo")
    b1.config(state=DISABLED, text="downloading..")
    # Do time consuming stuff here.
    backend.requestPage(title_text.get())
    b1.config(state=NORMAL, text="Start")
    queue.put([88,90]) #Just if I need this later.
    print("End of foo")


# Function to check state of thread1 and to update progressbar #
def progress(thread, queue):
    print("progrese girdi")
    # starts thread #
    thread.start()

    # defines indeterminate progress bar (used while thread is alive) #
    print("Here is after 'thread start()'")

    pb1 = ttk.Progressbar(window, orient='horizontal', mode='indeterminate')

    # defines determinate progress bar (used when thread is dead) #
    pb2 = ttk.Progressbar(window, orient='horizontal', mode='determinate')
    pb2['value'] = 100

    # places and starts progress bar #
    pb1.grid(row=14, pady=3, columnspan=50)

    pb1.start()

    # checks whether thread is alive #
    while thread.is_alive():
        window.update()
        pass

    # once thread is no longer active, remove pb1 and place the '100%' progress bar #
    pb1.destroy()
    pb2.grid(row=14, pady=3, columnspan=50)

    # retrieves object from queue #
    work = queue.get()
    print("Leaving 'progress' function ", work)
    return work

def getUrlFromTextBar():
    # list1.insert(END, "\nExtracting data and creating table..")
    # list1.insert(END, "\nTotal number of properties found: 243")
    # list1.insert(END, "\nTime elapsed: 9.62 sec")
    # list1.insert(END, "\nYour data is ready to save!")
    # list1.insert(END, "\nClick on 'Save as' and choose a format to import to your device")
    if title_text.get() != "":
        global url
        url = title_text.get()
        printText()
        # Create thread object, targeting function to do 'stuff' #
        thread1 = threading.Thread(target=foo, args=())
        #thread2 = threading.Thread(target=changeFrame, args=())
        print("Thread1 created, progress about to be created")
        work = progress(thread1, queue)
        print("Finished all")

    else:
        messagebox.showwarning("", "This URL is not valid!!")


def printText(): #For testing purposes!!
    list1.insert(END, url)

def donothing():
    #     filewin = Toplevel(window)
    #     filewin.geometry("150x150")
    # button = Button(filewin, text="Do nothing button")#, command=changeFrame)
    # button.pack()
    return
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
window.geometry("750x450")
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
