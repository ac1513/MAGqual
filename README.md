# MAGqual
MAGqual is a command line tool that will evaluate the quality of metagenomic bins and generate required metadata in line with the MIMAG standards (as outlined in [Bowers et al. 2017](https://www.nature.com/articles/nbt.3893)). 

## MAGqual Set-Up

Here is a step-by-step guide on how to install MAGqual from the GitHub repository at https://github.com/ac1513/MAGqual.

### Step 1: Clone the MAGqual repository

Open a command-line interface (CLI) or terminal on your computer or computer cluster. Change to the directory where you want to install MAGqual. Then, run the following command to clone the MAGqual repository from GitHub:

```
git clone https://github.com/ac1513/MAGqual.git
```
This will create a copy of the MAGqual repository on your computer.

### Step 2: Install dependencies

* Conda (package manager)
* Snakemake v.6.17.1 or higher (workflow manager)

In order to run MAGqual, Conda and Snakemake are required.

Miniconda can be installed following the instructions for your system in the [Miniconda documentation](https://docs.conda.io/en/latest/miniconda.html). 

Once Miniconda is installed, Snakemake can be installed following the instructions in the [Snakemake documentation](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html). 

MAGqual will handle the other dependancies while the pipeline is running through the use of Conda environments.

## Running MAGqual 

### Quick start quide 

Once you have created an environment with Snakemake in you can run MAGqual with the following command:

```python MAGqual.py --asm assembly.fa --bins bins_dir/```

* `--asm` corresponds to the location of the assembly used to generate the metagenome bins 
* `--bins` is the location of the directory containing the metagenomic bins to be run through MAGqual (in fasta format)

#### Full Help documentation:
```
usage: MAGqual.py [-h] -a ASSEMBLY -b BINDIR [-p PREFIX] [-j JOBS] [--cluster CLUSTER] [--checkmdb CHECKMDB] [--baktadb BAKTADB]

Required: python MAGqual.py -a/--asm assembly.fa -b/--bins bins_dir/ 

options:
  -h, --help            show this help message and exit
  -a ASSEMBLY, --asm ASSEMBLY
                        location of the assembly used to generate the bins (Required)
  -b BINDIR, --bins BINDIR
                        location of the directory containing the bins to run through MAGqual (required)
  -p PREFIX, --prefix PREFIX
                        prefix for the MAGqual run, default = MAGqual_YYYYMMDD
  -j JOBS, --jobs JOBS  The number of cores to be used or if running on a HPC the number of jobs
                        to be run concurrently, default = 1
  --cluster CLUSTER     OPTIONAL: The type of cluster to run MAGqual on a HPC system (available options: slurm), 
                        don’t use if running MAGqual locally.
  --checkmdb CHECKMDB   OPTIONAL: location of a ready installed database for CheckM
  --baktadb BAKTADB     OPTIONAL: location of a ready installed database for Bakta, note must be v5.0 or above
```
### Additional Options

* `-p / --prefix`: Specify a prefix for the output files (Default: MAGqual_YYYYMMDD)
* `-j / --jobs`: If running locally this is the number of cores to be used, if using the --cluster option and running on a HPC queue this corresponds to the number of jobs to be run concurrently, (Default:1)

### Optional

#### CheckM and Bakta databases
MAGqual will handle the installation of both CheckM and Bakta, however if you have previously used either of these tools it is possible to speed up the process and save file space by specifying the location of pre-downloaded databases. 

##### CheckM database
If you already have the CheckM database downloaded you can specify the location using the parameter `--checkm_db` to skip the download, otherwise MAGqual will download the required databases for CheckM for you (this will be the most recent version which is dated 2015-01-16).

##### Bakta database 
If no Bakta database is provided MAGqual will automatically download the lightweight Bakta database (as the full database is large and can take a long time to download). NOTE: MAGqual uses Bakta v1.7.0 which requires a database version of > 5.0.  
However, for more accurate MAG annotation we recommend downloading the full database (from [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7669534.svg)](https://doi.org/10.5281/zenodo.7669534) following the instructions in the [Bakta documentation](https://bakta.readthedocs.io/en/latest/BAKTA.html#database-download)) and specifying the location for MAGqual using the parameter `--bakta_db`. This database can then be use for each subsequent MAGqual run. 

### Running on a computing cluster
MAGqual can be integrated into a HPC queuing system using the following option: 
* `--cluster`: Current option: `slurm`, run MAGqual with options configured to run on a HPC computer cluster with queuing architecture.  
Currently the only queuing system available is `slurm`, however it is possible to run MAGqual on different queuing systems through the Snakemake framework - see [Running on different queuing architechture](#running-on-different-queuing-architechture) below.

## For those familiar with Snakemake

It is possible (and encouraged) to further tweak MAGqual parameters if you are familiar with Snakemake. 
### Running on different queuing architechture

### Additional Notes:
MAGqual is compatible with Python 3.10.1 or higher.
Make sure to clone the MAGqual repository regularly to get the latest updates and bug fixes.
Refer to the MAGqual documentation in the GitHub repository for more information on how to use the tool and interpret the results.
Congratulations! You have successfully installed MAGqual on your system. 
