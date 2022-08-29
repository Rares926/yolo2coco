from pathlib import Path

from create_annotations import (
    create_image_annotation,
    create_annotation_from_yolo_format,
)

from Utils.utils import (get_data,
                         get_classes_list)
import cv2
import argparse
import json
import numpy as np

Data = {
        "train":{},
        "test":{}
        }


def get_args():
    parser = argparse.ArgumentParser("Yolo format annotations to COCO dataset format")
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="Absolute path for yolo format dataset.",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Name the output location for the coco dataset format",
    )
    args = parser.parse_args()
    return args



def main(opt):

    print("Start!")
    classes = get_classes_list(opt)
    data = get_data(opt,Data,classes)

    path = Path("parentdirectory/annotations")
    path.mkdir(parents=True, exist_ok=True)

    print("hehe")


if __name__ == "__main__":
    options = get_args()
    main(options)