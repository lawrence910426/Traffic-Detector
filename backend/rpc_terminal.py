import argparse
from routes.rpc_controller.controller import RpcController
import time

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("VIDEO_PATH", type=str)
    
    # Traffic specific parameters
    parser.add_argument("--mode", type=str, choices=[
        "straight", "t_intersection", "cross_intersection"], default='straight')
    
    parser.add_argument("--detector_line_t", type=str, default='536,1136,558,1884')
    parser.add_argument("--detector_line_a", type=str, default='508,628,629,22')
    parser.add_argument("--detector_line_b", type=str, default='597,1866,1088,1881')
    parser.add_argument("--detector_line_x", type=str, default='0,0,1000,1000')
    parser.add_argument("--detector_line_y", type=str, default='0,0,1000,1000')

    parser.add_argument("--stable_period", type=int, default=1000)
    parser.add_argument("--output_name", type=str, default='this-is-some-uuid')
    return parser.parse_args()

# Wait until the RPC Server is ready.
time.sleep(5)

if __name__ == "__main__":
    args = parse_args()

    mapping = {
        "T": args.detector_line_t,
        "A": args.detector_line_a,
        "B": args.detector_line_b,
        "X": args.detector_line_x,
        "Y": args.detector_line_y
    }
    task_params = {
        "Mode": args.mode,
        "Stabilization_Period": args.stable_period,
        "Input_Video_Path": args.VIDEO_PATH,
        "Output_Video_Path": args.output_name
    }
    for key, value in mapping.items():
        task_params[key] = {
            "x1": value.split(',')[0],
            "y1": value.split(',')[1],
            "x2": value.split(',')[2],
            "y2": value.split(',')[3],
        }

    RpcController.init_task(task_params)
    while True:
        task_info = RpcController.get_task()
        print("[Running] ", task_info["Progress"])
        if task_info["Progress"] == 100:
            print("[Program Complete]", task_info)
            break
