#!/usr/bin/env python3
import sys,os
import subprocess as sp
import tkinter as tk
from PIL import Image, ImageTk
import time

FolderPath = os.path.dirname(os.path.abspath('FractalGenerator.py')) #get directory name

window = tk.Tk() #start main instance

columnNames = ['Cube','Tree A','Tree B'] #set column names for organization
columns=list(range(len(columnNames))) #make a column list

rowNames=['Title','X Rotation','Y Rotation','Z Rotation','Scale','Extra1','Extra2','Choice','Iterations','Button'] #row names
rows = list(range(len(rowNames))) #make a row list

window.columnconfigure(columns,minsize=400) #configure grid parameters
window.rowconfigure(rows,minsize=60)

#### GUI Elements ######################################################

#NOTE: I haven't commented any of this because there isn't much to explain, it's just setting up the graphical part.
    #  I tried to make the variable names and order of things as straightforward as possible.

### CUBE COLUMN ###

lblCubeTitle = tk.Label(window,text='Cube Settings',font=('Helvetica',20))
lblCubeTitle.grid(row=rowNames.index('Title'), column=columnNames.index('Cube'))

sclCubeIter = tk.Scale(window,label='Number of Iterations*',from_=1,to=2,orient='horizontal',length=200,tickinterval=1,resolution=1)
sclCubeIter.grid(row=rowNames.index('Iterations'), column=columnNames.index('Cube'))

sclCubeXAngle = tk.Scale(window,label='Euler X Angle',from_=0,to=45,orient='horizontal',length=350,tickinterval=15,resolution=5)
sclCubeXAngle.grid(row=rowNames.index('X Rotation'), column=columnNames.index('Cube'))

sclCubeYAngle = tk.Scale(window,label='Euler Y Angle',from_=0,to=45,orient='horizontal',length=350,tickinterval=15,resolution=5)
sclCubeYAngle.grid(row=rowNames.index('Y Rotation'), column=columnNames.index('Cube'))

sclCubeZAngle = tk.Scale(window,label='Euler Z Angle',from_=0,to=45,orient='horizontal',length=350,tickinterval=15,resolution=5)
sclCubeZAngle.grid(row=rowNames.index('Z Rotation'), column=columnNames.index('Cube'))

sclCubeScale = tk.Scale(window,label='Scale Ratio',from_=0.1,to=1,orient='horizontal',length=250,resolution=0.05)
sclCubeScale.grid(row=rowNames.index('Scale'), column=columnNames.index('Cube'))

sclCubeVerts = tk.Scale(window,label='Vertex Ratio',from_=0.05,to=1,orient='horizontal',length=250,resolution=0.05)
sclCubeVerts.grid(row=rowNames.index('Extra1'), column=columnNames.index('Cube'))

frmAddSub = tk.Frame(bd=16)
frmAddSub.grid(row=[rowNames.index('Extra2')], column=columnNames.index('Cube'),rowspan=2)

rbtAddSub = tk.IntVar()
btnAdd = tk.Radiobutton(frmAddSub,text='Add',variable=rbtAddSub,value=1,indicatoron=0,height=5,width=20)
btnAdd.grid(row=0,column=0)
btnSub = tk.Radiobutton(frmAddSub,text='Subtract',variable=rbtAddSub,value=2,indicatoron=0,height=5,width=20)
btnSub.grid(row=0,column=1)

btnAdd.select()

btnGenCube = tk.Button(window,text='Generate Fractal',height=4)
btnGenCube.grid(row=rowNames.index('Button'), column=columnNames.index('Cube'),pady=20,sticky='N')

### TREE A COLUMN ###

lblTreeATitle = tk.Label(window,text='Tree A Settings',font=('Helvetica',20))
lblTreeATitle.grid(row=rowNames.index('Title'), column=columnNames.index('Tree A'))

sclTreeAXAngle = tk.Scale(window,label='Euler X Angle',from_=-15,to=15,orient='horizontal',length=300,tickinterval=10,resolution=1)
sclTreeAXAngle.grid(row=rowNames.index('X Rotation'), column=columnNames.index('Tree A'))

sclTreeAYAngle = tk.Scale(window,label='Euler Y Angle',from_=10,to=40,orient='horizontal',length=300,tickinterval=10,resolution=1)
sclTreeAYAngle.grid(row=rowNames.index('Y Rotation'), column=columnNames.index('Tree A'))

sclTreeAZAngle = tk.Scale(window,label='Branch Twist',from_=0,to=180,orient='horizontal',length=350,tickinterval=30,resolution=15)
sclTreeAZAngle.grid(row=rowNames.index('Z Rotation'), column=columnNames.index('Tree A'))

