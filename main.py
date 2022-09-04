import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import re

image = cv2.imread('res/ss2.png', 0)
wid = image.shape[1]
height = image.shape[0]


## Dimensions based on a 1440p screen
lt_minx = wid * 0.567
lt_maxx = wid * 0.586

name_minx = wid * 0.180
name_maxx = wid * 0.195

car_minx = wid * 0.390
car_maxx = wid * 0.430

table_start_y = height * 0.208

# print(f"{wid} + {height}")
# scale_percent = 75 # percent of original size
# width = int(image.shape[1] * scale_percent / 100)
# height = int(image.shape[0] * scale_percent / 100)
# dim = (width, height)
# image = cv2.resize(image, dim)

image = cv2.threshold(image, 220, 255, cv2.THRESH_BINARY)[1]


d = pytesseract.image_to_data(image, output_type=Output.DICT)
image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)

## Player Names
alphanumeric = re.compile(r'[a-zA-Z0-9]')
for i, text in enumerate(d['text']):
    if alphanumeric.match(text):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        if x > name_minx and x < name_maxx and d['conf'][i] > 0.8 and y > table_start_y:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

## Car types
letter = re.compile(r'[a-zA-Z]')
for i, text in enumerate(d['text']):
    if letter.match(text):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        if x > car_minx and x < car_maxx and y > table_start_y:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            print(text)
            print(f"{d['level'][i]} {d['line_num'][i]} {d['conf'][i]} {d['block_num'][i]}")

    
total_rec = 0
# Find the total time and lap time
time = re.compile(r"[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]")
for i, text in enumerate(d['text']):
    if time.match(text):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        if x > lt_minx and x < lt_maxx and y > table_start_y:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            print(text)
            print(f"{d['level'][i]} {d['line_num'][i]} {d['conf'][i]} {d['block_num'][i]}")
  
## Grid the image for measuring where the table lies
x_locs = [x for x in range(0, 2559, 100)]
y_locs = [x for x in range(0, 1439, 100)]
#grid
for i in x_locs:
    image = cv2.line(image, (i, 0), (i, 1439), (0, 255, 0), thickness=2)
for i in y_locs:
    image = cv2.line(image, (0, i), (2559, i), (0, 255, 0), thickness=2)
#detection zones
detections_x = [lt_minx, lt_maxx, name_minx, name_maxx, car_maxx, car_minx]
for i in detections_x:
    image = cv2.line(image, (int(i), 0), (int(i), 1439), (127, 127, 0), thickness=2)


cv2.imshow('img', image)
cv2.waitKey(0)
cv2.imwrite("res/out.png", image)
print(f"{total_rec}")
pass