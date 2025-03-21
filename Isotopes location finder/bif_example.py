#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from BIF import BIFReader
import pdb

bif_filename = "/home/jc/Downloads/m400/RadImage1.bif"

image = BIFReader(bif_filename)


# Lets collapse the polar bins into one single bin per azimuthal direction
image_t = image.compton.T
new_image = []
for polar_bin in image_t:
    new_image.append(np.sum(polar_bin))

new_image = np.array(new_image)

normalized_line_image = new_image / np.sum(new_image)

plt.plot(normalized_line_image)
# plt.show()


x,y,z = [0, 0 ,0]
yaw = 0

bin_width = 0.05 # m

x_bins = 100
y_bins = 100

map_image = np.zeros((y_bins, x_bins))

map_image[20][20] = 100

plt.figure()
plt.imshow(map_image)
plt.show()


# pdb.set_trace()
# tets= 1