sclTreeAScale = tk.Scale(window,label='Scale Ratio',from_=0.1,to=1,orient='horizontal',length=250,resolution=0.05)
sclTreeAScale.grid(row=rowNames.index('Scale'), column=columnNames.index('Tree A'))

sclTreeAHeight = tk.Scale(window,label='Height',from_=0.2,to=5,orient='horizontal',length=350,resolution=0.2,tickinterval=1)
sclTreeAHeight.grid(row=rowNames.index('Extra1'), column=columnNames.index('Tree A'))

sclTreeAWidth = tk.Scale(window,label='Width',from_=0.2,to=5,orient='horizontal',length=350,resolution=0.2,tickinterval=1)
sclTreeAWidth.grid(row=rowNames.index('Extra2'), column=columnNames.index('Tree A'))

frmTreeSelect = tk.Frame(bd=16)
frmTreeSelect.grid(row=[rowNames.index('Choice')], column=columnNames.index('Tree A'),columnspan=2)

rbtTreeSelect = tk.IntVar()
btnAOnly = tk.Radiobutton(frmTreeSelect,text='Use Only A',variable=rbtTreeSelect,value=1,indicatoron=0,height=5,width=20)
btnAOnly.grid(row=0,column=0)
btnCombo = tk.Radiobutton(frmTreeSelect,text='Combine A and B',variable=rbtTreeSelect,value=2,indicatoron=0,height=5,width=20)
btnCombo.grid(row=0,column=1)
btnBOnly = tk.Radiobutton(frmTreeSelect,text='Use Only B',variable=rbtTreeSelect,value=3,indicatoron=0,height=5,width=20)
btnBOnly.grid(row=0,column=2)
btnCombo.select()

sclTreeIter= tk.Scale(window,label='Number of Iterations',from_=1,to=8,orient='horizontal',length=200,tickinterval=1,resolution=1)
sclTreeIter.grid(row=rowNames.index('Iterations'), column=columnNames.index('Tree A'),columnspan=2)

btnGenTree = tk.Button(window,text='Generate Tree',height=4,width=30)
btnGenTree.grid(row=rowNames.index('Button'), column=columnNames.index('Tree A'),columnspan=2,pady=20,sticky='N')

### TREE B COLUMN ###

lblTreeBTitle = tk.Label(window,text='Tree B Settings',font=('Helvetica',20))
lblTreeBTitle.grid(row=rowNames.index('Title'), column=columnNames.index('Tree B'))

sclTreeBXAngle = tk.Scale(window,label='Euler X Angle',from_=-15,to=15,orient='horizontal',length=300,tickinterval=10,resolution=1)
sclTreeBXAngle.grid(row=rowNames.index('X Rotation'), column=columnNames.index('Tree B'))

sclTreeBYAngle = tk.Scale(window,label='Euler Y Angle',from_=10,to=40,orient='horizontal',length=300,tickinterval=10,resolution=1)
sclTreeBYAngle.grid(row=rowNames.index('Y Rotation'), column=columnNames.index('Tree B'))

sclTreeBZAngle = tk.Scale(window,label='Branch Twist',from_=0,to=180,orient='horizontal',length=350,tickinterval=30,resolution=15)
sclTreeBZAngle.grid(row=rowNames.index('Z Rotation'), column=columnNames.index('Tree B'))

sclTreeBScale = tk.Scale(window,label='Scale Ratio',from_=0.1,to=1,orient='horizontal',length=250,resolution=0.05)
sclTreeBScale.grid(row=rowNames.index('Scale'), column=columnNames.index('Tree B'))

sclTreeBHeight = tk.Scale(window,label='Height',from_=0.2,to=5,orient='horizontal',length=350,resolution=0.2,tickinterval=1)
sclTreeBHeight.grid(row=rowNames.index('Extra1'), column=columnNames.index('Tree B'))

sclTreeBWidth = tk.Scale(window,label='Width',from_=0.2,to=5,orient='horizontal',length=350,resolution=0.2,tickinterval=1)
sclTreeBWidth.grid(row=rowNames.index('Extra2'), column=columnNames.index('Tree B'))

#### Default Setting ################################

sclCubeIter.set(2)
sclCubeScale.set(0.5)
sclCubeVerts.set(0.3)

sclTreeAXAngle.set(0)
sclTreeAYAngle.set(15)
sclTreeAZAngle.set(45)
sclTreeAScale.set(0.75)
sclTreeAHeight.set(2)
sclTreeAWidth.set(1)

sclTreeBXAngle.set(10)
sclTreeBYAngle.set(25)
sclTreeBZAngle.set(90)
sclTreeBScale.set(0.75)
sclTreeBHeight.set(2)
sclTreeBWidth.set(1)

sclTreeIter.set(5)

#### GUI Functionality ##############################

