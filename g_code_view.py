#!/usr/bin/env python

import numpy as np
import argparse
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('tkagg')

# ==============================================================================

arg = argparse.ArgumentParser()
arg.add_argument ('-f', '--file', required=True, help='ім`я вхідного файлу (обов`язковий)')
arg.parse_args()

input_file = arg.parse_args().file

# ==============================================================================


with open(input_file) as file:
    data = file.read()

# ==============================================================================

ax = plt.figure().add_subplot(projection='3d')

xs=0
ys=0
zs=0

x_points=[]
y_points=[]
z_points=[]

for row in data.split('\n'):

       for b in row.split():
              if b.find('X') != -1:
                     xs = float(b.replace('X', ''))
              if b.find('Y') != -1:
                     ys = float(b.replace('Y', ''))
              if b.find('Z') != -1:
                     zs = float(b.replace('Z', ''))
       if row.find('X') != -1 or row.find('Y') != -1 or row.find('Z') != -1:
              x_points.append(xs)
              y_points.append(ys)
              z_points.append(zs)

ax.set_box_aspect((np.ptp(x_points), np.ptp(y_points), np.ptp(z_points)*5))

ax.plot(x_points, y_points, z_points)

plt.show() 
