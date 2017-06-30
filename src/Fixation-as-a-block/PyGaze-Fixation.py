# -*- coding: cp1252 -*-
import csv
import json
import os

max_err = 3


def writeToCsvFile(filename, ts, time, x, y,  leftEyepSize, rightEyepSize, diferenceTime):
    fileNameWithoutExtension = filename.split(".")[0]
    outputFilenameCSV= filename + ".txt"
    with open(outputFilenameCSV, 'ab') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=' ')
        csvWriter.writerow([timestamp, time, x, y, leftEyepSize, rightEyepSize, diferenceTime])


def calculateAvg(filename, ccount_lines_per_fixation, startTimeTS, startTime, lastTimeTS, lastTime, duration, xAcumulate, yAcumulate, leftEyepSizeAcumulate, rightEyepSizeAcumulate):
    avgX = (xAcumulate/count_lines_per_fixation)
    avgY = (yAcumulate/count_lines_per_fixation)
    avgPSizeL = (leftEyepSizeAcumulate/count_lines_per_fixation)
    avgPSizeR = (rightEyepSizeAcumulate/count_lines_per_fixation)
    line = [startTimeTS, lastTimeTS, duration, avgX, avgY, avgPSizeL, avgPSizeR]
    writeToFile(filename, line)


def processFile(filename):
    lastUserTime = 0
    count_lines_per_fixation = 0
    start_positions = []
    x1 = []
    y1 = []
    in_fixation = False
    is_moving = True
    with open(filename) as file:
        print "Procesando " + str(filename)
        for line in file:
            json_data = json.loads(line)
            if (json_data["category"]== "tracker"):
                ts = json_data["values"]["frame"]["timestamp"]
                time = json_data["values"]["frame"]["time"] # Do something with this
                x = json_data["values"]["frame"]["avg"]["x"]
                y = json_data["values"]["frame"]["avg"]["y"]
                n_positions = [x,y]
                left_eye_psize = json_data["values"]["frame"]["lefteye"]["psize"]
                right_eye_psize= json_data["values"]["frame"]["righteye"]["psize"]
                # Check is the n position is the fixation start
                if is_moving:
                    x1.append(x)
                    y1.append(y)
                    if len(x1) == 5:
                        # Check if deviation is small enough
                        if max(xl)-min(xl) < maxerr and max(yl)-min(yl) < maxerr:
                            is_moving = False
                            in_fixation = True
                        # Remove oldeset sample
                        xl.pop(0); yl.pop(0)
                    start_fixation_ts = ts
                    start_fixation_time = time
                    start_fixation_positions= [x1[len(xl)-1],yl[len(yl)-1]]
                # I'm in a fixation
                elif not is_moving:  # is not is_moving
                    # Now check is the n position is the fixation end
                    if ((start_positions[0]-n_positions[0])**2  + (start_positions[1]-n_positions[1])**2)**0.5 > maxerr: # Pythagoras
                        ending_fixation_ts = ts
                        ending_fixation_time = time
                        ending_fixation_positions = n_positions
                        duration_of_fixation = last_time-start_time
                        calculateAvg(filename, count_lines_per_fixation, start_fixation_ts, start_fixation_time, ending_fixation_ts, ending_fixation_time, duration_of_fixation, x_accumulated, y_accumulated, left_eye_psize_accumulated, right_eye_psize_accumulated)   
                elif in_fixation:
                    count_lines_per_fixation += 1
                    time_accumulated += float(json_data["values"]["frame"]["time"])
                    x_accumulated += float(json_data["values"]["frame"]["avg"]["x"])
                    y_accumulated += float(json_data["values"]["frame"]["avg"]["y"])
                    left_eye_psize_accumulated += float(json_data["values"]["frame"]["lefteye"]["psize"])
                    right_eye_psize_accumulated += float(json_data["values"]["frame"]["righteye"]["psize"]) 
                # Finally, reset the counters
                count_lines_per_fixation = 0
                time_accumulated = 0
                x_accumulated = 0
                y_accumulated = 0
                left_eye_psize_accumulated = 0
                right_eye_psize_accumulated = 0
                start_fixation_ts = 0
                start_fixation_time = 0
                start_fixation_positions= []
                ending_fixation_ts = 0
                ending_fixation_time = 0
                ending_fixation_positions = []
                duration_of_fixation = 0


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
