import numpy as np

def evaluate_attribute_classification(gt_result, pt_result):
    """
    Input:
        gt_result: ndarray with shape N*L, value of positive is 1 and other are -1
        pt_result: ndarray with shape N*L, value in positive is 1 and other are -1
        N is the number of samples while L is the number of attributes
    Output:
        result: a dictionary which contains instance-based and label-based evaluation
            result['label_pos_acc']: recall of each attribute on positive samples 
            result['label_neg_acc']: recall of each attribute on negative samples
            result['label_acc']: mean accuracy of each attribute

            result['instance_acc']: accuracy of instance-based evaluation
            result['instance_precision']:  precision of instance-based evaluation
            result['instance_recall']: recall of instance-based evaluation
            result['instance_F1']: F1 of instance-based evaluation
    """
    # compute the label-based accuracy
    assert type(gt_result) == np.ndarray 
    assert type(pt_result) == np.ndarray
    if gt_result.shape != pt_result.shape:
        print 'Shape beteen groundtruth and predicted results are different'
    # compute the label-based accuracy
    result = {}
    gt_pos = np.sum((gt_result == 1).astype(float), axis=0)
    gt_neg = np.sum((gt_result == -1).astype(float), axis=0)
    pt_pos = np.sum((gt_result == 1).astype(float) * (pt_result == 1).astype(float), axis=0)
    pt_neg = np.sum((gt_result == -1).astype(float) * (pt_result == -1).astype(float), axis=0)
    label_pos_acc = 1.0*pt_pos/gt_pos
    label_neg_acc = 1.0*pt_neg/gt_neg
    label_acc = (label_pos_acc + label_neg_acc)/2.0
    result['label_pos_acc'] = label_pos_acc
    result['label_neg_acc'] = label_neg_acc
    result['label_acc'] = label_acc
    # compute the instance-based accuracy
    # precision
    gt_pos = np.sum((gt_result == 1).astype(float), axis=1)
    pt_pos = np.sum((pt_result == 1).astype(float), axis=1)
    floatersect_pos = np.sum((gt_result == 1).astype(float)*(pt_result == 1).astype(float), axis=1)
    union_pos = np.sum(((gt_result == 1)+(pt_result == 1)).astype(float),axis=1)
    # avoid empty label in predicted results
    cnt_eff = float(gt_result.shape[0])
    for iter, key in enumerate(gt_pos):
        if key == 0:
            union_pos[iter] = 1
            pt_pos[iter] = 1
            gt_pos[iter] = 1
            cnt_eff = cnt_eff - 1
            continue
        if pt_pos[iter] == 0:
            pt_pos[iter] = 1
    instance_acc = np.sum(floatersect_pos/union_pos)/cnt_eff
    instance_precision = np.sum(floatersect_pos/pt_pos)/cnt_eff
    instance_recall = np.sum(floatersect_pos/gt_pos)/cnt_eff
    floatance_F1 = 2*instance_precision*instance_recall/(instance_precision+instance_recall)
    result['instance_acc'] = instance_acc
    result['instance_precision'] = instance_precision
    result['instance_recall'] = instance_recall
    result['instance_F1'] = floatance_F1
    return result

def test_evaluate_attribute_classification():
    gt_result = np.random.random((100, 35))
    pt_result = np.random.random((100, 35))
    gt_result[gt_result >= 0.5] = 1
    gt_result[gt_result < 0.5] = -1
    pt_result[pt_result >= 0.5] = 1
    pt_result[pt_result < 0.5] = -1
    result = evaluate_attribute_classification(gt_result, pt_result) 
    print "label-based metric:\n mA: %.4f" % (np.mean(result['label_acc']))
    print "instance-based metric: \n"
    print "acc: %.4f, prec: %.4f, rec: %.4f, F1: %.4f"%(
        result['instance_acc'], result['instance_precision'], 
        result['instance_recall'], result['instance_F1'])

if __name__ == "__main__":
    test_evaluate_attribute_classification()

