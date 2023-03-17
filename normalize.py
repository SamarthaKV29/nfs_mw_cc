import cv2
from tqdm import tqdm


def process_video(in_path, out_path):
    cap = cv2.VideoCapture(in_path)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    print("Processing video: %s: %dx%d %d FPS" % (in_path, width, height, fps))

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

            # Resize Frame to 720p
            resized_frame = cv2.resize(frame, (new_width, new_height))

            # Convert the frame to grayscale
            gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

            # Apply histogram equalization to the grayscale frame
            equalized = cv2.equalizeHist(gray)

            # Convert the equalized frame back to BGR
            bgr = cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)

            # Write the frame to the output video
            out.write(bgr)

    else:
        print("Failed to resize video: %s" % in_path)

    cap.release()
    out.release()
    cv2.destroyAllWindows()
