#/usr/bin/env python
"""
Code to explore any seismic migrations in the seismicity catalogs

Plot according to Shelly and Beroza 2007
=============================================
: Chavannes-pres-rennens
: May 2021
: Konstantinos Michailos
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.dates as mpdates
import datetime as dt

font = {'family': 'normal',
        'weight': 'normal',
        'size': 18}
matplotlib.rc('font', **font)
# Set figure width to 12 and height to 9
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 15
fig_size[1] = 10
plt.rcParams["figure.figsize"] = fig_size
subplot_rect = {'left': 0.08, 'right': 0.96, 'bottom': 0.08, 'top': 0.95, 'wspace': 0.1, 'hspace': 0.1}

def dist_calc(loc1, loc2):
    """
    Function to calculate the distance in km between two points.

    Uses the flat Earth approximation. Better things are available for this,
    like `gdal <http://www.gdal.org/>`_.

    :type loc1: tuple
    :param loc1: Tuple of lat, lon, depth (in decimal degrees and km)
    :type loc2: tuple
    :param loc2: Tuple of lat, lon, depth (in decimal degrees and km)

    :returns: Distance between points in km.
    :rtype: float
    :author: Calum Chamberlain
    """
    R = 6371.009  # Radius of the Earth in km
    dlat = np.radians(abs(loc1[0] - loc2[0]))
    dlong = np.radians(abs(loc1[1] - loc2[1]))
    ddepth = abs(loc1[2] - loc2[2])
    mean_lat = np.radians((loc1[0] + loc2[0]) / 2)
    dist = R * np.sqrt(dlat ** 2 + (np.cos(mean_lat) * dlong) ** 2)
    dist = np.sqrt(dist ** 2 + ddepth ** 2)
    return dist


def plot_migration(catalog, prof_points_str, prof_points_dip,
                   swath=50,
                   point_names_str = ["A","A'"],
                   point_names_dip = ["B","B'"],
                   profile_name='AB',
                   show=True, save=True):

    def calculate_profile(ref_pnt, profile_width):
        prof_dist, prof_dep, prof_mag, prof_time, prof_str_orig, prof_index = [], [], [], [], [], []
        cos_lat = np.cos(ref_pnt[0][1] * np.pi / 180)
        vec_ab = ref_pnt[1] - ref_pnt[0]
        vec_ab[0] *= cos_lat
        abs_ab = np.linalg.norm(vec_ab)
        for i in range(num_events):
            loc_c = np.array([lon[i], lat[i]])
            vec_ac = loc_c - ref_pnt[0]
            vec_ac[0] *= cos_lat
            abs_ac = np.linalg.norm(vec_ac)
            cos = vec_ac.dot(vec_ab) / abs_ab / abs_ac
            if abs_ac * (1 - cos ** 2) ** 0.5 > profile_width / 111.: continue
            if cos < 0 or abs_ac * cos > abs_ab: continue
            prof_dist.append(abs_ac * cos * 111)
            prof_dep.append(dep[i])
            prof_mag.append(mag[i])
            prof_time.append(orig_time[i])
            prof_str_orig.append(str_orig[i])
            prof_index.append(index[i])
        return prof_dist, prof_dep, prof_mag, abs_ab * 111, prof_time, prof_str_orig, prof_index

    # get specific params
    prof_width = swath
    # plot subplot
    ref_points_str = prof_points_str
    ref_points_dip = prof_points_dip
    mag = []
    lat = []
    lon = []
    dep = []
    orig_time = []
    orig_time_ = []
    str_orig = []
    index = []
    for i, ev in enumerate(catalog):
        if ev.origins[-1].depth / 1000 < 110 and ev.origins[-1].depth / 1000 > 40:
            mag.append(ev.magnitudes[-1].mag)
            lat.append(ev.origins[-1].latitude)
            lon.append(ev.origins[-1].longitude)
            dep.append(ev.origins[-1].depth / 1000)
            str_orig.append(str(ev.origins[-1].time))
            eq_date = dt.datetime.strptime(str(ev.origins[-1].time), '%Y-%m-%dT%H:%M:%S.%fZ')
            orig_time_.append(eq_date)
            index.append(i + 1)
            orig_time.append(mpdates.date2num(dt.datetime.strptime(str(ev.origins[-1].time), '%Y-%m-%dT%H:%M:%S.%fZ')))
    num_events = len(lat)

    prof_dist_str, prof_dep_str, prof_mag_str, \
    abs_ab_str, prof_time_str, prof_str_orig_str, prof_index_str = calculate_profile(ref_points_str, prof_width)
    prof_dist_dip, prof_dep_dip, prof_mag_dip, \
    abs_ab_dip, prof_time_dip, prof_str_orig_dip, prof_index_dip = calculate_profile(ref_points_dip, prof_width)
    times_dip = [dt.datetime.strptime(d,'%Y-%m-%dT%H:%M:%S.%fZ').date() for d in prof_str_orig_dip]
    times_str = [dt.datetime.strptime(d,'%Y-%m-%dT%H:%M:%S.%fZ').date() for d in prof_str_orig_str]

    dot_size_str = []
    for m in prof_mag_str:
        dot_size_str.append(m*70)

    dot_size_dip = []
    for m in prof_mag_dip:
        dot_size_dip.append(m*70)

    ax1 = plt.subplot2grid((6, 2), (0, 0), colspan=1, rowspan=2)
    ax1 = plt.gca()
    plt.grid('True', linestyle="-", color='gray', linewidth=0.1, alpha=0.2)
    plt.scatter(prof_dist_str, prof_dist_dip, edgecolor="k", alpha=0.9, s=dot_size_str, marker='o',
                label='Tibet 1D', c=prof_dist_str, cmap='jet')
    ax1.set_ylim([0, max(prof_dist_dip) + 20])
    cbaxes = inset_axes(ax1, width="65%", height="5%", loc='lower left',
                        bbox_to_anchor=(1.1, 0.15, 1, 1),
                        bbox_transform=ax1.transAxes,
                        borderpad=0, )
    cbar = plt.colorbar(cax=cbaxes, orientation='horizontal',
                        extend='both',
                        label='Distance along-strike (km)')
    ax1.set_xlabel("Distance along-strike C-C' (km)", fontname='Courier', fontsize=18)
    ax1.set_ylabel('Distance \n perpendicular \n to strike (km)', fontname='Courier', fontsize=18)
    ax1.xaxis.set_label_position('top')
    ax1.xaxis.tick_top()
    ax2 = plt.subplot2grid((6, 2), (2, 0), colspan=2, rowspan=2)
    plt.grid('True', linestyle="-", color='gray', linewidth=0.1, alpha=0.2)
    ax2.scatter(times_dip, prof_dist_dip, edgecolor="k", alpha=0.9, s=dot_size_dip, marker='o',
                label='Tibet 1D', c=prof_dist_str, cmap='jet', zorder=3)
    ax2.tick_params(bottom=True, top=True, left=True, right=False)
    ax2.set_ylim([0, max(prof_dist_dip) + 10])
    ax2.set_xticklabels([])
    ax2.set_ylabel("Distance \n perpendicular \n to strike (km)", fontname='Courier', fontsize=18)
    ax3 = plt.subplot2grid((6, 2), (4, 0), colspan=2, rowspan=2)
    plt.grid('True', linestyle="-", color='gray', linewidth=0.1, alpha=0.2)
    ax3.scatter(times_str, prof_dist_str, edgecolor="k", alpha=0.9, s=dot_size_str, marker='o',
                label='Tibet 1D', c=prof_dist_str, cmap='jet', zorder=3)
    ax3.tick_params(bottom=True, top=True, left=True, right=False)
    ax3.set_ylim([0, max(prof_dist_str) + 10])
    ax3.set_xlabel('Time (UTC)',fontname='Courier', fontsize=18)
    ax3.set_ylabel("Distance \n along-strike (km)", fontname='Courier', fontsize=18)
    plt.tight_layout()
    plt.savefig('dist_along_str_dip_' + profile_name + '.png', format='png', dpi=300)
    plt.show()

    return

