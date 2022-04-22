#######################################################################################################################
# Description: Map showing the seismic networks used
#
# Konstantinos Michailos
# Lausanne
# August 2020
#######################################################################################################################
# ------------------------------------------------------------------------------------------------------------------- #
# Output name
out=frontiers_manu_figure_1.eps
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
west=83.0
proj='-JM6i'
# ------------------------------------------------------------------------------------------------------------------- #
echo Make basemap...
gmt pscoast -W1/0.05 -Dl $proj -R$west/$east/$south/$north -K -Y1 -B2WSen -P > $out
# ------------------------------------------------------------------------------------------------------------------- #
echo Plot topo....
gmt grdimage -R -J files/tibet.80.93.26.35.3sec.filled.grd -Chim.cpt -O -K >> $out
# ------------------------------------------------------------------------------------------------------------------- #
gmt pscoast -W1/0.05 -Df -J -R -K -O  -P -N1/0.05p,black -L89/29.2/30/100+l+u >> $out

gmt psxy -R -J files/him/thrusts.gmt -Wgray28 -Ggray28 -W.70p -Sf0.5c/0.03i+l+t -O -K >> $out
gmt psxy -R -J files/him/normal_faults.gmt -W.70p -Wgray28 -Gblack -Sf0.5c/0.01i+l+b -O -K >> $out
gmt psxy -R -J files/him/dextral_faults.gmt -W.70p -Sf1c/0.1i+r+s+o1 -Gblack -Wgray28 -O -K >> $out
# ----------
# Create cpt
gmt makecpt -Cviridis -T40/110/10  > seis.cpt
awk '{if ($9 > 50) print $8, $7, 2}' files/catalogs/HIMNT_cat.txt | gmt psxy -R -J -O -K -h1 -Sc -i0,1,2+s0.03 \
-t0 -W0.5p,red >> $out
awk '{if ($4 > 50) print $3, $2, 2}' files/catalogs/NSCdeepEQS_cat_candidates.txt | gmt psxy -R -J -O -K -h1 -Sx -i0,1,2+s0.03 \
-t0 -W0.5p,black >> $out
# ----------------
echo Plot scales...
gmt psscale -Dx0.2/1.6+o0/0i+w1.3i/0.08i+h+e -R -J -Chim.cpt -Bx2000f1000 -By+l"Topography (m)" \
 -O -K --FONT_ANNOT_PRIMARY=7p >> $out
