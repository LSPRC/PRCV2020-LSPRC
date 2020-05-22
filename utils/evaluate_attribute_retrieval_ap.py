import numpy as np

def evaluate_attribute_retrieval_ap(scores, groundtruth):
    """
    scores:
        ndarray with shape [1,N], multiple attribute similarity scores
    groundtruth:
        ndarray with shape [1,N], binary groundtruth flag, ranging in 0,1
    """
    assert type(scores) == np.ndarray 
    assert type(groundtruth) == np.ndarray
    assert scores.shape[0] == 1 and len(scores.shape) == 2
    assert groundtruth.shape[0] == 1 and len(scores.shape) == 2

    index = np.argsort(scores[0,:])[::-1]
    gt_sort = groundtruth[0,index]
    gt_position = np.argwhere(gt_sort == 1)[:,0]
    ap = 0.0
    ngood = np.sum(groundtruth)
    for cnt, pos in enumerate(gt_position):
        ap = ap + (cnt+1.0)/(pos+1.0)
    ap = ap/ngood
    return ap

def test_evaluate_attribute_retrieval_ap():
    scores = np.random.rand(1,5)
    groundtruth = np.random.randint(1,10,5).reshape(1,5)%2
    ap = evaluate_attribute_retrieval_ap(scores, groundtruth)
    print scores, groundtruth, ap

if __name__ == "__main__":
    test_evaluate_attribute_retrieval_ap()
