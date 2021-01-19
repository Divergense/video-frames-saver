# video_frames_saver
Saves some frames of multiple video files (in particular from youtube).

### Todo:

- add dstat files processing

- bar detection

- object detection web site

# Usage

Write video frames to output video file:

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

Delete unpair files:

~~~~
src_dir = Path('...')
dst_dir = Path('...')

dltr = DeleteUnpairs(src_dir, dst_dir, 'xml', 'png')
dltr.delete()
~~~~
