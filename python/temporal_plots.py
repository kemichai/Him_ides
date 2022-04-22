"""
Ploting functions
KM
Feb 2021
"""
import datetime as dt
from itertools import cycle
from copy import deepcopy
import numpy as np
import matplotlib.dates as mdates
from eqcorrscan.utils.mag_calc import calc_b_value, calc_max_curv
import matplotlib.pyplot as plt
from collections import Counter


def get_cat_details(catalog):
    """
    This small function reads a catalog and provides a bunch of lists with
    the earthquake location details.
    """
    import matplotlib.dates as mpdates
    import datetime as dt

    mag = []
    lat = []
    lon = []
    dep = []
    orig_time = []
    orig_time_ = []
    str_orig = []
    for ev in catalog:
        mag.append(ev.magnitudes[-1].mag)
        lat.append(ev.origins[-1].latitude)
        lon.append(ev.origins[-1].longitude)
        dep.append(ev.origins[-1].depth/1000)
        str_orig.append(str(ev.origins[-1].time))
        eq_date = dt.datetime.strptime(str(ev.origins[-1].time), '%Y-%m-%dT%H:%M:%S.%fZ')
        orig_time_.append(eq_date)
        orig_time.append(mpdates.date2num(dt.datetime.strptime(str(ev.origins[-1].time), '%Y-%m-%dT%H:%M:%S.%fZ')))
    return str_orig, orig_time, orig_time_, lat, lon, dep, mag


def cut_cat(catalog, coordinates):
    """

    """
    from shapely.geometry import Polygon, Point
    import numpy as np
    from obspy import Catalog

    latitudes = coordinates[0]
    longitudes = coordinates[1]

    p= Polygon((np.asarray(list(zip(latitudes, longitudes)))))

    cut_catalog = Catalog()
    for event in catalog:
        ev_lat = event.origins[-1].latitude
        ev_lon = event.origins[-1].longitude
        if p.contains(Point(ev_lat, ev_lon)):
            cut_catalog.append(event)

    return cut_catalog


def create_lines(x, y, color='black'):
    """Creates vertical lines for plot"""
    from matplotlib import collections as matcoll
    lines = []
    for i in range(len(x)):
        pair=[(x[i],0), (x[i], y[i])]
        lines.append(pair)
    line_collection = matcoll.LineCollection(lines, linewidths=(0.2,),
                                         colors=color)
    return line_collection


