#######################################################################################################################
# Description: Cross-sections of seismicity
#
# Konstantinos Michailos
# Lausanne
# August 2020
#######################################################################################################################
# ------------------------------------------------------------------------------------------------------------------- #
# Output name
out=frontiers_manu_figure_3AB.eps
# ------------------------------------------------------------------------------------------------------------------- #
# Define stuffz (area plotted, size of letters, etc)
gmt set FORMAT_GEO_MAP D
gmt set FORMAT_GEO_MAP D
gmt set FONT_ANNOT_PRIMARY Helvetica
gmt set FONT_ANNOT_PRIMARY 10
gmt set FONT_LABEL 12
gmt set MAP_FRAME_TYPE plain
gmt psbasemap -R -JX18/20 -P -B -K > $out
# ------------------------------------------------------------------------------------------------------------------- #
# Create projections
start_lon='86.35'
start_lat='28.65'
end_lon='88.0'
end_lat='28.2'
width='50'
awk '{print $1, $2, $3, $4, $5}' files/NLL_locations.dat | gmt project -C$start_lon/$start_lat -E$end_lon/$end_lat\
 -W-$width/$width -Q -Fpz > projection1.dat
awk '{print $1, $2, $3, $4, $5}' files/HDD_locations.dat | gmt project -C$start_lon/$start_lat -E$end_lon/$end_lat\
 -W-$width/$width -Q -Fpz > projection1_hdd.dat
# ------------------------------------------------------------------------------------------------------------------- #
start_lon_per='87'
start_lat_per='28.15'
end_lon_per='87.3'
end_lat_per='28.7'
width_per='60'
awk '{print $1, $2, $3, $4, $5}' files/NLL_locations.dat | gmt project -C$start_lon_per/$start_lat_per -E$end_lon_per/$end_lat_per\
 -W-$width_per/$width_per -Q -Fpz > projection2.dat
 awk '{print $1, $2, $3, $4, $5}' files/HDD_locations.dat | gmt project -C$start_lon_per/$start_lat_per -E$end_lon_per/$end_lat_per\
 -W-$width_per/$width_per -Q -Fpz > projection2_hdd.dat
# ------------------------------------------------------------------------------------------------------------------- #
awk '{print($1,$2,$3)}' projection1_hdd.dat | gmt psxy -Sci -i0,1,2s0.025 -W.5,black  -R0/170/40/100.5 -JX15/-5 \
-Bxafg1000+l"Distance (km)" -By10+l"Depth (km)" -Y14 -X1 -BwSnE -O -K >> $out
awk '{print($1,$2,$4 * 1.455)}' projection1_hdd.dat | gmt psxy -R -J -O -K -Ey+p7p,lightgray,- >> $out
awk '{print($1,$2,$3)}' projection1_hdd.dat | gmt psxy -Sci -i0,1,2s0.025 -W.1,black -Gdarkgray  -R -J -O -K  >> $out
awk '{print($1,$2,$4)}' projection1.dat | gmt psxy -W1,red -Gred -R -J -O -K -Ey >> $out
awk '{print($1,$2,$3)}' projection1.dat | gmt psxy -Sci -i0,1,2s0.025 -W.5,black -R -J -O -K  >> $out
# ------------------------------------------------------------------------------------------------------------------- #
gmt pstext -R -JX -O -K -F+f14p,Helvetica,gray10+jB  -TO -Gwhite -W0.1 >> $out << END
4 48 A
160 48 A'
END
gmt pstext -R -JX -O -K -F+f8p,Helvetica,gray10+jB   >> $out << END
4 95 Swath: 50 km
END
# ------------------------------------------------------------------------------------------------------------------- #
awk '{print($1,$2,$3)}' projection2_hdd.dat | gmt psxy -Sci -i0,1,2s0.025 -W.5,black  -R0/80.5/40/100.5 -JX7/-5 \
-Bxafg1000+l"Distance (km)" -By10+l"Depth (km)" -Y-7 -X0 -BwSnE -O -K >> $out
awk '{print($1,$2,$4 * 1.455)}' projection2_hdd.dat | gmt psxy -R -J -O -K -Ey+p7p,lightgray,- >> $out
awk '{print($1,$2,$3)}' projection2_hdd.dat | gmt psxy -Sci -i0,1,2s0.025 -W.1,black -Gdarkgray  -R -J -O -K  >> $out
awk '{print($1,$2,$4)}' projection2.dat | gmt psxy -W1,red -Gred -R -J -O -K -Ey >> $out
awk '{print($1,$2,$3)}' projection2.dat | gmt psxy -Sci -i0,1,2s0.025 -W.5,black -R -J -O -K  >> $out
# ------------------------------------------------------------------------------------------------------------------- #
gmt pstext -R -JX -O -K -F+f14p,Helvetica,gray10+jB  -TO -Gwhite -W0.1 >> $out << END
4 48 B
70 48 B'
END
gmt pstext -R -JX -O -K -F+f8p,Helvetica,gray10+jB   >> $out << END
4 95 Swath: 60 km
END
# ------------------------------------------------------------------------------------------------------------------- #
gmt psxy -R -J -T -O >> $out
gmt psconvert -Tf -A $out
evince ${out%.*}.pdf
# ------------------------------------------------------------------------------------------------------------------- #
# Delete temporary files
rm frontiers_manu_figure_3AB.eps projection2_hdd.dat projection2.dat projection1_hdd.dat projection1.dat
