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
    filenameCSV= filename + "-onlyZ2" + extension
    with open(filenameCSV, 'ab') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=' ')
        csvWriter.writerow(line)

def getContentPerFile(isInterfazVisual, fileInMemory, filename, users):
    for user in users:
        for line in fileInMemory:
            if (user == int(line[1])):
                userCoordinateX = float(line[5])
                userCoordinateY = float(line[6])
                if (isZone2(isInterfazVisual, userCoordinateX, userCoordinateY)):
                    writeFile(filename, line)
    print filename + " processed successful \n"
            
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
    isVisual = False
    currentDir = os.getcwd()
    for filename in os.listdir(currentDir):
        if ".py" in filename:
            print " "
        elif "out.txt" in filename:
            print " "
        else:
            print "processing " + str(filename)
            fileInMemory = writeFileToMemory(filename)
            usersInFile = obtainUsersFromFile(fileInMemory)
            getContentPerFile(isVisual, fileInMemory, str(filename), usersInFile)

if __name__ == '__main__':
    main()
    
