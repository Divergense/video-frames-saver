import datetime
from pathlib import Path
from shutil import copyfile
from contextlib import contextmanager

import cv2
import pafy
from tqdm.notebook import tqdm



class FramesWriter():
    def __init__(self, src_paths, frame_step=200, frame_count=10, preproc=None):
        '''
        The class saves frames of multiple video files.
        
        Params:
            - src_paths - list of video paths
            - dst_path  - path to directory where frames will be written
            - preproc   - preprocessing function that apllies to src_paths
        '''
        self.FRAME_STEP = frame_step
        self.FRAME_COUNT = frame_count
        self.preproc = preproc
        self.src_paths = src_paths if preproc is None else preproc(src_paths)
        self.processed_files = []
        
        
    def write(self, dst_path):
        for src_path in tqdm(self.src_paths, desc='Files'):
            self.write_frames_(dst_path, src_path)
            
        self.processed_files.extend(self.src_paths)
        self.src_paths = []
            
    
    def add(self, src_paths, preproc=None):
        if preproc is None:
            if self.preproc is None:
                preproc = lambda x: x
            else:
                preproc = self.preproc
                
        self.src_paths.extend(preproc(src_paths))
            
            
    @contextmanager
    def video_capture(self, *args, **kwargs):
        video_reader = cv2.VideoCapture(*args, **kwargs)
        video_reader.set(1, self.FRAME_STEP)
        try:
            yield video_reader
        finally:
            video_reader.release()
            
            
    def write_frames_(self, dst_path, src_path=None):
        video_src = 0 if src_path is None else src_path
        with self.video_capture(video_src) as cap:
            i = 0
            pbar = tqdm(total=self.FRAME_COUNT, desc='Frames')
            while True:
                is_ok, image = cap.read()
                
                if not is_ok or ((i // self.FRAME_STEP) == self.FRAME_COUNT):
                    break

                if i % self.FRAME_STEP == 0:
                    cv2.imwrite(dst_path + f'{datetime.datetime.now()}.png', image)
                    pbar.update(1)
                
                i += 1
            
            pbar.close()
                    
                    
def Urls2Paths(urls):
    '''
    Transforms youtube url paths to video paths. 
    '''
    pathes = []
    for url in tqdm(urls):
        vPafy = pafy.new(url)
        play = vPafy.getbest(preftype="mp4")
        pathes.append(play.url)
        
    return pathes
