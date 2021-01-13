# video_frames_saver
Saves some frames of multiple video files (particularly from youtube).

# Usage

~~~~
url1 = 'path_to_video_file'
url2 = ...
url3 = ...
url4 = ...
url5 = ...

frames_writer = FramesWriter(src_paths=[url1, url2, url3], preproc=Urls2Paths)
frames_writer.add([url4, url5])
frames_writer.write(output_dir)
~~~~
