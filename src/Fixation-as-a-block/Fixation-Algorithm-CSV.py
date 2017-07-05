# -*- coding: cp1252 -*-
import csv
import json
import os
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


max_error = 30
total_samples_per_fixation = 5

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
  avg_x = float((x_accumulated/counter_lines_per_fixation))
  avg_y = float((y_accumulated/counter_lines_per_fixation))
  avg_psize_left = float((left_eye_psize_accumulated/counter_lines_per_fixation))
  avg_psize_right = float((right_eye_psize_accumulated/counter_lines_per_fixation))
  # Only do if AOI 2 - Visual Interface
  if (avg_x >= 1 and avg_x <= 700 and avg_y >= 200 and avg_y <= 800):
    #print "hola"
    line = [start_ts, end_ts, duration, avg_x, avg_y, avg_psize_left, avg_psize_right]
    write_to_file(filename, line)
  #else:
  #  print "No AOI2 Found"
    

def is_deviation_lower_than_maxerror(x1,y1):
  #logger.info("Calculating deviation")
  d1 = max(x1)-min(x1)
  d2 = max(y1)-min(y1)
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
    #logger.info("pythagoras is not greater than maxerror. Still is a fixation")
    return False


def is_full_sample_rate(x1):
  #logger.info("Checking if x1 has the total of fixations")
  if len(x1) == total_samples_per_fixation:
    #logger.info("len(x1) is equal to total_samples")
    return True
  else:
    #logger.info("len(x1) is not equal to total_samples")
    return False


def get_data_from_line(line_csv):
  #logger.info("Get data from new line of the json file")  
  line_data = []
  x = float(line_csv[2])   #line_csv["values"]["frame"]["avg"]["x"]
  y = float(line_csv[3])   #line_csv["values"]["frame"]["avg"]["y"]
  ts = float(line_csv[0])  #line_csv["values"]["frame"]["timestamp"]
  time = float(line_csv[1])  #line_csv["values"]["frame"]["time"]
  left_eye_psize = 0  #line_csv["values"]["frame"]["lefteye"]["psize"]
  right_eye_psize= 0  #line_csv["values"]["frame"]["righteye"]["psize"]
  line_data.append(x)
  line_data.append(y)
  line_data.append(ts)
  line_data.append(time)
  line_data.append(left_eye_psize)
  line_data.append(right_eye_psize)
  return line_data


def processFile(filename):
  x1,y1 = [],[]
  is_eye_moving = True
  #FIX: para poder solucionar el tema del termino de las fijaciones
  start_position,actual_position,end_position, last_position= [],[],[],[]
  start_time,start_ts = 0,0
  end_time,end_ts = 0,0
  aoi = 0
  counter_lines_per_fixation = 0
  x_accumulated,y_accumulated = 0,0
  left_eye_psize_accumulated,right_eye_psize_accumulated = 0,0
  with open(filename, 'rb') as csvfile:
    line_csv = csv.reader(csvfile, delimiter=' ')
    for line in line_csv:
      data = get_data_from_line(line)
      if ((data[0] > 0 and data[0] <= 1920) and (data[1] > 0 and data[1] <= 1080)):
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
              #FIX: para poder solucionar el tema del termino de las fijaciones
              last_position = start_position
              if (x1[-1] >= 1 and x1[-1] <= 700 and y1[-1] >= 200 and y1[-1] <= 800):
                print "[Fixation START] at:", start_position    #, start_ts, start_time
                aoi += 1
            else:
              x1.pop(0); y1.pop(0)
        else:
          logger.info("Im in a fixation")
          counter_lines_per_fixation += 1
          x_accumulated += data[0]
          y_accumulated += data[1]
          left_eye_psize_accumulated += data[4]
          right_eye_psize_accumulated += data[5]
          #FIX: para poder solucionar el tema del termino de las fijaciones
          #last_position = [data[0],data[1]]

          #Now, check is ending a fixation
          #print "fixation point at:", actual_position   #, data[2], data[3]
          if is_pythagoras_greater_than_maxerror(start_position, actual_position):
            #FIX: para poder solucionar el tema del termino de las fijaciones
            end_position = actual_position
            #end_position = last_position
            end_ts = data[2]
            end_time = data[3]
            #logger.info("Ending a fixation")
            print "[Fixation END] at:", end_position   #, end_ts, end_time
            print "lines per fixation:", counter_lines_per_fixation
            # Write to a file
            calculate_avg(filename, counter_lines_per_fixation, start_ts, start_time, end_ts, end_time, x_accumulated, y_accumulated, left_eye_psize_accumulated, right_eye_psize_accumulated)

            # Reset variables
            counter_lines_per_fixation = 0 
            is_eye_moving = True
            x1,y1 = [],[]
            start_time,start_ts = 0,0
            end_time,end_ts = 0,0
            x_accumulated,y_accumulated = 0,0
            #FIX: para poder solucionar el tema del termino de las fijaciones
            start_position,actual_position,end_position, last_position = [],[],[],[]
            
    print "tot_aoi ", aoi

      
def main():
  currentDir = os.getcwd()
  print "Current directory: " + str(currentDir)
  for filename in os.listdir(currentDir):
    if ".txt" in filename:
      print str(filename) + " Cannot be process"
    if ".csv" in filename:
      print "Opening: " + filename
      processFile(filename)
      print "Finish processing: " + filename
      print "\n"
    else:
      print str(filename) + " Cannot be process"
  print "Ending"


if __name__ == "__main__":
  main()