gmt psscale -Dx0.2/0.7+o0/0i+w1.3i/0.08i+h+e -R -J  -Cseis.cpt -Bx20f10 -By+l"Hypocentral depth (km)" \
-O -K --FONT_ANNOT_PRIMARY=7p >> $out
# ----------------
echo Plot country names...
gmt pstext -R -J -O -K  -F+f6p,Helvetica,black+jBL+a0 -Gwhite >> $out << END
83.2 27 INDIA
83.1 29.0 NEPAL
84.0 29.5 CHINA
89.5 28 BHUTAN
89.0 24.0 BANGLADESH
END
# -=================================================================================================================- #
# ------------------------------------------------------------------------------------------------------------------- #
echo Plot focal mechanisms
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||  #
echo Plotting Udayapur earthquake...
# 1988 Udayapur (Chen and Kao 1996)
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
# 1986 (Chen et al 1988)
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
# 1991 (Zhu and Helmberger, 1994)
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
# 1992 (Zhu and Helmberger, 1996)
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
# 1973, 1976 (Molnar and Chen 1983; Chen et al 1981)
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
# 2005 GCMT 200503262032A XIZANG
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
# 2010 GCMT 201002260442A XIZANG
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
echo Ploting Alvizuri fm 20020508175659380 M 3.70
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
# Dielh et al. fms
gmt psmeca -R -J -Sm0.3 -Zseis.cpt -O -K >> $out << END
89.4094  26.7404   24.00  -0.680  -0.996   1.677   0.864  -0.449   0.078   21   89.4094  26.7404
89.9439  26.1699   18.00   1.328  -4.385   3.058   0.112   1.843   1.311   21   89.9439  26.1699 COMMENT
88.9414  27.2020   21.00  -0.345  -3.710   4.055   1.185  -1.288   1.702   21   88.9414  27.2020 COMMENT
89.9392  26.1547   18.00   1.155  -6.035   4.881  -0.152   2.496   2.592   21   89.9392  26.1547 COMMENT
89.9392  26.1621   18.00   0.270  -1.030   0.760   0.007   0.555   0.519   22   89.9392  26.1621 COMMENT
89.6006  26.5733   18.00   0.186  -4.431   4.246   0.097  -0.165   0.483   22   89.6006  26.5733 COMMENT
88.7203  27.3376   21.00   1.359  -1.294  -0.065  -0.180  -0.173   0.290   23   88.7203  27.3376 COMMENT
92.4051  27.5387   12.00   4.312  -7.793   3.481   6.100  -3.799  -1.128   20   92.4051  27.5387 COMMENT
91.3724  26.0667   15.00   0.143  -0.629   0.486  -0.760   1.449   0.527   21   91.3724  26.0667 COMMENT
92.4497  27.1611    9.00   0.265  -1.336   1.071  -0.180   1.722   1.686   21   92.4497  27.1611 COMMENT
90.9386  27.5188   21.00   0.965  -0.287  -0.679   2.834   0.552  -0.566   21   90.9386  27.5188 COMMENT
92.3784  27.6804   12.00   1.757  -2.747   0.990   0.234  -0.875   1.258   21   92.3784  27.6804 COMMENT
92.6848  27.5985    9.00   2.470  -3.562   1.092   2.712  -1.428  -0.526   21   92.6848  27.5985 COMMENT
90.3520  26.6192   21.00   1.345  -6.059   4.714   0.493  -2.403  -0.837   21   90.3520  26.6192 COMMENT
91.2771  27.2825   15.00   2.390  -6.432   4.042   0.999  -3.264  -7.495   21   91.2771  27.2825 COMMENT
90.2721  26.0376   15.00   0.037  -3.233   3.196   1.633   0.725   7.689   21   90.2721  26.0376 COMMENT
92.7158  27.6231    9.00   0.474  -0.929   0.455   0.445  -0.535  -0.119   22   92.7158  27.6231 COMMENT
90.2555  28.0158   70.00  -0.008  -0.970   0.979  -0.384   0.054   0.004   22   90.2555  28.0158 COMMENT
92.5423  26.7081   42.00   1.225  -1.196  -0.029  -0.137   0.362  -0.406   22   92.5423  26.7081 COMMENT
92.5501  26.6835   42.00   1.230  -1.356   0.126   0.332  -0.500  -0.611   22   92.5501  26.6835 COMMENT
92.5296  27.3003   12.00   0.206  -1.254   1.048  -0.952   0.567  -0.908   22   92.5296  27.3003 COMMENT
92.5083  27.0763   42.00   1.021   1.449  -2.470   3.152  -0.687   3.280   22   92.5083  27.0763 COMMENT
END
# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||  #
echo de la Torre et al 2007
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
##
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
# -=================================================================================================================- #
echo Plot seismic stations...
awk '{print $4, $3}' files/sta_HiCLIMB.txt |
    gmt psxy -R -J -St.25 -W0.5p -Gdodgerblue -O -K -t10 >> $out
awk '{print $4, $3}' files/sta_HiCLIMB_not_used.txt |
    gmt psxy -R -J -St.25 -W0.5p,dodgerblue -O -K  >> $out
awk '{print $4, $3}' files/sta_HIMNT.txt |
    gmt psxy -R -J -Si.22 -W0.5p -Gred -O -K -t0>> $out
awk '{print $4, $3}' files/sta_bhutan_pilot.txt |
    gmt psxy -R -J -Si.22 -W0.5p -Gorange -t0 -O -K  >> $out
awk '{print $4, $3}' files/sta_IC.txt |
    gmt psxy -R -J -Si.22 -W0.5p -Gdarkorange2 -O -K  >> $out
