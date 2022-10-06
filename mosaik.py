## open image

## generate points of interest

## divide image
### check if point is in rectangle
### average color

## save list as dill
import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches as patches
import random

img_color = cv2.imread("a_girl_with_a_flower_in_her_hair_1939.1.108.jpg",1)
img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

choices = [1, 2, 3]
weights = (0.0, 0.0, 1.0)

def split_rectangle(rectangle, direction, divisions):

    new_rectangles = []
    height = rectangle[2]
    width = rectangle[3]
    x_s = rectangle[0]
    y_s = rectangle[1]
    y_e = y_s + height
    x_e = x_s + width

    if direction == 0:
        for i in range(divisions):
            inc = round((y_e - y_s)/(divisions-i))
            new_rectangles.append([x_s, y_s, inc, width])
            y_s = y_s + inc + 1
    elif direction == 1:
        for i in range(divisions):
            inc = round((x_e - x_s)/(divisions-i))
            new_rectangles.append([x_s, y_s, height, inc])
            x_s = x_s + inc + 1

    return new_rectangles


rect = [0, 0, img_color.shape[0], img_color.shape[1]]

rect_list = [rect]

for i in range(5):
    new_rect_list = []
    for rectangle in rect_list:
        number_of_divisions = random.choices(choices, cum_weights=weights, k=1)[0]
        new_rect_list.extend(split_rectangle(rectangle,i%2,number_of_divisions))
    rect_list = new_rect_list

print(rect_list)