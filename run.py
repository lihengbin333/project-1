########################################################
# author = Hengbin Li
# User interface for neural_style.py
########################################################


import tkinter
import os
import sys

import subprocess
from tkinter import *
from tkinter.filedialog import *

try:
    from PIL import Image
except:
    import Image


INPUT_IMAGE = ''
STYLE_IMAGE = []
OUTPUT_IMAGE = ''
Iterations = 0
WIDTH = 0
STYLE_SCALE = 0.0
CW = 0.0
SW = 0.0
LR = 0.0
ftypes = [('Image Files', '*.tif *.jpg *.png')]
##########################################


def input_images():
    filename = askopenfilename(filetypes=ftypes)
    v1.set(filename)
    global INPUT_IMAGE
    INPUT_IMAGE = filename
def style_images():
    filename = askopenfilename(filetypes=ftypes)
    v2.set(filename)
    global STYLE_IMAGE
    STYLE_IMAGE.append(filename)
def output_images():
    filename = asksaveasfilename(filetypes=ftypes)
    v3.set(filename)
    global OUTPUT_IMAGE
    OUTPUT_IMAGE = filename+'.jpg'
def iteration():
    x =500
    y = 2000
    global Iterations
    Iterations =int(v4.get())
    
    if Iterations < x or Iterations>2000 :
        messagebox.showinfo('Errpr', 'Please a number between 500 to 2000')
def _width():
    global WIDTH
    WIDTH = int(v5.get())
    
def _stylescale():
    global STYLE_SCALE
    STYLE_SCALE = float(v6.get())
def contentweight():
    global CW
    CW = float(v7.get())
def styleweight():
    global SW
    SW = float(v8.get())
def learningrate():
    global LR
    LR = float(v9.get())
    
def stylize():
    cwd = os.getcwd()
    program = cwd+'/neural_style.py'
    args=['python',program,'--content',INPUT_IMAGE,'--styles',STYLE_IMAGE,'--output',OUTPUT_IMAGE]
    if Iterations != 0:
        args.append('--iterations')
        args.append(str(Iterations))
    if WIDTH != 0:
        args.append('--width')
        args.append(str(WIDTH))
    if STYLE_SCALE !=0:
        args.append('--style-scales')
        args.append(str(STYLE_SCALE))
    if CW != 0:
        args.append('--content-weight')
        args.append(str(CW))
    if SW !=0:
        args.append('--style-weight')
        args.append(str(SW))
    if LR!=0:
        args.append("--learning-rate")
        args.append(str(LR))

    
    p=subprocess.Popen(args, stderr=subprocess.STDOUT,stdout=subprocess.PIPE, shell = True)
    result = p.communicate()[0]
    results =result.split()
    for x in results:
        print(x)
    im=Image.open(OUTPUT_IMAGE).show()
##########################################


    
w = tkinter.Tk()
w.title("Neural Style")
w.geometry("900x400")
app = Frame(w)
app.grid()

label1 = Label(app, text = 'Input Image Path: ', font =8).grid()
v1 = StringVar()
v1.set('')
entry = Entry(app,text=v1,width=80).grid(row=0, column=1)
button1 = Button(app,text="Browse",command=input_images).grid(row=0, column=2)

label2 = Label(app, text = 'Style Image Path: ',font = 8).grid()
v2 = StringVar()
v2.set('')
entry2 = Entry(app, text=v2, width=80).grid(row=1, column=1)
button2 = Button(app, text='Browse',command=style_images).grid(row=1, column=2)

label3 = Label(app, text = 'Output Path: ', font =8).grid()
v3 = StringVar()
v3.set('')
entry3 = Entry(app, text =v3, width=80).grid(row=2,column=1)
button3 = Button(app,text= 'Browse',command=output_images).grid(row=2,column=2)

label4 = Label(app, text = 'Iterations(500-2000):', font=6).grid()
v4 = IntVar()
v4.set(0)
entry4 = Entry(app, text =v4, width =20).grid(row=3,column=1)
button4 = Button(app, text='Change',command=iteration).grid(row=3,column=2)

label5 = Label(app,text ='Width: ', font=10).grid()
v5=IntVar()
v5.set(0)
entry5 = Entry(app, text =v5, width =20).grid(row=4,column=1)
button5 = Button(app,text= 'Change', command =_width).grid(row=4,column=2)

label6 = Label(app,text ='Style Scale(default: 1.0): ', font=10).grid()
v6=DoubleVar()
v6.set(0)
entry6 = Entry(app, text =v6, width =20).grid(row=5,column=1)
button6 = Button(app,text= 'Change', command =_stylescale).grid(row=5,column=2)

label7 = Label(app,text ='Content Weight(default: 5): ', font=10).grid()
v7=DoubleVar()
v7.set(0)
entry7 = Entry(app, text =v7, width =20).grid(row=6,column=1)
button7 = Button(app,text= 'Change', command =contentweight).grid(row=6,column=2)

label8 = Label(app,text ='Style Weight(default: 100): ', font=10).grid()
v8=DoubleVar()
v8.set(0)
entry8 = Entry(app, text =v8, width =20).grid(row=7,column=1)
button8 = Button(app,text= 'Change', command =styleweight).grid(row=7,column=2)

label9 = Label(app,text ='Learning Rate(default: 10): ', font=10).grid()
v9=DoubleVar()
v9.set(0)
entry9 = Entry(app, text =v9, width =20).grid(row=8,column=1)
button9 = Button(app,text= 'Change', command =learningrate).grid(row=8,column=2)

button10 = Button(app,text='Stylize',width = 10,command = stylize).grid(row=9,column=1)

w.mainloop()


   
