import cv2
from tqdm import tqdm


def resize_video(in_path, out_path):
    print("Resizing video: %s" % in_path)
    cap = cv2.VideoCapture(in_path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    resize_ratio = 720 / height
    new_width = int(width * resize_ratio)
    new_height = 720

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, fps, (new_width, new_height))

    if cap.isOpened():
        for i in tqdm(range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))):
            ret, frame = cap.read()
            if not ret:
                break

            resized_frame = cv2.resize(frame, (new_width, new_height))
            out.write(resized_frame)

    else:
        print("Failed to resize video: %s" % in_path)

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def histogram_equalization_video(in_path, out_path):
    print("Equalizing video: %s" % in_path)
    cap = cv2.VideoCapture(in_path)

    # Get the frame dimensions and frames per second
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Create a VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

    if cap.isOpened():
        for i in tqdm(range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))):
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Apply histogram equalization to the grayscale frame
            equalized = cv2.equalizeHist(gray)

            # Convert the equalized frame back to BGR
            bgr = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)

            # Write the frame to the output video
            out.write(bgr)

    # Release the VideoCapture and VideoWriter objects
    cap.release()
    out.release()

    # Close all windows
    cv2.destroyAllWindows()