def interevent_times_single_cluster(catalog, outfile_name, coordinates,
                show=True, save=True):
    import matplotlib.dates as mpdates
    import matplotlib
    from numpy import arange
    import matplotlib.pyplot as plt
    from obspy import read_events, Catalog

    cat_1 = cut_cat(catalog, coordinates[0:2])
    cat_2 = cut_cat(catalog, coordinates[2:4])
    cat_12 = cat_1 + cat_2
    cat_3 = cut_cat(catalog, coordinates[4:6])
    cat_5_ = cut_cat(catalog, coordinates[8:10])
    # ONLY PLOT THE EVENTS THAT ARE NOT IN THE subcatalogs...
    cat_5 = Catalog()
    for ev in cat_5_:
        if ev not in cat_1 and ev not in cat_2 and ev not in cat_3:
            cat_5.append(ev)

    # South Tibet - Eastern Nepal
    str_orig_1, tibet_orig_1, tibet_orig__1, lat_1, lon_1, dep_1, mag_1 = get_cat_details(cat_12)
    str_orig_3, tibet_orig_3, tibet_orig__3, lat_3, lon_3, dep_3, mag_3 = get_cat_details(cat_3)
    # All the catalog
    str_orig_all, tibet_orig_all, tibet_orig__all, lat_all, lon_all, dep_all, mag_all = get_cat_details(cat_5)

    font = {'family': 'normal',
            'weight': 'normal',
            'size': 18}
    matplotlib.rc('font', **font)
    # Set figure width to 12 and height to 9
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 13
    fig_size[1] = 8
    plt.rcParams["figure.figsize"] = fig_size
    # Set path and figure name
    fig_name = outfile_name
    mindate = mpdates.date2num(dt.datetime.strptime('20010901', '%Y%m%d'))
    maxdate = mpdates.date2num(dt.datetime.strptime('20030501', '%Y%m%d'))

    def prep_for_interevent_plot(str_orig_, tibet_orig_in, tibet_orig__in, lat_, lon_, dep_, mag_):
        """
        """

        # Remove bad mags (some have -5 if there are not enough amplitudes)
        mag = []
        lat = []
        lon = []
        tibet_orig = []
        tibet_orig_ = []
        for i, magnitude in enumerate(mag_):
            if magnitude > -3:
                mag.append(magnitude)
                lat.append(lat_[i])
                lon.append(lon_[i])
                tibet_orig.append(tibet_orig_in[i])
                tibet_orig_.append(tibet_orig__in[i])

        dates = tibet_orig_
        mindate = mpdates.date2num(dt.datetime.strptime('20010901', '%Y%m%d'))
        maxdate = mpdates.date2num(dt.datetime.strptime('20030501', '%Y%m%d'))
        x = range(int(mindate), int(maxdate))
        xdates = [mpdates.num2date(xd) for xd in x]

        counts = arange(0, len(dates))
        # Calculate interevent times
        interevent_time = np.diff(dates)
        # Convert start times to num
        converted_starting_time = matplotlib.dates.date2num(dates)
        # Convert end times to num
        dates = dates[1::]
        converted_finish_time = matplotlib.dates.date2num(dates + interevent_time)

        converted_starting_time = converted_starting_time[1::]
        converted_delta = converted_finish_time - converted_starting_time

        mag=mag[1::]
        lon=lon[1::]
        lat=lat[1::]

        dot_size = []
        for m in mag:
            dot_size.append(m*30)


        return dates, converted_delta, mag, dot_size, lon, lat

    dates_a, converted_delta_a, mag_a, dot_size_a, lon_a, lat_a = prep_for_interevent_plot(str_orig_1, tibet_orig_1, tibet_orig__1, lat_1, lon_1, dep_1, mag_1)
    dates_c, converted_delta_c, mag_c, dot_size_c, lon_c, lat_c = prep_for_interevent_plot(str_orig_3, tibet_orig_3, tibet_orig__3, lat_3, lon_3, dep_3, mag_3)
    dates_all, converted_delta_all, mag_all, dot_size_all, lon_all, lat_all = prep_for_interevent_plot(str_orig_all, tibet_orig_all, tibet_orig__all, lat_all, lon_all, dep_all, mag_all)

    ax2 = plt.subplot2grid((2, 4), (0, 0), colspan=3, rowspan=2)
    ax2.set_yscale('log')
    ax2.set_xlim([mindate, maxdate])
    ax2.xaxis.set_major_locator(mpdates.YearLocator())
    ax2.xaxis.set_major_formatter(mpdates.DateFormatter('%Y'))
    ax2.xaxis.set_minor_locator(mpdates.MonthLocator())
    plt.scatter(dates_a, converted_delta_a, edgecolor="dodgerblue",
                alpha=0.7, s=50, marker='o', linewidths=2,
                facecolor='none', zorder=3, label='Cluster 1')
    ax2.scatter(dates_c, converted_delta_c, edgecolor="none",
                alpha=0.7, s=50, marker='X',
                facecolor='red', zorder=2, label='Cluster 2')
    ax2.scatter(dates_all, converted_delta_all, alpha=0.6, s=60, marker='+',
                facecolor='gray', zorder=1, label='Full catalog', linewidth=1.0)
    ax2.set_xlim([mindate, maxdate])
    ax2.set_ylabel('Interevent times (days)', fontsize=18, multialignment='center')
    ax2.set_ylim([0.01, 100])
    ax2.get_yaxis().set_label_coords(-0.09, 0.5)
    ax2.tick_params(bottom=True, top=True, left=True, right=True)
    ax2.set_xlabel(r'Time (UTC)', fontsize=18)
    plt.legend(loc='lower left', fontsize=16, bbox_to_anchor=(1, 0.1))
    #
    ax4 = plt.subplot2grid((2, 4), (0, 3), colspan=1, rowspan=1)
    ax4.scatter(lon_all, lat_all,
                alpha=0.6, s=60, marker='+', linewidth=1,
                facecolor='gray', zorder=1)
    ax4.scatter(lon_c, lat_c, edgecolor="none", linewidths=2,
                alpha=0.7, s=dot_size_c, marker='X',
                facecolor='red', zorder=2)
    ax4.scatter(lon_a, lat_a, edgecolor="dodgerblue", linewidths=2,
                alpha=0.7, s=dot_size_a, marker='o',
                label='Tibet 1D', facecolor='none', zorder=3)
    ax4.yaxis.set_label_position("right")
    ax4.yaxis.tick_right()
    ax4.set_xlim([83., 89.])
    ax4.set_ylim([26., 30.])
    plt.xticks(np.arange(83, 90, 1))
    ax4.tick_params(bottom=True, top=True, left=True, right=True)
    ax4.set_ylabel('Latitude ($^\circ$)',fontname='Courier', fontsize=18)
    ax4.set_xlabel('Longitude ($^\circ$)',fontname='Courier', fontsize=18)
    if save:
        plt.savefig(fig_name, bbox_inches="tight", format='png', dpi=300)
    if show:
        plt.show()
    return


