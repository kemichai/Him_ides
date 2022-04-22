How to run the codes
--------------------
The simplest way to run the Python codes is using anaconda and a virtual environment [conda-install link](https://docs.conda.io/en/latest/miniconda.html).

Once you have installed conda, create a new environment with the following dependencies using:
```bash
conda config --add channels conda-forge
conda create -n him_seis python=3.7 eqcorrscan=0.4.2 ipython pip obspy matplotlib numpy pandas pyproj shapely basemap
source activate him_seis
```
Now you should be able to run the following and make the plots:
```python
# Run this command to create figures 5 to 9 of the publication
python Figures_5-9.py

# Run the following to create figure 10 of the publication
python Figure_10.py
```