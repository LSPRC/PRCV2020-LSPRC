# file: load_rap_attributes_data_mat.py
# brief: To use the mat data under python.
# author: CRIPAC
# version: 1.0
import sys
import numpy as np
from utils.file_operation import *

def loadRAPReID(data_filename):
    """
    load mat file under python.
    Note: It's not a general function, but based on the structure of 
    the variable in mat file.

    Input:
        data_filename - the mat file
    Return:
        Rap reid data in a dictionary whose key is the same with
        that in mat file.
    """

    data = loadMat(data_filename)
    char_existed = data_filename.find('/')
    if char_existed == -1:
        root_key = data_filename.split('.')[0]
    else:
        filename = data_filename.split('/')[-1]
        root_key = filename.split('.')[0]
    # Information (image_filename, id, cam_id and day) of training samples.
    training_set = data[root_key][0][0][0]
    # Image filename of test samples.
    test_samples_filename = data[root_key][0][0][1]
    test_set = [ item[0][0] for item in test_samples_filename ]
    test_set = np.asarray(test_set)
    #print(test_set.shape)
    dataset = {'training_set': training_set, \
        'test_set': test_set}
    return dataset

if __name__=='__main__':

    #filename = '/data1/da.li/projects/LSPR/data/ReID/RAP_reid_data.mat'
    filename = '/data1/da.li/projects/LSPR/data/new/RAP_reid_data.mat'
    data = loadRAPReID(filename)
    print(data)
    # Image filename of training samples (to get each item of the filename like
    # this: training_samples_filename[0][0][0], <type 'numpy.unicode'>).
    #training_samples_filename = data[root_key][0][0][2]
    #image_filenames_train = [ item[0][0] for item in training_samples_filename ]
    #image_filenames_train = np.asarray(image_filenames_train)
