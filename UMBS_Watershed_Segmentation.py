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
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
## Import Canopy height model from the University of Michigan Biological station
chm = gdal.Open('/Users/lavran_pagano/Downloads/CanopyHeightModelGtif-1/NEON_D05_UMBS_DP3_680000_5040000_CHM.tif')
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
local_maxi = local_maxi.astype(int)
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
# Extract tree canopy area, and min and max heght for all trees 
def get_TreeProps(tree,chm_array, labels):
    indexes_of_tree = np.asarray(np.where(labels==tree.label)).T
    tree_crown_heights = chm_array[indexes_of_tree[:,0],indexes_of_tree[:,1]]
    return [tree.label,
            np.float(tree.area),
            tree.major_axis_length,]
#Get the properties of each tree
tree_properties = regionprops(labels,chm_array)
TreeProps_chm = np.array([get_TreeProps(tree, chm_array, labels) for tree in tree_properties])
#Rename coulmns
TreePropslist = pd.DataFrame(TreeProps_chm)
TreePropslist.columns = ['ID','Crown_Area','Crown_Diameter']
fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
#Look at the distribution of tree crowns
fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
plt.style.use('fivethirtyeight')
#plot crown area a a subplot
axs[0].hist(TreePropslist.Crown_Area, edgecolor='black')
axs[0].title.set_text('Crown Area')
axs[0].set_xlabel('Meters')
#plot crown diameter as a subplot
axs[1].hist(TreePropslist.Crown_Diameter,edgecolor='black')
axs[1].title.set_text('Crown Diameter')
axs[1].set_xlabel('Meters')
#get summary satsistics for all tree crowns in the chm
TreePropslist[['Crown_Area','Crown_Diameter']].describe()

