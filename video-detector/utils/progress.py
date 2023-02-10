
class Progress_Divider:
    def __init__(self, l=0, r=1):
        self.left = l
        self.right = r
    
    def get_progress(self, progress_ratio):
        progress = self.left + progress_ratio * (self.right - self.left)
        return progress
