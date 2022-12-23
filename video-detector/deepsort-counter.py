import os
import cv2
import time
import argparse
import torch
import warnings
import numpy as np
import sys
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), 'thirdparty/fast-reid'))


from detector import build_detector
from deep_sort import build_tracker
from utils.draw import draw_boxes, draw_flow, draw_detector
from utils.parser import get_config
from utils.log import get_logger
from utils.io import write_results
from utils.progress import Progress
from stabilization.stabilizer import Stabilizer
from counter import *

class Sharingan(object):
    def __init__(self, cfg, args, video_path):
        self.cfg = cfg
        self.args = args
        self.video_path = video_path
        self.logger = get_logger("root")
        self.logger.setLevel(logging.INFO)
        self.backSub = cv2.createBackgroundSubtractorKNN()

        use_cuda = args.use_cuda and torch.cuda.is_available()
        if not use_cuda:
            self.logger.info("Running in cpu mode might be very slow!")

        if args.display:
            cv2.namedWindow("test", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("test", args.display_width, args.display_height)

        self.enabled_classes = {
            0: 'person',
            1: 'bicycle',
            2: 'car',
            3: 'motorbike',
            5: 'bus',
            7: 'truck'
        }
        self.mcu_weight = {
            0: 0, # Person
            1: 0, # Bicycle
            2: 2, # Car
            3: 1, # Motorbike
            5: 4, # Bus
            7: 4  # Truck
        }
        
        self.detector = build_detector(cfg, use_cuda=use_cuda)
        self.deepsort = {}
        for k in self.enabled_classes:
            self.deepsort[k] = build_tracker(cfg, use_cuda=use_cuda)
        self.class_names = self.detector.class_names


    def __enter__(self):
        assert os.path.isfile(self.video_path), "Path error"
        self.vdo = cv2.VideoCapture(self.video_path)
        self.im_width = int(self.vdo.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.im_height = int(self.vdo.get(cv2.CAP_PROP_FRAME_HEIGHT))
        assert self.vdo.isOpened()

        if self.args.save_path:
            os.makedirs(self.args.save_path, exist_ok=True)

            # path of saved video and results
            self.save_video_path = os.path.join(self.args.save_path, self.args.output_name + ".mp4")
            self.save_results_path = os.path.join(self.args.save_path, self.args.output_name + ".txt")
            self.save_yield_path = os.path.join(self.args.save_path, self.args.output_name + ".out")

            # create video writer
            fourcc = cv2.VideoWriter_fourcc(*'avc1')
            self.writer = cv2.VideoWriter(
                self.save_video_path, fourcc, 
                self.vdo.get(cv2.CAP_PROP_FPS), 
                (self.im_width, self.im_height)
            )

            # logging
            self.logger.info("Save results to {}".format(self.args.save_path))
            self.yield_logger = open(self.save_yield_path, "w+")

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.yield_logger.close()
        if exc_type:
            self.logger.info(exc_type, exc_value, exc_traceback)

    def draw_detector(self, img):
        if self.args.mode == "straight":
            img = draw_detector(img, Line(*self.args.detector_line.split(",")), (255, 255, 255))
        if self.args.mode == "t_intersection":
            img = draw_detector(img, Line(*self.args.detector_line_a.split(",")), (0, 0, 255))
            img = draw_detector(img, Line(*self.args.detector_line_b.split(",")), (0, 255, 0))
            img = draw_detector(img, Line(*self.args.detector_line_t.split(",")), (255, 0, 0))
        if self.args.mode == "cross_intersection":
            img = draw_detector(img, Line(*self.args.detector_line_a.split(",")), (0, 0, 255))
            img = draw_detector(img, Line(*self.args.detector_line_b.split(",")), (0, 255, 0))
            img = draw_detector(img, Line(*self.args.detector_line_t.split(",")), (255, 0, 0))
            img = draw_detector(img, Line(*self.args.detector_line_t.split(",")), (255, 127, 0))
        return img

    def run(self):
        # calculate the stabilization transform
        stable_fixer = Stabilizer(self.args.stable_period, Progress(0, 10))
        fixed_transform = stable_fixer.get_transform(self.vdo)
        progress = Progress(10, 99)

        # initialize detection line & counters
        detection_counter = {}
        for enabled_cls_id in self.enabled_classes:
            if self.args.mode == "straight":
                detection_counter[enabled_cls_id] = Counter(
                    self.vdo.get(cv2.CAP_PROP_FPS),
                    Line(*self.args.detector_line.split(","))
                )
            if self.args.mode == "t_intersection":
                detection_counter[enabled_cls_id] = TCounter(
                    self.vdo.get(cv2.CAP_PROP_FPS),
                    Line(*self.args.detector_line_a.split(",")),
                    Line(*self.args.detector_line_b.split(",")),
                    Line(*self.args.detector_line_t.split(","))
                )
            if self.args.mode == "cross_intersection":
                detection_counter[enabled_cls_id] = CrossCounter(
                    self.vdo.get(cv2.CAP_PROP_FPS),
                    Line(*self.args.detector_line_a.split(",")),
                    Line(*self.args.detector_line_b.split(",")),
                    Line(*self.args.detector_line_x.split(",")),
                    Line(*self.args.detector_line_y.split(","))
                )
        
        width = int(self.vdo.get(cv2.CAP_PROP_FRAME_WIDTH)) 
        height = int(self.vdo.get(cv2.CAP_PROP_FRAME_HEIGHT))

        results = []
        idx_frame = 0
        self.vdo.set(cv2.CAP_PROP_POS_FRAMES, 0)
        while self.vdo.grab():
            idx_frame += 1
            if idx_frame % self.args.frame_interval:
                continue
            if idx_frame >= len(fixed_transform):
                break

            start = time.time()

            # fetch image
            _, ori_im = self.vdo.retrieve()

            # fix image. stabilize then foreground masking
            fixed_im = stable_fixer.fix_frame(ori_im, fixed_transform[idx_frame], width, height)
            fg_im = fixed_im
            
            # convert to rgb
            fg_im_rgb = cv2.cvtColor(fg_im, cv2.COLOR_BGR2RGB)

            # do detection
            bbox_xywh, cls_conf, cls_ids = self.detector(fg_im_rgb)

            # enumerate traffic class
            for k in self.enabled_classes:
                mask = cls_ids == k
                
                # do tracking
                outputs = self.deepsort[k].update(
                    bbox_xywh[mask], 
                    cls_conf[mask], 
                    fg_im_rgb
                )
                
                # draw boxes for visualization
                if len(outputs) > 0:
                    bbox_tlwh = []
                    bbox_xyxy = outputs[:, :4]
                    identities = outputs[:, -1]
    
                    for i in range(len(outputs)):
                        bb_xyxy, bb_id = bbox_xyxy[i], identities[i]
                        bbox_tlwh.append(self.deepsort[k]._xyxy_to_tlwh(bb_xyxy))
                        detection_counter[k].update(bb_id, Box(*bb_xyxy))
                
                    fg_im = draw_boxes(fg_im, bbox_xyxy, identities)
                    results.append((idx_frame - 1, bbox_tlwh, identities))
            
            # Sum up the MCU and draw the statistics
            mcu_counter = MCU()
            detector_flow = {}
            for k in detection_counter:
                key = self.enabled_classes[k]
                detector_flow[key] = detection_counter[k].getFlow()
                mcu_counter.increment_mcu(
                    detector_flow[key], 
                    self.mcu_weight[k]
                )
            fg_im = draw_flow(fg_im, mcu_counter.get_mcu())


            

            end = time.time()

            if self.args.display:
                cv2.imshow("test", fg_im)
                cv2.waitKey(1)

            if self.args.save_path:
                self.writer.write(fg_im)

            # save results
            write_results(self.save_results_path, results, 'mot')

            # logging
            log = "time: {:.03f}s, fps: {:.03f}, detection numbers: {}, tracking numbers: {}, " \
                .format(end - start, 1 / (end - start), bbox_xywh.shape[0], len(outputs))
            log += progress.get_progress(idx_frame / len(fixed_transform) * 100)
            self.logger.info(log)
            self.yield_logger.write(log + '\n')
            self.yield_logger.flush()

        flow = {}
        for k in self.enabled_classes:
            cls_name = self.enabled_classes[k]
            flow[cls_name] = detection_counter[k].getFlow()
        flow = str(flow)
        
        log = f"Flow: {flow}, " + Progress(99, 100).get_progress(100)
        self.logger.info(log)
        self.yield_logger.write(log + '\n')
        self.yield_logger.flush()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("VIDEO_PATH", type=str)
    parser.add_argument("--config_mmdetection", type=str, default="./configs/mmdet.yaml")
    parser.add_argument("--config_detection", type=str, default="./configs/yolov3.yaml")
    parser.add_argument("--config_deepsort", type=str, default="./configs/deep_sort.yaml")
    parser.add_argument("--config_fastreid", type=str, default="./configs/fastreid.yaml")
    parser.add_argument("--fastreid", action="store_true")
    parser.add_argument("--mmdet", action="store_true")
    parser.add_argument("--display", action="store_true")
    parser.add_argument("--frame_interval", type=int, default=1)
    parser.add_argument("--display_width", type=int, default=800)
    parser.add_argument("--display_height", type=int, default=600)
    parser.add_argument("--save_path", type=str, default="./output/")
    parser.add_argument("--cpu", dest="use_cuda", action="store_false", default=True)

    # Traffic specific parameters
    parser.add_argument("--mode", type=str, choices=[
        "straight", "t_intersection", "cross_intersection"], default='straight')
    
    # Straight road
    parser.add_argument("--detector_line", type=str, default='0,0,1000,1000')

    # T intersection
    parser.add_argument("--detector_line_t", type=str, default='0,0,1000,1000')
    parser.add_argument("--detector_line_a", type=str, default='0,0,1000,1000')
    parser.add_argument("--detector_line_b", type=str, default='0,0,1000,1000')

    # Cross intersection (a and b were declared. only x and y needs to be declared.)
    parser.add_argument("--detector_line_x", type=str, default='0,0,1000,1000')
    parser.add_argument("--detector_line_y", type=str, default='0,0,1000,1000')

    parser.add_argument("--stable_period", type=int, default=1000)
    parser.add_argument("--output_name", type=str, default='results')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    cfg = get_config()
    if args.mmdet:
        cfg.merge_from_file(args.config_mmdetection)
        cfg.USE_MMDET = True
    else:
        cfg.merge_from_file(args.config_detection)
        cfg.USE_MMDET = False
    cfg.merge_from_file(args.config_deepsort)
    if args.fastreid:
        cfg.merge_from_file(args.config_fastreid)
        cfg.USE_FASTREID = True
    else:
        cfg.USE_FASTREID = False

    with Sharingan(cfg, args, video_path=args.VIDEO_PATH) as vdo_trk:
        vdo_trk.run()
