import pandas as pd
import pytube
import os, time
import subprocess
from torch import cuda

# read video list:
videos = pd.read_csv('videos.csv', header=None)
print("\nFound {} videos to download:\n".format(len(videos)))

for video in videos.iterrows():
    video_id = video[1][0].strip('\\\'')

    # Set youtube stream:
    youtube_url = 'https://www.youtube.com/watch?v={}'.format(video_id)
    youtube = pytube.YouTube(youtube_url)
    video = youtube.streams.get_highest_resolution()
    video_title = video.title.replace(" ", "_")
    video_length = video._monostate.duration
    video_fps = video.fps
    # donwload video.mp4 to output/{video_id} folder
    t0 = time.time()
    video.download('output/{}'.format(video_id), filename=video_title)
    t1 = time.time()
    print("downloaded video {}: \"{}\" - {:,.0f}s".format(video_id, video.title, t1-t0))

    # create folder openpose/output/{video_id}/joints
    print(os.getcwd())
    os.chdir('openpose/')
    print(os.getcwd())
    path_to_video = '../output/{}/{}.mp4'.format(video_id, video_title)
    path_to_output = '../output/{}'.format(video_id+'_fps_'+str(video_fps))



    # record system info

    # record time.time()
    t_init = time.time()

    # # optional: cut video to dt seconds
    # dt = 10
    # subprocess.run(['ffmpeg', '-y', '-loglevel', 'info', '-i', '{}'.format(path_to_video), '-t', '{}'.format(dt), '{}'.format(path_to_video+'.mp4')])
    # path_to_video = path_to_video+'.mp4'

    # extract joints.json
    subprocess.run(['./build/examples/openpose/openpose.bin',
                    '--video', '{}'.format(path_to_video),
                    '--write_json', '{}'.format(path_to_output),
                    '--write_video', '{}/openpose.avi'.format(path_to_output),
                    '--display', '0',
                    '--hand',
                    '--face',
                    '--keypoint_scale', '3'],
                   shell=False
                   )

    # record time.time()
    t_end = time.time()
    gpu_name = cuda.get_device_name(0)
    process_length = (t_end - t_init)

    # print log of time it took:
    print('extracting joints for video {} took {:,.2f} minutes'.format(video_id, (t_end - t_init)/60))
    print('video {} length {}, took {} - {:,.2f} seconds to process'.format(video_id, video_length, gpu_name, process_length))

    # stitch openpose/output/{video_id}/joints into {video_id}.json

    # TODO: copy output to remote storage
