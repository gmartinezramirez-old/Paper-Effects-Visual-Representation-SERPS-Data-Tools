import csv
import os

def writeFile(filename, line):
    extension = "-clean.txt"
    filenameCSV= filename + extension
    with open(filenameCSV, 'ab') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=' ')
        csvWriter.writerow(line)

def removeDotsTS(TS):
    dotsCounter = 0
    newTS = ""
    for character in TS:
        if dotsCounter < 2:
            if character == ".":
                dotsCounter += 1
                character = ""
        newTS += character
    return float(newTS)

def isCoordinateCorrect(lineValues):
    ''' line[1] = x, line[2] = y
    '''
    if float(lineValues[1]) > 0 and float(lineValues[1]) <= 1920 and float(lineValues[2]) > 0 and float(lineValues[2]) <= 1080:
        return True
    else:
        return False

def separateInFiles(fileInMemory, filename):
    for line in fileInMemory:
        idUser = filename
        TS = removeDotsTS(str(line[0]))
        if len(line) == 3:
            if (isCoordinateCorrect(line)):
                valueX=float(line[1])
                valueY=float(line[2])
                valuesFiltered = [idUser, TS, valueX, valueY]
        else:
            mouseStatus = str(line[1])
            valuesFiltered = [idUser, TS, mouseStatus]
        writeFile(filename, valuesFiltered)

def writeFileToMemory(filename):
    with open(filename, 'rb') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=' ')
        matrixValues = list(readCSV)
    return matrixValues

def removeFileExtension(filename):
    filenameWithoutExtension = str(filename).split(".")[0]
    return filenameWithoutExtension

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
            fileOnlyName = removeFileExtension(filename)
            separateInFiles(fileInMemory, str(fileOnlyName))

if __name__ == '__main__':
    main()

