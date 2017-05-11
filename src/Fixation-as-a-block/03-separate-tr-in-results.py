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

def writeResultados(INFile):
    print "Write to resultados.txt"
    CSVfilename = "Tr.txt" # Archivo logs
    with open(CSVfilename, 'rb') as csvfile:
        TRFile = csv.reader(csvfile, delimiter=' ')
        for lineIN in INFile:
            idUser = int(lineIN[0])
            startTime = float(lineIN[1])
            endTime = float(lineIN[2])
            for lineTR in TRFile:
                if (idUser == int(lineTR[1])
                    and startTime <= float(lineTR[2])
                    and endTime >= float(lineTR[2])):
                    writeToCSVResultados(lineTR)
            csvfile.seek(0)

def writeContenidos(matrixValues):
    print "Write to contenidos.txt"
    CSVfilename = "Tr.txt" # Archivo logs
    with open(CSVfilename, 'rb') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=' ')
        for listValues in matrixValues:
            print listValues
            idUser = int(listValues[0])
            startTime = float(listValues[1]) #antes row[2], ahora row[1]
            endTime = float(listValues[2])
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
        matrixValues = list(readCSV)
    return matrixValues

def main():
    matrixValues = writeMatrixPermanency()
    writeResultados(matrixValues)

if __name__ == '__main__':
    main()
    
