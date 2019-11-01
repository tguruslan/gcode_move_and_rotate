#!/usr/bin/env python

import sys

# ==============================================================================


with open(sys.argv[1]) as file:
    data = file.read()

# ==============================================================================


def sizes(i_data):
    max_x = max_y = min_x = min_y = 0

    for row in data.split('\n'):
        for b in row.split():
            if b.find('X') != -1:
                x = float(b.replace('X', ''))
                if x > max_x:
                    max_x = x
                if x < min_x:
                    min_x = x
            if b.find('Y') != -1:
                y = float(b.replace('Y', ''))
                if y > max_y:
                    max_y = y
                if y < min_y:
                    min_y = y

    return [max_x, max_y, min_x, min_y]

# ==============================================================================


def rotate_data(i_data):
    n_data = ''
    for row in i_data.split('\n'):
        n_row = []
        for b in row.split():
            if b.find('X') != -1:
                n_val = -float(b.replace('X', ''))+g_size[0]-g_size[2]
                b = '{axis}{val}'.format(axis='Y', val=n_val)
            if b.find('Y') != -1:
                val = b.replace('Y', '')
                b = '{axis}{val}'.format(axis='X', val=float(val))
            n_row.append(b)
        n_data += ' '.join(n_row)+"\n"

    return n_data


rotate = float(sys.argv[4])

if rotate != 0:
    if rotate == -90:
        rotate = 270
    for i in range(int(rotate / 90)):
        g_size = sizes(data)
        data = rotate_data(data)

# ==============================================================================


def morror_xy(i_data, xy):
    n_data = ''
    for row in i_data.split('\n'):
        n_row = []
        for b in row.split():
            if b.find('X') != -1:
                if xy == 'X':
                    n_val = -float(b.replace('X', ''))+g_size[0]-g_size[2]
                    b = 'X{val}'.format(val=n_val)
            if b.find('Y') != -1:
                if xy == 'Y':
                    n_val = -float(b.replace('Y', ''))+g_size[1]-g_size[3]
                    b = 'Y{val}'.format(val=n_val)
            n_row.append(b)
        n_data += ' '.join(n_row)+"\n"

    return n_data


mirror = sys.argv[5]

if mirror != 0:
    g_size = sizes(data)
    data = morror_xy(data, mirror)

# ==============================================================================


def scale(i_data, rate):
    rate = float(int(rate) / 100)
    n_data = ''
    for row in i_data.split('\n'):
        n_row = []
        for b in row.split():
            if b.find('X') != -1:
                x = float(b.replace('X', ''))
                b = 'X{n_x}'.format(n_x=((x - g_size[2]) * rate + x))
            if b.find('Y') != -1:
                y = float(b.replace('Y', ''))
                b = 'Y{n_y}'.format(n_y=((y - g_size[3]) * rate + y))
            n_row.append(b)
        n_data += ' '.join(n_row)+"\n"
    return n_data



if sys.argv[6] != 0:
    g_size = sizes(data)
    data = scale(data, sys.argv[6])

# ==============================================================================


def move_xy(i_data, x, y):
    n_data = ''
    for row in i_data.split('\n'):
        n_row = []
        for b in row.split():
            if b.find('X') != -1:
                b = 'X{n_x}'.format(n_x=(float(b.replace('X', ''))+x))
            if b.find('Y') != -1:
                b = 'Y{n_y}'.format(n_y=(float(b.replace('Y', ''))+y))
            n_row.append(b)
        n_data += ' '.join(n_row)+"\n"
    return n_data


n_X = float(sys.argv[2])
n_Y = float(sys.argv[3])

if n_X != 0 or n_Y != 0:
    data = move_xy(data, n_X, n_Y)

# ==============================================================================

with open(sys.argv[1].replace('.gcode', '')+"_new.gcode", 'w') as file:
    file.write(data)