def mag_vs_time_plus_cumulative(catalog, outfile_name, coordinates, show=True, save=True):
    import matplotlib.dates as mpdates
    import matplotlib
    import matplotlib.pyplot as plt
    from eqcorrscan.utils.mag_calc import calc_b_value, calc_max_curv
    from obspy import read_events, Catalog

    cat_1_ = cut_cat(catalog, coordinates[0:2])
    cat_2 = cut_cat(catalog, coordinates[2:4])
    cat_1 = cat_1_ + cat_2
    cat_1.events.sort(key=lambda x: x.preferred_origin().time)

    cat_3 = cut_cat(catalog, coordinates[4:6])
    cat_5_ = cut_cat(catalog, coordinates[8:10])
    cat_5 = Catalog()
    for ev in cat_5_:
        if ev not in cat_1 and ev not in cat_2 and ev not in cat_3:
            cat_5.append(ev)

    # South Tibet - Eastern Nepal
    str_orig_1, tibet_orig_1, tibet_orig__1, lat_1, lon_1, dep_1, mag_1 = get_cat_details(cat_1)
    # str_orig_2, tibet_orig_2, tibet_orig__2, lat_2, lon_2, dep_2, mag_2 = get_cat_details(cat_2)
    str_orig_3, tibet_orig_3, tibet_orig__3, lat_3, lon_3, dep_3, mag_3 = get_cat_details(cat_3)
    # All the catalog
    str_orig_all, tibet_orig_all, tibet_orig__all, lat_all, lon_all, dep_all, mag_all = get_cat_details(cat_5)
    str_orig_all_, tibet_orig_all_, tibet_orig__all_, lat_all_, lon_all_, dep_all_, mag_all_ = get_cat_details(catalog)

    def calc_cumulative(data):
        # evaluate the histogram
        values, base = np.histogram(data, bins=len(data))
        #evaluate the cumulative
        cumulative = np.cumsum(values)
        return cumulative

    cumul_1 = calc_cumulative(tibet_orig_1)
    # cumul_2 = calc_cumulative(tibet_orig_2)
    cumul_3 = calc_cumulative(tibet_orig_3)
    cumul_all_ = calc_cumulative(tibet_orig_all_)

    dot_size1 = []
    for m in mag_1:
        dot_size1.append(m*30)
    dot_size3 = []
    for m in mag_3:
        dot_size3.append(m*30)

    font = {'family': 'normal',
            'weight': 'normal',
            'size': 18}
    matplotlib.rc('font', **font)
    # Set figure width to 12 and height to 9
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 13
    fig_size[1] = 8
    plt.rcParams["figure.figsize"] = fig_size
    # Set path and figure name
    fig_name = outfile_name

    # Define minimum and maximum datetimes for plot
    mindate = mpdates.date2num(dt.datetime.strptime('20011001', '%Y%m%d'))
    maxdate = mpdates.date2num(dt.datetime.strptime('20030501', '%Y%m%d'))
    fig_name = outfile_name
    ln_coll_tibet_1 = create_lines(tibet_orig_1, mag_1, color='gray')
    ln_coll_tibet_3 = create_lines(tibet_orig_3, mag_3, color='gray')

    fig = plt.figure()
    ax1 = plt.subplot2grid((2, 4), (0, 0), colspan=3, rowspan=2)
    ax1.set_xlabel('Time (UTC)',fontname='Courier', fontsize=18)
    ax1.set_ylabel('Magnitude', color='black')
    ax1.set_xlim([mindate, maxdate])
    ax1.set_ylim([0, 5])

    ax1.tick_params(axis='y', labelcolor='black')
    ax1.xaxis.set_major_locator(mpdates.YearLocator())
    ax1.xaxis.set_major_formatter(mpdates.DateFormatter('%Y'))
    ax1.xaxis.set_minor_locator(mpdates.MonthLocator())
    ax1.add_collection(ln_coll_tibet_1)
    ax1.add_collection(ln_coll_tibet_3)
    ax1.scatter(tibet_orig_1, mag_1,  edgecolor='dodgerblue',alpha=0.7, s=50, marker='o',
                facecolor='none', zorder=3, linewidths=2, label='Cluster 1')
    ax1.scatter(tibet_orig_3, mag_3, edgecolor='none',alpha=0.7, s=50, marker='X',
                facecolor='red', zorder=3, linewidths=2, label='Cluster 2')
    ax1.scatter(tibet_orig_all, mag_all,edgecolor="k",alpha=0.6, s=60, marker='+',
                facecolor='gray', zorder=1, linewidth=1.0, label="Full catalog")
    plt.legend(loc='upper left', fontsize=16)
    #
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('Cumulative number', color='gray')  # we already handled the x-label with ax1
    ax2.plot(tibet_orig_1, cumul_1, zorder=2, color='black', linestyle='--', linewidth=2.5, label=' ')
    ax2.plot(tibet_orig_3, cumul_3, zorder=2, color='black', linestyle=':', linewidth=2.5, label=' ')
    ax2.plot(tibet_orig_all_, cumul_all_, zorder=2, color='black', linestyle='-', linewidth=2.5, label=' ')
    ax2.set_ylim([0, 420])
    ax2.set_xlim([mindate, maxdate])
    ax2.tick_params(axis='y', labelcolor='gray')
    plt.legend(loc='upper left', fontsize=16, bbox_to_anchor=(0.22, 1))
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    #
    ax4 = plt.subplot2grid((2, 4), (0, 3), colspan=1, rowspan=1)
    ax4.scatter(lon_all, lat_all, edgecolor="k",alpha=0.6, s=60, marker='+',
                facecolor='gray', zorder=1, linewidth=1.0)
    ax4.scatter(lon_1, lat_1, edgecolor='dodgerblue', alpha=0.7, s=60, marker='o',
                facecolor='none', zorder=3, linewidths=2)
    ax4.scatter(lon_3, lat_3, edgecolor='none', alpha=0.7, s=60, marker='X',
                facecolor='red', zorder=3, linewidths=2)
    ax4.yaxis.set_label_position("right")
    ax4.yaxis.tick_right()
    ax4.set_xlim([83., 89.])
    ax4.set_ylim([26., 30.])
    plt.xticks(np.arange(83, 90, 1))
    ax4.tick_params(bottom=True, top=True, left=True, right=True)
    ax4.set_ylabel('Latitude ($^\circ$)',fontname='Courier', fontsize=18)
    ax4.set_xlabel('Longitude ($^\circ$)',fontname='Courier', fontsize=18)
    if save:
        plt.savefig(fig_name, bbox_inches="tight", format='png', dpi=300)
    if show:
        plt.show()
    return

