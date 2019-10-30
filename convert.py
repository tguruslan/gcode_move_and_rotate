#!/usr/bin/env python

import sys

# ==============================================================================


with open(sys.argv[1]) as file:
    data = file.read()

# ==============================================================================


def sizes(input_data):
    max_x = 0
    max_y = 0
    min_x = 0
    min_y = 0

    for row in data.split('\n'):
        for b in row.split():
            if b.find('X') != -1:
                x = float(b.replace('X',''))
                if x > max_x:
                    max_x = x
                if x < min_x:
                    min_x = x
            if b.find('Y') != -1:
                y = float(b.replace('Y',''))
                if y > max_y:
                    max_y = y
                if y < min_y:
                    min_y = y

    return [max_x, max_y, min_x, min_y]

# ==============================================================================


def rotate_data(input_data):
    new_data = ''
    for row in input_data.split('\n'):
        new_row = []
        for b in row.split():
            if b.find('X') != -1:
                val = b.replace('X', '')
                new_row.append('{axis}{val}'.format(axis='Y',val=float(- float(val) + gcode_size[0] - gcode_size[2])))
            elif b.find('Y') != -1:
                val = b.replace('Y', '')
                new_row.append('{axis}{val}'.format(axis='X',val=float(val)))
            else:
                new_row.append(b)
        new_data += ' '.join(new_row)+"\n"

    return new_data


rotate = float(sys.argv[4])

if rotate != 0:
    if rotate == -90:
        rotate = 270
    for i in range(int(rotate / 90)):
        gcode_size = sizes(data)
        data = rotate_data(data)

# ==============================================================================


def morror_xy(input_data, xy):
    new_data = ''
    for row in input_data.split('\n'):
        new_row = []
        for b in row.split():
            if b.find('X') != -1:
                if xy == 'X':
                    val = b.replace('X', '')
                    new_row.append('X{val}'.format(val=float(- float(val) + gcode_size[0] - gcode_size[2])))
                else:
                    new_row.append(b)
            elif b.find('Y') != -1:
                if xy == 'Y':
                    val = b.replace('Y', '')
                    new_row.append('Y{val}'.format(val=float(- float(val) + gcode_size[1] - gcode_size[3])))
                else:
                    new_row.append(b)
            else:
                new_row.append(b)
        new_data += ' '.join(new_row)+"\n"

    return new_data


mirror = sys.argv[5]

if mirror != 0:
    gcode_size = sizes(data)
    data = morror_xy(data, mirror)

# ==============================================================================


def move_xy(input_data, x, y):
    new_data = ''
    for row in input_data.split('\n'):
        new_row = []
        for b in row.split():
            if b.find('X') != -1:
                new_row.append('X{new_x}'.format(new_x=float(float(b.replace('X', '')) + x)))
            elif b.find('Y') != -1:
                new_row.append('Y{new_y}'.format(new_y=float(float(b.replace('Y', '')) + y)))
            else:
                new_row.append(b)
        new_data += ' '.join(new_row)+"\n"
    return new_data


new_X = float(sys.argv[2])
new_Y = float(sys.argv[3])

if new_X != 0 or new_Y != 0:
    data = move_xy(data, new_X, new_Y)

# ==============================================================================

with open(sys.argv[1].replace('.gcode','')+"_new.gcode", 'w') as file:
    file.write(data)
