import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import re

image = cv2.imread('res/ss2.png', 0)
wid = image.shape[1]
height = image.shape[0]

lt_minx = wid * 0.54
lt_maxx = wid * 0.60

name_minx = wid * 0.18
name_maxx = wid * 0.20

car_minx = wid * 0.4
car_maxx = wid * 0.42

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
        if x > name_minx and x < name_maxx and d['conf'][i] > 0.8:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

## Car types
letter = re.compile(r'[a-zA-Z]')
for i, text in enumerate(d['text']):
    if letter.match(text):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        if x > car_minx and x < car_maxx:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            print(text)
            print(f"{d['level'][i]} {d['line_num'][i]} {d['conf'][i]} {d['block_num'][i]}")

    
total_rec = 0
# Find the total time and lap time
time = re.compile(r"[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]")
for i, text in enumerate(d['text']):
    if time.match(text):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        if x > 1400 and x < 1500:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            print(text)
            print(f"{d['level'][i]} {d['line_num'][i]} {d['conf'][i]} {d['block_num'][i]}")
  

cv2.imshow('img', image)
cv2.waitKey(0)
cv2.imwrite("res/out.png", image)
print(f"{total_rec}")
pass