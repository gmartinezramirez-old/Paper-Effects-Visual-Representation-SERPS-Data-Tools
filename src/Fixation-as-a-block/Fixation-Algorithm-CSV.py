# -*- coding: cp1252 -*-
import csv
import json
import os
import logging
from math import atan2, degrees

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAXERROR = 30
PXFIXTRESH = 30

TOTAL_SAMPLES_PER_FIXATION = 5

FIXTRESH = 1.5  # Degrees; Maximal distance from fixation start (if gaze wanders beyond this, fixation has stopped)
FIXTIMETRESH = 100  # Milliseconds; Amount of time gaze has to linger within self.fixtresh to be marked as a fixation

FIXATIONS_IN_AOI2_AVG = 0


def write_to_file(filename, line):
    # logger.info("Writing to a file")
    filename_without_extension = filename.split(".")[0]
    output_filename_csv = filename + ".txt"
    with open(output_filename_csv, 'ab') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=' ')
        csv_writer.writerow(line)


def is_fixation_belongs_to_aoi2(avg_x, avg_y):
    if (avg_x >= 1 and avg_x <= 700) and (avg_y >= 200 and avg_y <= 800):
        return True
    else:
        return False


def calculate_avg(filename, total_lines_per_fixation, x_accumulated, y_accumulated):
    # logger.info("Calculate avg")
    # TODO: REMOVE, ONLY TEMP
    global FIXATIONS_IN_AOI2_AVG
    avg_x = float((x_accumulated / total_lines_per_fixation))
    avg_y = float((y_accumulated / total_lines_per_fixation))
    print "avg_x:", avg_x, " avg_y:", avg_y
    if is_fixation_belongs_to_aoi2:
        FIXATIONS_IN_AOI2_AVG += 1
        # print "AOI2"
        # line = [avg_x, avg_y]
        # write_to_file(filename, line)


# NOT USED
""""
def is_deviation_lower_than_maxerror(x1, y1):
    # logger.info("Calculating deviation")
    d1 = max(x1) - min(x1)
    d2 = max(y1) - min(y1)
    if d1 < max_error and d2 < max_error:
        return True
    else:
        return False
"""


def is_pythagoras_greater_than_maxerror(n_position, start_position):
    # logger.info("Calculating pythagoras")
    if (n_position[0] - start_position[0]) ** 2 + (n_position[1] - start_position[1]) ** 2 > PXFIXTRESH ** 2:
        # logger.info("pythagoras is greater than maxerror. Then is the end of fixation")
        return True
    else:
        # logger.info("pythagoras is not greater than maxerror. Still is a fixation")
        return False


def is_sample_far_starting_position(actual_position, start_position):
    if is_pythagoras_greater_than_maxerror(actual_position, start_position):
        return True
    else:
        return False


# NOT USED
def is_full_sample_rate(x1):
    # logger.info("Checking if x1 has the total of fixations")
    if len(x1) == TOTAL_SAMPLES_PER_FIXATION:
        # logger.info("len(x1) is equal to total_samples")
        return True
    else:
        # logger.info("len(x1) is not equal to total_samples")
        return False


def is_valid_sample(gaze_position):
    """Checks if the sample provided is valid, based on EyeTribe specific
    criteria (for internal use)

    arguments
    gaze_pos	--	a (x,y) gaze position tuple, as returned by
    				self.sample()

    returns
    valid		--	a Boolean: True on a valid sample, False on
    				an invalid sample
    """
    if (gaze_position[0] > 0 and gaze_position[0] <= 1920) and (gaze_position[1] > 0 and gaze_position[1] <= 1080):
        return True
    else:
        return False


def get_data_from_line(line_csv):
    # logger.info("Get data from new line of the json file")
    line_data = []
    ts, time = float(line_csv[0]), float(line_csv[1])
    x, y = float(line_csv[2]), float(line_csv[3])
    line_data.append(ts)
    line_data.append(time)
    line_data.append(x)
    line_data.append(y)
    return line_data


def is_fixation_time_surpassed_threshold(t1, t0):
    if t1 - t0 >= FIXTIMETRESH:
        return True
    else:
        return False


def start_fixation(t1, gaze_position):
    return t1, gaze_position, True


def end_fixation(t1, gaze_position):
    return t1, gaze_position, False


def print_fixation_info(lines_per_fixation, start_position, start_time, end_position, end_time):
    print "\tLines per fixation:", lines_per_fixation
    print "\t\tSTART AT:", start_position, "time:", start_time
    print "\t\tEND AT:", end_position, "time:", end_time
    print "-------------------\n"


