# MAGqual

## 

## MAGqual Set-up

### Initial installation

MAGqual requires only Conda and Snakemake installed in order to run as it will handle all other software installation. 

`conda create -c conda-forge -c bioconda -n snakemake snakemake`
`conda activate snakemake`

### CheckM database
If you already have the CheckM database downloaded you can specify the location using the parameter `checkm_db` to skip the download, otherwise MAGqual will download the required databases for CheckM for you (this will be the most recent version which is dated 2015-01-16).

### Bakta database 
If no Bakta database location is provided MAGqual will automatically download the lightweight Bakta database (as the full database is large and can take a long time to download). 
However, for more accurate MAG annotation we recommend downloading the full database (from [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7669534.svg)](https://doi.org/10.5281/zenodo.7669534) following the instructions in the [Bakta documentation](https://bakta.readthedocs.io/en/latest/BAKTA.html#database-download)) and specifying the location for MAGqual using the parameter `bakta_db`. This database can then be use for each subsequent MAGqual run.