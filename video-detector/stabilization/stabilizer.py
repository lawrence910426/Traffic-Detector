import numpy as np
import cv2

from utils.loop_exception import LoopException

class Stabilizer:
	def __init__(self, args, progress, logger):
		self.smoothing = args.stable_period
		self.start_buffer_frame = args.start_buffer_frame
		self.end_frame = args.end_frame

		self.progress = progress
		self.logger = logger

	def movingAverage(self, curve, radius): 
		window_size = 2 * radius + 1
		# Define the filter 
		f = np.ones(window_size) / window_size 
		# Add padding to the boundaries 
		curve_pad = np.lib.pad(curve, (radius, radius), 'edge') 
		# Apply convolution 
		curve_smoothed = np.convolve(curve_pad, f, mode='same') 
		# Remove padding 
		curve_smoothed = curve_smoothed[radius:-radius]
		# return smoothed curve
		return curve_smoothed 

	def smooth(self, trajectory): 
		smoothed_trajectory = np.copy(trajectory) 
		# Filter the x, y and angle curves
		for i in range(3):
			smoothed_trajectory[:,i] = self.movingAverage(
				trajectory[:,i], 
				radius=self.smoothing
			)
	
		return smoothed_trajectory

	def init_loop(self, cp):
		self.cp = cp
		self.n_frames = int(cp.get(cv2.CAP_PROP_FRAME_COUNT))
		self.index = self.start_buffer_frame

		self.cp.set(cv2.CAP_PROP_POS_FRAMES, self.start_buffer_frame) 
		_, prev = self.cp.read()
		self.prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

		self.transforms = np.zeros((self.end_frame - self.start_buffer_frame, 3), np.float32) 

	def finalize_loop(self):
		trajectory = np.cumsum(self.transforms, axis=0) 
		smoothed_trajectory = self.smooth(trajectory)
		difference = smoothed_trajectory - trajectory
		transforms_smooth = self.transforms + difference
		return transforms_smooth

	def loop(self):
		if self.index >= self.end_frame - 2:
			raise LoopException

		prev_pts = cv2.goodFeaturesToTrack(
			self.prev_gray, 
			maxCorners=200, 
			qualityLevel=0.01, 
			minDistance=30, 
			blockSize=3
		)

		succ, curr = self.cp.read()
		if not succ:
			raise LoopException

		curr_gray = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)
		curr_pts, status, err = cv2.calcOpticalFlowPyrLK(
			self.prev_gray, curr_gray, 
			prev_pts, None
		)

		idx = np.where(status == 1)[0]
		prev_pts, curr_pts = prev_pts[idx], curr_pts[idx]
		m, _ = cv2.estimateAffinePartial2D(prev_pts, curr_pts)

		dx, dy = m[0, 2], m[1, 2]
		da = np.arctan2(m[1, 0], m[0, 0])
		self.transforms[self.index - self.start_buffer_frame] = [dx, dy, da] 

		self.prev_gray = curr_gray

		progress_status = self.progress.get_progress(
			(self.index - self.start_buffer_frame) / (self.end_frame - self.start_buffer_frame))
		log = f"Frame: {str(self.index - self.start_buffer_frame)} / {str(self.end_frame - self.start_buffer_frame)}, " + \
			f"Pts: {str(len(prev_pts))}, " + \
			f"Progress: {str(int(progress_status * 100))}"
		self.logger.info(log)

		self.index += 1
		return progress_status


	def fix_frame(self, frame, transform, width, height):
		dx = transform[0]
		dy = transform[1]
		da = transform[2]

		m = np.zeros((2, 3), np.float32)
		m[0,0] = np.cos(da)
		m[0,1] = -np.sin(da)
		m[1,0] = np.sin(da)
		m[1,1] = np.cos(da)
		m[0,2] = dx
		m[1,2] = dy

		frame_stabilized = cv2.warpAffine(frame, m, (width, height))
		return frame_stabilized

if __name__ == 'main':
	cp = cv2.VideoCapture('videos/zhongsi-rd.mp4')

	n_frames = int(cp.get(cv2.CAP_PROP_FRAME_COUNT))
	width = int(cp.get(cv2.CAP_PROP_FRAME_WIDTH)) 
	height = int(cp.get(cv2.CAP_PROP_FRAME_HEIGHT))
	fps = cp.get(cv2.CAP_PROP_FPS)
	print("# of frames: ", n_frames)
	print("width of video", width)
	print("height of video", height)
	print("fps of video", fps)

	out = cv2.VideoWriter('video-out.mp4', 0x7634706d, fps, (width, height))

	fixer = Stabilizer(300)
	# Calculate the stabilization transform
	transform = fixer.get_transform(cp)

	# Apply transform to video
	cp.set(cv2.CAP_PROP_POS_FRAMES, 0) 
	for i in range(n_frames - 2):
		succ, curr = cp.read()
		if not succ:
			break
		frame = fixer.fix_frame(succ, transform[i], width, height)
		out.write(frame)
		print("Frame: " + str(i) +  "/" + str(n_frames) + " -  Stabilizing video")

	cp.release()
	out.release()
	cv2.destroyAllWindows()

