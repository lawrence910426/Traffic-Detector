# YOLOv5 by Ultralytics, GPL-3.0 license
"""
Run inference on images, videos, directories, streams, etc.

Usage:
    $ python path/to/detect.py --source path/to/img.jpg --weights yolov5s.pt --img 640
"""

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.backends.cudnn as cudnn
import cv2

FILE = Path(__file__).absolute()
sys.path.append(FILE.parents[0].as_posix())  # add yolov5/ to path

from .models.experimental import attempt_load
from .utils.general import check_img_size, non_max_suppression, xyxy2xywh, scale_coords
from .utils.torch_utils import select_device
from .utils.augmentations import letterbox

class YOLOv5(object):
    def __init__(self, weights='detector/YOLOv5/weight/best.pt',  # model.pt path(s)
            imgsz=[640, 640],  # inference size (pixels)
            conf_thres=0.25,  # confidence threshold
            iou_thres=0.45,  # NMS IOU threshold
            max_det=1000,  # maximum detections per image
            device='cuda:0',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
            classes=None,  # filter by class: --class 0, or --class 0 2 3
            agnostic_nms=False,  # class-agnostic NMS
            augment=False,  # augmented inference
            visualize=False,  # visualize features
            half=False,  # use FP16 half-precision inference
        ):
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.max_det = max_det
        self.device = device
        self.half = half
        self.augment = augment
        self.visualize = visualize
        self.classes = classes
        self.agnostic_nms = agnostic_nms
        self.imgsz = imgsz
        self.auto = True

        # Initialize
        device = select_device(device)
        half &= device.type != 'cpu'  # half precision only supported on CUDA

        # Load model

        model = attempt_load(weights, map_location=device)  # load FP32 model
        self.stride = int(model.stride.max())  # model stride
        self.names = model.module.names if hasattr(model, 'module') else model.names  # get class names

        if half:
            model.half()  # to FP16

        imgsz = check_img_size(imgsz, s=stride)  # check image size

        if device.type != 'cpu':
            model(torch.zeros(1, 3, *imgsz).to(device).type_as(next(model.parameters())))  # run once

        self.model = model
        
    @torch.no_grad()
    def __call__(self, ori_img):
        img = ori_img.copy()

        # Convert
        img = letterbox(img, self.imgsz, stride=self.stride, auto=self.auto)[0]
        img = img.transpose((2, 0, 1))  # HWC to CHW
        img = np.ascontiguousarray(img)

        img = torch.from_numpy(img).to(self.device)
        img = img.half() if self.half else img.float()  # uint8 to fp16/32
        img = img / 255.0  # 0 - 255 to 0.0 - 1.0
        if len(img.shape) == 3:
            img = img[None]  # expand for batch dim

        # Inference
        pred = self.model(img, augment=self.augment, visualize=self.visualize)[0]

        # NMS
        pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, self.classes, self.agnostic_nms, max_det=self.max_det)
        det = pred[0]
        det[:, :4] = scale_coords(img.shape[2:], det[:, :4], ori_img.shape).round()

        # Process predictions
        size, i = len(det), 0
        _xywh, _conf, _cls = np.zeros((size, 4)), np.zeros((size)), np.zeros((size))
        for *xyxy, conf, cls in det:
            xywh = xyxy2xywh(torch.tensor(xyxy).view(1, 4)).view(-1).tolist()
            xywh = list(map(int, xywh))
            xywh[2], xywh[3] = max(1, xywh[2]), max(1, xywh[3])
            _xywh[i], _conf[i], _cls[i] = xywh, conf, cls
            i += 1
        return _xywh, _conf, _cls

if __name__ == 'main':
    model = YOLOv5()
    img = cv2.imread('test_images/imtest1.jpeg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    xywh, conf, cls = model(img)
    print(xywh, conf, cls)