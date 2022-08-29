import numpy as np 
import os 
import cv2
from pathlib import Path

def debug(opt,classes):

    paths = ["/train.txt", "/test.txt"]
    for path in paths:
        to_be_debuged_path = Path(opt.path + path)
        if to_be_debuged_path.is_file():
            debug_file(str(to_be_debuged_path), classes)

def debug_file(path, classes):
    color_list = np.random.randint(low=0, high=256, size=(len(classes), 3)).tolist()

    # read the file
    file = open(path, "r")
    read_lines = file.readlines()
    file.close()

    for line in read_lines:
        print("Image Path : ", line)
        # read image file
        img_file = cv2.imread(line[:-1])

        # read .txt file
        label_path = line[:-4] + "txt"
        label_file = open(label_path, "r")
        label_read_line = label_file.readlines()
        label_file.close()

        for line1 in label_read_line:
            label_line = line1

            category_id = label_line.split()[0]
            x_center = float(label_line.split()[1])
            y_center = float(label_line.split()[2])
            width = float(label_line.split()[3])
            height = float(label_line.split()[4])

            int_x_center = int(img_file.shape[1] * x_center)
            int_y_center = int(img_file.shape[0] * y_center)
            int_width = int(img_file.shape[1] * width)
            int_height = int(img_file.shape[0] * height)

            min_x = int_x_center - int_width / 2
            min_y = int_y_center - int_height / 2
            width = int(img_file.shape[1] * width)
            height = int(img_file.shape[0] * height)

            print("class name :", classes[int(category_id)])
            print("x_upper_left : ", min_x, "\t", "y_upper_left : ", min_y)
            print("width : ", width, "\t", "\t", "height : ", height)
            print()

            # Draw bounding box
            cv2.rectangle(
                img_file,
                (int(int_x_center - int_width / 2), int(int_y_center - int_height / 2)),
                (int(int_x_center + int_width / 2), int(int_y_center + int_height / 2)),
                color_list[int(category_id)],
                3,
            )

        cv2.imshow(line, img_file)
        delay = cv2.waitKeyEx()

        # If you press ESC, exit
        if delay == 27 or delay == 113:
            break

        cv2.destroyAllWindows()