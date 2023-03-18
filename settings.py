import os
from models.annotation import Annotation


# Define paths
base_dir = "data"
videos_dir = "data/original"
processed_dir = "data/processed"
annotated_dir = "data/annotated"
labels_dir = "data/labels"

CLIP_REGION_DEFAULT = Annotation.Area((405, 389), (838, 688))
