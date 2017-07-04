# -*- coding: cp1252 -*-
import csv
import json
import os
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_error = 30
total_samples_per_fixation = 3

def write_to_file(filename, line):
  #logger.info("Writing to a file")
  filename_without_extension = filename.split(".")[0]
  output_filename_csv= filename + ".txt"
  with open(output_filename_csv, 'ab') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=' ')
    csv_writer.writerow(line)


def calculate_avg(filename, counter_lines_per_fixation, start_ts, start_time, end_ts, end_time, x_accumulated, y_accumulated, left_eye_psize_accumulated, right_eye_psize_accumulated):
  #logger.info("Calculate avg")
  duration = end_time - start_time
  avg_x = (x_accumulated/counter_lines_per_fixation)
  avg_y = (y_accumulated/counter_lines_per_fixation)
  avg_psize_left = (left_eye_psize_accumulated/counter_lines_per_fixation)
  avg_psize_right = (right_eye_psize_accumulated/counter_lines_per_fixation)
  # Only do if AOI 2 - Visual Interface
  if (avg_x >= 1 and avg_x <= 700 and avg_y >= 200 and avg_y <= 800):             
    #line = [start_ts, end_ts, duration, avgX, avgY, avgPSizeL, avgPSizeR]
    #line = [startTimeTS, lastTimeTS, duration, avgX, avgY, avgPSizeL, avgPSizeR]
    line = [start_ts, end_ts, duration, avg_x, avg_y, avg_psize_left, avg_psize_right]
    write_to_file(filename, line)
    

def is_deviation_lower_than_maxerror(x1,y1):
  #logger.info("Calculating deviation")
  d1 = max(x1)-min(x1)
  d2 = max(y1)-min(y1)
  #logging.info('%s before you %s', 'Look', 'leap!')
  #logging.info('Los valores son de d1:%s, d2:%s', d1, d2)
  if d1 < max_error and d2 < max_error:
    return True
  else:
    return False


def is_pythagoras_greater_than_maxerror(starting_positions, n_positions):
  #logger.info("Calculating pythagoras")
  if ((starting_positions[0]-n_positions[0])**2  + (starting_positions[1]-n_positions[1])**2)**0.5 > max_error:
    #logger.info("pythagoras is greater than maxerror. Then is the end of fixation")
    return True
  else:
    #logger.info("pythagoras is not greater than maxerror")
    return False


def is_full_sample_rate(x1):
  #logger.info("Checking if x1 has the total of fixations")
  if len(x1) == total_samples_per_fixation:
    #logger.info("len(x1) is equal to total_samples")
    return True
  else:
    #logger.info("len(x1) is not equal to total_samples")
    return False


def get_data_from_line(line_json):
  #logger.info("Get data from new line of the json file")  
  line_data = []
  x = line_json["values"]["frame"]["avg"]["x"]
  y = line_json["values"]["frame"]["avg"]["y"]
  ts = line_json["values"]["frame"]["timestamp"]
  time = line_json["values"]["frame"]["time"]
  left_eye_psize = line_json["values"]["frame"]["lefteye"]["psize"]
  right_eye_psize= line_json["values"]["frame"]["righteye"]["psize"]
  line_data.append(x)
  line_data.append(y)
  line_data.append(ts)
  line_data.append(time)
  line_data.append(left_eye_psize)
  line_data.append(right_eye_psize)
  return line_data


def processFile(filename):
  x1 = []
  y1 = []
  is_eye_moving = True
  start_position = []
  actual_position = []
  end_position = []
  start_time = 0
  start_ts = 0
  end_time = 0
  end_ts = 0
  counter_lines_per_fixation = 0
  x_accumulated = 0
  y_accumulated = 0
  left_eye_psize_accumulated = 0
  right_eye_psize_accumulated = 0
  with open(filename) as file:
    for line in file:
      line_json = json.loads(line)
      if (line_json["category"]== "tracker"):
        data = get_data_from_line(line_json)
        actual_position = [data[0], data[1]]
        if is_eye_moving:
          x1.append(data[0])
          y1.append(data[1])
          if is_full_sample_rate(x1):
            if is_deviation_lower_than_maxerror(x1, y1):
              #logger.info("Starting fixation")
              x_accumulated += data[0]
              y_accumulated += data[1]
              left_eye_psize_accumulated += data[4]
              right_eye_psize_accumulated += data[5]    
              counter_lines_per_fixation += 1
              is_eye_moving = False
              start_position = [x1[-1], y1[-1]]
              start_ts = data[2]
              start_time = data[3]
              #print "[Fixation START] at", start_position, start_ts, start_time 
            else:
              x1.pop(0); y1.pop(0)
        else:
          #logger.info("Im in a fixation")
          counter_lines_per_fixation += 1
          x_accumulated += data[0]
          y_accumulated += data[1]
          left_eye_psize_accumulated += data[4]
          right_eye_psize_accumulated += data[5]
          #Now, check is ending a fixation
          #print "fixation point at", actual_position, data[2], data[3]
          if is_pythagoras_greater_than_maxerror(start_position, actual_position):
            end_position = actual_position
            end_ts = data[2]
            end_time = data[3]
            #logger.info("Ending a fixation")
            #print "[Fixation END] at", end_position, end_ts, end_time
            #print "lines per fixation:", counter_lines_per_fixation
            # Write to a file
            calculate_avg(filename, counter_lines_per_fixation, start_ts, start_time, end_ts, end_time, x_accumulated, y_accumulated, left_eye_psize_accumulated, right_eye_psize_accumulated)

            #TODO GONZALO: Al parecer esta funcionando
            # Reset variables
            counter_lines_per_fixation = 0 
            is_eye_moving = True
            x1 = []
            y1 = []
            start_time = 0
            start_ts = 0
            end_time = 0
            end_ts = 0

        
def main():
  currentDir = os.getcwd()
  print "Current directory: " + str(currentDir)
  for filename in os.listdir(currentDir):
    if ".txt" in filename:
      print str(filename) + " Cannot be process"
    if ".json" in filename:
      print "Opening: " + filename
      processFile(filename)
      print "Finish processing: " + filename
      print "\n"
    else:
      print str(filename) + " Cannot be process"
  print "Ending"


if __name__ == "__main__":
  main()
