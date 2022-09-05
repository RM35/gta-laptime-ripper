import cv2
import numpy as np
import pytesseract
from pytesseract import Output
import re
import datetime

image = cv2.imread('res/ss.png', 0)
wid = image.shape[1]
height = image.shape[0]


# Dimensions based on a 1440p screen
lt_minx = wid * 0.567
lt_maxx = wid * 0.586

name_minx = wid * 0.180
name_maxx = wid * 0.195

car_minx = wid * 0.390
car_maxx = wid * 0.430

table_start_y = height * 0.208

row_threshhold = 20

race_name_minx = wid * 0.156
race_name_maxx = wid * 0.400
race_name_miny = height * 0.104
race_name_maxy = height * 0.139

image = cv2.threshold(image, 220, 255, cv2.THRESH_BINARY)[1]

d = pytesseract.image_to_data(image, output_type=Output.DICT)
image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
alphanumeric = re.compile(r'[a-zA-Z0-9]')

# Idea is to get lap time then car and name from the same row (+- row threshold)
times = []
# Find Lap time
time = re.compile(r"[0-9][0-9]:[0-9][0-9].[0-9][0-9][0-9]")
for i, text in enumerate(d['text']):
    if time.match(text):
        (x, y, w, h) = (d['left'][i], d['top']
                        [i], d['width'][i], d['height'][i])
        if x > lt_minx and x < lt_maxx and y > table_start_y:
            row_y = y
            name = ""
            car = ""
            # Mark it blue
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            lap_time = d['text'][i]
            # Now find name and car on this row
            for j, jtext in enumerate(d['text']):
                if alphanumeric.match(jtext):
                    (x, y, w, h) = (d['left'][j], d['top']
                                    [j], d['width'][j], d['height'][j])
                    if y > row_y - row_threshhold and y < row_y + row_threshhold:
                        if x > name_minx and x < name_maxx and d['conf'][i] > 0.8 and y > table_start_y:
                            # Mark name
                            image = cv2.rectangle(
                                image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            name = jtext
                        if x > car_minx and x < car_maxx and y > table_start_y:
                            # Mark car
                            image = cv2.rectangle(
                                image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                            car = jtext
                        if name != "" and car != "":
                            times.append([name, car, lap_time])
                            break

racename = ""
# get racename
for i, text in enumerate(d['text']):
    if alphanumeric.match(text):
        (x, y, w, h) = (d['left'][i], d['top']
                        [i], d['width'][i], d['height'][i])
        if x > race_name_minx and x < race_name_maxx and y > race_name_miny and y < race_name_maxy:
            racename += text
            image = cv2.rectangle(
                image, (x, y), (x + w, y + h), (0, 0, 255), 2)

# # debug:::: Grid the image for measuring where the table lies
# x_locs = [x for x in range(0, 2559, 100)]
# y_locs = [x for x in range(0, 1439, 100)]
# # grid
# for i in x_locs:
#     image = cv2.line(image, (i, 0), (i, 1439), (0, 255, 0), thickness=2)
# for i in y_locs:
#     image = cv2.line(image, (0, i), (2559, i), (0, 255, 0), thickness=2)
# # detection zones
# detections_x = [lt_minx, lt_maxx, name_minx, name_maxx, car_maxx, car_minx]
# for i in detections_x:
#     image = cv2.line(image, (int(i), 0), (int(i), 1439),
#                      (127, 127, 0), thickness=2)

timenow = datetime.datetime.now().strftime("%d.%m.%y %H.%M.%S")
filename = racename + timenow

cv2.imwrite(f"res/{filename}.png", image)

with open(f"res/{filename}.txt", "w", encoding="utf-8") as f:
    for record in times:
        f.write(f"{record[0]},{record[1]},{record[2]}\n")
