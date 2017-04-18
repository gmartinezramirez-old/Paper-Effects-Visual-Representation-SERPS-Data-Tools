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
    filenameCSV= filename + "count-wheels" + extension
    with open(filenameCSV, 'ab') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=' ')
        csvWriter.writerow(line)

def isAMouseClick(mouseStatus):
    if "MouseClickLeft" in mouseStatus:
        return True
    else: return False

def isAMouseWheel(mouseStatus):
    if "Wheel" in mouseStatus:
        return True
    else: return False

def hasClickedInZoneBefore(mouseStatus, lastMouseStatus):
    if mouseStatus == lastMouseStatus:
        return True
    else: return False
    
def isPositiveMouseWheel(mouseWheelStatus):
    status = mouseWheelStatus.split("=")
    if int(status[1]) > 0:
        return True
    else: return False

def countZonesForClickInFile(isVisual, fileInMemory, filename, users):
    hasClickedOnTheZone = False
    lastMouseStatus = ""
    lastCoordinateXData = 0
    lastCoordinateYData = 0
    for user in users:
        mouseWheelPositiveAccumulateZ1 = 0
        mouseWheelNegativeAccumulateZ1 = 0
        mouseWheelPositiveAccumulateZ2 = 0
        mouseWheelNegativeAccumulateZ2 = 0
        mouseWheelPositiveAccumulateZ3 = 0
        mouseWheelNegativeAccumulateZ3 = 0
        mouseWheelPositiveAccumulateZ4 = 0
        mouseWheelNegativeAccumulateZ4 = 0
        mouseWheelPositiveAccumulateZ5 = 0
        mouseWheelNegativeAccumulateZ5 = 0
        for line in fileInMemory:
            if str(user) == str(line[1]):
                mode = str(line[0])
                if len(line) == 4:
                    mouseStatus = str(line[3])
                    if isAMouseWheel(mouseStatus) and not hasClickedInZoneBefore(mouseStatus, lastMouseStatus):
                        if isZone1(isVisual, lastCoordinateXData, lastCoordinateYData):
                            if isPositiveMouseWheel(mouseStatus):
                                mouseWheelPositiveAccumulateZ1 += 1
                            else: mouseWheelNegativeAccumulateZ1 += 1
                        elif isZone2(isVisual, lastCoordinateXData, lastCoordinateYData):
                            if isPositiveMouseWheel(mouseStatus):
                                mouseWheelPositiveAccumulateZ2 += 1
                            else: mouseWheelNegativeAccumulateZ2 += 1
                        elif isZone3(isVisual, lastCoordinateXData, lastCoordinateYData):
                            if isPositiveMouseWheel(mouseStatus):
                                mouseWheelPositiveAccumulateZ3 += 1
                            else: mouseWheelNegativeAccumulateZ3 += 1
                        elif isZone4(isVisual, lastCoordinateXData, lastCoordinateYData):
                            if isPositiveMouseWheel(mouseStatus):
                                mouseWheelPositiveAccumulateZ4 += 1
                            else: mouseWheelNegativeAccumulateZ4 += 1
                        else:
                            if isPositiveMouseWheel(mouseStatus):
                                mouseWheelPositiveAccumulateZ5 += 1
                            else: mouseWheelNegativeAccumulateZ5 += 1
                else:
                    lastMouseStatus = ""
                    lastCoordinateXData=float(line[3])
                    lastCoordinateYData=float(line[4])
        listResultsZone1 = [mode, user, 1, mouseWheelPositiveAccumulateZ1, mouseWheelNegativeAccumulateZ1]
        listResultsZone2 = [mode, user, 2, mouseWheelPositiveAccumulateZ2, mouseWheelNegativeAccumulateZ2]
        listResultsZone3 = [mode, user, 3, mouseWheelPositiveAccumulateZ3, mouseWheelNegativeAccumulateZ3]
        listResultsZone4 = [mode, user, 4, mouseWheelPositiveAccumulateZ4, mouseWheelNegativeAccumulateZ4]
        listResultsZone5 = [mode, user, 5, mouseWheelPositiveAccumulateZ5, mouseWheelNegativeAccumulateZ5]
        #print listResultsZone1
        #print listResultsZone2
        #print listResultsZone3
        #print listResultsZone4
        #print listResultsZone5
        writeFile(filename, listResultsZone1)
        writeFile(filename, listResultsZone2)
        writeFile(filename, listResultsZone3)
        writeFile(filename, listResultsZone4)
        writeFile(filename, listResultsZone5)        
     
def writeFileToMemory(filename):    
    with open(filename, 'rb') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=' ')
        matrixValues = list(readCSV)
    return matrixValues

def obtainUsersFromFile(fileInMemory):
    users = []
    for line in fileInMemory:
        users.append(int(line[1]))
    userSet = set(users)
    return userSet

def main():
    currentDir = os.getcwd()
    isVisual = False
    #isVisual = True
    #testvar1 = "Wheel=-120"
    #listvar = testvar1.split("=")
    #print listvar[1]
    #if isPositiveMouseWheel(testvar1):
    #    print "positivo"
    #else: print "negativo"
    for filename in os.listdir(currentDir):
        if ".py" in filename:
            print " "
        elif "out.txt" in filename:
            print " "
        else:
            print "processing " + str(filename)
            fileInMemory = writeFileToMemory(filename)
            usersInFile = obtainUsersFromFile(fileInMemory)
            countZonesForClickInFile(isVisual, fileInMemory, str(filename), usersInFile)

if __name__ == '__main__':
    main()
    
