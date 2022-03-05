# Import modules
import matplotlib.pyplot as plt 
import pandas as pd
from tkinter import *
from tkinter import messagebox

#Define the lists
dims,data,Num = [],[],[]
dimsnames = ['Width','Thickness','Length','Graph Color']

#Graph, save and display the graph
def execute(xlbl,ylbl,name):
    plt.xlabel(f"{xlbl}")
    plt.ylabel(f"{ylbl}")
    plt.grid()
    plt.savefig(f"{name}.jpg")
    plt.show()

#Create dataframe
def getDataFrame(data):
    dat = {'Force': data[0], 'Stroke': data[1], 'Stress': data[2], 'Strain': data[3]}
    return pd.DataFrame(dat, columns = ['Force', 'Stroke','Stress','Strain']).astype(float)

#Extract data into lists then dataframes
def fetchlists(files_names):
    data = []
    
    for k in range(len(files_names)):
        SampleNum = k
        
        for j,x in enumerate(files_names[k]):
            df = pd.read_csv(x, skiprows = 1).drop([0])
            
            if j == 0:
                data.append([[i for i in df["Force"]], [i for i in df["Stroke"]], [float(i)/(dims[SampleNum][0]*dims[SampleNum-1][1]) for i in df['Force']], [float(i)/dims[SampleNum-1][2] for i in df['Stroke']]])
            
            else:

                for i in df["Force"]:
                    i = float(i)
                    data[SampleNum][0].append(i)
                    i = i/(dims[SampleNum][1]*dims[SampleNum][0])
                    data[SampleNum][2].append(i)

                for i in df["Stroke"]:
                    i = float(i)
                    data[SampleNum][1].append(i)
                    i = i/dims[SampleNum][2]
                    data[SampleNum][3].append(i)
                    
        dataFrame = [getDataFrame(i) for i in data]

    # Graph the data
    for i in range(len(data)):
        plt.plot(dataFrame[i]['Stroke'], dataFrame[i]['Force'],color = dims[i][3])
        execute("Displacement (in mm)","Force (in N)",f"{i}_strokeforce.jpg")
        plt.plot(dataFrame[i]['Strain'], dataFrame[i]['Stress'],color = dims[i][3])
        execute("Strain (dimensionless)","Stress (in MPa)",f"{i}_strainstress.jpg")

    for i in range(len(data)):
        plt.plot(dataFrame[i]['Stroke'], dataFrame[i]['Force'],color = dims[i][3])
    execute("Displacement (in mm)","Force (in N)","all_strokeforce.jpg")

    for i in range(len(data)):
        plt.plot(dataFrame[i]['Strain'], dataFrame[i]['Stress'],color = dims[i][3])
    execute("Strain (dimensionless)","Stress (in MPa)","all_strainstress.jpg")  
    
    messagebox.showinfo('Successful!','Graphs have been saved successfully in folder!\nYou can exit the program!')

#Clear previous frame
def clearframe():
     for widgets in frame.winfo_children():
        widgets.destroy()
        
#Ask the user for the names of the files per sample
def fetch_names(files_num):
    files = []
    
    #Ask for the names of the files
    clearframe()
    for k,i in enumerate(files_num):
        label = Label(frame,text = f"Enter the names of files,in order, for sample number {k+1}")
        label.pack()
        files.append([])
        for x in range(i):
            name = Entry(frame,width = 20)
            name.pack()
            files[k].append(name)
            
    #Send the names of files to another fucntion
    btn2 = Button(frame,text = "Enter",command = lambda:fetchlists([[i.get() for i in files[k]] for k in range(len(files))]))
    btn2.pack()
    window.mainloop()
    
#Ask the user for the number of files per sample
def find_samples(num_samples, data, lst = dims):
    entries = []
    for i in range(len(data)//4):
        lst.append([float(data[i*4]),float(data[i*4+1]),float(data[i*4+2]),data[i*4+3]])
    
    #Create new widgets in frame
    clearframe()
    for i in range(num_samples):
        label = Label(frame,text = f"Enter the number of files for sample number {i+1}")
        label.grid(column= 0,row = i)
        name = Entry(frame,width = 10)
        name.grid(column = 1, row = i)
        entries.append(name)
        
    #Send the number of files to another function
    btn2 = Button(frame,text = "Enter",command = lambda:fetch_names([int(i.get()) for i in entries]))
    btn2.grid(column = 0, row = len(entries)*2)
    window.mainloop()

# The first frame of the program
def mainframe():
    label = Label(frame, text = 'Enter the number of samples!')
    label.grid(column = 0,row = 0)
    spin = Spinbox(frame, from_=0, to=100)
    spin.grid(column=0,row=1)
    btn = Button(frame, text="Enter",command = lambda: find_dims(spin))
    btn.grid(column=1, row=1)
    mainloop()

# Second frame to ask for dimensions
def find_dims(spin):
    entries = []
    sample = int(spin.get())
    clearframe()
    
    for i in range(sample):
        label = Label(frame,text = f"Enter the dimensions of sample number {i+1}: ")
        label.grid(column= 0,row = i*5)
        for x in range(4):
            label = Label(frame,text = f"{dimsnames[x]}")
            label.grid(column= 0,row = i*5+(x+1))
            name = Entry(frame,width = 10)
            name.grid(column = 1, row = i*5+(x+1))
            entries.append(name)
            
    btn = Button(frame, text="Enter",command = lambda: find_samples(sample,[i.get() for i in entries]))
    btn.grid(column=0, row=5*sample+1)
    mainloop()
    
# Create tkinter window and frame, we will not destroy frames.
# Just a single frame and create new widgets for each step.
window = Tk()
window.title("App")
frame = Frame(window)
frame.pack(side="top", expand=True, fill="both")
mainframe()