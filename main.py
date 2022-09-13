from pathlib import Path

from Utils.debug import debug
from Utils.utils import (get_data,
                         get_classes_list)

import argparse
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
        help="Either to copy the images at the output path too",
    )
    parser.add_argument(
        "-s",
        "--show",
        action='store_true',
        help="Either to display the images and their annotations or not ",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Visualize bounding box and print annotation information",
    )

    args = parser.parse_args()
    return args


def main(opt):

    classes = get_classes_list(opt)
    print("Start!")

    if opt.debug is True:
        debug(opt, classes)
        print("Debug Finished!")
    else:
        data = get_data(opt,Data,classes)

        annot_path = opt.output+"/annotations"
        Path(annot_path).mkdir(parents=True, exist_ok=True)

        for key in data:
            if data[key]:
                file_name = annot_path + "/instances_" + str(key) + ".json"
                with open(file_name, "w") as outfile:
                    json.dump(data[key], outfile, indent=4)

    print("heheDONE")
    


if __name__ == "__main__":
    options = get_args()
    main(options)