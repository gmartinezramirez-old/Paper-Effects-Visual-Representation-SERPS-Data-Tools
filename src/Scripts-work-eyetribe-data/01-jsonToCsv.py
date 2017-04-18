# -*- coding: cp1252 -*-
import csv
import json
import os

def writeToCsvHeader(filename):
    # Remove extension from a filename
    fileNameWithoutExtension = filename.split(".")[-1]
    outputFilenameCSV= filename + ".txt"
    with open(outputFilenameCSV, 'wb') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=' ')
        csvWriter.writerow(["TS", "TIME", "X", "Y", "LEFTPSIZE", "RIGHTPSIZE"])

def writeToCsvFile(filename, ts, time, x, y,  leftEyepSize, rightEyepSize):
    fileNameWithoutExtension = filename.split(".")[-1]
    outputFilenameCSV= filename + ".txt"
    with open(outputFilenameCSV, 'ab') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=' ')
        csvWriter.writerow([ts,time, x, y,  leftEyepSize, rightEyepSize])

def printValues(filename,x,y,time,ts):
    print filename
    print x
    print y
    print time
    print ts

def processFile(filename):
    with open(filename) as file:
        print "Procesando " + str(filename)
        writeToCsvHeader(filename)
        for line in file:
            json_data = json.loads(line)
            # if fix = true then do it
            if (json_data["category"]== "tracker"):
                ts = json_data["values"]["frame"]["timestamp"]
                time = json_data["values"]["frame"]["time"]
                x = json_data["values"]["frame"]["avg"]["x"]
                y = json_data["values"]["frame"]["avg"]["y"]
                leftEyepSize= json_data["values"]["frame"]["lefteye"]["psize"]
                rightEyepSize= json_data["values"]["frame"]["righteye"]["psize"]
                writeToCsvFile(filename, ts, time, x, y, leftEyepSize, rightEyepSize)
        fileNameWithoutExtension = filename.split(".")[-1]
        outputFilenameCSV= filename + ".txt"
        print str(outputFilenameCSV) + " escrito con exito!"

def main():
    currentDir = os.getcwd()
    print "Current dir is: " + str(currentDir)
    for filename in os.listdir(currentDir):
        if ".json" in filename:
            processFile(filename)
        else:
            print str(filename) + " no se puede procesar"

  
if __name__ == "__main__":
    main()
