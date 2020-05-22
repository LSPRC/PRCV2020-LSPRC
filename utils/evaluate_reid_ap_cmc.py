import numpy as np

def evaluate_reid_ap_cmc(query_pid, query_cam, gallery_pids, gallery_cams, seperate_cam=False):
    """
    Input: 
        query_pid: scalar value 
        query_cam: scalar value
        gallery_pids: a 1xN ndarray
        gallery_cams: a 1xN ndarray
        seperate_cam: bool value, represent whether to use cross camera test or not
            when it is set as False, the different identities in the same camera of 
            the query id are also used as effective samples in the gallery set. This 
            could enlarge the gallery set and  the ap will decrease.
    Output:
        return a ap scalar and a cmc ndarray with shape 1*N 
    """
    assert type(gallery_pids) == np.ndarray
    assert type(gallery_cams) == np.ndarray
    assert gallery_pids.shape[0] == 1 and len(gallery_pids.shape) == 2
    assert gallery_cams.shape[0] == 1 and len(gallery_cams.shape) == 2

    cmc = np.zeros(gallery_pids.shape)
    ngood = np.sum((query_pid == gallery_pids) & (query_cam != gallery_cams))
    ap = 0.0
    good_now = 1.0
    current_rank = 1
    first_flag = 0
    for n, (p, c) in enumerate(zip(gallery_pids[0, :], gallery_cams[0, :])):
        if good_now == ngood + 1:
            break
        # handle junk images
        if seperate_cam:
            junk = c == query_cam
        else:
            junk = p == query_pid and c == query_cam
        if junk:
            continue
        # compute the ap and cmc 
        if p == query_pid and c != query_cam:
            # compute the average precision
            ap = ap + good_now/current_rank
            # compute the cmc curve 
            if first_flag == 0:
                cmc[0, current_rank-1:] = 1
                first_flag = 1
            good_now = good_now + 1
        current_rank = current_rank + 1
    ap = ap/ngood
    return ap, cmc

def test_evaluate_reid_ap_cmc():
    query_pid = np.random.randint(1, 5, 1)[0]
    query_cam = np.random.randint(1, 5, 1)[0]
    gallery_pids = np.random.randint(1, 5, 10).reshape(1,10)
    gallery_cams = np.random.randint(1, 5, 10).reshape(1,10)
    print query_pid, query_cam
    print gallery_pids, gallery_cams

    ap, cmc = evaluate_reid_ap_cmc(query_pid, query_cam, gallery_pids, gallery_cams, seperate_cam=False)
    print ap, cmc, ' under seperate_cam=False'
    ap, cmc = evaluate_reid_ap_cmc(query_pid, query_cam, gallery_pids, gallery_cams, seperate_cam=True)
    print ap, cmc, ' under seperate_cam=True'
    pass

if __name__ == "__main__":
    test_evaluate_reid_ap_cmc()
