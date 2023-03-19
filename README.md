# NFS MW CC

## How to run
### Setup

Download and install `python v3.11` and corresponding `python-pip`

### Run
1. Clone the repository
2. Enter the folder `cd nfs_mw_cc`
3. Run the program and follow the instructions

```
pip3.11 install -r requirements.txt
python3.11 main.py -h
```

You should see the following help
```
$ python3.11 main.py -h
Starting main
usage: main.py [-h] (-p | -a) [--width {640,896,1024,1280}]

options:
  -h, --help            show this help message and exit
  -p, --process         Process/Re-process videos
  -a, --annotate        Launch annotate tool
  --width {640,896,1024,1280}
                        Annotate Window width
```

## How to use

### Process

> Annotate works only with processed videos

We use the process function to normalize the videos into a consistent format and resolution. Place your videos into `data/original` to start. Please make sure videos are `mp4` only.

To start the process function, run this command

```
python3.11 main.py -p
```

You should see something like this

```
Starting main
Processing video: data/original\1.mp4: 1920x1200 30 FPS
Processing video: data/original\3.mp4: 1920x1200 30 FPS
Processing video: data/original\2.mp4: 1920x1200 30 FPS
100%|████████████████████████████████████████████| 236/236 [00:16<00:00, 14.72it/s]
100%|████████████████████████████████████████████| 459/459 [00:27<00:00, 16.98it/s]
100%|████████████████████████████████████████████| 492/492 [00:28<00:00, 17.48it/s]

Processed 3 videos
```
The processed videos may be found in processed folder.

### Annotate

Annotation means you need to identify what are the areas of interest. So to run the tool, you can use this command:

```
python3.11 main.py -a
```

This will start the tool. The default resolution is 1024x576, owing to performance. 

To specify a larger (720p is max) or smaller resolution, you can use this command:

```
python3.11 main.py -a --width 640
OR
python3.11 main.py -a --width 1280
```

So once you have the tool running, you can use these controls
```
Mouse: Select Area of interest (Once per clip - Can change it until scoring)
Keys: Space=Next Frame, z=Prev Frame, q=Quit, n=Next Video, p=Prev Video, s=Start/Stop capture clip, d=Cancel/Drop captured clip, 1,2,3,4,5: Score for clip
```

Use `Space` to play and `z` to rewind the video. Use the mouse to draw a rectangle around an area of interest. You can redraw this rectangle any number of times as long as you aren't scoring. Once scored, the rectangle is stored along with the other values for that particular clip.

For example, you can hold `Space` until you reach a point of interest in the video. Tap `s` to start capture. Then you can use `z` and `Space` to get to the frame number where you want to clip to start. Next, hold `Space` or tap it until you reach the point where you want to stop the capture. Tap `s` again to end and get into scoring mode. Lastly, use keys `1` `2` `3` `4` or `5` to choose the score. Continue until you have all the clips annotated. Once done, you can proceed to next video. If you started capture by mistake, you can tap `d` to drop capture. If you tap `d` again, it will drop the previous capture.

The output jsons will be stored in the `data/annotated` dir.

# About

This project deals with processing my NFS videos. I am using Chat GPT to help me with a solution to this unique problem:

> I have a bunch of videos, they are game recording videos of the NFS Most Wanted 2008. I have lots of these videos, but the interesting part of the videos are clips of a specific pattern. Basically the game is about racing simulation and I have driven around in "Free roam" mode so much that I have collections of "close calls". I want to create a AI solution that can process these long videos for me, and extract the clips of all the close calls.

Here's what Chat GPT recommended:

That's good to hear! With that many close calls per video, you should be able to create a robust AI solution for this task. Here are some more specific recommendations for the different steps involved:

1. Collect and preprocess the data: Make sure that all the videos are in a consistent format and resolution. You may also want to normalize the brightness and contrast levels across all the videos to make it easier for the AI model to detect the close calls.

2. Annotate the data: Create a dataset of annotated frames from the videos, where each annotated frame contains a bounding box around the close call. To save time and effort, you can use a semi-automated approach where you first detect close calls using a pre-trained object detection model (e.g., YOLO or RetinaNet) and then manually verify and correct the detections.

3. Train a computer vision model: Use a deep learning framework like TensorFlow or PyTorch to train an object detection model to detect close calls in the videos. You can use a pre-trained model as a starting point and fine-tune it on your annotated dataset. For best results, consider using a model architecture that is designed for object detection, such as Faster R-CNN or Mask R-CNN.

4. Apply the model to extract close call clips: Once you have a trained model, you can use it to detect close calls in the videos and extract the corresponding clips. You can use a video processing library like OpenCV to extract the clips from the original video files.

5. Evaluate and refine the model: Test the extracted clips to ensure that they are accurate and representative of the close calls you are interested in. Refine the model and retrain it as necessary to improve its performance.

6. Deploy the solution: Once you have a model that is accurate and reliable, you can deploy it to process your collection of game recording videos and extract the close call clips.

To make the AI solution more efficient, you can use a multi-threaded or distributed processing approach to analyze multiple videos simultaneously. You may also want to consider using a GPU-accelerated deep learning framework to speed up the training and inference processes.