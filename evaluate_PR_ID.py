#########################################
# Brief  : evaluate the results of PR-ID
# Version: 0.1
# Author : CRIPAC
#########################################
import os
import sys
import numpy as np

from utils.evaluate_reid_ap_cmc import evaluate_reid_ap_cmc
from utils.file_operation import *

def txt2NumpyArray(data_filename):
    f = open(data_filename, 'r')
    raw_data = f.readlines()

    list_data = []
    for idx, items in enumerate(raw_data):
        items = items.strip()
        items = items.split(',')
        items[0] = items[0].split('.')[0]
        items[0] = items[0][-5:]
        list_data.append(items)
    f.close();
    
    np_data = np.asarray(list_data).astype(int)
    return np_data

def loadQueryData(filename):
    f = open(filename, 'r')
    raw_data = f.readlines()
    list_data = []
    for idx, item in enumerate(raw_data):
        item = item.strip()
        item = item.split('.')[0][-5:]
        list_data.append(int(item)-1)
    f.close()
    np_data = np.asarray(list_data).astype(int)
    return np_data

def loadRes(filename, delimiter=',', skip_rows=0, dtype=float):
    def iterFunc():
        with open(filename, 'r') as infile:
            for _ in range(skip_rows):
                next(infile)
            for line in infile:
                line = line.rstrip().split(delimiter)
                for item in line:
                    yield dtype(item)
        loadRes.rowlength = len(line)

    data = np.fromiter(iterFunc(), dtype=dtype)
    data = data.reshape((-1, loadRes.rowlength))
    # Here we asume that the query result meets the format rules
    data = data[:, 1::2]
    return data.astype(int)

def calmAP(probes, gallary_set, res):
    probe_cnt = 0
    ap_list = []
    for line in res:
        probe_idx = probes[probe_cnt]
        probe_pid = gallary_set[probe_idx][2]
        probe_cam = gallary_set[probe_idx][1]
        res_pids = gallary_set[line, 2]
        res_cams = gallary_set[line, 1]
        cols = res_cams.shape[0]
        row = 1
        res_pids = res_pids.reshape((row, cols))
        res_cams = res_cams.reshape((row, cols))
        ap, cmc = evaluate_reid_ap_cmc(probe_pid, probe_cam, res_pids, res_cams)
        ap_list.append(ap)
        probe_cnt = probe_cnt + 1
        print '==== Probe cnt: %d' % probe_cnt
        print '  AP = %f' % ap
    ap_np = np.asarray(ap_list)
    mAP = np.mean(ap_np)
    return mAP

def run(dirname, idx, output_filename):
    # Collect all the folders(groups) under a specific path.
    groups = collectFolders(dirname)
    # Load query data
    queries_filename = 'data/query_test_image_name.txt'
    queries = loadQueryData(queries_filename)
    # Load gallary data
    gallary_filename = 'data/ReID_testdata_info.txt'
    gallary_set = txt2NumpyArray(gallary_filename)
    # Evaludate
    PROBES_NUM_ = 7202
    out_items = []
    for group in groups:
        files_dir = os.path.join(group, 'pr-id', idx)
        files = collectFiles(files_dir)
        for file_dir in files:
            print files_dir
            if 'ali' in file_dir:
                continue
            rows = getRows(file_dir)
            # Results
            if rows == PROBES_NUM_ + 1:
                print 'The file has header.'
                res = loadRes(file_dir, skip_rows=1)
            else:
                print 'The file has no header'
                res = loadRes(file_dir)
            print '====================================='
            mAP = calmAP(queries, gallary_set, res)
            group_nm = group.split('/')[-1]
            file_nm = file_dir.split('/')[-1]
            item = {'group': group_nm, 'file': file_nm, 'mAP': mAP}
            out_items.append(item)
    saveCSV(output_filename, out_items)
    return

def test():
    # Final Test (modify it to the real path storing the query resutl)
    res_filename = '/data1/LSPR/outputs/pr-id/query_result.csv'
    # Filename End (modify the following two filenames to the real path)
    query_filename = 'data/query_test_image_name.txt'
    gallary_filename = 'data/ReID_testdata_info.txt'

    probes = loadQueryData(query_filename)
    gallary_set = txt2NumpyArray(gallary_filename)
    res = loadRes(res_filename)
    mAP = calmAP(probes, gallary_set, res)
    return mAP

if __name__=="__main__":
    mAP = test()
    print "======================"
    print "mAP = %f" % mAP
