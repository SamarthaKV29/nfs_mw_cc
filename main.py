import os
import helpers.tools as tools
import argparse

from settings import base_dir, videos_dir, processed_dir, annotated_dir, labels_dir

# Create directories if they don't exist
os.makedirs(base_dir, exist_ok=True)
os.makedirs(videos_dir, exist_ok=True)
os.makedirs(processed_dir, exist_ok=True)
os.makedirs(annotated_dir, exist_ok=True)
os.makedirs(labels_dir, exist_ok=True)


def main():
    print("Starting main")

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--process', help='Process/Re-process videos', action='store_true')
    group.add_argument('-a', '--annotate', help='Launch annotate tool', action='store_true')
    group.add_argument('-g', '--generate-labels', help='Generate label from annotated data', action='store_true')
    parser.add_argument('--width', help='Sizes: 640 896 1024 1280', choices=[640, 896, 1024, 1280], required=False)
    parser.add_argument('--height', help='Sizes: 640 896 1024 1280', choices=[360, 504, 576, 720], required=False)

    args = parser.parse_args()

    if args.process:
        tools.clean_up(processed_dir)
        tools.process_videos(videos_dir, processed_dir)
    if args.annotate:
        w = 1024
        h = 576

        if args.width is not None:
            w = args.width
        if args.height is not None:
            h = args.height

        tools.annotate_videos(processed_dir, annotated_dir, w, h)

    if args.generate_labels:
        tools.generate_labels(annotated_dir, labels_dir)


if __name__ == '__main__':
    main()
