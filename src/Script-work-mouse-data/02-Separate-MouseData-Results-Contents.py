import csv

def writeToCSVResultados(row):
    filenameCSV="resultados.txt"
    with open(filenameCSV, 'ab') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=' ')
        csvWriter.writerow(row)

def writeToCSVContenidos(row):
    filenameCSV="contenidos.txt"
    with open(filenameCSV, 'ab') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=' ')
        csvWriter.writerow(row)

def writeResultados(matrixValues):
    print "Write to resultados.txt"
    CSVfilename = "Tr.txt" # Archivo logs
    with open(CSVfilename, 'rb') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=' ')
        for listValues in matrixValues:
            #print listValues #DEBUG
            idUser = int(listValues[0])
            startTime = float(listValues[1])
            endTime = float(listValues[2])
            for row in readCSV:
                if (idUser == int(row[1])
                    and startTime <= float(row[2])
                    and endTime >= float(row[2])):
                    writeToCSVResultados(row)
            csvfile.seek(0)

def writeContenidos(matrixValues):
    print "Write to contenidos.txt"
    CSVfilename = "Tr.txt" # Archivo logs
    with open(CSVfilename, 'rb') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=' ')
        for listValues in matrixValues:
            print listValues
            idUser = int(listValues[0])
            startTime = float(listValues[1])
            endTime = float(listValues[2])
            # in Tr - Vs.txt
            # 0: type, 1: userID, 2: TS
            # if len(linea) = 4: 3: statusmouse
            # else if len(linea) = 5  3:x 4:y
            for row in readCSV:
                 if (idUser == int(row[1]) and not
                     (startTime <= float(row[2]) and
                      endTime >= float(row[2]))):
                    writeToCSVContenidos(row)
            csvfile.seek(0)

def writeMatrixPermanency():
    CSVfilename = "in.csv" # Archivo permanencia: in.csv
    with open(CSVfilename, 'rb') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        # row[0]: User ID
        # row[1]: Session ID
        # row[2]: Start timestamp
        # row[3]: End timestamp
        #AHORANO 0: tipo  1: userID, 2: TS  3: X   4: Y
        # archivo in: 0: user ID, 1: start TS, 2: end TS
        matrixValues = list(readCSV)
    return matrixValues

def main():
    matrixValues = writeMatrixPermanency()
    #ComparateWithLogFile(matrixValues)
    writeResultados(matrixValues)
    writeContenidos(matrixValues)

if __name__ == '__main__':
    main()
    
