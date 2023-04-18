# MAGqual
MAGqual is a command line tool that will evaluate the quality of metagenomic bins and generate required metadata in line with the MIMAG standards (as outlined in [Bowers et al. 2017](https://www.nature.com/articles/nbt.3893)). 

## MAGqual Set-Up

Here is a step-by-step guide on how to install MAGqual from the GitHub repository at https://github.com/ac1513/MAGqual.

### Step 1: Clone the MAGqual repository

Open a command-line interface (CLI) or terminal on your computer or computer cluster. Change to the directory where you want to install MAGqual. Then, run the following command to clone the MAGqual repository from GitHub:

bash
```git clone https://github.com/ac1513/MAGqual.git```
This will create a copy of the MAGqual repository on your computer.

### Step 2: Install dependencies

* Conda (package manager)
* Snakemake v. 6.17 or higher

In order to run MAGqual, Conda and Snakemake (>v6.13) are required. 
Miniconda can be installed following the instructions in the [Anaconda documentation](https://docs.conda.io/en/latest/miniconda.html) and Snakemake can be installed following the instructions in the [Snakemake documentation](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html). 


## Running MAGqual 

### Quick start quide 
Once the dependencies are installed you can run MAGqual using the following command:

```python MAGqual.py```

### Optional: CheckM and Bakta databases
MAGqual will handle the installation of both CheckM and Bakta, however if you have previously used either of these tools it is possible to speed up the process and save file space by specifying the location of pre-downloaded databases. 

#### CheckM database
If you already have the CheckM database downloaded you can specify the location using the parameter `checkm_db` to skip the download, otherwise MAGqual will download the required databases for CheckM for you (this will be the most recent version which is dated 2015-01-16).

#### Bakta database 
If no Bakta database is provided MAGqual will automatically download the lightweight Bakta database (as the full database is large and can take a long time to download). NOTE: MAGqual uses Bakta v1.7.0 which requires a database version of > 5.0.
However, for more accurate MAG annotation we recommend downloading the full database (from [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7669534.svg)](https://doi.org/10.5281/zenodo.7669534) following the instructions in the [Bakta documentation](https://bakta.readthedocs.io/en/latest/BAKTA.html#database-download)) and specifying the location for MAGqual using the parameter `bakta_db`. This database can then be use for each subsequent MAGqual run. 

### Additional Notes:
MAGqual is compatible with Python 3.10.1 or higher.
Make sure to clone the MAGqual repository regularly to get the latest updates and bug fixes.
Refer to the MAGqual documentation in the GitHub repository for more information on how to use the tool and interpret the results.
Congratulations! You have successfully installed MAGqual on your system. 
