import csv, re, codecs
import os, glob
from itertools import filterfalse
from itertools import chain

#read in Google Analytics files

masterfile = "../data/all_consolidated.csv"
db1_file = "../original_data/UCD-04 Dbase Report (DB1) Monthly View.csv"
GAdir = "../original_data/historical_data"

#read a CSV file and filter blank lines
def readCSV(fileName):
    with open(fileName, 'r') as f1:
        filt = filterfalse(lambda line: line.startswith('\n'), f1)
        ga_reader = csv.reader(filt)
        row_num = 0
        row_array = []
        for row in ga_reader:
            print(row)

def processDB1(db1_file):
    with open(db1_file, 'r') as f1:
        filt = filterfalse(lambda line: line.startswith('\n'), f1)
        db_reader = csv.reader(filt)
        row_num = 0
        db_set = set() #to hold unique database names
        db_dict = {} #to hold usage data for each db
        # { (db_name, month) => usage }
        headers = next(db_reader, None)
        for row in db_reader:
            db_set.add(row[0])
            db_name = row[0]
            month = row[4]
            searches = row[6]
            #print(db_name, month)
            db_dict[(db_name, month)] = searches
        return db_dict, db_set

#create a column for each database, filling in rows with  searches
def appendDbCol(master, db_dict, db_set):
    with open(master, 'r') as f1, open('../data/DB1_web_combined.csv', 'w') as out_file:
        filt = filterfalse(lambda line: line.startswith('\n'), f1)
        db_reader = csv.reader(filt)
        db_writer = csv.writer(out_file)
        row_num = 0
        headers = next(db_reader, None)
        #add db names to the header
        for db in db_set:
            headers.append(db)
        headers_clean = []
        for h in headers:
            headers_clean.append(h.replace(' ','_'))
        db_writer.writerow(headers_clean)
        for row in db_reader:
            col_num = 0
            for col in headers:
                #print(col, col_num)
                try:
                    row.append(db_dict[col,row[0]])
                except:
                    print("key error")
                    try:
                        row[col_num]
                    except:
                        print("data here")
                        row.append(None)
                    pass
                col_num += 1
            #print(row)
            db_writer.writerow(row)

def processGaFiles(GAdirectory):
    os.chdir(GAdirectory)
    for file in glob.glob("Analytics*"):
        print(file)
        readCSV(file)

#readCSV(masterfile)
#processDB1(db1_file)
#processGaFiles(GAdir)
db_dict,db_set = processDB1(db1_file)
appendDbCol(masterfile, db_dict, db_set)

