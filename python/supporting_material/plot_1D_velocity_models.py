"""
Plot 1D velocity models.


: Lausanne
: September 2020
: Konstantinos Michailos
"""
import platform
from obspy import read_events, read, Stream, Catalog, read_inventory
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from obspy.geodetics import degrees2kilometers

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


# Scatter plot points
Vp_nepal = [5.5, 5.7, 6.3, 8.0]
Vp_tibet = [5.8, 5.8, 6.9, 8.6]
Vp_grad = [5.8, 5.8, 5.8, 6.4, 6.9, 7.6, 8.1, 8.6]
Vp_iasp = [5.8, 6.5, 8.0, 8.1]
Vs_nepal = [3.2, 3.2, 3.7, 4.5]
Vs_tibet = [3.3, 3.5, 4.0, 4.9]
Vs_grad = [3.2, 3.5, 3.5, 3.7, 3.9, 4.4, 4.7, 4.9]
Vs_iasp = [3.4, 3.8, 4.4, 4.5]
depth_limits_nepal = [0.0, 3.0, 23.0, 55.0]
depth_limits_tibet = [0.0, 3.0, 40.0, 70.0]
depth_limits_grad = [0.0, 3.0, 40.0, 46.0, 52.0, 58.0, 64.0, 70.0]
depth_limits_iasp = [0.0, 20.0, 35.0, 71.0]

# Line points
l_Vp_nepal = [5.5, 5.5, 5.7, 5.7, 6.3, 6.3, 8.0, 8.0]
l_Vs_nepal = [3.2, 3.2, 3.2, 3.2, 3.7, 3.7, 4.5, 4.5]
l_depth_limits_nepal = [0.0, 3.0, 3.0, 23.0, 23.0, 55.0, 55.0, 80.0]

l_Vp_iasp = [5.8, 5.8, 6.5, 6.5, 8.0, 8.0, 8.1, 8.1]
l_Vs_iasp = [3.4, 3.4, 3.8, 3.8, 4.4, 4.4, 4.5, 4.5]
l_depth_limits_iasp = [0.0, 20.0, 20.0, 35.0, 35.0, 71.0, 71.0, 80.0]

l_Vp_tibet = [5.8, 5.8, 5.8, 5.8, 6.9, 6.9, 8.6, 8.6]
l_Vs_tibet = [3.3, 3.3, 3.5,3.5, 4.0,4.0, 4.9, 4.9]
l_depth_limits_tibet = [0.0, 3.0, 3.0, 40.0, 40.0, 70.0, 70.0, 80.0]

l_Vs_grad = [3.2, 3.2, 3.5, 3.5, 3.5, 3.5, 3.7, 3.7, 3.9, 3.9, 4.4, 4.4, 4.7, 4.7, 4.9, 4.9]
l_Vp_grad = [5.8, 5.8, 5.8, 5.8, 5.8, 5.8, 6.4, 6.4, 6.9, 6.9, 7.6, 7.6, 8.1, 8.1, 8.6, 8.6]
l_depth_limits_grad = [0.0, 3.0, 3.0, 4.0, 40.0, 46.0, 46.0, 52.0, 52.0, 58.0, 58.0, 64.0, 64.0, 70.0, 70.0, 80.0]

l_Vp_Vs_nepal = []
for i, vp in enumerate(l_Vp_nepal):
        vpvs = vp/l_Vs_nepal[i]
        l_Vp_Vs_nepal.append(vpvs)
l_Vp_Vs_tibet = []
for i, vp in enumerate(l_Vp_tibet):
        vpvs = vp/l_Vs_tibet[i]
        l_Vp_Vs_tibet.append(vpvs)
l_Vp_Vs_grad = []
for i, vp in enumerate(l_Vp_grad):
        vpvs = vp/l_Vs_grad[i]
        l_Vp_Vs_grad.append(vpvs)
l_Vp_Vs_iasp = []
for i, vp in enumerate(l_Vp_iasp):
        vpvs = vp/l_Vs_grad[i]
        l_Vp_Vs_iasp.append(vpvs)


outfile_name = '1D_velocity_models.png'
fig_name = '/home/kmichall/Desktop/' + outfile_name

ax1 = plt.subplot2grid((1, 1), (0, 0), colspan=1)
ax1.plot(l_Vp_iasp, l_depth_limits_iasp,linestyle='-',
         color='black', linewidth=3., label='IASP91', zorder=1)
ax1.plot(l_Vp_nepal, l_depth_limits_nepal,linestyle='-.',
         color='dodgerblue', linewidth=3., label='Nepal 1D', zorder=1)
ax1.plot(l_Vp_tibet, l_depth_limits_tibet,linestyle='--',
         color='red', linewidth=3., label='Tibet 1D', zorder=1)
ax1.plot(l_Vp_grad, l_depth_limits_grad,linestyle=':',
         color='orange', linewidth=3, label='Gradational')
#
ax1.plot(l_Vs_iasp, l_depth_limits_iasp, linestyle='-',
         color='black', linewidth=3., zorder=1)
ax1.plot(l_Vs_nepal, l_depth_limits_nepal, linestyle='-.',
         color='dodgerblue', linewidth=3., zorder=1)
ax1.plot(l_Vs_tibet, l_depth_limits_tibet, linestyle='--',
         color='red', linewidth=3., zorder=1)
ax1.plot(l_Vs_grad, l_depth_limits_grad, linestyle=':',
         color='orange', linewidth=3, zorder=1)
ax1.legend(loc="upper right", markerscale=1., scatterpoints=1,
           fontsize=16, framealpha=1, borderpad=1)
ax1.set_ylabel(r'Depth (km)', fontname='Courier' ,fontsize=18)
ax1.set_xlabel(r'Velocity (km/s)',fontname='Courier' ,fontsize=18)
# plt.axhline(0, color='black')
ax1.set_xlim([2.0, 10.0])
ax1.set_ylim([0, 80])
plt.gca().invert_yaxis()
# ax1.xaxis.tick_top()
# ax1.xaxis.set_label_position('top')
ax1.tick_params(bottom=True, top=True, left=True, right=True)
plt.savefig(fig_name, format='png', dpi=300)
plt.show()


# Vp/Vs
# ax2 = plt.subplot2grid((1, 3), (0, 2))
# ax2.set_xlim([1.0, 9.0])
# ax2.set_ylim([0, 80])
# plt.gca().invert_yaxis()
# ax2.set_xlim([1.5, 2.3])
# ax2.xaxis.tick_top()
# ax2.set_xlabel(r'Vp/Vs',fontname='Courier' ,fontsize=18)
# ax2.xaxis.set_label_position('top')
# ax2.set_yticklabels([])
# ax2.xaxis.set_ticks(np.arange(1.4, 2.2, 0.2))
# plt.axvline(1.77, color='black')
# ax2.plot(l_Vp_Vs_nepal, l_depth_limits_nepal, linestyle='-.', color='dodgerblue', linewidth=3.)
# ax2.plot(l_Vp_Vs_iasp, l_depth_limits_iasp, linestyle='-', color='black', linewidth=3.)
# ax2.plot(l_Vp_Vs_tibet, l_depth_limits_tibet, linestyle='--', color='red', linewidth=3.)
# ax2.plot(l_Vp_Vs_grad, l_depth_limits_grad, linestyle=':', color='orange', linewidth=3.)
# ax2.tick_params(bottom=True, top=True, left=True, right=True)
# plt.tight_layout()
# plt.savefig(fig_name, format='png', dpi=300)
# plt.show()
