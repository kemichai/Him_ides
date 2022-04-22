# Him_ides - Himalayan Intermediate-Depth earthquakes

Description
------------
Set of codes (Python and GMT) for reproducing the results and plots from the manuscript titled
"Spatio-Temporal Evolution of Intermediate-Depth 
Seismicity Beneath the Himalayas: Implications for 
Metamorphism and Tectonics" published in 
Frontiers [link](https://www.frontiersin.org/articles/10.3389/feart.2021.742700/full).

How to run the codes
------------
The simplest way to run the Python codes is using anaconda and a virtual environment [conda-install link](https://docs.conda.io/en/latest/miniconda.html).

Once you have installed conda, create a new environment with the following dependencies using:
```bash
conda config --add channels conda-forge
conda create -n him_seis python=3.7 eqcorrscan=0.4.2 ipython pip obspy matplotlib numpy pandas pyproj shapely basemap
source activate him_seis
```

The GMT codes are written in GMT 5.


Note
------------
Codes here only reproduce our results in the specific publication.
For different applications the codes will need to be modified.


