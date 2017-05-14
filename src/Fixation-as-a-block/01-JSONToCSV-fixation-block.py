# -*- coding: cp1252 -*-
import csv
import json
import os

def writeToCsvFile(filename, ts, time, x, y,  leftEyepSize, rightEyepSize, diferenceTime):
    fileNameWithoutExtension = filename.split(".")[-1]
    outputFilenameCSV= filename + "inverted.txt"
    with open(outputFilenameCSV, 'ab') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=' ')
        csvWriter.writerow([ts,time, x, y,  leftEyepSize, rightEyepSize, diferenceTime])

def processFile(filename):
    lastUserTime = 0
    with open(filename) as file:
        print "Processing: " + str(filename)
        for line in file:
            json_data = json.loads(line)
            if json_data["category"] == "tracker":
                if json_data["values"]["frame"]["fix"] == True:
                    ts = json_data["values"]["frame"]["timestamp"]
                    time = json_data["values"]["frame"]["time"]
                    x = json_data["values"]["frame"]["avg"]["x"]
                    y = json_data["values"]["frame"]["avg"]["y"]
                    leftEyepSize= json_data["values"]["frame"]["lefteye"]["psize"]
                    rightEyepSize= json_data["values"]["frame"]["righteye"]["psize"]
                    if lastUserTime == 0:
                        diferenceTime = 0
                        lastUserTime = time
                    else:
                        diferenceTime = time - lastUserTime
                        lastUserTime = time
                    writeToCsvFile(filename, ts, time, x, y, leftEyepSize, rightEyepSize, diferenceTime)

def processInvertedFile(filename):
    lastUserTime = 0
    print "Processing: " + str(filename)
    for line in reversed(open(filename).readlines()):
        json_data = json.loads(line)
        if (json_data["category"]== "tracker"):
            if(json_data["values"]["frame"]["fix"] == True):
                ts = json_data["values"]["frame"]["timestamp"]
                time = json_data["values"]["frame"]["time"]
                x = json_data["values"]["frame"]["avg"]["x"]
                y = json_data["values"]["frame"]["avg"]["y"]
                leftEyepSize= json_data["values"]["frame"]["lefteye"]["psize"]
                rightEyepSize= json_data["values"]["frame"]["righteye"]["psize"]
                if lastUserTime == 0:
                    diferenceTime = 0
                    lastUserTime = time
                else:
                    diferenceTime = time - lastUserTime
                    lastUserTime = time
                writeToCsvFile(filename, ts, time, x, y, leftEyepSize, rightEyepSize, diferenceTime)

def main():
    currentDir = os.getcwd()
    print "Current working dir: " + str(currentDir)
    for filename in os.listdir(currentDir):
        if ".json" in filename:
            processInvertedFile(filename)
        else:
            print str(filename) + " cant be process"

if __name__ == "__main__":
    main()
