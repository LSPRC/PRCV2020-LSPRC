# File operations
# da.li
# v0.1 on 2018/03/09

import os
import csv
import scipy.io

def loadCSV(filename):
    is_existed = os.path.exists(filename)
    assert is_existed == True
    
    data = []
    with open(filename) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        #headers = csv_reader.fieldnames
        for line in csv_reader:
            data.append(line)
        #print csv_reader
    return data

def saveCSV(filename, data):
    assert filename is not None
    assert data is not None
    is_csv = filename.find('.csv')
    assert is_csv > 0

    titles = []
    for key, value in data[0].items():
        titles.append(key)
    with open(filename, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=titles)
        csv_writer.writeheader()
        csv_writer.writerows(data)
    return

def loadMat(filename):
    is_existed = os.path.exists(filename)
    assert is_existed == True

    mat = scipy.io.loadmat(filename)

    return mat

def loadTxt(filename):
    is_existed = os.path.exists(filename)
    assert is_existed == True

    res = []
    fp = open(filename)
    for line in fp:
        res.append(line.strip('\n'))
    fp.close()
    return res

def saveTxt(filename, data):
    with open(filename, 'w') as f:
        for item in data:
            f.write("%s\n" % item)
    return
