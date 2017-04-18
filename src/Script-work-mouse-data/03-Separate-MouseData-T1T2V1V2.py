import csv
import os

def writeFile(filename, line):
    filename = str(line[0])
    extension = ".txt"
    filenameCSV= filename + extension
    with open(filenameCSV, 'ab') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=' ')
        csvWriter.writerow(line)

def separateInFiles(fileInMemory, filename):
    for line in fileInMemory:
        secuenceType = str(line[0])
        userID = str(line[1])
        TS = str(line[2])
        if len(line) == 5:
            valueX=float(line[3])
            valueY=float(line[4])
            valuesFiltered = [secuenceType, userID, TS, valueX, valueY]
        else:
            mouseAction = str(line[3])
            valuesFiltered = [secuenceType, userID, TS, mouseAction]
        writeFile(filename, valuesFiltered)

def writeFileToMemory(filename):    
    with open(filename, 'rb') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=' ')
        matrixValues = list(readCSV)
    return matrixValues

def main():
    currentDir = os.getcwd()
    for filename in os.listdir(currentDir):
        if ".py" in filename:
            print " "
        elif "out.txt" in filename:
            print " "
        else:
            print "processing " + str(filename)
            fileInMemory = writeFileToMemory(filename)
            separateInFiles(fileInMemory, str(filename))

if __name__ == '__main__':
    main()
    
