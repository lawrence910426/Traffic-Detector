import warnings
import os
import cv2
import time
import torch
import numpy as np
import sys
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), 'thirdparty/fast-reid'))


from detector import build_detector
from deep_sort import build_tracker
from utils.draw import draw_boxes, draw_flow, draw_detector
from utils.log import get_logger
from utils.progress import Progress_Divider
from utils.loop_exception import LoopException
from stabilization.stabilizer import Stabilizer
from counter import *

class TrafficCounter(object):
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
            # 0: 'person',
            1: 'bicycle',
            2: 'car',
            3: 'motorbike',
            5: 'bus',
            7: 'truck'
        }
        self.mcu_weight = {
            # 0: 0, # Person
            1: 1, # Bicycle
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

        self.build_info()

    def build_info(self):
        assert os.path.isfile(self.video_path), "Path error"
        self.vdo = cv2.VideoCapture(self.video_path)
        self.im_width = int(self.vdo.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.im_height = int(self.vdo.get(cv2.CAP_PROP_FRAME_HEIGHT))
        assert self.vdo.isOpened()

        if self.args.save_path:
            os.makedirs(self.args.save_path, exist_ok=True)

            # path of saved video and results
            self.save_video_path = os.path.join(self.args.save_path, self.args.output_name + ".mp4")
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
        
        self.logger.info(
            "Detection line arguments " +
            str(self.args.detector_line_a) + " " +
            str(self.args.detector_line_b) + " " +
            str(self.args.detector_line_x) + " " +
            str(self.args.detector_line_y) + " " +
            str(self.args.detector_line_t) + " " +
            str(self.args.mode)
        )
        self.detect_a = Line(*self.args.detector_line_a.split(","), True)
        self.detect_b = Line(*self.args.detector_line_b.split(","), True)
        self.detect_x = Line(*self.args.detector_line_x.split(","), True)
        self.detect_y = Line(*self.args.detector_line_y.split(","), True)
        self.detect_t = Line(*self.args.detector_line_t.split(","), True)
        return self

    def init_loop(self):
        start_frame = self.args.start_frame
        end_frame = self.args.end_frame
        n_frames = int(self.vdo.get(cv2.CAP_PROP_FRAME_COUNT))

        start_frame = max(0, min(n_frames, start_frame))
        end_frame = n_frames if end_frame == -1 else end_frame
        end_frame = max(0, min(n_frames, end_frame))
        start_buffer_frame = max(0, min(n_frames, start_frame - 300))

        self.logger.info(
            "Start buffer frame: " + str(start_buffer_frame) + ", " + \
            "Start frame: " + str(start_frame) + ", " \
            "End frame: " + str(end_frame))

        self.start_frame, self.start_buffer_frame, self.end_frame = \
            start_frame, start_buffer_frame, end_frame
        self.args.start_frame, self.args.start_buffer_frame, self.args.end_frame = \
            start_frame, start_buffer_frame, end_frame

        # Initialize loop flags
        self.loop_state = "INIT"

        # initialize detection line & counters
        self.detection_counter = {}
        for enabled_cls_id in self.enabled_classes:
            if self.args.mode == "straight":
                self.detection_counter[enabled_cls_id] = StraightCounter(
                    self.logger, self.detect_x, self.detect_y, self.detect_z
                )
            if self.args.mode == "t_intersection":
                self.detection_counter[enabled_cls_id] = TCounter(
                    self.logger, self.detect_a, self.detect_b, self.detect_t
                )
            if self.args.mode == "cross_intersection":
                self.detection_counter[enabled_cls_id] = CrossCounter(
                    self.logger, self.detect_a, self.detect_b, self.detect_x, self.detect_y
                )
        
        self.width = int(self.vdo.get(cv2.CAP_PROP_FRAME_WIDTH)) 
        self.height = int(self.vdo.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    def finalize_loop(self):
        flow = {}
        for k in self.enabled_classes:
            cls_name = self.enabled_classes[k]
            flow[cls_name] = self.detection_counter[k].getFlow()
        
        log = f"Flow: {flow}"
        self.logger.info(log)
        self.yield_logger.write(log + '\n')
        self.yield_logger.flush()
        return flow
    
    def draw_mode_detector(self, img):
        if self.args.mode == "straight":
            img = draw_detector(img, self.detect_x, (0, 0, 255))
            img = draw_detector(img, self.detect_y, (0, 255, 0))
        if self.args.mode == "t_intersection":
            img = draw_detector(img, self.detect_a, (255, 0, 0))
            img = draw_detector(img, self.detect_b, (0, 255, 0))
            img = draw_detector(img, self.detect_t, (0, 0, 255))
        if self.args.mode == "cross_intersection":
            img = draw_detector(img, self.detect_a, (255, 0, 0))
            img = draw_detector(img, self.detect_b, (0, 255, 0))
            img = draw_detector(img, self.detect_x, (0, 0, 255))
            img = draw_detector(img, self.detect_y, (0, 127, 255))
        return img

    def loop(self):
        if self.loop_state == "INIT":
            self.stable_fixer = Stabilizer(
                self.args, Progress_Divider(0, 0.1), self.logger)
            self.stable_fixer.init_loop(self.vdo)
            self.loop_state = "STABILIZE"
            return 0 # Progress = 0%

        elif self.loop_state == "STABILIZE":
            try:
                progress = self.stable_fixer.loop()
                return progress
            except LoopException as e:
                self.loop_state = "DETECT"
                self.detection_progress = Progress_Divider(0.1, 0.99)
                self.fixed_transform = self.stable_fixer.finalize_loop()
                
                self.vdo.set(cv2.CAP_PROP_POS_FRAMES, self.start_buffer_frame)
                self.idx_frame = self.start_buffer_frame
                return 0.1 # Progress = 10%

        elif self.loop_state == "DETECT":
            progress = self.detection_progress.get_progress(
                (self.idx_frame - self.start_buffer_frame) / 
                (self.end_frame - self.start_buffer_frame))
            
            if self.idx_frame % self.args.frame_interval:
                self.idx_frame += 1
                return progress

            start = time.time()

            # fetch image
            succ, ori_im = self.vdo.read()
            if not succ or self.idx_frame >= self.end_frame:
                raise LoopException

            # fix image. stabilize then foreground masking
            fixed_im = self.stable_fixer.fix_frame(
                ori_im, self.fixed_transform[self.idx_frame - self.start_buffer_frame], 
                self.width, self.height)
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
                        if self.start_frame <= self.idx_frame and self.idx_frame < self.end_frame:
                            self.detection_counter[k].update(bb_id, Box(*bb_xyxy))

                    fg_im = draw_boxes(fg_im, bbox_xyxy, identities)
            
            # Sum up the MCU and draw the statistics
            mcu_counter = MCU()
            detector_flow = {}
            for k in self.detection_counter:
                key = self.enabled_classes[k]
                detector_flow[key] = self.detection_counter[k].getFlow()
                mcu_counter.increment_mcu(
                    detector_flow[key], 
                    self.mcu_weight[k]
                )
            if self.args.mode == "straight":
                fg_im = draw_flow(fg_im, detector_flow)
            else:
                fg_im = draw_flow(fg_im, mcu_counter.get_mcu())
            fg_im = self.draw_mode_detector(fg_im)

            end = time.time()

            if self.args.save_path:
                self.writer.write(fg_im)

            # logging
            log = f"time: {end - start}s, " + \
                  f"fps: {1 / (end - start)}, " + \
                  f"detection numbers: {bbox_xywh.shape[0]}, " + \
                  f"tracking numbers: {len(outputs)}, " + \
                  f"progress: {str(int(progress * 100))}"
            
            self.logger.info(log)
            self.yield_logger.write(log + '\n')
            self.yield_logger.flush()

            self.idx_frame += 1
            return progress
