import os
from models.annotation import Annotation


# Define paths
base_dir = "data"
videos_dir = "data/original"
processed_dir = "data/processed"
annotated_dir = "data/annotated"
labels_dir = "data/labels"


ANNOTATE_WINDOW_W = [640, 896, 1024, 1280]
ANNOTATE_WINDOW_H = [360, 504, 576, 720]

CLIP_REGION_DEFAULT = Annotation.Area((405, 389), (838, 688))
