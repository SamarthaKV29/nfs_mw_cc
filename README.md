# NFS MW CC

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

So currently this project is in it's `Step 1`

> How to do step 1

To collect and preprocess the data, you can follow these steps:

1. Gather all the game recording videos of NFS Most Wanted 2008 that you have and store them in a directory on your computer. Make sure that the videos are in a consistent format and resolution.

2. Use a video processing library like OpenCV to normalize the brightness and contrast levels across all the videos. You can do this by applying a histogram equalization or a gamma correction transformation to each frame of the video.

3. Split the videos into shorter clips to make it easier to annotate and train the AI model. You can use a video editing software like Adobe Premiere or a command-line tool like FFmpeg to split the videos into smaller clips.

Here's an example command to split a video into 30-second clips using FFmpeg:
```
ffmpeg -i input.mp4 -c copy -map 0 -segment_time 30 -f segment output_%03d.mp4
```