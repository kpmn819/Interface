import tkinter as tk
def doorbell(event):
    print('You rang?')

window = tk.Tk()
window.title(' User Interface Part 1')
window.geometry('640x480')
newlabel = tk.Label(text = " This is a label ")
newlabel.grid(column=0,row=0)

mybutton = tk.Button(window, text = "Doorbell", bg='red')
mybutton.grid(column=1,row=4)
mybutton.bind("<Button-1>",doorbell)

tk.OptionMenu(window,tk.IntVar(),"Age","15+","25+","40+")

window.mainloop()