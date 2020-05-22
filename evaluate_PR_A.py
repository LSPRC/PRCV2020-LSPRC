#########################################
# Brief  : evaluate the results of PR-A
# Version: 0.1
# Author : CRIPAC
#########################################
import os
import sys
import numpy as np

from utils.file_operation import *
from utils.evaluate_attribute_classification import evaluate_attribute_classification
from utils.evaluate_attribute_retrieval_ap import evaluate_attribute_retrieval_ap

def loadTxt2NpArray(filename, delimiter=',', skip_rows=0, dtype=float):
    def iterFunc():
        with open(filename, 'r') as infile:
            for _ in range(skip_rows):
                next(infile)
            for line in infile:
                line = line.rstrip().split(delimiter)
                for item in line:
                    yield dtype(item)
        loadTxt2NpArray.rowlength = len(line)

    data = np.fromiter(iterFunc(), dtype=dtype)
    data = data.reshape((-1, loadTxt2NpArray.rowlength))
    return data.astype(dtype)

def loadAttrRecognitionRes(filename, has_header=False, threshold=0.5):
    if has_header:
        raw_data = loadTxt2NpArray(filename, skip_rows=1)
    else:
        raw_data = loadTxt2NpArray(filename)
    attr_res = raw_data[:, 1:]
    attr_res[ attr_res > threshold ] = 1
    attr_res[ attr_res <= threshold ] = -1
    return attr_res

def loadQueryRes(filename, has_header=False):
    if has_header:
        raw_data = loadTxt2NpArray(filename, skip_rows=1)
    else:
        raw_data = loadTxt2NpArray(filename)
    query_res = raw_data[:, 2::2]
    # We asume that the query result meets the format rules.
    image_index = raw_data[:, 1::2]
    #image_index = raw_data[:, 1::2] - 1
    image_index = image_index.astype(int)
    return query_res, image_index

def loadAttrGt(filename):
    raw_data = loadTxt2NpArray(filename, dtype=int)
    attr_data_gt = raw_data[:,1:]
    return attr_data_gt

def generateQueryGt(query_filename, attr_gt):
    query_list = []
    with open(query_filename, 'r') as infile:
        for line in infile:
            line = line.rstrip().split(' ')
            temp = []
            for item in line:
                temp.append(int(item))
            query_list.append(temp)
    query_gt_cols = attr_gt.shape[0]
    query_gt = np.empty((0,query_gt_cols), int)
    for query in query_list:
        attrs_num = len(query)
        query_gt_data_cols = attr_gt[:, query]
        query_gt_data = np.sum(query_gt_data_cols, axis=1)
        query_gt_data[ query_gt_data!=attrs_num ] = 0
        query_gt_data[ query_gt_data==attrs_num ] = 1
        query_gt_data = query_gt_data.reshape((1, query_gt_cols))
        query_gt = np.append(query_gt, query_gt_data, axis=0)
    return query_gt

def evalAttrRecognitionRes(attr_res, attr_gt):
    eval_res = evaluate_attribute_classification(attr_gt, attr_res)
    return eval_res

def evalQueryRes(query_res, image_index, query_gt):
    cnt = 0
    aps = []
    images_num = query_gt.shape[1]
    for scores in query_res:
       ap = evaluate_attribute_retrieval_ap(scores.reshape((1, images_num)), \
           query_gt[cnt,:].reshape((1, images_num)), \
           image_index[cnt, :])
       aps.append(ap)
       cnt = cnt + 1
       print('%d: %f' % (cnt, ap))
       #break
    mAP1 = sum(aps[0:55]) / float(len(aps[0:55]))
    mAP2 = sum(aps[55:97]) / float(len(aps[55:97]))
    mAP3 = sum(aps[97:181]) / float(len(aps[97:181]))
    mAP4 = sum(aps[181:]) / float(len(aps[181:]))
    print(mAP1, mAP2, mAP3, mAP4, (mAP1+mAP2+mAP3+mAP4)/4.0)
    mAP = sum(aps)/float(len(aps))
    return mAP

def test():
    # Modify the followings to the real filenames.
    attr_gt_filename = "data/Attr_testdata_info.txt"
    query_filename = "data/attr_query_index.txt"
    query_res_filename = "../../outputs/query_res_DL_zhike.csv"
    # Load attr ground truth
    attr_gt = loadAttrGt(attr_gt_filename)
    # Generate query ground truth
    query_gt = generateQueryGt(query_filename, attr_gt)
    # Load query results
    query_res, image_idx = loadQueryRes(query_res_filename)
    print(image_idx)
    # mAP
    mAP = evalQueryRes(query_res, image_idx, query_gt)
    print mAP

if __name__=='__main__':
    test()
