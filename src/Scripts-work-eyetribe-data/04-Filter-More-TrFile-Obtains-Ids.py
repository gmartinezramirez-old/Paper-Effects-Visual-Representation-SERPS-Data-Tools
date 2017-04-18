import csv
import os

def writeFile(filename, line):
    #filename = str(line[0])
    extension = "-ids.txt"
    filenameCSV= filename + extension
    with open(filenameCSV, 'ab') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=' ')
        csvWriter.writerow(line)

def separateInFiles(fileInMemory, filename):
    for line in fileInMemory:
        secuenceType = line[0] # T1, T2, etc
        userID = line[1]
        valueX = line[4]
        valueY = line[5]
        valuesFiltered = [secuenceType, userID, valueX, valueY]
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
    
