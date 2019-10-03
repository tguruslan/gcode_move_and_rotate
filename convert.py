#!/usr/bin/env python

import sys

new_f = open(sys.argv[1].replace('.gcode','')+"_new.gcode","w+")
old_ff = open(sys.argv[1], 'rb')
old_f = open(sys.argv[1], 'rb')
new_X = float(sys.argv[2])
new_Y = float(sys.argv[3])
rotate = float(sys.argv[4])
mirror = sys.argv[5]

max_x = 0
max_y = 0
min_x = 0
min_y = 0

for i in old_ff:
    for b in i.decode("utf-8").split():
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

old_ff.close()

def gcode_calc(value, axis):
    val = float(value.replace(axis,''))
    if axis == 'X':
        if mirror == 'X':
            if rotate == 90:
                axis = 'Y'
                new_val = val + new_Y
            elif rotate == 180:
                new_val = val + new_X
            elif rotate == 270 or rotate == -90:
                axis = 'Y'
                new_val = - val + max_x - min_x + new_Y
            elif rotate == 0:
                new_val = - val + max_x - min_x + new_X
        elif mirror == 'Y':
            if rotate == 90:
                axis = 'Y'
                new_val = - val + max_x - min_x + new_Y
            elif rotate == 180:
                new_val = - val + max_x - min_x + new_X
            elif rotate == 270 or rotate == -90:
                axis = 'Y'
                new_val = val + new_Y
            elif rotate == 0:
                new_val = val + new_X
        else:
            if rotate == 90:
                axis = 'Y'
                new_val = - val + max_x - min_x + new_Y
            elif rotate == 180:
                new_val = - val + max_x - min_x + new_X
            elif rotate == 270 or rotate == -90:
                axis = 'Y'
                new_val = val + new_Y
            elif rotate == 0:
                new_val = val + new_X
    else:
        if mirror == 'X':
            if rotate == 90:
                axis = 'X'
                new_val = val + new_X
            elif rotate == 180:
                new_val = - val + max_y - min_y + new_Y
            elif rotate == 270 or rotate == -90:
                axis = 'X'
                new_val = - val + max_y - min_y + new_X
            elif rotate == 0:
                new_val = val + new_Y
        elif mirror == 'Y':
            if rotate == 90:
                axis = 'X'
                new_val = - val + max_y - min_y + new_X
            elif rotate == 180:
                new_val = val + new_Y
            elif rotate == 270 or rotate == -90:
                axis = 'X'
                new_val = val + new_X
            elif rotate == 0:
                new_val = - val + new_Y + max_y - min_y
        else:
            if rotate == 90:
                axis = 'X'
                new_val = val + new_X
            elif rotate == 180:
                new_val = - val + max_y - min_y + new_Y
            elif rotate == 270 or rotate == -90:
                axis = 'X'
                new_val = - val + max_y - min_y + new_X
            elif rotate == 0:
                new_val = val + new_Y

    return '{ax}{c}'.format(ax=axis, c=new_val)

for a in old_f:
    new_row = []
    for b in a.decode("utf-8").split():
        if b.find('X') != -1:
            new_row.append(gcode_calc(b, 'X'))
        elif b.find('Y') != -1:
            new_row.append(gcode_calc(b, 'Y'))
        else:
            new_row.append(b)
    new_f.write(' '.join(new_row)+"\n")

old_f.close()
new_f.close()
