import matplotlib.pyplot as plt 
import pandas as pd
data =[] 
dims = []
Num = []
colors = []
def getDataFrame(data):
    dat = {'Force': data[0], 'Stroke': data[1], 'Stress': data[2], 'Strain': data[3]}
    return pd.DataFrame(dat, columns = ['Force', 'Stroke','Stress','Strain']).astype(float)
def fetchlists(FileName,SampleNum):
    SampleNum=int(SampleNum)
    df = pd.read_csv(FileName, skiprows = 1).drop([0])
    if SampleNum not in Num:
        Num.append(SampleNum)
        width = float(input("Enter width of sample number {}: ".format(SampleNum)))
        thickness = float(input("Enter thickness of sample number {}: ".format(SampleNum)))
        length = float(input("Enter length of sample number {}: ".format(SampleNum)))
        dims.append([width,thickness,length])
        return [i for i in df["Force"]], [i for i in df["Stroke"]], [float(i)/(dims[SampleNum-1][0]*dims[SampleNum-1][1]) for i in df['Force']], [float(i)/dims[SampleNum-1][2] for i in df['Stroke']]
    else:
        for i in df["Force"]:
            i = float(i)
            data[SampleNum-1][0].append(i)
            i = i/(dims[SampleNum-1][1]*dims[SampleNum-1][0])
            data[SampleNum-1][2].append(i)
        for i in df["Stroke"]:
            i = float(i)
            data[SampleNum-1][1].append(i)
            i = i/dims[SampleNum-1][2]
            data[SampleNum-1][3].append(i)

NumSamples = int(input("Enter the number of samples: "))
for i in range(1, NumSamples+1):
    print("___________________________ Enter data for sample number {} ___________________________".format(i))

    NumFiles = int(input("Enter number of files for sample number {}: ".format(i)))
    FilePath = input("Enter the name of the first file with the extension: ")
    data.append(list(fetchlists(FilePath,i)))
    if NumFiles > 1:
        for j in range (2, NumFiles+1):
            FilePath = input("Enter the name of file number {} for sample number {}: ".format(j,i))
            fetchlists(FilePath,i)
    color = input("Choose a color for curve {}: ".format(i))
    colors.append(color)
    print("\n___________________________Sample {} registered! ___________________________".format(i))

dataFrame = [getDataFrame(i) for i in data]
for i in range(NumSamples):
    plt.plot(dataFrame[i]['Stroke'], dataFrame[i]['Force'], color = colors[i])
    plt.xlabel("Displacement (in mm)")
    plt.ylabel("Force (in N)")
    plt.grid()
    plt.show()
    plt.plot(dataFrame[i]['Strain'], dataFrame[i]['Stress'], color = colors[i])
    plt.xlabel("Strain (dimensionless)")
    plt.ylabel("Stress (in MPa)")
    plt.grid()
    plt.show()
for i in range(NumSamples):
    plt.plot(dataFrame[i]['Stroke'], dataFrame[i]['Force'], color = colors[i])
plt.xlabel("Displacement (in mm)")
plt.ylabel("Force (in N)")
plt.grid()
plt.show()
for i in range(NumSamples):
    plt.plot(dataFrame[i]['Strain'], dataFrame[i]['Stress'], color = colors[i])
plt.xlabel("Strain (dimensionless)")
plt.ylabel("Stress (in MPa)")
plt.grid()
plt.show()

