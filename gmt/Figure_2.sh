#######################################################################################################################
# Description: Map showing the deep earthquake events in the European Alps...
#
# Konstantinos Michailos
# Lausanne
# August 2020
#######################################################################################################################
# ------------------------------------------------------------------------------------------------------------------- #
# Output name
out=frontiers_manu_figure_2.eps
# ------------------------------------------------------------------------------------------------------------------- #
# Define stuffz (area plotted, size of letters, etc)
gmt set FORMAT_GEO_MAP D
gmt set FORMAT_GEO_MAP D
gmt set FONT_ANNOT_PRIMARY Helvetica
gmt set FONT_ANNOT_PRIMARY 8
gmt set FONT_LABEL Helvetica
gmt set LABEL_FONT_SIZE 7
gmt set MAP_FRAME_TYPE plain
# Map boundaries
north=30.0
south=26.0
east=90.0
west=83.05
# Basemap projection
proj='-JM6i'
gmt makecpt -Cgray -Z -T0/9000/500 -I > topo.cpt
# ------------------------------------------------------------------------------------------------------------------- #
echo Make basemap...
gmt pscoast -W1/0.05 -Dl $proj -R$west/$east/$south/$north -K -Y1 -B2WSen -P > $out
# ------------------------------------------------------------------------------------------------------------------- #
echo Using this clipped grid...
gmt grdimage -R -J files/tibet.80.93.26.35.3sec.filled.grd -Chim.cpt -O -K >> $out
# ------------------------------------------------------------------------------------------------------------------- #
gmt pscoast -W1/0.05 -Df -J -R -K -O  -P -N1/0.05p,black -L89/29.2/30/100+l+u >> $out
# ------------------------------------------------------------------------------------------------------------------- #
echo Plot country names...
gmt pstext -R -J -O -K  -F+f6p,Helvetica,black+jBL+a0 -Gwhite >> $out << END
83.2 27 INDIA
83.1 29.0 NEPAL
84.0 29.5 CHINA
89.5 28 BHUTAN
89.0 24.0 BANGLADESH
END
# Main clusters
gmt psxy -R -J -Wthin,black -O -K  >> $out << END
86.3 27.6
88.4 27.6
88.4 28.85
86.3 28.85
86.3 27.6
END
gmt psxy -R -J files/him/thrusts.gmt -Wgray28 -Ggray28 -W.70p -Sf0.5c/0.03i+l+t -O -K >> $out
gmt psxy -R -J files/him/normal_faults.gmt -W.70p -Wgray28 -Gblack -Sf0.5c/0.01i+l+b -O -K >> $out
gmt psxy -R -J files/him/dextral_faults.gmt -W.70p -Sf1c/0.1i+r+s+o1 -Gblack -Wgray28 -O -K >> $out
# -=================================================================================================================- #
echo Plot seismic stations...
awk '{print $4, $3}' files/sta_HIMNT.txt |
    gmt psxy -R -J -Si.2 -W0.5p -Gwhite -O -K -t20>> $out
awk '{print $4, $3}' files/sta_HiCLIMB.txt |
    gmt psxy -R -J -St.2 -W0.5p -Gwhite  -O -K -t20 >> $out
#awk '{print $4, $3}' ../files/sta_HiCLIMB_not_used.txt |
#    gmt psxy -R -J -Si.2 -W0.5p,white -O -K  >> $out
awk '{print $4, $3}' files/sta_bhutan_pilot.txt |
    gmt psxy -R -J -Si.2 -W0.5p -Gwhite -t20 -O -K  >> $out
awk '{print $4, $3}' files/sta_IC.txt |
    gmt psxy -R -J -Si.2 -W0.5p -Gwhite -O -K  >> $out
