## open image

## generate points of interest

## divide image
### check if point is in rectangle
### average color

## save list as dill
import cv2
import numpy as np
import random
import pandas as pd
import dill as pickle


output_file_name = "flowers.pkl"

class Rectangle:
    def __init__(self, x_min, y_min, y_max, x_max, h, w, r, g, b):
        self.x_min = x_min
        self.y_min = y_min
        self.y_max = y_max
        self.x_max = x_max
        self.h = h
        self.w = w
        self.r = r
        self.g = g
        self.b = b


def split_rectangle(rectangle, direction, divisions):

    new_rectangles = []
    height = rectangle[2]
    width = rectangle[3]
    x_s = rectangle[0]
    y_s = rectangle[1]
    y_e = y_s + height
    x_e = x_s + width

    if divisions != 3:
        if direction == 0:
            for i in range(divisions):
                inc = round((y_e - y_s)/(divisions-i))
                new_rectangles.append([x_s, y_s, inc, width])
                y_s = y_s + inc #+ 1
        elif direction == 1:
            for i in range(divisions):
                inc = round((x_e - x_s)/(divisions-i))
                new_rectangles.append([x_s, y_s, height, inc])
                x_s = x_s + inc #+ 1
    else:
        sub_divs = random.choices([2, 3], cum_weights=(0.3, 0.7), k=1)[0]
        if sub_divs == 2:
            l_or_r = random.choices([0, 1], cum_weights=(0.5, 1.0), k=1)[0]
            if l_or_r == 0:
                if direction == 0:
                    inc = round((y_e - y_s)/3)
                    new_rectangles.append([x_s, y_s, inc, width])
                    y_s = y_s + inc #+ 1
                    new_rectangles.append([x_s, y_s, height-inc, width])
                elif direction == 1:
                    inc = round((x_e - x_s)/3)
                    new_rectangles.append([x_s, y_s, height, inc])
                    x_s = x_s + inc #+ 1       
                    new_rectangles.append([x_s, y_s, height, width-inc])
            if l_or_r == 1:
                if direction == 0:
                    inc = round((y_e - y_s)/3*2)
                    new_rectangles.append([x_s, y_s, inc, width])
                    y_s = y_s + inc #+ 1
                    new_rectangles.append([x_s, y_s, height-inc, width])
                elif direction == 1:
                    inc = round((x_e - x_s)/3*2)
                    new_rectangles.append([x_s, y_s, height, inc])
                    x_s = x_s + inc #+ 1       
                    new_rectangles.append([x_s, y_s, height, width-inc])
        if sub_divs == 3:
            if direction == 0:
                for i in range(divisions):
                    inc = round((y_e - y_s)/(divisions-i))
                    new_rectangles.append([x_s, y_s, inc, width])
                    y_s = y_s + inc #+ 1
            elif direction == 1:
                for i in range(divisions):
                    inc = round((x_e - x_s)/(divisions-i))
                    new_rectangles.append([x_s, y_s, height, inc])
                    x_s = x_s + inc #+ 1
                    

    return new_rectangles


def points_in_rectangle(rect, points, threshold):
    points_x = points[points['x'].between(rect[0], rect[0]+rect[3])]
    points_y = points_x[points_x['y'].between(rect[1], rect[1]+rect[2])]
    if points_y.shape[0] > threshold:
        return True
    else:
        return False

img_color = cv2.imread("a_girl_with_a_flower_in_her_hair_1939.1.108.jpg",1)
img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

# hist normalisation
clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(100,100))
cl1 = clahe.apply(img_gray)
# find edges
edges = cv2.Canny(cl1, 170, 250, apertureSize=3, L2gradient=True)
# other good choices: 150/350
# coordinates of edges
indices = np.where(edges != [0])
edge_coordinates = list(zip(indices[1], indices[0]))
edge_coordinates = pd.DataFrame(edge_coordinates[::10], columns=['x','y'])

# dimensions of first rectangle
rect = [0, 0, img_color.shape[0], img_color.shape[1]]
# initialize rect_list
rect_list = [rect]
# choices for split_rectangle
choices = [1, 2, 3]
weights = (0.0, 0.2, 0.8)
edge_threshold  = 5

for i in range(12):
    new_rect_list = []
    for rectangle in rect_list:
        if rect[2] > 4 and rect[3] > 4:
            if points_in_rectangle(rectangle, edge_coordinates, edge_threshold):
                number_of_divisions = random.choices(choices, cum_weights=weights, k=1)[0]
                new_rect_list.extend(split_rectangle(rectangle,i%2,number_of_divisions))
            else:
                number_of_divisions = 1
                new_rect_list.extend(split_rectangle(rectangle,i%2,number_of_divisions))
            
    rect_list = new_rect_list

output = []

for rect in rect_list:
    img_small = img_color[rect[1]:rect[1]+rect[2], rect[0]:rect[0]+rect[3]]
    col = img_small.mean(axis=0).mean(axis=0)
    # converte color to RGB
    col = col[::-1]
    tmp = Rectangle(x_min=rect[0], y_min=rect[1],
                   y_max=rect[1]+rect[2],x_max=rect[0]+rect[3],
                   h=rect[2], w=rect[3],
                   r=col[0]/255,g=col[1]/255,b=col[2]/255)
    output.append(tmp)

with open(output_file_name, 'wb') as file:
    pickle.dump(output, file)