def GenerateCube(window):
    for child in window.winfo_children(): #disable all elements so user knows the computer is working
        try:
            child.config(state='disable')
        except:
            pass
        child.update_idletasks()
        
    X = str(sclCubeXAngle.get()) #pack up user inputted data
    Y = str(sclCubeYAngle.get())
    Z = str(sclCubeZAngle.get())
    scale = str(sclCubeScale.get())
    vertRatio = str(sclCubeVerts.get())
    iterations = str(sclCubeIter.get())
    mode = str(rbtAddSub.get())
    
    datalist = [mode,vertRatio,scale,X,Y,Z,iterations]
    f = open('CubeData.txt','w') #write data to text file for processing by the script
    f.write(','.join(datalist))
    f.close()
    
    info = sp.run(['blender','-b','--python',FolderPath+'/DiffCube.py'],capture_output=True).stdout.decode() 
                                                    #run the relevant python script in blender, get output for render name
    popup = tk.Toplevel(window) #create a popup window to show render
    infolines = info.split('\n') #split the information from the shell into lines
    
    for renderName in (line for line in infolines if 'Saved' in line): #find the line containing the render filename
        renderLine=renderName
    
    renderName = renderLine.split("'")[1] #extract the render filename
    renderName = FolderPath + renderName[1:]
    
    image = Image.open(renderName) #open the render image file, tkinter can't open png images itself so these packages help
    photo = ImageTk.PhotoImage(image)
    
    renderImage = tk.Label(popup,image=photo) #create a label widget to contain the image
    renderImage.image = photo #you must assign the image to something, otherwise python garbage collection will get rid of it
    renderImage.pack() #pack the label to display it
    
    for child in window.winfo_children(): #re-enable the interface so the user can generate another fractal
        try:
            child.config(state='normal')
        except:
            pass
        child.update_idletasks()
        
    
def GenerateTree(window):
    for child in window.winfo_children():
        try:
            child.config(state='disable')
        except:
            pass
        child.update_idletasks()
        
    X1 = str(sclTreeAXAngle.get()) #pack up user inputted data
    Y1 = str(sclTreeAYAngle.get())
    Z1 = str(sclTreeAZAngle.get())
    scale1 = str(sclTreeAScale.get())
    h1 = str(sclTreeAHeight.get())
    w1 = str(sclTreeAWidth.get())
    
    X2 = str(sclTreeBXAngle.get())
    Y2 = str(sclTreeBYAngle.get())
    Z2 = str(sclTreeBZAngle.get())
    scale2 = str(sclTreeBScale.get())
    h2 = str(sclTreeBHeight.get())
    w2 = str(sclTreeBWidth.get())
    
    iterations = str(sclTreeIter.get())
    mode = rbtTreeSelect.get()
    
    if mode == 1: #Assign the tree lists based on what combination setting the user selected.
        lstA = [X1,Y1,Z1,scale1,h1,w1,iterations]
        lstB = lstA
    elif mode == 3:
        lstA = [X2,Y2,Z2,scale2,h2,w2,iterations]
        lstB = lstA
    else:
        lstA = [X1,Y1,Z1,scale1,h1,w1,iterations]
        lstB = [X2,Y2,Z2,scale2,h2,w2,iterations]
        
        
    f = open('TreeData.txt','w') #write data to text file for processing by the script
    f.write(','.join(lstA)+'\n')
    f.write(','.join(lstB))
    f.close()
    
    
    info = sp.run(['blender','-b','--python',FolderPath+'/ComboTree.py'],capture_output=True).stdout.decode()
                        #run the relevant python script in blender, get output for render name
    popup = tk.Toplevel(window) #create a popup window to show render
    infolines = info.split('\n') #split the information from the shell into lines
    
    for renderName in (line for line in infolines if 'Saved' in line): #find the line containing the render filename
        renderLine=renderName
    
    renderName = renderLine.split("'")[1] #extract the name of the render image
    renderName = FolderPath + renderName[1:]
    
    image = Image.open(renderName) #open the render image file, tkinter can't open png images itself so these packages help
    photo = ImageTk.PhotoImage(image)
    
    renderImage = tk.Label(popup,image=photo) #create a label widget to contain the image
    renderImage.image = photo #you must assign the image to something, otherwise python garbage collection will get rid of it
    renderImage.pack()
    
    for child in window.winfo_children(): #re-enable the interface so the user can generate another fractal
        try:
            child.config(state='normal')
        except:
            pass
        child.update_idletasks()
    

btnGenCube.config(command=lambda : GenerateCube(window)) #set Cube button to run GenerateCube when pressed

btnGenTree.config(command=lambda : GenerateTree(window)) #set Cube button to run GenerateCube when pressed

window.mainloop() #show the interface
