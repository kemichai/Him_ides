"""
Code to reproduce Figures from the submitted
manuscript on Frontiers on the intermediate depth seismicity.

: location: Chavannes-pres-renens
: time: August 2021
: author: KM
"""

from obspy import read_events, read, Stream, Catalog, read_inventory
import matplotlib
import matplotlib.pyplot as plt
import os

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


def cut_cat(catalog, coordinates):
    """"""
    from shapely.geometry import Polygon, Point
    import numpy as np
    from obspy import Catalog

    latitudes = coordinates[0]
    longitudes = coordinates[1]

    p= Polygon((np.asarray(list(zip(latitudes, longitudes)))))
    rest_cat = Catalog()
    cut_catalog = Catalog()
    for event in catalog:
        ev_lat = event.origins[-1].latitude
        ev_lon = event.origins[-1].longitude
        if p.contains(Point(ev_lat, ev_lon)):
            cut_catalog.append(event)
        else:
            rest_cat.append(event)
    return cut_catalog, rest_cat


def _finalise_figure(fig, **kwargs):  # pragma: no cover
    """
    Internal function to wrap up a figure.
    {plotting_kwargs}
    """
    import matplotlib.pyplot as plt

    title = kwargs.get("title")
    show = kwargs.get("show", True)
    save = kwargs.get("save", False)
    savefile = kwargs.get("savefile", "EQcorrscan_figure.png")
    return_fig = kwargs.get("return_figure", False)
    size = kwargs.get("size", (15.5, 12.5))
    fig.set_size_inches(size)
    if title:
        fig.suptitle(title)
    if save:
        fig.savefig(savefile, bbox_inches="tight")
        Logger.info("Saved figure to {0}".format(savefile))
    if show:
        plt.show(block=True)
    if return_fig:
        return fig
    fig.clf()
    plt.close(fig)
    return None


def obspy_3d_plot(inventory, catalog, **kwargs):
    """
    Plot obspy Inventory and obspy Catalog classes in three dimensions.

    :type inventory: obspy.core.inventory.inventory.Inventory
    :param inventory: Obspy inventory class containing station metadata
    :type catalog: obspy.core.event.catalog.Catalog
    :param catalog: Obspy catalog class containing event metadata
    {plotting_kwargs}

    :returns: :class:`matplotlib.figure.Figure`

    .. rubric:: Example:

    >>> from obspy.clients.fdsn import Client
    >>> from obspy import UTCDateTime
    >>> from eqcorrscan.utils.plotting import obspy_3d_plot
    >>> client = Client('IRIS')
    >>> t1 = UTCDateTime(2012, 3, 26)
    >>> t2 = t1 + 86400
    >>> catalog = client.get_events(starttime=t1, endtime=t2, latitude=-43,
    ...                             longitude=170, maxradius=5)
    >>> inventory = client.get_stations(starttime=t1, endtime=t2, latitude=-43,
    ...                                 longitude=170, maxradius=10)
    >>> obspy_3d_plot(inventory=inventory, catalog=catalog) # doctest: +SKIP

    .. plot::

        from obspy.clients.fdsn import Client
        from obspy import UTCDateTime
        from eqcorrscan.utils.plotting import obspy_3d_plot
        client = Client('IRIS')
        t1 = UTCDateTime(2012, 3, 26)
        t2 = t1 + 86400
        catalog = client.get_events(starttime=t1, endtime=t2, latitude=-43,
                                    longitude=170, maxradius=5)
        inventory = client.get_stations(starttime=t1, endtime=t2, latitude=-43,
                                        longitude=170, maxradius=10)
        obspy_3d_plot(inventory=inventory, catalog=catalog)
    """
    nodes = []
    for ev in catalog:
        nodes.append((ev.origins[-1].latitude,
                      ev.origins[-1].longitude,
                      ev.origins[-1].depth / 1000))
    # Will plot borehole instruments at elevation - depth if provided
    all_stas = []
    for net in inventory:
        for sta in net:
            if len(sta.channels) > 0:
                all_stas.append((sta.latitude, sta.longitude,
                                 sta.elevation / 1000 -
                                 sta.channels[0].depth / 1000))
            else:
                Logger.warning('No channel information attached, '
                               'setting elevation without depth')
                all_stas.append((sta.latitude, sta.longitude,
                                 sta.elevation / 1000))
    fig = threeD_seismplot(
        stations=all_stas, nodes=nodes, **kwargs)
    return fig

