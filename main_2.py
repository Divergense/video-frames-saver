import math
import numpy as np

from tqdm.notebook import tqdm
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import datetime
from pathlib import Path
from shutil import copyfile
from contextlib import contextmanager

import cv2
import pafy
from skimage.feature import hog
from skimage import data, exposure



@contextmanager
def video_capture(*args, **kwargs):
    """
    kwargs is dedicated for 'set' method arguments: 'propId' and 'value'
    """
    
    measure = kwargs.get('propId', 1)
    start = kwargs.get('value', 0)
    
    video_capture = cv2.VideoCapture(*args)
    video_capture.set(measure, start)
    try:
        yield video_capture
    finally:
        video_capture.release()
            
            
@contextmanager
def video_writer(*args, **kwargs):
    """
    Must be given video_capture or named arguments exclusive.

    Named arguments are: 'fourcc', 'frame_w', 'frame_h' and 'fps'.

    Warning: if given video name already exists previous video will be rewritten. 
    """
    
    video_capture = kwargs.get('video_capture', None)
    fourcc = kwargs.get('fourcc', cv2.VideoWriter_fourcc(*'MP4V'))
    if video_capture is None:
        frame_w = kwargs.get('frame_w', 480)
        frame_h = kwargs.get('frame_h', 360)
        fps = kwargs.get('fps', 24)
    else:
        frame_w = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_h = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        
    # Potential trouble if codec does't correspond to output file extension
    video_writer = cv2.VideoWriter(*args, fourcc, fps, (frame_w, frame_h))
    try:
        yield video_writer
    finally:
        video_writer.release()


class FramesWriter():
    def __init__(self, src_paths, frame_step=200, frame_count=10, preproc=None):
        """
        The class saves frames of multiple video files.
        
        Params:
            - src_paths - list of video paths
            - dst_path  - path to directory where frames will be written
            - preproc   - preprocessing function that apllies to src_paths
        """
        
        self.FRAME_START = 0
        self.FRAME_STEP = frame_step
        self.FRAME_COUNT = frame_count
        self.preproc = preproc
        self.src_paths = src_paths if preproc is None else preproc(src_paths)
        self.processed_files = []
        
        
    def write_frames(self, dst_path):
        for src_path in tqdm(self.src_paths, desc='Files'):
            self.write_frames_(dst_path, src_path)
            
        self.processed_files.extend(self.src_paths)
        self.src_paths = []
            
    
    def add(self, src_paths, preproc=None):
        # need to rewrite this method
        if preproc is None:
            if self.preproc is None:
                preproc = lambda x: x
            else:
                preproc = self.preproc
                
        self.src_paths.extend(preproc(src_paths))
            
            
    def write_frames_(self, dst_path, src_path=None):
        video_src = 0 if src_path is None else src_path
        with video_capture(video_src) as cap:
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
            
            
    def write_videos(self, dst_dir, time_ranges):
        """
        time_ranges - list of nested list each of it contains tuples that 
            define start - stop range in seconds.
        
        Pay attention on time complexity.
        """

        assert len(self.src_paths) == len(time_ranges), 'Wrong number of source videos and time ranges.' 
        
        video_num = 0
        pbar = tqdm(sum(map(len, time_ranges)), desc='Files')
        for src_path, time_range in zip(self.src_paths, time_ranges):
            for start, stop in time_range:
                start, stop = 1000 * start, 1000 * stop
                dst_file = dst_dir / f'{video_num}.mp4'
                with video_capture(str(src_path), propId=cv2.CAP_PROP_POS_MSEC, value=start) as cap:
                    with video_writer(str(dst_file), video_capture=cap) as writer_cap:
                        while True:
                            is_ok, image = cap.read()
                            cur_time = cap.get(cv2.CAP_PROP_POS_MSEC)
                            if is_ok and (cur_time <= stop):
                                writer_cap.write(np.uint8(image))
                            else:
                                writer_cap.release()
                                break
                video_num += 1
                pbar.update(1)
                    
                    
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
