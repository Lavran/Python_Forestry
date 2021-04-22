#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 10:32:40 2021

@author: lavran_pagano
"""
import gdal
from skimage.morphology import watershed
from skimage.feature import peak_local_max
from skimage.measure import regionprops
from scipy import ndimage as ndi
## Import Canopy height model of the University of Michigan Biological station
chm = gdal.Open('MosaicCanopyHeightmodels.tif')
gt = chm.GetGeoTransform()
chm_proj = chm.GetProjection()#get projection info
band = chm.GetRasterBand(1)#read in band 
chm_array = band.ReadAsArray()
#inspect
plt.figure()
plt.imshow(chm_array)
# find tree tops
#Calculate local maximum points in the smoothed CHM
local_maxi = peak_local_max(chm_array,indices=False, footprint=np.ones((5, 5)))
#convert our bolean list to a list of integers
local_maxi = local_maxi.astype(int
#mark the tree tops
markers = ndi.label(local_maxi)[0]
chm_mask = chm_array
chm_mask[chm_array!= 0] = 1
# Watershed segmentation
labels = watershed(chm_array, markers, mask=chm_mask)
labels_for_plot = labels.copy()
labels_for_plot = np.array(labels_for_plot,dtype = np.float32)
labels_for_plot[labels_for_plot==0] = np.nan
max_labels = np.max(labels)

# Extract tree canopy area, and min and max heght for all trees in UMBS
def get_TreeProps(tree,chm_array, labels):
    indexes_of_tree = np.asarray(np.where(labels==tree.label)).T
    tree_crown_heights = chm_array[indexes_of_tree[:,0],indexes_of_tree[:,1]]
    return [tree.label,
            np.float(tree.area),
            tree.major_axis_length,
            tree.max_intensity,
            tree.min_intensity]
#Get the properties of each segment
tree_properties = regionprops(labels,chm_array)
TreeProps_chm = np.array([get_TreeProps(tree, chm_array, labels) for tree in tree_properties])
X = TreeProps_chm[:,1:]
tree_ids = TreeProps_chm[:,0]