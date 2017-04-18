import csv
import os

def isZone1(isInterfazVisual, userCoordinateX, userCoordinateY):
    if (isInterfazVisual):
        zoneCoordinateX1 = float(1)
        zoneCoordinateY1 = float(1)
        zoneCoordinateX2 = float(900)
        zoneCoordinateY2 = float(200)
    else: # If not isInterfaceVisual Then is Tradicional
        zoneCoordinateX1 = float(150)
        zoneCoordinateY1 = float(1)
        zoneCoordinateX2 = float(860)
        zoneCoordinateY2 = float(150)
    
    if (userCoordinateX >= zoneCoordinateX1 and
        userCoordinateX <= zoneCoordinateX2 and
        userCoordinateY >= zoneCoordinateY1 and
        userCoordinateY <= zoneCoordinateY2):
        return True
    else:
        return False

def isZone2(isInterfazVisual, userCoordinateX, userCoordinateY):
    if (isInterfazVisual):
        zoneCoordinateX1 = float(1)
        zoneCoordinateY1 = float(200)
        zoneCoordinateX2 = float(700)
        zoneCoordinateY2 = float(800)
    else: # If not isInterfaceVisual Then is Tradicional
        zoneCoordinateX1 = float(240)
        zoneCoordinateY1 = float(150)
        zoneCoordinateX2 = float(960)
        zoneCoordinateY2 = float(1000)
    
    if (userCoordinateX >= zoneCoordinateX1 and
        userCoordinateX <= zoneCoordinateX2 and
        userCoordinateY >= zoneCoordinateY1 and
        userCoordinateY <= zoneCoordinateY2):
        return True
    else:
        return False

def isZone3(isInterfazVisual, userCoordinateX, userCoordinateY):
    if (isInterfazVisual):
        zoneCoordinateX1 = float(550)
        zoneCoordinateY1 = float(850)
        zoneCoordinateX2 = float(960)
        zoneCoordinateY2 = float(1080)
    else: # If not isInterfaceVisual Then is Tradicional
        zoneCoordinateX1 = float(1)
        zoneCoordinateY1 = float(150)
        zoneCoordinateX2 = float(240)
        zoneCoordinateY2 = float(350)
    
    if (userCoordinateX >= zoneCoordinateX1 and
        userCoordinateX <= zoneCoordinateX2 and
        userCoordinateY >= zoneCoordinateY1 and
        userCoordinateY <= zoneCoordinateY2):
        return True
    else:
        return False
    
def isZone4(isInterfazVisual, userCoordinateX, userCoordinateY):
    if (isInterfazVisual):
        zoneCoordinateX1 = float(1)
        zoneCoordinateY1 = float(900)
        zoneCoordinateX2 = float(480)
        zoneCoordinateY2 = float(1050)
    else: # If not isInterfaceVisual Then is Tradicional
        zoneCoordinateX1 = float(1430)
        zoneCoordinateY1 = float(120)
        zoneCoordinateX2 = float(1750)
        zoneCoordinateY2 = float(350)
    
    if (userCoordinateX >= zoneCoordinateX1 and
        userCoordinateX <= zoneCoordinateX2 and
        userCoordinateY >= zoneCoordinateY1 and
        userCoordinateY <= zoneCoordinateY2):
        return True
    else:
        return False

def writeFile(filename, line):
    extension = ".txt"
    filenameCSV= "-new" + extension
    with open(filenameCSV, 'ab') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=' ')
        csvWriter.writerow(line)

def isAClick(mouseStatus):
    if "MouseClickLeft" in mouseStatus:
        return True
    else: return False

def hasClickedInZoneBefore(mouseStatus, lastMouseStatus):
    if mouseStatus == lastMouseStatus:
        return True
    else: return False

def countZonesForClickInFile(fileInMemory, filename):
    clickZone1 = 0
    clickZone2 = 0
    clickZone3 = 0
    clickZone4 = 0
    clickZone5 = 0
    hasClickedOnTheZone = False
    lastMouseStatus = ""
    lastCoordinateXData = 0
    lastCoordinateYData = 0
    isInterfazVisual = True
    for line in fileInMemory:
        if len(line) == 4:
            mouseStatus = str(line[3])
            if isAClick(mouseStatus) and not hasClickedInZoneBefore(mouseStatus, lastMouseStatus):
                if isZone1(isInterfazVisual, lastCoordinateXData, lastCoordinateYData):
                    clickZone1 += 1
                elif isZone2(isInterfazVisual, lastCoordinateXData, lastCoordinateYData):
                    clickZone2 += 1
                elif isZone3(isInterfazVisual, lastCoordinateXData, lastCoordinateYData):
                    clickZone3 += 1
                elif isZone4(isInterfazVisual, lastCoordinateXData, lastCoordinateYData):
                    clickZone4 += 1
                else:
                    clickZone5 += 1
        else:
            lastMouseStatus = ""
            lastCoordinateXData=float(line[3])
            lastCoordinateYData=float(line[4])
    listResultsZone1 = [1, clickZone1]
    listResultsZone2 = [2, clickZone2]
    listResultsZone3 = [3, clickZone3]
    listResultsZone4 = [4, clickZone4]
    listResultsZone5 = [5, clickZone5]
    writeFile(filename, listResultsZone1)
    writeFile(filename, listResultsZone2)
    writeFile(filename, listResultsZone3)
    writeFile(filename, listResultsZone4)
    writeFile(filename, listResultsZone5)        
    print "zone 1: " + str(clickZone1)
    print "zone 2: " + str(clickZone2)
    print "zone 3: " + str(clickZone3)
    print "zone 4: " + str(clickZone4)
    print "zone 5: " + str(clickZone5)
            
def writeFileToMemory(filename):    
    with open(filename, 'rb') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=' ')
        matrixValues = list(readCSV)
    return matrixValues

def writeOutput():
    listResultsZone1 = [1, clickZone1]
    listResultsZone2 = [2, clickZone2]
    listResultsZone3 = [3, clickZone3]
    listResultsZone4 = [4, clickZone4]
    listResultsZone5 = [5, clickZone5]
    writeFile(listResultsZone1)
    writeFile(listResultsZone2)
    writeFile(listResultsZone3)
    writeFile(listResultsZone4)
    writeFile(listResultsZone5)

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
            countZonesForClickInFile(fileInMemory, str(filename))
    #writeOutput()

if __name__ == '__main__':
    main()
    
