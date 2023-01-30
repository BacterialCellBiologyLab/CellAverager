import os
import numpy as np
from skimage.io import imread
from matplotlib import pyplot as plt

count = 0
colors = ["r", "b"]
for ht in os.listdir("Heatmaps"):
    img = imread("Heatmaps" + os.sep + ht)
    img /= np.max(img)
    y = img[:, int(img.shape[1]/2)]
    x = [yy*100/img.shape[0] for yy in range(0, img.shape[0])]

    filtered_y = y > 0.75

    left_c = int(np.min((filtered_y*x)[np.nonzero(filtered_y*x)]))
    right_c = int(np.max(filtered_y * x))

    plt.plot(y, x, c=colors[count], label=ht)
    plt.plot([0.75, 0.75], [0, 100], c="gray", linestyle="dashed")
    plt.plot([0.35, 1], [left_c, left_c], c=colors[count], linestyle="dashed")
    plt.plot([0.35, 1], [right_c, right_c], c=colors[count], linestyle="dashed")
    count += 1
plt.legend()
plt.show()