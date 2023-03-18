import os
import cv2
import json
from models.annotation import Annotation
from settings import CLIP_REGION_DEFAULT

# Define colors
orange = (50, 165, 255)
red = (55, 55, 255)
green = (25, 155, 25)

# Initialize globals
clip_region = CLIP_REGION_DEFAULT
base_frame = None
frame = None
frame_num = 0
start_point = None
end_point = None


# Define mouse callback function
def _handle_mouse(event, x, y, flags, params):
    global clip_region, frame_num, frame, start_point, end_point, base_frame
    cap = params[0]
    props = params[1]

    if not props['is_playing'] and event == cv2.EVENT_MOUSEMOVE and start_point is not None and frame is not None:
        _draw_rectangle(frame, Annotation.Area(start_point, (x, y)), props, False)

    if props['is_playing'] and event == cv2.EVENT_LBUTTONDOWN:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        if not ret:
            start_point = None
            props['is_playing'] = True
            return

        clip_region = CLIP_REGION_DEFAULT
        start_point = (x, y)
        end_point = None
        props['is_playing'] = False

    if not props['is_playing'] and event == cv2.EVENT_LBUTTONUP:
        end_point = (x, y)
        # print("Rectangle Coordinates:", (start_point, end_point))
        clip_region = Annotation.Area(start_point, end_point)
        start_point = None
        end_point = None
        base_frame = None
        frame[:] = (0, 0, 0)
        props['is_playing'] = True


def _draw_rectangle(frame, region, props, filled):
    global base_frame
    if not filled and base_frame is None:
        base_frame = frame.copy()

    overlay = frame.copy()
    rect_weight = 0.2 if filled else 0.5
    frame_weight = 0.8 if filled else 0.5
    src2 = frame if filled else base_frame
    cv2.rectangle(overlay, tuple(region.start), tuple(region.end), (0, 200, 0), cv2.FILLED if filled else 3)
    cv2.addWeighted(overlay, rect_weight, src2, frame_weight, 0, frame)
    cv2.imshow(props['window_name'], frame)


def _annotate_videos(files, out_path, w, h):
    total_videos = len(files)
    current_video = 0

    print("Total: %d" % total_videos)

    while True:
        # print("Current: %d" % current_video)
        if current_video in range(0, total_videos):
            current_video += _annotate_video(files[current_video], out_path, w, h)
        else:
            break


def _annotate_video(in_path, out_path, win_w, win_h):
    global frame_num, clip_region, frame

    out_name = os.path.splitext(os.path.basename(in_path))[0] + '.json'
    out_file = os.path.join(out_path, out_name)

    props = {
        'started': False,
        'window_name': "NFS MW CC: Annotate Tool",
        'go_to_next': False,
        'go_to_prev': False,
        'show_table': True,
        'is_scoring': False,
        'is_playing': True,
        'clips': []
    }

    if os.path.isfile(out_file):
        with open(out_file, 'r') as f:
            data = json.load(f)
            for d in data:
                props['clips'].append(Annotation(**d))

    # print([str(clip) for clip in props['clips']])

    frame_num = props['clips'][-1].end if len(props['clips']) > 0 else 0

    # Setup window
    cap = cv2.VideoCapture(in_path)
    cv2.namedWindow(props['window_name'], cv2.WINDOW_NORMAL)
    cv2.resizeWindow(props['window_name'], win_w, win_h)
    cv2.setMouseCallback(props['window_name'], _handle_mouse, (cap, props))

    frames_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    while cap.isOpened():
        if frame_num < 0:
            props['go_to_prev'] = True
            break
        if frame_num > frames_count:
            props['go_to_next'] = True
            break

        key = cv2.waitKey(1) & 0xFF

        if frame_num in range(0, frames_count):
            for clip in props['clips']:
                if frame_num in range(clip.start, clip.end):
                    clip_region = clip.area

        def show_frame(f, props):
            current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
            showing_prompt = False

            if f in range(0, frames_count):
                if f != current_frame:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, f)

                ret, frame = cap.read()
                if not ret:
                    return

                # Add text to frame
                if props['started']:
                    cv2.putText(frame, f"Start: {start}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, orange, 2)

                if not props['started'] and props['show_table']:
                    i = 0
                    for call in props['clips']:
                        cv2.putText(frame, f"Start: {call.start} End: {call.end} Score: {call.score}", (10, 60 + i), cv2.FONT_HERSHEY_SIMPLEX, 0.7, green, 2)
                        i += 30

                if props['is_scoring']:
                    if not showing_prompt:
                        cv2.imshow(props['window_name'], frame)
                        cv2.putText(frame, f"Enter the score: [1 - 5]", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, red, 2)
                        cv2.imshow(props['window_name'], frame)
                        key = cv2.waitKey(1) & 0xFF
                        showing_prompt = True

                    if key is not None:
                        if key in range(49, 55):
                            score = (key - 48)
                            props['clips'].append(Annotation(start, end, score, clip_region))
                            props['is_scoring'] = False
                            props['started'] = False
                            props['show_table'] = True
                        else:
                            cv2.putText(frame, f"Please hit a number between 1-5 using your keyboard", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, red, 2)
                            cv2.imshow(props['window_name'], frame)

                        if key == ord('d'):
                            props['is_scoring'] = False
                            props['started'] = False
                            props['show_table'] = True

                _draw_rectangle(frame, clip_region, props, True)

                cv2.putText(frame, f"Frame: {frame_num}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, red, 2)
                cv2.imshow(props['window_name'], frame)

        if props['is_playing']:
            if key == ord(' '):
                frame_num += 1

            elif key == ord('z'):
                frame_num -= 1

            if key == ord('s'):
                if not props['started']:
                    props['started'] = True
                    start = frame_num
                else:
                    props['started'] = False
                    end = frame_num
                    props['show_table'] = False
                    props['is_scoring'] = True

            if key == ord('d'):
                if not props['started']:
                    print("Drop last item")
                    if len(props['clips']) > 0:
                        props['clips'].pop()
                else:
                    print("Drop %d" % start)
                    props['started'] = False

            if key == ord('n'):
                props['go_to_next'] = True
                break

            if key == ord('p'):
                props['go_to_prev'] = True
                break

            if key == ord('r'):
                frame_num = 0

            show_frame(frame_num, props)

        if key == ord('q'):
            props['go_to_next'] = False
            props['go_to_prev'] = False
            break

    cap.release()
    cv2.destroyAllWindows()

    with open(out_file, 'w') as f:
        json.dump(props['clips'], f, default=vars)

    if props['go_to_next']:
        return 1
    elif props['go_to_prev']:
        return -1
    else:
        return -2