def calc_bvalues(mag, Mc, M_max, mag_steps, cdf):
    """"""
    x = []
    y = []
    for i, magnitude in enumerate(mag_steps):
        if magnitude >= Mc + 0.4 <= M_max:
            x.append(magnitude)
            y.append(cdf[i])
    fit = np.polyfit(x, np.log10(y), 1)
    fit_fn = np.poly1d(fit)
    return fit_fn, fit


def multi_mfd_plot(catalog_one, cat_3, cat, outfile_name='Fig_7.png'):
    # Calculations for each catalog
    mag_one = [event.magnitudes[-1].mag for event in catalog_one]
    Mc_one = round(calc_max_curv(mag_one, plotvar=False), 2)
    M_max_one = max(mag_one)
    mag_3 = [event.magnitudes[-1].mag for event in cat_3]
    Mc_3 = round(calc_max_curv(mag_3, plotvar=False), 2)
    M_max_3 = max(mag_3)
    mag = [event.magnitudes[-1].mag for event in cat]
    Mc = round(calc_max_curv(mag, plotvar=False), 2)
    M_max = max(mag)

    # Define name for output
    savefile = outfile_name
    # --------------------------------------------------------------------------- #
    fig, ax1 = plt.subplots()
    bins = np.arange(0.55, 4.55, 0.2)
    n, bins, patches = ax1.hist(mag, bins, histtype='step', color='gray',
                                alpha=0.2, linewidth=2, linestyle='-',
                                edgecolor='black', fill=True, label='Full catalog')
    n1, bins1, patches1 = ax1.hist(mag_one, bins, histtype='step',
                                   alpha=0.2, linewidth=2., linestyle='--',
                                   edgecolor='black', fill=False, label='Cluster 1')
    n3, bins3, patches3 = ax1.hist(mag_3, bins, histtype='step',
                                   alpha=0.2, linewidth=2., linestyle=':',
                                   edgecolor='black', fill=False, label='Cluster 3')
    ax1.set_ylabel('Frequency', fontname='Courier', fontsize=18)
    ax1.set_ylim([0, max(n) + 0.5 * max(n)])
    plt.xlabel('Magnitude', fontname='Courier', fontsize=18)

    # --------------------------------------------------------------------------- #
    counts = Counter(mag)
    cdf = np.zeros(len(counts))
    mag_steps = np.zeros(len(counts))
    for i, magnitude in enumerate(sorted(counts.keys(), reverse=True)):
        mag_steps[i] = magnitude
        if i > 0:
            cdf[i] = cdf[i - 1] + counts[magnitude]
        else:
            cdf[i] = counts[magnitude]
    fit_fn_all, fit_all = calc_bvalues(mag, Mc, M_max, mag_steps, cdf)
    mag2plot = [m for m in mag if m >= Mc + 0.4 <= M_max]
    # --------------------------------------------------------------------------- #
    counts_1 = Counter(mag_one)
    cdf_1 = np.zeros(len(counts_1))
    mag_steps_1 = np.zeros(len(counts_1))
    for i, magnitude in enumerate(sorted(counts_1.keys(), reverse=True)):
        mag_steps_1[i] = magnitude
        if i > 0:
            cdf_1[i] = cdf_1[i - 1] + counts_1[magnitude]
        else:
            cdf_1[i] = counts_1[magnitude]
    fit_fn_1, fit_1 = calc_bvalues(mag_one, Mc_one, M_max_one, mag_steps_1, cdf_1)
    mag2plot1 = [m for m in mag_one if m >= Mc_one + 0.4 <= M_max_one]
    # --------------------------------------------------------------------------- #
    counts_3 = Counter(mag_3)
    cdf_3 = np.zeros(len(counts_3))
    mag_steps_3 = np.zeros(len(counts_3))
    for i, magnitude in enumerate(sorted(counts_3.keys(), reverse=True)):
        mag_steps_3[i] = magnitude
        if i > 0:
            cdf_3[i] = cdf_3[i - 1] + counts_3[magnitude]
        else:
            cdf_3[i] = counts_3[magnitude]
    fit_fn_3, fit_3 = calc_bvalues(mag_3, Mc_3, M_max_3, mag_steps_3, cdf_3)
    mag2plot3 = [m for m in mag_3 if m >= Mc_3 + 0.4 <= M_max_3]
    # --------------------------------------------------------------------------- #
    ax2 = ax1.twinx()
    ax2.scatter(mag_steps, np.log10(cdf), edgecolor="k", alpha=0.5, s=50,
                marker='+', facecolor='black', zorder=1, linewidth=1.0)
    ax2.scatter(mag_steps_1, np.log10(cdf_1), edgecolor='dodgerblue',
                alpha=0.5, s=25, marker='o', facecolor='none',
                zorder=3, linewidths=2)
    ax2.scatter(mag_steps_3, np.log10(cdf_3), edgecolor='none',
                alpha=0.5, s=25, marker='X', facecolor='red',
                zorder=3, linewidths=2)
    ax2.set_ylabel('Log$_{10}$ of cumulative density', fontname='Courier',
                   fontsize=18)
    plt.xlim([0.5, max(mag) + 0.2])
    plt.ylim([min(np.log10(cdf)), max(np.log10(cdf)) + 0.5])

    ax2.plot(mag2plot, fit_fn_all(mag2plot), '-k', linewidth=2.5,
             label='Full catalog, b = ' + str(abs(fit_all[0]))[0:4] + '\nM$_C$ = ' + str(
                 min(mag2plot)) + ' (N = ' + str(len(mag)) + ')')
    ax2.plot(mag2plot1, fit_fn_1(mag2plot1), '--', color='dodgerblue', linewidth=2.5,
             label='Cluster 1, b = ' + str(abs(fit_1[0]))[0:4] + '\nM$_C$ = ' + str(min(mag2plot1)) + ' (N = ' + str(
                 len(mag_one)) + ')')
    ax2.plot(mag2plot3, fit_fn_3(mag2plot3), ':', color='red', linewidth=2.5,
             label='Cluster 2, b = ' + str(abs(fit_3[0]))[0:4] + '\nM$_C$ = ' + str(min(mag2plot3)) + ' (N = ' + str(
                 len(mag_3)) + ')')
    ax2.set_ylabel('Log$_{10}$ of cumulative density', fontname='Courier', fontsize=18)
    plt.legend(loc=1, fontsize=16)
    plt.savefig(savefile, bbox_inches="tight", format='jpg', dpi=300)
    plt.show()

