from tracker.deep_sort.deep_sort import DeepSort
from tracker.ocsort.ocsort import OCSort

def build_tracker(cfg, use_cuda):
    if cfg.USE_DEEPSORT:
        if cfg.USE_FASTREID:
            return DeepSort(model_path=cfg.FASTREID.CHECKPOINT, model_config=cfg.FASTREID.CFG, 
                    max_dist=cfg.DEEPSORT.MAX_DIST, min_confidence=cfg.DEEPSORT.MIN_CONFIDENCE, 
                    nms_max_overlap=cfg.DEEPSORT.NMS_MAX_OVERLAP, max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE, 
                    max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET, use_cuda=use_cuda)

        else:
            return DeepSort(model_path=cfg.DEEPSORT.REID_CKPT, 
                    max_dist=cfg.DEEPSORT.MAX_DIST, min_confidence=cfg.DEEPSORT.MIN_CONFIDENCE, 
                    nms_max_overlap=cfg.DEEPSORT.NMS_MAX_OVERLAP, max_iou_distance=cfg.DEEPSORT.MAX_IOU_DISTANCE, 
                    max_age=cfg.DEEPSORT.MAX_AGE, n_init=cfg.DEEPSORT.N_INIT, nn_budget=cfg.DEEPSORT.NN_BUDGET, use_cuda=use_cuda)
    if cfg.USE_OCSORT:
        return OCSort(0.3) # According to deep sort
    if cfg.USE_BYTETRACK:
        pass
    