def threeD_seismplot(stations, nodes, **kwargs):
    """
    Plot seismicity and stations in a 3D, movable, zoomable space.

    Uses matplotlibs Axes3D package.

    :type stations: list
    :param stations:
        list of one tuple per station of (lat, long, elevation), with up
        positive.
    :type nodes: list
    :param nodes:
        list of one tuple per event of (lat, long, depth) with down positive.
    {plotting_kwargs}

    :returns: :class:`matplotlib.figure.Figure`

    .. Note::
        See :func:`eqcorrscan.utils.plotting.obspy_3d_plot` for example output.
    """
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    stalats, stalongs, staelevs = zip(*stations)
    evlats, evlongs, evdepths = zip(*nodes)
    # Cope with +/-180 latitudes...
    _evlongs = []
    for evlong in evlongs:
        if evlong < 0:
            evlong = float(evlong)
            evlong += 360
        _evlongs.append(evlong)
    evlongs = _evlongs
    _stalongs = []
    for stalong in stalongs:
        if stalong < 0:
            stalong = float(stalong)
            stalong += 360
        _stalongs.append(stalong)
    stalongs = _stalongs
    staelevs = [-1 * depth for depth in staelevs]
    evdepths = [1 * depth for depth in evdepths]

    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(evlats, evlongs, evdepths, marker="o", c=evdepths, s=50,
               label='Hypocenters', edgecolor='k', alpha=0.6, cmap='viridis')

    ax.scatter(stalats, stalongs, staelevs, marker="v", c="r",
               label='Stations')
    ax.set_ylabel("Longitude (deg)")
    ax.set_xlabel("Latitude (deg)")
    ax.set_zlabel("Depth (km)")
    ax.get_xaxis().get_major_formatter().set_scientific(False)
    ax.get_yaxis().get_major_formatter().set_scientific(False)
    plt.legend()
    plt.gca().invert_zaxis()
    # plt.gca().invert_yaxis()
    plt.gca().invert_xaxis()

    fig = _finalise_figure(fig=fig, **kwargs)  # pragma: no cover
    return fig

def obspy_3d_plot_2cats(inventory, catalog1, catalog1_rest, catalog2, **kwargs):
    """"""
    nodes1 = []
    for ev in catalog1:
        if ev.origins[-1].depth / 1000 >= 40. and ev.origins[-1].depth / 1000 < 100.:
            nodes1.append((ev.origins[-1].latitude,
                          ev.origins[-1].longitude,
                          ev.origins[-1].depth / 1000,
                          ev.magnitudes[-1].mag))
    nodes1_rest = []
    for ev in catalog1_rest:
        nodes1_rest.append((ev.origins[-1].latitude,
                      ev.origins[-1].longitude,
                      ev.origins[-1].depth / 1000,
                      ev.magnitudes[-1].mag))
    nodes2 = []
    for ev in catalog2:
        nodes2.append((ev.origins[-1].latitude,
                       ev.origins[-1].longitude,
                       ev.origins[-1].depth / 1000,
                       ev.magnitudes[-1].mag))
    # Will plot borehole instruments at elevation - depth if provided
    all_stas = []
    for net in inventory:
        for sta in net:
            if len(sta.channels) > 0:
                all_stas.append((sta.latitude, sta.longitude,
                                 sta.elevation / 1000 -
                                 sta.channels[0].depth / 1000))
            else:
                Logger.warning('No channel information attached, '
                               'setting elevation without depth')
                all_stas.append((sta.latitude, sta.longitude,
                                 sta.elevation / 1000))
    fig = threeD_seismplot_2cats(
        stations=all_stas, nodes1=nodes1, nodes1_rest=nodes1_rest, nodes2=nodes2, **kwargs)
    return fig