def print_current_data(message, start_position, lines_per_fixation):
    print message, start_position, "lineas:", lines_per_fixation


def process_file(filename):
    start_position, actual_position, end_position, last_position, real_end_position = [], [], [], [], []
    t0, t1 = 0, 0
    is_fixation_has_started = False
    total_fixations, fixations_in_aoi2 = 0, 0
    lines_per_fixation, x_accum_per_fixation, y_accum_per_fixation = 0, 0, 0
    with open(filename, 'rb') as csvfile:
        line_csv = csv.reader(csvfile, delimiter=' ')
        for line in line_csv:
            sample = get_data_from_line(line)
            gaze_position = [sample[2], sample[3]]
            if is_valid_sample(gaze_position):
                #print "new sample:", sample
                gaze_actual_time = sample[1]
                if not is_fixation_has_started:
                    if not start_position:
                        #print "\tTEST A"
                        start_position = gaze_position
                        t0 = gaze_actual_time
                    else:
                        if is_sample_far_starting_position(gaze_position, start_position):
                            print "\tTEST B", start_position, gaze_position, "t1:", t1, "t0", t0, sample
                            start_position = gaze_position
                            t0 = gaze_actual_time
                        else:  # Is Close
                            t1 = gaze_actual_time
                            print "\tTEST C", start_position, gaze_position,"t1:", t1, "t0", t0, sample
                            if is_fixation_time_surpassed_threshold(t1, t0):  # return time and starting position
                                start_time, start_position, is_fixation_has_started = start_fixation(t1, gaze_position)
                                lines_per_fixation += 1
                                x_accum_per_fixation += gaze_position[0]
                                y_accum_per_fixation += gaze_position[1]
                                print_current_data("[Begin Fixation]", start_position, lines_per_fixation)
                            #TODO: ¿QUE PASA EN CASO CONTRARIO?
                else:  # Fixation has begun
                    if is_sample_far_starting_position(gaze_position, start_position):
                        end_time, end_position, is_fixation_has_started = end_fixation(gaze_actual_time, gaze_position)
                        #TODO: ACTIVAR PARA RECUPERAR LA LINEA ANTES DEL FINAL DE FIJACION
                        # real_end_position = last_position
                        # print "real end:", real_end_position
                        print_fixation_info(lines_per_fixation, start_position, start_time, end_position, end_time)
                        #TODO: ACTIVAR PARA CALCULAR AVG E IMPRIMIR TEXTO O VARIABLE
                        #calculate_avg(filename, lines_per_fixation, x_accum_per_fixation, y_accum_per_fixation)

                        # Reset variables
                        # t1, t0 = 0, 0
                        lines_per_fixation, x_accum_per_fixation, y_accum_per_fixation = 0, 0, 0
                        # TODO: ESTA LINEA CAMBIA TODO, 2am: PARECE QUE NO
                        # start_position, actual_position, end_position, last_position = [], [], [], []
                    else:
                        x_accum_per_fixation += gaze_position[0]
                        y_accum_per_fixation += gaze_position[1]
                        lines_per_fixation += 1
                        #last_position = gaze_position
                        print_current_data("[In Fixation]", gaze_position, lines_per_fixation)
                        # print "Fixations AOI2 NO AVG:", fixations_in_aoi2
                        # print "Fixations AOI2 AVG:", FIXATIONS_IN_AOI2_AVG
                        # print "TOTAL FIXATIONS:", total_fixations
        #TODO: ACTIVAR PARA VERIFICAR FIJACIONES EN AOI2
        #print "FIXATION IN AOI2:", FIXATIONS_IN_AOI2_AVG

def main():
    current_dir = os.getcwd()
    print "Current directory: " + str(current_dir)
    for filename in os.listdir(current_dir):
        if ".txt" in filename:
            print str(filename) + " Cannot be process"
        if ".csv" in filename:
            print "Opening: " + filename
            process_file(filename)
            print "Finish processing: " + filename
            print "\n"
        else:
            print str(filename) + " Cannot be process"
    print "Ending"


if __name__ == "__main__":
    main()



# TODO: NO FUNCIONA CON PROMEDIOS, ARROJA 886 REGISTROS
# calculate_avg(filename, lines_per_fixation, x_accum_per_fixation, y_accum_per_fixation)
# TODO: CON POSICIONES FINALES, ARROJA 179 REGISTROS
# if is_fixation_belongs_to_aoi2(end_position[0], end_position[1]):
#    fixations_in_aoi2 += 1
# TODO: CON POSICIONES INICIALES, ARROJA 181 REGISTROS
# if is_fixation_belongs_to_aoi2(start_position[0], start_position[1]):
#    fixations_in_aoi2 += 1
