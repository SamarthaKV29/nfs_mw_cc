import os
import normalize

# Define paths
videos_path = "videos/original"
resized_path = "videos/resized"
equalized_path = "videos/equalized"

# Create directories if they don't exist
os.makedirs(resized_path, exist_ok=True)
os.makedirs(equalized_path, exist_ok=True)

def clean_up():
    # Define output directories
    resize_dir = 'videos/resized/'
    equalize_dir = 'videos/equalized/'

    # Remove contents of resize_dir
    for filename in os.listdir(resize_dir):
        file_path = os.path.join(resize_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    # Remove contents of equalize_dir
    for filename in os.listdir(equalize_dir):
        file_path = os.path.join(equalize_dir, filename)
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
    for file in os.listdir(videos_path):
        if file.endswith(".mp4"):
            in_path = os.path.join(videos_path, file)
            resize_path = os.path.join(resized_path, file)
            equalize_path = os.path.join(equalized_path, file)

            normalize.resize_video(in_path, resize_path)
            normalize.histogram_equalization_video(in_path, equalize_path)

if __name__ == '__main__':
    main()