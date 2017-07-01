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
    if ccount_lines_per_fixation > 0:                  # VP: Lo coloqué porque daba error de division para 0, aunque debería ir el operador DIFERENTE, no mayor que
        print "Results of the fixation block"                                 # VP: Lo puse solo para saber si ingresa, en realidad siempre llega el contador en CERO, no se por qué?
        avgX = (xAcumulate/ccount_lines_per_fixation)   # VP: Cambié count_lines_per_fixation por ccount_lines_per_fixation
        avgY = (yAcumulate/ccount_lines_per_fixation)   # VP: Cambié count_lines_per_fixation por ccount_lines_per_fixation
        avgPSizeL = (leftEyepSizeAcumulate/ccount_lines_per_fixation)   # VP: Cambié count_lines_per_fixation por ccount_lines_per_fixation
        avgPSizeR = (rightEyepSizeAcumulate/ccount_lines_per_fixation)  # VP: Cambié count_lines_per_fixation por ccount_lines_per_fixation
    
        # Test: print variables
        print avgX, avgY
       

        # If coord is in AOI 2 - Visual Interface
        """
        if (avgX >= 1 and avgX <= 700 and avgY >= 200 and avgY <= 800):             # VP: Aumenté esto para que solo escriba las que están en el área de interés 2, el resto no importa para este análisis
            line = [startTimeTS, lastTimeTS, duration, avgX, avgY, avgPSizeL, avgPSizeR]
            writeToFile(filename, line)
        """

def processFile(filename):
    lastUserTime = 0
    count_lines_per_fixation = 0
    start_positions = 0, 0      # VP: temporalmente asigné valores porque estaba: [] pero daba error en la línea 67: IndexError: list index out of range. Debe ser la fijación en la que estoy porque con esa calculo Pitágoras, estaba vacío y daba error
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
                        if max(x1)-min(x1) < max_err and max(y1)-min(y1) < max_err:         # VP: cambié maxerr por max_err
                            is_moving = False
                            in_fixation = True
                        # Remove oldeset sample
                        x1.pop(0); y1.pop(0)
                    start_fixation_ts = ts
                    start_fixation_time = time
                    start_fixation_positions= (x1[len(x1)-1],y1[len(y1)-1])         # VP: cambie [x1[len(xl)-1],yl[len(yl)-1]] por (x1[len(x1)-1],y1[len(y1)-1])
                # I'm in a fixation
                elif not is_moving:  # is not is_moving
                    # Now check is the n position is the fixation end
                    if ((start_positions[0]-n_positions[0])**2  + (start_positions[1]-n_positions[1])**2)**0.5 > max_err: # Pythagoras          # VP: cambié maxerr por max_err
                        ending_fixation_ts = ts
                        ending_fixation_time = time
                        ending_fixation_positions = n_positions
                        duration_of_fixation = ending_fixation_time - start_fixation_time   # VP: cambié last_time-start_time  por ending_fixation_time - start_fixation_time
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
    print "Finalizó proceso"


if __name__ == "__main__":
    main()
