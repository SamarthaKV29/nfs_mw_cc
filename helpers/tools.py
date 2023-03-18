import json
import os
import concurrent.futures
from helpers.normalize_helper import process_video
from helpers.annotation_helper import _annotate_videos


def annotate_videos(processed_dir, annotated_dir, w, h):
    # list all video files
    processed_files = [os.path.join(processed_dir, f) for f in os.listdir(processed_dir) if f.endswith(".mp4")]
    _annotate_videos(processed_files, annotated_dir, w, h)


# Takes json files and converts them to labels
def generate_labels(in_path, out_path):
    for filename in os.listdir(in_path):
        in_file = os.path.join(in_path, filename)
        if os.path.isfile(in_file):
            with open(in_file, 'r') as f:
                data = json.load(f)
                


def process_videos(videos_dir, processed_dir, ):
    # list all video files
    video_files = [os.path.join(videos_dir, f) for f in os.listdir(videos_dir) if f.endswith(".mp4")]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # process videos in parallel
        futures = []
        for video_file in video_files:
            processed_file = os.path.join(processed_dir, os.path.basename(video_file))
            futures.append(executor.submit(process_video, video_file, processed_file))

        # show progress
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            print(f"Processed {i+1}/{len(futures)} videos")
            # check for exceptions
            try:
                _ = future.result()
            except Exception as e:
                print(f"Error processing video: {e}")


def clean_up(processed_dir):
    # Remove contents of processed_dir
    for filename in os.listdir(processed_dir):
        file_path = os.path.join(processed_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
