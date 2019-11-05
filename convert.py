#!/usr/bin/env python

import sys, argparse

# ==============================================================================


arg = argparse.ArgumentParser()
arg.add_argument ('-f', '--file', required=True, help='ім`я вхідного файлу (обов`язковий)')
arg.add_argument ('-t', '--save_to', default=0, help='ім`я файлу в для збереження (якщо не вказати, то буде такеж як оригінальне але з приставкою _new)')
arg.add_argument ('-x', '--move_x', default=0, help='зміщення по Х в мм')
arg.add_argument ('-y', '--move_y', default=0, help='зміщення по У в мм')
arg.add_argument ('-r', '--rotate', default=0, help='поворот на кут (кратне 90)')
arg.add_argument ('-m', '--mirror', default=0, help='відзеркалення осі (назва осі)')
arg.add_argument ('-s', '--scale', default=0, help='маштаб у відсотках, підтримується відємний')
arg.add_argument ('-c', '--combine', default=0, help='комбінувати код (приклад 2x3x10 або 1x2x8 ... де перше клькість по Х друге кількість по Y третє відступ)')
arg.parse_args()

input_file = arg.parse_args().file
save_to = arg.parse_args().save_to
move_x = int(arg.parse_args().move_x)
move_y = int(arg.parse_args().move_y)
rotate = int(arg.parse_args().rotate)
mirror = arg.parse_args().mirror
scale = int(arg.parse_args().scale)
combine = arg.parse_args().combine

# ==============================================================================


with open(input_file) as file:
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
        size_x = max_x - min_x
        size_y = max_y - min_y
    return [max_x, max_y, min_x, min_y, size_x, size_y]

# ==============================================================================


def rotate_data(i_data):
    n_data = ''
    for row in i_data.split('\n'):
        n_row = []
        for b in row.split():
            if b.find('X') != -1:
                n_val = -float(b.replace('X', ''))+g_size[4]
                n_b = '{axis}{val}'.format(axis='Y', val=n_val)
            elif b.find('Y') != -1:
                val = b.replace('Y', '')
                n_b = '{axis}{val}'.format(axis='X', val=float(val))
            else:
                n_b = b
            n_row.append(n_b)
        n_data += "{n_r}\n".format(n_r=' '.join(n_row))

    return n_data


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
                    n_val = -float(b.replace('X', ''))+g_size[4]
                    n_b = 'X{val}'.format(val=n_val)
            elif b.find('Y') != -1:
                if xy == 'Y':
                    n_val = -float(b.replace('Y', ''))+g_size[5]
                    n_b = 'Y{val}'.format(val=n_val)
            else:
                n_b = b
            n_row.append(n_b)
        n_data += "{n_r}\n".format(n_r=' '.join(n_row))

    return n_data


if mirror != 0:
    g_size = sizes(data)
    data = morror_xy(data, mirror)

# ==============================================================================


def scale_code(i_data, rate):
    rate = float(rate / 100)
    n_data = ''
    for row in i_data.split('\n'):
        n_row = []
        for b in row.split():
            if b.find('X') != -1:
                x = float(b.replace('X', ''))
                n_b = 'X{n_x}'.format(n_x=((x - g_size[2]) * rate + x))
            elif b.find('Y') != -1:
                y = float(b.replace('Y', ''))
                n_b = 'Y{n_y}'.format(n_y=((y - g_size[3]) * rate + y))
            else:
                n_b = b
            n_row.append(n_b)
        n_data += "{n_r}\n".format(n_r=' '.join(n_row))
    return n_data



if scale != 0:
    g_size = sizes(data)
    data = scale_code(data, scale)

# ==============================================================================


def move_xy(i_data, x, y):
    n_data = ''
    for row in i_data.split('\n'):
        n_row = []
        for b in row.split():
            if b.find('X') != -1:
                n_b = 'X{v}'.format(v=(float(b.replace('X', ''))+x))
            elif b.find('Y') != -1:
                n_b = 'Y{v}'.format(v=(float(b.replace('Y', ''))+y))
            else:
                n_b = b
            n_row.append(n_b)
        n_data += "{n_r}\n".format(n_r=' '.join(n_row))
    return n_data

if move_x != 0 or move_y != 0:
    data = move_xy(data, move_x, move_y)

# ==============================================================================

def combine_gcode(i_data, x, y, offset):
    out_data = ""
    g_size = sizes(data)
    for i in range(int(x)):
        for j in range(int(y)):
            m_x = int((g_size[4] + int(offset)) * i)
            m_y = int((g_size[5] + int(offset)) * j)
            out_data += move_xy(i_data, m_x, m_y)
    if move_x != 0 or move_y != 0:
        out_data = move_xy(data, move_x, move_y)
    return out_data


if combine != 0:
    params=combine.split('x')
    data = combine_gcode(data, params[0], params[1], params[2])


# ==============================================================================

if save_to == 0:
    save_to = '{name}_new.gcode'.format(name=input_file.replace('.gcode', ''))

with open(save_to, 'w') as file:
    file.write(data)
