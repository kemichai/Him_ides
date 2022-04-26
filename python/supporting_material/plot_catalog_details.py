"""

:Konstantinos Michailos
:Lausanne
:February 2021
"""

import platform
from obspy import read_events
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import matplotlib.dates as mpdates
import datetime as dt
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


def plot_depth_histos(catalog, outfile_name='hypocentral_depths.png', show=True, save=True):
    """
    Reads a quakeml and plots histogram of hypocentral depths.
    """
    # Get hypocentral depths in km
    dep = []
    for i, ev in enumerate(catalog):
        dep.append(ev.origins[-1].depth/1000)

    fig_name = outfile_name
    bins = np.arange(-8, 201, 2)
    ax = plt.subplot2grid((1, 1), (0, 0), colspan=1, rowspan=1)
    ax.hist(dep, bins, histtype='step', orientation='vertical',
             alpha=0.7, linewidth=1.5, linestyle='-', facecolor='gray',
             color='gray', edgecolor='black', fill=True, label='All NonLinLoc locations')
    ax.set_ylabel(r'Number of events', fontname='Courier', fontsize=18)
    ax.set_xlim([0, 105])

    ax.set_xlabel(r'Hypocentral depth (km)', fontname='Courier', fontsize=18)
    plt.axvline(np.mean(dep), color='k', linestyle='dashed', linewidth=1, label='Mean depth')
    plt.axvline(np.percentile(dep, 90), color='k', linestyle='dotted',
                     linewidth=1, label='90th percentile')
    plt.legend(loc=1, fontsize=16)
    if save:
        plt.savefig(fig_name, bbox_inches="tight", format='png', dpi=300)
    if show:
        plt.show()
    return ax

def plot_cat_details(catalog, outfile_name='catalog_details.png', show=True, save=True):
    """

    """
    from obspy.geodetics import degrees2kilometers
    import matplotlib.ticker as ticker

    # Number of P-wave phase picks
    P1numbers = []
    # Number of S-wave phase picks
    S1numbers = []
    # Root mean square of the travel time residuals for the final earthquake location
    rms = []
    # Same as rms but with more decimals
    rms_new = []
    # greatest azimuthal angle without observation
    azim = []
    # number of observations (P- and S-wave arrival times)
    nobs = []
    # Distance to the closest station
    dist = []
    for event in catalog:
        # print(event)
        ev_P_picks = []
        ev_S_picks = []
        for pick in event.picks:
            if pick.phase_hint == 'P':
                ev_P_picks.append(pick)
            elif pick.phase_hint == 'S':
                ev_S_picks.append(pick)
        P1numbers.append(len(ev_P_picks))
        S1numbers.append((len(ev_S_picks)))
        all_distances = []
        for arr in event.origins[0].arrivals:
            distance_in_degrees = arr.distance
            distance_in_km = degrees2kilometers(distance_in_degrees)
            all_distances.append(distance_in_km)
        dist.append(min(all_distances))

        rms.append(round(event.origins[0].quality.standard_error,2))
        rms_new.append(event.origins[0].quality.standard_error)
        azim.append(event.origins[0].quality.azimuthal_gap)

    print(np.mean(dist))
    print(np.std(dist))

    # Create a matrix containing the number of P- and S- picks of each event
    matrix = []
    for i in range(len(P1numbers)):
        matrix.append([P1numbers[i], S1numbers[i]])
    myarray = np.asarray(matrix)

    fig_name = outfile_name

    # Create plot
    bins = np.arange(-2.5, 302.5, 5)
    ax = plt.subplot2grid((2, 2), (0, 0), colspan=1)
    ax.hist(dist, bins, histtype='step', orientation='vertical',
             color='gray',facecolor='gray', alpha=0.7, linewidth=1.5,
             edgecolor='k',fill=True)
    ax.set_xlim([0, np.percentile(dist, 95) + 50])
    ax.set_ylabel('Number of events', fontsize=18)
    ax.set_xlabel('Distance to the closest station (km)', fontsize=18, fontname='Courier')

    bins2 = np.arange(-0.05, 2.05, 0.03)
    ax1 = plt.subplot2grid((2, 2), (0, 1), colspan=1)
    ax1.hist(rms, bins2, histtype='step', orientation='vertical',
             color='gray',facecolor='gray', alpha=0.7, linewidth=1.5,
             edgecolor='k',fill=True, label='2001-2005')
    ax1.set_xlabel(r'RMS (s)', fontsize=18, fontname='Courier')
    ax1.set_ylabel('Number of events', fontsize=18)

    ax1.set_xlim([0, 1.0])

    bins3 = np.arange(-0.5, 35.5, 1)
    ax2 = plt.subplot2grid((2, 2), (1, 0), colspan=1)
    colors = ['grey', 'black']
    labels = ['P-wave picks', 'S-wave picks']
    ax2.hist(myarray, bins3, histtype='bar', color=colors, label=labels, edgecolor='black')
    ax2.legend(prop={'size': 15})
    ax2.set_xlabel(r'Number of picks', fontname='Courier', fontsize=18)
    ax2.set_ylabel(r'Number of events', fontsize=18)
    ax2.set_xlim([0, 35.0])



    bins4 = np.arange(-0.5, 360.5, 10)
    ax6 = plt.subplot2grid((2, 2), (1, 1), colspan=1)
    ax6.hist(azim, bins4,  histtype='step', orientation='vertical',
             color='gray',facecolor='gray', alpha=0.7, linewidth=1.5,
             edgecolor='k',fill=True, label='2001-2005')
    ax6.set_xlabel(r'Azimuthal gap ($^\circ$)', fontname='Courier', fontsize=18)
    ax6.set_ylabel(r'Number of events',fontname='Courier', fontsize=18)
    ax6.axis('tight')
    ax6.xaxis.set_ticks(np.arange(0, 360, 100))
    ax6.xaxis.set_major_formatter(ticker.FormatStrFormatter('%i'))
    ax6.set_xlim([0, 360])
    plt.tight_layout()

    if save:
        plt.savefig(fig_name, format='png', dpi=300)
    if show:
        plt.show()
    return

# Read catalog
cat_path = (work_dir + '/quakeml/')
cat_name = 'Himalayan_Intermediate_depth_earthquake_catalog_Michailos_et_al_2021.xml'
print(f'Reading catalog stored on: "{cat_path}",'
      f'\nUnder the name: "{cat_name}"')
cat = read_events(cat_path + cat_name)
print(f'Read catalog"{cat_name}"!!!')

# Make plots
ax3 = plot_depth_histos(cat)
plot_cat_details(cat)
