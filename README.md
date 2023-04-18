# MAGqual

## 

## MAGqual Set-up
### MAGqual  

`git clone https://github.com/ac1513/MAGqual`


### Dependency installation
In order to run MAGqual, Conda and Snakemake (>v6.13) are required. 
Miniconda can be installed following the instructions in the [Anaconda documentation](https://docs.conda.io/en/latest/miniconda.html) and Snakemake can be installed following the instructions in the [Snakemake documentation](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html). 

### CheckM database
If you already have the CheckM database downloaded you can specify the location using the parameter `checkm_db` to skip the download, otherwise MAGqual will download the required databases for CheckM for you (this will be the most recent version which is dated 2015-01-16).

### Bakta database 
If no Bakta database is provided MAGqual will automatically download the lightweight Bakta database (as the full database is large and can take a long time to download). NOTE: MAGqual uses Bakta v1.7.0 which requires a database version of > 5.0.
However, for more accurate MAG annotation we recommend downloading the full database (from [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7669534.svg)](https://doi.org/10.5281/zenodo.7669534) following the instructions in the [Bakta documentation](https://bakta.readthedocs.io/en/latest/BAKTA.html#database-download)) and specifying the location for MAGqual using the parameter `bakta_db`. This database can then be use for each subsequent MAGqual run. 