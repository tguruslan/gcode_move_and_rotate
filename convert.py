#!/usr/bin/env python

import sys


new_f = open(sys.argv[1].replace('.gcode','')+"_new.gcode","w+")
old_ff = open(sys.argv[1], 'rb')
old_f = open(sys.argv[1], 'rb')
new_X = float(sys.argv[2])
new_Y = float(sys.argv[3])
rotate = float(sys.argv[4])

max_x = 0
max_y = 0
min_x = 0
min_y = 0

for i in old_ff:
    for b in i.decode("utf-8").split():
        if b.find('X') != -1:
            if float(b.replace('X','')) > max_x:
                max_x = float(b.replace('X',''))
            if float(b.replace('X','')) < min_x:
                min_x = float(b.replace('X',''))
        if b.find('Y') != -1:
            if float(b.replace('Y','')) > max_x:
                max_y = float(b.replace('Y',''))
            if float(b.replace('Y','')) < min_x:
                min_x = float(b.replace('Y',''))

old_ff.close()

def gcode_calc(value, axis):
    val = float(value.replace(axis,''))
    if rotate == 90:
        if axis == 'X':
            axis = 'Y'
            new_val = - val + max_x - min_x + new_Y
        else:
            axis = 'X'
            new_val = val + new_X
    elif rotate == 180:
        if axis == 'X':
            new_val = - val + max_x - min_x + new_X
        else:
            new_val = - val + max_y - min_y + new_Y
    elif rotate == 270 or rotate == -90:
        if axis == 'X':
            axis = 'Y'
            new_val = val + new_Y
        else:
            axis = 'X'
            new_val = - val + max_y - min_y + new_X
    elif rotate == 0:
        if axis == 'X':
            new_val = val + new_X
        else:
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