# -=================================================================================================================- #
# ------------------------------------------------------------------------------------------------------------------- #
# Create cpt
gmt makecpt -Cviridis -T40/110/5 > seis.cpt
# ------------------------------------------------------------------------------------------------------------------- #
# -=================================================================================================================- #
echo Plotting seismicity data...
# < 40 km depths with hq locations
awk '{print $1, $2, 3}' files/shallow_hq.dat | gmt psxy -S+i -i0,1,2s0.01 -W.7,black \
-R -J -B -O -K >> $out
gmt pstext -R -J -O -K -F+f6p,Helvetica,gray20+jBL+a0 -Gwhite -W0.5,black  >> $out << END
83.5 27.57 MFT
89.2 27.1 DCFZ
88.0 28.6 1
86.0 27.0 2
END
awk '{print $1, $2, $4}' files/deep_lq.dat | gmt psxy -Sc -i0,1,2s0.07 -W.25,black \
-R -J -B -O -K  >> $out
awk '{print $1, $2, $3, $4}' files/All_events.dat | gmt psxy -i0,1,2,3s0.07 -Sc -R -J \
-O -K  -W.25 -Cseis.cpt >> $out
# -=================================================================================================================- #
# ------------------------------------------------------------------------------------------------------------------- #
echo Plot scale...
gmt psscale -Dx0.25/1+o0/0.1i+w1.2i/0.08i+h+e -R -J -Cseis.cpt -Bx20f10 -Bx+l"Hypocentral depth (km)" -O -K >> $out
# ------------------------------------------------------------------------------------------------------------------- #
# Plot mount Everest location for a reference point
gmt psxy -R -J -Sx.3 -W1.5p,black -Gwhite -O -K  >> $out << END
86.9250 27.9881
END
gmt pstext -R -J -O -K -F+f7p,Helvetica,gray10+jBL+a0 >> $out << END
84.7 26.2 45 mm/yr
END
# Direction is in degrees from north
gmt psxy -SV0.15i+ea -Wthin -GBlack -O -K -R -J >> $out << END
84.9 26.3 22.1 1.0
END
#---------------------------------------------------------------------------------------------------------- #
#---------------------------------------------------------------------------------------------------------- #
echo Plot focal mechanisms
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||  #
echo Plotting Udayapur earthquake...
# 1988 Udayapur Chen and Kao 1996
gmt psxy -R -J -Wblack -W0.5p -O -K  >> $out << END
86.62 26.75
86.62 26.25
END
gmt psxy -R -J -Ss.15 -W0.3p -O -K -Cseis.cpt >> $out << END
86.62 26.75 46
END
gmt psmeca -R -J -Sa0.3 -Zseis.cpt -O -K >> $out << END
86.62 26.25 46 239 54 2 6.6 0 0
END
gmt pstext -R -J -O -K  -F+f5p,Helvetica,black+jBL+a0 -Gwhite >> $out << END
#86.0 26.05 M6.6 1988 Udayapur
86.58 26.05 IV
END
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||  #
#1986 Chen et al 1988
gmt psxy -R -J -Wblack -W0.5p -O -K  >> $out << END
86.567 28.654
87 29
END
gmt psxy -R -J -Ss.1 -W0.3p -Cseis.cpt -O -K  >> $out << END
86.567 28.654 85
END
gmt psmeca -R -J -Sa0.3 -Zseis.cpt -O -K >> $out << END
87 29 85 140 46 -163 5.5 0 0
END
gmt pstext -R -J -O -K  -F+f5p,Helvetica,black+jBL+a0 -Gwhite >> $out << END
#87.12 29 M5.5 1986
87.12 29 III
END
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||  #
#1991 Zhu and Helmberger 1996
gmt psxy -R -J -Wblack -W0.5p -O -K  >> $out << END
87.984 27.878
88.7 28.2
END
gmt psxy -R -J -Ss.1 -W0.3p -Cseis.cpt -O -K  >> $out << END
87.984 27.878 70
END
gmt psmeca -R -J -Sa0.3 -Zseis.cpt -O -K >> $out << END
88.7 28.2 70 112 82 -179 4.7 0 0
END
gmt pstext -R -J -O -K  -F+f5p,Helvetica,black+jBL+a0 -Gwhite >> $out << END
#88.82 28.2 M4.7 1991
88.82 28.2 V
END
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||  #
#1992 Zhu and Helmberger 1996
gmt psxy -R -J -Wblack -W0.5p -O -K  >> $out << END
87.958 28.151
88.45 28.5
END
gmt psxy -R -J -Ss.1 -W0.3p -Cseis.cpt -O -K  >> $out << END
87.958 28.151 80
END
gmt psmeca -R -J -Sa0.3 -Zseis.cpt -O -K >> $out << END
88.45 28.5 80  46 66 -22  4.9 0 0
END
gmt pstext -R -J -O -K -F+f5p,Helvetica,black+jBL+a0 -Gwhite >> $out << END
#88.56 28.5 M4.9 1992
88.56 28.5 VI
END
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||  #
# 1973, 1976 Molnar and Chen 1983; Chen et al 1981
gmt pstext -R -J -O -K  -F+f5p,Helvetica,black+jBL+a0 -Gwhite >> $out << END
#89.22 29.566 M4.9 I # 1973
#89.64 29.782 M5.4 II # 1976
89.22 29.566 I
89.64 29.782 II
END
gmt psmeca -R -J -Sa0.3 -Zseis.cpt -O -K >> $out << END
89.141 29.566 85 220 60 -24  4.9 0 0
89.544 29.782 90 215 52 -68  5.4 0 0
END
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||  #
#2005 GCMT 200503262032A XIZANG
gmt psxy -R -J -Wblack -W0.5p -O -K  >> $out << END
87.95	28.08
88.45 28.3
END
gmt psxy -R -J -Ss.1 -W0.3p -Cseis.cpt -O -K  >> $out << END
87.95	28.08 70
END
gmt psmeca -R -J -Sa0.3 -Zseis.cpt -O -K >> $out << END
88.45 28.3	70	109	62	179	4.7	0	0
END
gmt pstext -R -J -O -K -F+f5p,Helvetica,black+jBL+a0 -Gwhite >> $out << END
#88.56 28.3 M4.7 2005
88.56 28.3 X
END
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||  #
#2010 GCMT 201002260442A XIZANG
gmt psxy -R -J -Wblack -W0.5p -O -K  >> $out << END
86.77	28.41
87.4 28.8
END
gmt psxy -R -J -Ss.1 -W0.3p -Cseis.cpt -O -K  >> $out << END
86.77	28.41 85
END
gmt psmeca -R -J -Sa0.3 -Zseis.cpt -O -K >> $out << END
87.4 28.8	84.5	12	69	-16	5.1	0	0
END
gmt pstext -R -J -O -K -F+f5p,Helvetica,black+jBL+a0 -Gwhite >> $out << END
#87.4 28.9 M5.1 2010
87.4 28.9 XI
END
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||  #
echo Plotting gcmt
# 1980, 2003 (111980A, 032503D) 2011 201109181240A
gmt psmeca -R -J -Sa0.3 -Zseis.cpt -O -K >> $out << END
#88.35	27.44	46	216	72	-12	6.9	0 0 #2011 Shikim eq
#89.82	26.92	56	40	70	-21	5.4	0	0 #2003
#89.05	27.42	44	209	51	-2	6.2	0	0 #1980
88.35	27.44	46	216	72	-12	6.9	0 0
89.82	26.92	56	40	70	-21	5.4	0	0
89.05	27.42	44	209	51	-2	6.2	0	0
END
gmt pstext -R -J -O -K -F+f5p,Helvetica,black+jBL+a0 -Gwhite >> $out << END
#88.35	27.54 M6.9 2011
#89.62	27.0 M5.4 2003
#89.15 27.42 M6.2 1980
88.35	27.54 XII
89.66	27.0 IX
89.15 27.42 VII
END
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||  #
echo Alvizuri fm Event 20020508175659380 M 3.70
# (2002-05-08T17:56:59 UTC)
gmt psxy -R -J -Wblack -W0.5p -O -K  >> $out << END
86.4885  28.5825
86.4885  28.95
END
gmt psxy -R -J -Ss.1 -W0.3p -Cseis.cpt -O -K  >> $out << END
86.4885  28.5825 75.9
END
gmt psmeca -R -J -Sa0.3 -Zseis.cpt -O -K >> $out << END
86.4885  28.95 75.9 215 75 25  3.7 0 0
END
gmt pstext -R -J -O -K -F+f5p,Helvetica,black+jBL+a0 -Gwhite >> $out << END
#86.4885  29.05 M3.7 2002
86.4885  29.05 VII
END
# de la Torre 2007
gmt psmeca -R -J -Sa0.3 -Zseis.cpt -O -K >> $out << END
#87.50 28.18 80  83  49 -135 3.3 0 0
#87.68 28.13 76  86  88  166 3.4 0 0
#86.52 28.52 84 125  65 -168 3.6 0 0 same as alvizuri
#87.75 27.81 62 333  31 -124 3.7 0 0
#87.93 28.21 90 181  76   30 3.6 0 0
#87.63 28.11 60  89  76 -136 3.6 0 0
#86.58 28.46 77  79  49  -21 3.9 0 0
END
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||  #
echo de la Torre
gmt psxy -R -J -Wblack -W0.5p -O -K  >> $out << END
87.50 28.18
87.7  28.6
END
gmt psxy -R -J -Ss.1 -W0.3p -Cseis.cpt -O -K  >> $out << END
87.50 28.18 80
END
gmt psmeca -R -J -Sa0.3 -Zseis.cpt -O -K >> $out << END
87.7  28.6 80  83  49 -135 3.3 0 0
END
gmt pstext -R -J -O -K -F+f5p,Helvetica,black+jBL+a0 -Gwhite >> $out << END
87.65  28.667 XIII
END
##
gmt psxy -R -J -Wblack -W0.5p -O -K  >> $out << END
87.68 28.13
88.2 28.6
END
gmt psxy -R -J -Ss.1 -W0.3p -Cseis.cpt -O -K  >> $out << END
87.68 28.13 76
END
gmt psmeca -R -J -Sa0.3 -Zseis.cpt -O -K >> $out << END
88.2  28.6 76  86  88  166 3.4 0 0
END
gmt pstext -R -J -O -K -F+f5p,Helvetica,black+jBL+a0 -Gwhite >> $out << END
88.2  28.667 XIV
END
##
gmt psxy -R -J -Wblack -W0.5p -O -K  >> $out << END
87.75 27.81
87.55  27.55
END
gmt psxy -R -J -Ss.1 -W0.3p -Cseis.cpt -O -K  >> $out << END
87.75 27.81 62
END
gmt psmeca -R -J -Sa0.3 -Zseis.cpt -O -K >> $out << END
87.55  27.55 62 333  31 -124 3.7 0 0
END
gmt pstext -R -J -O -K -F+f5p,Helvetica,black+jBL+a0 -Gwhite >> $out << END
87.55  27.42 XV
END
##
gmt psxy -R -J -Wblack -W0.5p -O -K  >> $out << END
87.93 28.21
88.45 28.7
END
gmt psxy -R -J -Ss.1 -W0.3p -Cseis.cpt -O -K  >> $out << END
87.93 28.21 90
END
gmt psmeca -R -J -Sa0.3 -Zseis.cpt -O -K >> $out << END
88.45 28.7 90 181 76 30 3.6 0 0
END
gmt pstext -R -J -O -K -F+f5p,Helvetica,black+jBL+a0 -Gwhite >> $out << END
88.52 28.75 XVI
END
##
gmt psxy -R -J -Wblack -W0.5p -O -K  >> $out << END
86.58 28.46
86.4 28.2
END
gmt psxy -R -J -Ss.1 -W0.3p -Cseis.cpt -O -K  >> $out << END
86.58 28.46 77
END
gmt psmeca -R -J -Sa0.3 -Zseis.cpt -O -K >> $out << END
86.4 28.2 77  79  49  -21 3.9 0 0
END
gmt pstext -R -J -O -K -F+f5p,Helvetica,black+jBL+a0 -Gwhite >> $out << END
86.3 28.07 XVIII
END
###
gmt psxy -R -J -Wblack -W0.5p -O -K  >> $out << END
87.63 28.11
87.95  28.6
END
gmt psxy -R -J -Ss.1 -W0.3p -Cseis.cpt -O -K  >> $out << END
87.63 28.11 60
END
gmt psmeca -R -J -Sa0.3 -Zseis.cpt -O -K >> $out << END
87.95  28.6 60  89  76 -136 3.6 0 0
END
gmt pstext -R -J -O -K -F+f5p,Helvetica,black+jBL+a0 -Gwhite >> $out << END
87.93  28.667 XVII
END
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||  #
gmt psmeca -R -J -Sm0.3 -Zseis.cpt -O -K >> $out << END
89.4094  26.7404   24.00  -0.680  -0.996   1.677   0.864  -0.449   0.078   21   89.4094  26.7404
89.9439  26.1699   18.00   1.328  -4.385   3.058   0.112   1.843   1.311   21   89.9439  26.1699 COMMENT
88.9414  27.2020   21.00  -0.345  -3.710   4.055   1.185  -1.288   1.702   21   88.9414  27.2020 COMMENT
89.9392  26.1547   18.00   1.155  -6.035   4.881  -0.152   2.496   2.592   21   89.9392  26.1547 COMMENT
89.9392  26.1621   18.00   0.270  -1.030   0.760   0.007   0.555   0.519   22   89.9392  26.1621 COMMENT
89.6006  26.5733   18.00   0.186  -4.431   4.246   0.097  -0.165   0.483   22   89.6006  26.5733 COMMENT
88.7203  27.3376   21.00   1.359  -1.294  -0.065  -0.180  -0.173   0.290   23   88.7203  27.3376 COMMENT
END
echo Create legend...
gmt set FONT_ANNOT_PRIMARY 8
gmt pslegend <<END -R -J -Dx3.71i/4.35i+w0i/0.0i/TC -C0.1i/0.1i -F+gwhite+pthin -P -O -K >> $out
G -0.05i
H 9 Earthquake locations
D0.1i 0.5p
S .04i c .2c springgreen4 0.5p,black 0.18i High-quality (depth > 40km)
G .07i
S .04i c .2c white 0.5p,black 0.18i Low-quality (depth > 40km)
#S .04i c .11c white 0.5p,dodgerblue 0.18i Carpenter (2010)
G .07i
S .04i + .11c black 0.5p 0.18i High-quality (depth < 40km)
END
# Scale for the magnitudes
gmt psxy -i0,1,2,3s0.07 -Sc -R -J -O -K  -W.25 -Cseis.cpt >> $out << END
83.9 26.85  190.0 5.0
83.9 26.80  190.0 4.0
83.9 26.76  190.0 3.0
83.9 26.73  190.0 2.0
83.9 26.71  190.0 1.0
END
gmt pstext -R -J -O -K  -F+f6p,Helvetica,gray10+jBL+a0  >> $out << END
83.99 26.85  M=5
#83.92 26.80  M=4.0
#83.92 26.76  M=3.0
#83.92 26.73  M=2.0
83.99 26.69  M=1
END
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
# Zoomed map top left
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
# ------------------------------------------------------------------------------------------------------------------- #
# Inset boundaries
north=28.85
south=27.6
east=88.4
west=86.3
# Basemap projection
proj='-JM3.5.i'
# ------------------------------------------------------------------------------------------------------------------- #
echo Make basemap...
gmt pscoast -W1/0.05 -Dl $proj -R$west/$east/$south/$north -K -O -Y11 -X-0.01 -B0.5WSen -P >> $out
# ------------------------------------------------------------------------------------------------------------------- #
echo Using this clipped grid...
gmt grdimage -R -J files/tibet.80.93.26.35.3sec.filled.grd -Chim.cpt -O -K >> $out
# ------------------------------------------------------------------------------------------------------------------- #
gmt pscoast -W1/0.05 -Df -J -R -K -O  -P -N1/0.05p,black -L88/28.7/30/40+l+u >> $out
# ------------------------------------------------------------------------------------------------------------------- #
awk '{print $1, $2, $4}' files/deep_lq.dat | gmt psxy -Sc -i0,1,2s0.07 -W.25,black \
-R -J -B -O -K  >> $out
# All_events
awk '{print $1, $2, $3, $4}' files/All_events.dat | gmt psxy -i0,1,2,3s0.07 -Sc -R -J \
-O -K  -W.25 -Cseis.cpt >> $out
awk '{print $1, $2, 3}' files/shallow_hq.dat | gmt psxy -S+i -i0,1,2s0.01 -W.7,black \
-R -J -B -O -K >> $out
##---------------------------------------------------------------------------------------------------------- #
## Plot cross section surface trace lines
start_lon='86.35'
start_lat='28.65'
end_lon='88.0'
end_lat='28.2'
width='50'

