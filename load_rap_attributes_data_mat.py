# file: load_rap_attributes_data_mat.py
# brief: To use the mat data under python.
# author: CRIPAC
# version: 1.0
import sys
import numpy as np
from utils.file_operation import *

def loadRAPAttr(data_filename):
    """
    load mat file under python.
    Note: It's not a general function, but based on the structure of 
    the variable in mat file.

    Input:
        data_filename - the mat file
    Return:
        Rap attributes data in a dictionary whose key is the same with
        that in mat file.
    """

    data = loadMat(data_filename)
    char_existed = data_filename.find('/')
    if char_existed == -1:
        root_key = data_filename.split('.')[0]
    else:
        filename = data_filename.split('/')[-1]
        root_key = filename.split('.')[0]

    # Train_Validation and Test sets
    tr_val_sets = data[root_key][0][0][0][0][0]
    test_set_items = data[root_key][0][0][1]
    test_set = np.asarray([ item[0][0] for item in test_set_items ])

    # Variables in Train_Validation
    tr_val_img_filenames_items = tr_val_sets[0]
    tr_val_img_filenames = np.asarray([ item[0][0] for item in \
        tr_val_img_filenames_items])
    attr_data = tr_val_sets[1]
    attr_names_cn_items = tr_val_sets[2]
    attr_names_cn = np.asarray([ item[0][0] for item in attr_names_cn_items ])
    attr_names_en_items = tr_val_sets[3]
    attr_names_en = np.asarray([ item[0][0] for item in attr_names_en_items ])
    partition = tr_val_sets[4]
    selected_attributes = tr_val_sets[5][0] - 1
    # Note that the minus one in selected_attributes as the index start with 0
    # in python but 1 in matlab!!

    # Partitions
    train_index = partition[0][0][0][0]
    val_index = partition[0][0][1][0]
    part = {'train_index': train_index, 'val_index': val_index}

    training_validation_sets = {'image_filenames': tr_val_img_filenames, \
        'attr_data': attr_data, 'attr_names_cn': attr_names_cn, \
        'attr_names_en': attr_names_en, 'partition': part, \
        'selected_attributes': selected_attributes}
    res = {'training_validation_sets': training_validation_sets, \
        'test_set': test_set}
    return res


if __name__=='__main__':

    #filename = \
    #    '/data1/da.li/projects/LSPR/data/Attributes/RAP_attributes_data.mat'
    filename = '/data1/da.li/projects/LSPR/data/new/RAP_attributes_data.mat'
    data = loadRAPAttr(filename)
    print(data)
