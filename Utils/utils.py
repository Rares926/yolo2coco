
from pathlib import Path

from Utils.create_annotations import (
    create_image_annotation,
    create_annotation_from_yolo_format
)

import cv2
import argparse
import json
import numpy as np
import imagesize
import shutil

coco_format = {"images": [{}], "categories": [], "annotations": [{}]}

def get_classes_list(opt):

    path = Path(opt.path + "/data.names") 
    classes = []

    with open(path, "r") as fp:
        read_lines = fp.readlines()

    classes = [line.replace("\n", "") for line in read_lines]

    return classes
    


def get_data(opt, Data, classes):

    train_path = Path(opt.path + "/train.txt")
    test_path = Path(opt.path + "/test.txt")

    copy_images = opt.copy_images

    if copy_images:
        images_path = opt.output+"/images"
        Path(images_path).mkdir(parents=True, exist_ok=True)

    if train_path.is_file():
        Data["train"]={"images": [{}], "categories": [], "annotations": [{}]}
        print("Processing train images:")
        Data["train"]["images"],Data["train"]["annotations"]=get_images_info_and_annotations(train_path, images_path)
        for index, label in enumerate(classes):
            categories = {
                "supercategory": "Defect",
                "id": index + 1,  # ID starts with '1' .
                "name": label,
            }
            Data["train"]["categories"].append(categories)

    if test_path.is_file():
        Data["test"]={"images": [{}], "categories": [], "annotations": [{}]}
        print("Processing test images:")
        Data["test"]["images"],Data["test"]["annotations"]=get_images_info_and_annotations(test_path, images_path)
        for index, label in enumerate(classes):
            categories = {
                "supercategory": "Defect",
                "id": index + 1,  # ID starts with '1' .
                "name": label,
            }
            Data["test"]["categories"].append(categories)

    return Data


def get_images_info_and_annotations(path: str, copy_path: str= " "):
    annotations = []
    images_annotations = []

    with open(path, "r") as fp:
        read_lines = fp.readlines()
    file_paths = [Path(line.replace("\n", "")) for line in read_lines]

    image_id = 0
    annotation_id = 1  # In COCO dataset format, you must start annotation id with '1'

    for file_path in file_paths:
        #if wanted copy the image 
        if copy_path != " ":
            shutil.copy(str(file_path),copy_path)

        # Check how many items have progressed
        print("Processing " + str(image_id) + " ..."+str(file_path.name)+"\n", end='')

        # Build image annotation, known the image's width and height
        w, h = imagesize.get(str(file_path))
        image_annotation = create_image_annotation(
            file_path=file_path, width=w, height=h, image_id=image_id
        )
        images_annotations.append(image_annotation)

        label_file_name = f"{file_path.stem}.txt"

        # check if annotations are in another folder 
        # if opt.yolo_subdir:
        #     annotations_path = file_path.parent / YOLO_DARKNET_SUB_DIR / label_file_name
        # else:

        annotations_path = file_path.parent / label_file_name

        if not annotations_path.exists():
            continue  # The image may not have any applicable annotation txt file.

        with open(str(annotations_path), "r") as label_file:
            label_read_line = label_file.readlines()

        # yolo format - (class_id, x_center, y_center, width, height)
        # coco format - (annotation_id, x_upper_left, y_upper_left, width, height)
        for line1 in label_read_line:
            label_line = line1
            category_id = (
                int(label_line.split()[0]) + 1
            )  # you start with annotation id with '1'
            x_center = float(label_line.split()[1])
            y_center = float(label_line.split()[2])
            width = float(label_line.split()[3])
            height = float(label_line.split()[4])

            float_x_center = w * x_center
            float_y_center = h * y_center
            float_width = w * width
            float_height = h * height

            min_x = int(float_x_center - float_width / 2)
            min_y = int(float_y_center - float_height / 2)
            width = int(float_width)
            height = int(float_height)

            annotation = create_annotation_from_yolo_format(
                min_x,
                min_y,
                width,
                height,
                image_id,
                category_id,
                annotation_id
                # segmentation=opt.box2seg,
            )
            annotations.append(annotation)
            annotation_id += 1

        image_id += 1  # if you finished annotation work, updates the image id.

    return images_annotations, annotations