gmt psxy << END -R -J -O -W1.,black,- -K>> $out
$start_lon $start_lat
$end_lon $end_lat
END
gmt pstext -R -J -D0/0.23 -O -K -F+f6p,Helvetica,gray10+jB -TO -Gwhite -W0.1 >> $out << END
$start_lon $start_lat A
END
gmt pstext -R -J -D0/0.23 -O -K -F+f6p,Helvetica,gray10+jB -TO -Gwhite -W0.1 >> $out << END
$end_lon $end_lat A'
END

start_lon_per='87'
start_lat_per='28.15'
end_lon_per='87.3'
end_lat_per='28.7'
width='60'

gmt psxy << END -R -J -O -W1.,black,- -K>> $out
$start_lon_per $start_lat_per
$end_lon_per $end_lat_per
END
gmt pstext -R -J -D0/0.23 -O -K -F+f6p,Helvetica,gray10+jB -TO -Gwhite -W0.1 >> $out << END
$start_lon_per $start_lat_per B
END
gmt pstext -R -J -D0/0.23 -O -K -F+f6p,Helvetica,gray10+jB -TO -Gwhite -W0.1 >> $out << END
$end_lon_per $end_lat_per B'
END
##---------------------------------------------------------------------------------------------------------- #
##---------------------------------------------------------------------------------------------------------- #
## Plot cross section surface trace lines
start_lon='87.7'
start_lat='28.2'
end_lon='88.25'
end_lat='27.65'
width='50'
gmt psxy << END -R -J -O -W1.,black,- -K>> $out
$start_lon $start_lat
$end_lon $end_lat
END
gmt pstext -R -J -D0/0.23 -O -K -F+f6p,Helvetica,gray10+jB -TO -Gwhite -W0.1 >> $out << END
$start_lon $start_lat C
$end_lon $end_lat C'
END
start_lon_per='87.7'
start_lat_per='27.75'
end_lon_per='88.25'
end_lat_per='28.1'
width='150'

gmt psxy << END -R -J -O -W1.,black,- -K>> $out
$start_lon_per $start_lat_per
$end_lon_per $end_lat_per
END
gmt pstext -R -J -D0/0.23 -O -K -F+f6p,Helvetica,gray10+jB -TO -Gwhite -W0.1 >> $out << END
$start_lon_per $start_lat_per D
$end_lon_per $end_lat_per D'
END
##---------------------------------------------------------------------------------------------------------- #
# Plot mount Everest location for a reference point
gmt psxy -R -J -Sx.3 -W1.5p,black -Gwhite -O -K  >> $out << END
86.9250 27.9881
END

# ------------------------------------------------------------------------------------------------------------------- #
gmt psxy -R -J -T -O >> $out
gmt psconvert -Tf -A $out
evince ${out%.*}.pdf
# ------------------------------------------------------------------------------------------------------------------- #
# Delete temporary files
rm frontiers_manu_figure_2.eps seis.cpt topo.cpt