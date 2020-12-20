import pandas as pd
import pytube
import os, time
import subprocess

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
    path_to_output = '../output/{}'.format(video_id)

    subprocess.run(['./build/examples/openpose/openpose.bin',
                    '--video', '{}'.format(path_to_video),
                    '--write_json', '{}'.format(path_to_output),
                    '--write_video', '{}/openpose.avi'.format(path_to_output),
                    '--display', '0',
                    '--hand',
                    '--face'],
                   shell=False
                   )



    # record system info

    # record time.time()
    t_init = time.time()

    # extract joints.json

    # record time.time()
    t_end = time.time()

    # keep log of time it tooke

    # stitch openpose/output/{video_id}/joints into {video_id}.json

    # TODO: copy output to remote storage