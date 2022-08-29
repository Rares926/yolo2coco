from pathlib import Path
from queue import Empty

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
import json

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
        "-o",
        "--output",
        type=str,
        help="Output location for the coco dataset format",
    )
    parser.add_argument(
        "-cpy",
        "--copy_images",
        action='store_true',
        help="Output location for the coco dataset format",
    )

    args = parser.parse_args()
    return args



def main(opt):

    print("Start!")
    classes = get_classes_list(opt)
    data = get_data(opt,Data,classes)

    annot_path = opt.output+"/annotations"
    Path(annot_path).mkdir(parents=True, exist_ok=True)


    for key in data:
        if data[key]:
            file_name = annot_path + "/instances_" + str(key) + ".json"
            with open(file_name, "w") as outfile:
                json.dump(data[key], outfile, indent=4)


    print("hehe")


if __name__ == "__main__":
    options = get_args()
    main(options)