import numpy as np
import matplotlib as mpl
from skimage.io import imread, imsave
from skimage.filters import threshold_isodata
from skimage.exposure import rescale_intensity
from skimage.color import gray2rgb
from skimage.util import img_as_uint
from matplotlib import pyplot as plt
from tkinter import filedialog as fd


heatmap_wt = rescale_intensity(imread("Data/NCTC TFGFP FM565/p2.tif"))
heatmap_dFtsK = rescale_intensity(imread("Data/NCTC dFtsK TFGFP FM565/p2.tif"))
heatmap_CplXR95C = rescale_intensity(imread("Data/NCTC dFtsK ClpXR95C TFGFP FM565/p2.tif"))
heatmap_dFtsKc = rescale_intensity(imread("Data/dFtsKc TF-GFP/p2_model.tif"))
heatmap_wt_na = rescale_intensity(imread("Data/NCTC TF-GFP + NA/p2_model.tif"))

mask_wt = heatmap_wt > threshold_isodata(heatmap_wt)
mask_dFtsK = heatmap_dFtsK > threshold_isodata(heatmap_dFtsK)
mask_CplXR95C = heatmap_CplXR95C > threshold_isodata(heatmap_CplXR95C)
mask_dFtsKc = heatmap_dFtsKc > threshold_isodata(heatmap_dFtsKc)
mask_wt_na = heatmap_wt_na > threshold_isodata(heatmap_wt_na)

filtered_wt = heatmap_wt * mask_wt
filtered_dFtsK = heatmap_dFtsK * mask_dFtsK
filtered_CplXR95C = heatmap_CplXR95C * mask_CplXR95C
filtered_dFtsKc = heatmap_dFtsKc * mask_dFtsKc
filtered_wt_na = heatmap_wt_na * mask_wt_na

min_int = np.min([np.min(heatmap_wt[np.nonzero(filtered_wt)]),
                  np.min(heatmap_dFtsK[np.nonzero(filtered_dFtsK)]),
                  np.min(heatmap_CplXR95C[np.nonzero(filtered_CplXR95C)]),
                  np.min(heatmap_dFtsKc[np.nonzero(filtered_dFtsKc)]),
                  np.min(heatmap_wt_na[np.nonzero(filtered_wt_na)])])

norm = mpl.colors.Normalize(vmin=min_int, vmax=1.0)
cmap = mpl.cm.get_cmap("coolwarm")

color_wt = np.zeros(np.shape(gray2rgb(heatmap_wt)))
color_dFtsK = np.zeros(np.shape(gray2rgb(heatmap_dFtsK)))
color_CplXR95C = np.zeros(np.shape(gray2rgb(heatmap_CplXR95C)))
color_dFtsKc = np.zeros(np.shape(gray2rgb(heatmap_dFtsKc)))
color_wt_na = np.zeros(np.shape(gray2rgb(heatmap_wt_na)))

def assign_color(filtered, color):

    for i in range(filtered.shape[0]):
        for ii in range(filtered.shape[1]):
            px = filtered[i, ii]
            if px == 0:
                color[i, ii] = (1.0, 1.0, 1.0)
            else:
                rgba = cmap(norm(px))
                color[i, ii] = (rgba[0], rgba[1], rgba[2])

assign_color(filtered_wt, color_wt)
assign_color(filtered_dFtsK, color_dFtsK)
assign_color(filtered_CplXR95C, color_CplXR95C)
assign_color(filtered_dFtsKc, color_dFtsKc)
assign_color(filtered_wt_na, color_wt_na)

imsave("coolwarm_p2_wt.png", color_wt)
imsave("coolwarm_p2_dFtsK.png", color_dFtsK)
imsave("coolwarm_p2_CplXR95C.png", color_CplXR95C)
imsave("coolwarm_p2_dFtsKc.png", color_dFtsKc)
imsave("coolwarm_p2_wt_na.png", color_wt_na)
