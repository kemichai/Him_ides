"""
Code to reproduce Figures from the submitted
manuscript on Frontiers on the intermediate depth seismicity.

: location: Chavannes-pres-renens
: time: August 2021
: author: KM
"""

import matplotlib
import matplotlib.pyplot as plt
from obspy import read_events
import temporal_plots as tp
import migration_plots as mp
import numpy as np
import os

# Get working directory
work_dir = os.getcwd()

# Set figure details
font = {'family': 'normal',
        'weight': 'normal',
        'size': 18}
matplotlib.rc('font', **font)
# Set figure width to 12 and height to 9
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 13
fig_size[1] = 8
plt.rcParams["figure.figsize"] = fig_size

# Read catalog
cat_path = (work_dir + '/quakeml/')
cat_name = 'Himalayan_Intermediate_depth_earthquake_catalog_Michailos_et_al_2021.xml'
print(f'Reading catalog stored on: "{cat_path}",'
      f'\nUnder the name: "{cat_name}"')
cat = read_events(cat_path + cat_name)
print(f'Read catalog"{cat_name}"!!!')

# Divide catalogs
coords = [[28, 28, 28.4, 29.5],[86.0, 87.4, 88.2, 86.0], # NE of everest 1
          [27.5, 27.5, 28.4, 28.0],[87.4, 88.6, 88.2, 87.4], # SE of one
          [26.5, 26.5, 27.25, 27.25],[85.9, 87.0, 87.0, 85.9], # Udayapur
          [29.9, 29.9, 30.9, 30.9],[83.3, 84.2, 84.2, 83.3], # NW of map
          [26.0, 26.0, 31.0, 31.0],[80.0, 90.0, 90.0, 80.0]] # ALL

# --------------------------------------------------------------------------- #
# Figures 1-4 are with GMT see map directory -------------------------------- #

# --------------------------------------------------------------------------- #
# Figure 5 magnitudes vs time ----------------------------------------------- #
tp.mag_vs_time_plus_cumulative(cat, outfile_name=work_dir + '/Fig_5.png',
                               coordinates=coords)

# --------------------------------------------------------------------------- #
# Figure 6 interevents ------------------------------------------------------ #
tp.interevent_times_single_cluster(cat, outfile_name=work_dir + '/Fig_6.png',
                                   coordinates=coords)

# --------------------------------------------------------------------------- #
# Figure 7 mfd for different catalogs --------------------------------------- #
# Define subcatalogs
cat_1 = tp.cut_cat(cat, coords[0:2])
cat_2 = tp.cut_cat(cat, coords[2:4])
catalog_one = cat_1 + cat_2
catalog_one.events.sort(key=lambda x: x.preferred_origin().time)
cat_3 = tp.cut_cat(cat, coords[4:6])

tp.multi_mfd_plot(catalog_one, cat_3, cat, outfile_name=work_dir+'/Fig_7.png')

# --------------------------------------------------------------------------- #
# Figures 8 and 9 Migration analysis ---------------------------------------- #
A_cross_section = np.array([[86.3, 28.75], [88.4, 27.75]])
B_cross_section = np.array([[86.8, 27.5], [87.8, 28.8]])
catalog = cat_2
catalog.events.sort(key=lambda e: e.origins[-1].time)
CC_cross_section = np.array([[87.7, 28.2], [88.25, 27.65]])
DD_cross_section = np.array([[87.4, 27.75], [88.25, 28.1]])
mp.plot_shelly2007(catalog,
                   prof_points_str=CC_cross_section,
                   prof_points_dip=DD_cross_section,
                   swath=200,
                   profile_name='CD',
                   point_names_str = ["C","C'"],
                   point_names_dip = ["D","D'"])

catalog =  cat_1
catalog.events.sort(key=lambda e: e.origins[-1].time)
BB_cross_section = np.array([[87, 28.15], [87.3, 28.7]])
AA_cross_section = np.array([[86.25, 28.75], [88.0, 28.2]])
mp.plot_migration(catalog,
                  prof_points_str=A_cross_section,
                  prof_points_dip=B_cross_section,
                  swath=250,
                  profile_name='AB',
                  point_names_str = ["A","A'"],
                  point_names_dip = ["B","B'"])

# --------------------------------------------------------------------------- #
# Figures 10 three dimensional figure --------------------------------------- #

