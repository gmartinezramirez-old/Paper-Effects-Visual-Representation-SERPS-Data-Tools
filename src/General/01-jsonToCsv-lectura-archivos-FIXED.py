# -*- coding: cp1252 -*-
import csv
import json
import os

#def writeToCsvFile(filename, ts, time, x, y,  leftEyepSize, rightEyepSize, diferenceTime):
#    fileNameWithoutExtension = filename.split(".")[-1]
#    outputFilenameCSV= filename + "inverted.txt"
#    with open(outputFilenameCSV, 'ab') as csvfile:
#        csvWriter = csv.writer(csvfile, delimiter=' ')
#        csvWriter.writerow([ts,time, x, y,  leftEyepSize, rightEyepSize, diferenceTime])

def writeToFile(filename, line):
    fileNameWithoutExtension = filename.split(".")[0]
    outputFilenameCSV= filename + ".txt"
    with open(outputFilenameCSV, 'ab') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=' ')
        csvWriter.writerow(line)

def calculateAvg(filename, counterLinesPerBlock, startTimeTS, startTime, lastTimeTS, lastTime, duration, xAcumulate, yAcumulate, leftEyepSizeAcumulate, rightEyepSizeAcumulate):
    avgX = (xAcumulate/counterLinesPerBlock)
    avgY = (yAcumulate/counterLinesPerBlock)
    avgPSizeL = (leftEyepSizeAcumulate/counterLinesPerBlock)
    avgPSizeR = (rightEyepSizeAcumulate/counterLinesPerBlock)
    line = [startTimeTS, lastTimeTS, duration, avgX, avgY, avgPSizeL, avgPSizeR]
    writeToFile(filename, line)

def processFile(filename):
    lastUserTime = 0
    counterLinesPerBlock = 0
    xAcumulate = 0
    yAcumulate = 0
    leftEyepSizeAcumulate = 0
    rightEyepSizeAcumulate = 0
    startTime = 0
    lastTime = 0
    duration = 0
    lastStatus = False
    print "Procesando " + str(filename)
    with open(filename) as file:
        for line in file:
            json_data = json.loads(line)
            if (json_data["category"]== "tracker"):
                # Fixation True indicates that is (1) start a new block or (2) is in a block
                if(json_data["values"]["frame"]["fix"] == True):
                    if lastStatus == False: #I am the beginning of the block
                        startTime = json_data["values"]["frame"]["time"]
                        startTimeTS = json_data["values"]["frame"]["timestamp"]
                    lastStatus = True
                    counterLinesPerBlock += 1
                    lastTime = json_data["values"]["frame"]["time"]
                    lastTimeTS = json_data["values"]["frame"]["timestamp"]   
                    xAcumulate += float(json_data["values"]["frame"]["avg"]["x"])
                    yAcumulate += float(json_data["values"]["frame"]["avg"]["y"])
                    leftEyepSizeAcumulate += float(json_data["values"]["frame"]["lefteye"]["psize"])
                    rightEyepSizeAcumulate += float(json_data["values"]["frame"]["righteye"]["psize"])

                # Fixation false is not a block
                else:
                    if lastStatus == True: #El ultimo status es la ultima linea del bloque
                        duration = lastTime-startTime
                        calculateAvg(filename, counterLinesPerBlock, startTimeTS, startTime, lastTimeTS, lastTime, duration, xAcumulate, yAcumulate, leftEyepSizeAcumulate, rightEyepSizeAcumulate)
                    lastStatus = False
                    counterLinesPerBlock = 0
                    timeAcumulate = 0
                    xAcumulate = 0
                    yAcumulate = 0
                    leftEyepSizeAcumulate = 0
                    rightEyepSizeAcumulate = 0
                    startTime = 0
                    lastTime = 0
def main():
    currentDir = os.getcwd()
    print "Directorio actual: " + str(currentDir)
    for filename in os.listdir(currentDir):
        if ".json" in filename:
            processFile(filename)
        else:
            print str(filename) + " no se puede procesar"

  
if __name__ == "__main__":
    main()
