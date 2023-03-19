import os
import helpers.tools as tools
import argparse

from settings import base_dir, videos_dir, processed_dir, annotated_dir, labels_dir, ANNOTATE_WINDOW_W, ANNOTATE_WINDOW_H

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
    parser.add_argument('--width', help='Annotate Window width', choices=ANNOTATE_WINDOW_W, required=False, type=int)

    # group.add_argument('-g', '--generate-labels', help='Generate label from annotated data', action='store_true')

    args = parser.parse_args()

    if args.process:
        if args.width:
            parser.error("--width is only allowed with -a/--annotate!")

        tools.clean_up(processed_dir)
        tools.process_videos(videos_dir, processed_dir)
    if args.annotate:
        w = ANNOTATE_WINDOW_W[2]
        h = ANNOTATE_WINDOW_H[2]

        if args.width is not None:
            idx = ANNOTATE_WINDOW_W.index(args.width)
            w = args.width
            h = ANNOTATE_WINDOW_H[idx]

        tools.annotate_videos(processed_dir, annotated_dir, w, h)

    # if args.generate_labels:
    #     tools.generate_labels(annotated_dir, labels_dir)


if __name__ == '__main__':
    main()