# -=================================================================================================================- #
# ------------------------------------------------------------------------------------------------------------------- #
echo Create legend...
gmt set FONT_ANNOT_PRIMARY 8
gmt pslegend <<END -R -J -Dx3.01i/4.i+w0i/0.0i/TC -C0.1i/0.1i -F+gwhite+pthin -P -O -K >> $out
G -0.05i
H 9 Seismic networks
D0.1i 0.5p
G .04i
S .04i i .11i red 0.2p 0.18i HIMNT (2001.09 - 2002.12)
G .07i
S .04i i .11i orange 0.2p 0.18i BPE (2002.01 - 2003.12)
G .07i
S .04i t .11i dodgerblue 0.2p 0.18i Hi-CLIMB (2002.09 - 2005.08)
G .07i
G 0.05i
H 9 Candidate intermediate depth events
D0.1i 0.5p
S .04i c .11c white 0.5p,red 0.18i Monsalve et al. (2006)
G .07i
#S .04i c .11c white 0.5p,dodgerblue 0.18i Carpenter (2010)
#G .07i
S .04i x .11c red 0.5p 0.18i NEMRC
END

gmt pstext -R -J -O -K -F+f6p,Helvetica,gray20+jBL+a0 -Gwhite -W0.5,black  >> $out << END
83.5 27.57 MFT
89.1 27. DCFZ
END

gmt pstext -R -J -O -K -F+f7p,Helvetica,gray10+jBL+a0 >> $out << END
83.72 26.8 45 mm/yr
END
# direction is in degrees from north
gmt psxy -SV0.15i+ea -Wthin -GBlack -O -K -R -J >> $out << END
84 26.9 22.1 1.0
END

# 1 to 4 stands for -1 to 4
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

# Plot mount Everest location for a reference point
gmt psxy -R -J -Sx.3 -W1.5p,black -Gwhite -O -K  >> $out << END
86.9250 27.9881
END

# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| #
# Inset (top left)
# ------------------------------------------------------------------------------------------------------------------- #
# Inset boundaries
north=40.0
south=25.0
east=100.0
west=70.0
# Basemap projection
proj='-JM2.75i'
gmt pscoast -W1/0.05 -Dl $proj -R$west/$east/$south/$north -K -O -X0 -Y10.25 -B10WseN  -P >> $out
# ------------------------------------------------------------------------------------------------------------------- #
echo Using this clipped grid ....
gmt grdimage -R -J files/tibet.70.100.25.40.0.5min.grd -Chim.cpt -O -K >> $out
# ------------------------------------------------------------------------------------------------------------------- #
#gmt pscoast -W1/0.05 -Df -J -R -K -O -Sazure1 -P -N1/0.05p,black -L75/28/29/500+l+u >> $out
# NO borders
gmt pscoast -W1/0.05 -Df -J -R -K -O -P -L75/28/29/500+l+u >> $out
gmt psxy -R -J files/him/thrusts.gmt -Wlightred -Glightred -W0.5p -Sf0.6c/0.01i+l+t -O -K >> $out
gmt psxy -R -J files/him/normal_faults.gmt -W.0p -Wdodgerblue -Gdodgerblue -Sf0.5c/0.01i+l+b -O -K >> $out
gmt psxy -R -J files/him/dextral_faults.gmt -W.0p -Sf1c/0.1i+r+s+o1 -Ggray20 -Wgray20 -O -K >> $out
#gmt psxy -R -J ../files/him/sinistral_faults.gmt -W.8p -Sf1c/0.1i+l+s+o1 -Gblack -O -K >> $out
gmt pstext -R -J -O -K  -F+f7p,Helvetica,black+jBL+a0 -Gwhite >> $out << END
78.4 26.0 INDIA
84.0 35.0 ASIA
END

gmt psxy -R -J files/him/dextral_faults.gmt -W.0p -Sf1c/0.1i+r+s+o1 -Ggray20 -Wgray20 -O -K >> $out
gmt pstext -R -J -O -K  -F+f6p,Helvetica,gray20+jBL+a0 -Gwhite >> $out << END
90.5 29 Study
90.5 28 Area
END
## Study area
gmt psxy -R -J -Wthin,black -O -K  >> $out << END
83 26
90 26
90 30.
83 30.
83 26
END
# ------------------------------------------------------------------------------------------------------------------- #
gmt psxy -R -J -T -O >> $out
gmt psconvert -Tf -A $out
evince ${out%.*}.pdf
# ------------------------------------------------------------------------------------------------------------------- #
# Delete temporary files
rm frontiers_manu_figure_1.eps seis.cpt