def threeD_seismplot_2cats(stations, nodes1, nodes1_rest, nodes2, **kwargs):
    """
    Plot seismicity and stations in a 3D, movable, zoomable space.

    Uses matplotlibs Axes3D package.

    :type stations: list
    :param stations:
        list of one tuple per station of (lat, long, elevation), with up
        positive.
    :type nodes: list
    :param nodes:
        list of one tuple per event of (lat, long, depth) with down positive.
    {plotting_kwargs}

    :returns: :class:`matplotlib.figure.Figure`

    .. Note::
        See :func:`eqcorrscan.utils.plotting.obspy_3d_plot` for example output.
    """
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    stalats, stalongs, staelevs = zip(*stations)
    evlats, evlongs, evdepths, evmags = zip(*nodes1)
    evlats_rest, evlongs_rest, evdepths_rest, evmags_rest = zip(*nodes1_rest)

    # Cope with +/-180 latitudes...
    _evlongs = []
    for evlong in evlongs:
        if evlong < 0:
            evlong = float(evlong)
            evlong += 360
        _evlongs.append(evlong)
    evlongs = _evlongs
    _stalongs = []
    for stalong in stalongs:
        if stalong < 0:
            stalong = float(stalong)
            stalong += 360
        _stalongs.append(stalong)
    stalongs = _stalongs
    staelevs = [-1 * depth for depth in staelevs]
    evdepths = [1 * depth for depth in evdepths]

    evlats2, evlongs2, evdepths2, evmags2 = zip(*nodes2)
    # Cope with +/-180 latitudes...
    _evlongs2 = []
    for evlong2 in evlongs2:
        if evlong2 < 0:
            evlong2 = float(evlong2)
            evlong2 += 360
        _evlongs2.append(evlong2)
    evlongs2 = _evlongs2
    evdepths2 = [1 * depth for depth in evdepths2]

    dot_size = []
    for m in evmags:
        dot_size.append(m*50)
    dot_size2 = []
    for m in evmags2:
        dot_size2.append(m*50)

    fig = plt.figure()
    ax = Axes3D(fig)
    p=ax.scatter(evlats, evlongs, evdepths, marker="o", c=evdepths, s=dot_size,
               label='Cluster 1', edgecolor='k', alpha=0.9, cmap='viridis')
    ax.scatter(evlats_rest, evlongs_rest,evdepths_rest,
                alpha=0.6, s=60, marker='+', linewidth=1,
                facecolor='gray', zorder=1, label='Rest of catalog')
    ax.scatter(evlats2, evlongs2, evdepths2, marker="o", c='k', s=dot_size2,
               label='Diehl et al. 2017', edgecolor='k', alpha=0.4)
    # Sikkim eq gcmt
    ax.scatter(27.44, 88.35, 46, marker="*", c='orange', s=700,
               label='M6.9 Sikkim (GCMT)', edgecolor='k', alpha=0.9)
    # Sikkim eq gcmt
    ax.scatter(27.8, 88.15, 50, marker="*", c='orange', s=700,
               label='M6.9 Sikkim (USGS)', edgecolor='gray', alpha=0.9)

    ax.scatter(stalats, stalongs, staelevs, marker="v", c="r", s=100,
               label='Stations')

    cbar = fig.colorbar(p, ax=ax, shrink=0.3, aspect=10, ticks=[40, 50, 60, 70, 80, 90, 100])
    cbar.set_label('Hypocentral depth (km)')
    # ax.plot(moho_lat, moho_lon, moho_dep)
    ax.set_ylabel("Longitude (deg)", )
    ax.set_xlabel("Latitude (deg)")
    ax.xaxis.labelpad = 15
    ax.yaxis.labelpad = 15
    ax.set_zlabel("Depth (km)")
    ax.get_xaxis().get_major_formatter().set_scientific(False)
    ax.get_yaxis().get_major_formatter().set_scientific(False)
    plt.legend(fontsize=15)
    plt.gca().invert_zaxis()
    # plt.gca().invert_yaxis()
    plt.gca().invert_xaxis()


    fig = _finalise_figure(fig=fig, **kwargs)  # pragma: no cover
    return fig


# Get working directory
work_dir = os.getcwd()

# Read catalog
cat_path = (work_dir + '/quakeml/')
cat_name = 'Himalayan_Intermediate_depth_earthquake_catalog_Michailos_et_al_2021.xml'
print(f'Reading catalog stored on: "{cat_path}",'
      f'\nUnder the name: "{cat_name}"')
cat = read_events(cat_path + cat_name)
print(f'Read catalog"{cat_name}"!!!')

td_cat = read_events(work_dir + '/quakeml/' + 'Diehl_et_al_2017.xml')

# See read_cat_cut_cat for adjusting or details
coord_DCF_IDEs = [28, 28, 25.8, 26.3, 28.4, 29.0],[86.0, 87.4, 90.0, 90.2, 88.2, 86.0]
cat_1, cat_rest = cut_cat(cat, coord_DCF_IDEs[0:2])
cat_td, cat_td_ = cut_cat(td_cat, coord_DCF_IDEs[0:2])


sta_path = (work_dir + '/metadata/')
inv = read_inventory(sta_path + '*xml')

# only DCF and IDEs
obspy_3d_plot_2cats(catalog1=cat_1, catalog1_rest=cat_rest, catalog2=cat_td, inventory=inv)
