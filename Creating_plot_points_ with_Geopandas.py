#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 10:07:46 2021

@author: lavran_pagano
"""
import geopandas as gpd
## Data cleaning
os.chdir('/Users/lavran_pagano/Downloads/Python_Scripts/Biomass_Estimation')
plots = pd.read_csv('UMBS_plots.csv')
plots.head()
biomass = pd.read_csv('AGB.csv')
biomass.head()
#filter to Measure_Year=2019
biomass_2019 = biomass[biomass['Measure_Year'] == 2019]
#group by to sum AGB for each Plot_ID
#make dataframe of just Plot_ID and AGB sum
biomass_sum = biomass_2019.groupby(by=['Plot_ID','Measure_Year']).sum().reset_index()[['Plot_ID','AGB','Measure_Year']]
#remove '#' from Plot_ID in plots
plots['Plot_ID'] = plots['Plot_ID'].apply(lambda x: x.replace('#', ''))
plots= plots.drop(['notes'], axis=1)
#merge with plots dataframe
merged_df = pd.merge(plots,biomass_sum, on='Plot_ID')
Plotbio_df = merged_df[['Plot_ID','AGB','Latitude', 'Longitude']]
#convert to a geodataframe
GeoDF = gpd.GeoDataFrame(Plotbio_df,geometry =gpd.points_from_xy(Plotbio_df['Latitude'],Plotbio_df['Longitude']))
GeoDF.crs = 'EPSG:26916'
# Inspect the shapefile
GeoDF.plot('AGB', cmap="Greens") 
#Export points to a shapefile and temporarly swiching working directorys 
os.chdir('/Users/lavran_pagano/Downloads/Python_Scripts/Biomass_Estimation/Plot_points')
GeoDF.to_file(filename = 'UMBSPlot_points.shp',driver = 'ESRI Shapefile')