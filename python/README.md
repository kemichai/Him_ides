# README #


Quick Summary:

This folder contains the python codes for reproducing the results and plots from the manuscript titled
"Spatio-Temporal Evolution of Intermediate-Depth 
Seismicity Beneath the Himalayas: Implications for 
Metamorphism and Tectonics" published in 
Frontiers [link](https://www.frontiersin.org/articles/10.3389/feart.2021.742700/full).


### Requirements:
The simplest way to run the codes is using anaconda and a virtual environment.
This way you won't damage your system python.  
If you do not already have an anaconda or miniconda install go to the
conda-install instructions and get yourself either of the two [conda-install](https://docs.conda.io/en/latest/miniconda.html).

Once you have installed conda, create a new environment with the following dependencies using:
```bash
conda config --add channels conda-forge
conda create -n him_seis python=3.7 eqcorrscan=0.4.2 ipython pip obspy matplotlib numpy pandas pyproj shapely basemap
conda activate him_seis
python Figures_5-9.py
```
