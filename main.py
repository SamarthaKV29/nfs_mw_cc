import os
import normalize
import concurrent.futures

# Define paths
video_dir = "videos/original"
processed_dir = "videos/processed"

# Create directories if they don't exist
os.makedirs(processed_dir, exist_ok=True)


def clean_up():
    # Remove contents of processed_dir
    for filename in os.listdir(processed_dir):
        file_path = os.path.join(processed_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def main():
    print("Starting main")
    clean_up()
    process_videos()


def process_videos():
    # list all video files
    video_files = [os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith(".mp4")]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # process videos in parallel
        futures = []
        for video_file in video_files:
            processed_file = os.path.join(processed_dir, os.path.basename(video_file))
            futures.append(executor.submit(normalize.process_video, video_file, processed_file))

        # show progress
        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            print(f"Processed {i+1}/{len(futures)} videos")
            # check for exceptions
            try:
                _ = future.result()
            except Exception as e:
                print(f"Error processing video: {e}")


if __name__ == '__main__':
    main()
