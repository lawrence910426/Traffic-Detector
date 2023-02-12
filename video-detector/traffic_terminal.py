import argparse
from utils.parser import get_config
from utils.loop_exception import LoopException
from traffic_counter import TrafficCounter

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
    
    parser.add_argument("--detector_line_t", type=str, default='536,1136,558,1884')
    parser.add_argument("--detector_line_a", type=str, default='508,628,629,22')
    parser.add_argument("--detector_line_b", type=str, default='597,1866,1088,1881')
    parser.add_argument("--detector_line_x", type=str, default='0,0,1000,1000')
    parser.add_argument("--detector_line_y", type=str, default='0,0,1000,1000')
    parser.add_argument("--detector_line_z", type=str, default='0,0,1000,1000')

    parser.add_argument("--stable_period", type=int, default=1000)
    parser.add_argument("--output_name", type=str, default='results')

    parser.add_argument("--start_frame", type=int, default=0)
    parser.add_argument("--end_frame", type=int, default=-1)
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

    args.detector_line_a = args.detector_line_a.split(",")
    args.detector_line_b = args.detector_line_b.split(",")
    args.detector_line_t = args.detector_line_y.split(",")
    args.detector_line_x = args.detector_line_x.split(",")
    args.detector_line_y = args.detector_line_y.split(",")
    args.detector_line_z = args.detector_line_z.split(",")

    vdo_trk = TrafficCounter(cfg, args, video_path=args.VIDEO_PATH)

    vdo_trk.init_loop()
    while True:
        try:
            vdo_trk.loop()
        except LoopException as e:
            break
    print(vdo_trk.finalize_loop())
    
    del vdo_trk
