# MAGqual

[![Snakemake](https://img.shields.io/badge/snakemake-≥6.17.1-brightgreen.svg?style=flat)](https://snakemake.readthedocs.io)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13384337.svg)](https://doi.org/10.5281/zenodo.13384337)

MAGqual is a command line tool built in Snakemake [(Mölder et al. 2021)](https://f1000research.com/articles/10-33/v2) that will evaluate the quality of metagenomic bins and generate required metadata in line with the MIMAG standards (as outlined in [Bowers et al. 2017](https://www.nature.com/articles/nbt.3893)). 

You can view an example [MAGqual output here](https://ac1513.github.io/MAGqual/MAGqual_manuscript_report.html).

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
### Additional Notes:
MAGqual is compatible with Python 3.10.1 or higher (as of April 2023).
Make sure to clone the MAGqual repository regularly to get the latest updates and bug fixes.
Refer to the MAGqual documentation in the GitHub repository for more information on how to use the tool and interpret the results.
Congratulations! You have successfully installed MAGqual on your system. 

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
                        path containing the directory containing the bins to run through MAGqual (Required)
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

* `-p / --prefix`: Specify a prefix for the output files (Default = MAGqual_YYYYMMDD)
* `-j / --jobs`: If running locally this is the number of cores to be used, if using the --cluster option and running on a HPC queue this corresponds to the number of jobs to be run concurrently, (Default = 1)

### Optional

#### CheckM and Bakta databases
MAGqual will handle the installation of both CheckM and Bakta, however if you have previously used either of these tools it is possible to speed up the process and save file space by specifying the location of pre-downloaded databases. 

##### CheckM database
If you already have the CheckM database downloaded you can specify the location using the parameter `--checkm_db` to skip the download, otherwise MAGqual will download the required databases for CheckM for you (this will be the most recent version which is dated 2015-01-16).

##### Bakta database 
If no Bakta database is provided MAGqual will automatically download the lightweight Bakta database (as the full database is large and can take a long time to download). NOTE: MAGqual uses Bakta v1.7.0 which requires a Bakta database version of > 5.0.  
However, for more accurate MAG annotation we recommend downloading the full database (from [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7669534.svg)](https://doi.org/10.5281/zenodo.7669534) following the instructions in the [Bakta documentation](https://bakta.readthedocs.io/en/latest/BAKTA.html#database-download)) and specifying the location for MAGqual using the parameter `--bakta_db`. This database can then be use for each subsequent MAGqual run. 

### Running on a computing cluster
MAGqual can be integrated into a HPC queuing system using the following option: 
* `--cluster`: Current option: `slurm`, run MAGqual with options configured to run on a HPC computer cluster with queuing architecture.  
The only queueing system integrated into MAGQual currently is `slurm`, however if this doesn't work for you it is possible to run MAGqual on different queuing systems through the Snakemake framework - see [Running on different queuing architechture](#running-on-different-queuing-architechture) below.

## For those familiar with Snakemake

It is possible (and encouraged) to further tweak MAGqual parameters if you are familiar with Snakemake.  
The config file: `config/config.yaml` can be edited directly for common parameters.  You can read more about Snakemake config files in the [Snakemake documentation page on Configuration](https://snakemake.readthedocs.io/en/stable/snakefiles/configuration.html) and more about the directory structure in the [Snakemake documentation page about Distribution and Reproducibility](https://snakemake.readthedocs.io/en/stable/snakefiles/deployment.html).  

The pipeline can be run from the MAGqual directory using the basic Snakemake command:
```
snakemake --use-conda -j 1
```  
This command can then be decorated with any of the command line options Snakemake allows - see the [Snakemake documentation](https://snakemake.readthedocs.io/en/stable/executing/cli.html) for options. 

### Running on different queuing architechture
Snakemake provides an easy way to run this pipeline on a computing cluster. We have provided support for a HPC with a Slurm queuing system, however this configuration is unlikely to work for everyone. 
Rule specific cluster information is held in the `config/cluster.json` - you can see more about the format of this file in the [Snakemake documentation](https://snakemake.readthedocs.io/en/stable/snakefiles/configuration.html#cluster-configuration-deprecated). This file can be edited, as can the command used to submit the pipeline.  
NOTE: When using the `--cluster slurm` option with MAGqual.py, the following is added to the Snakemake command:
```
--cluster-config config/cluster.json --cluster "sbatch -t {cluster.time} -c {cluster.threads} --mem-per-cpu {cluster.mem}
```

# Citation
If you use MAGqual in your research please cite the following:
> MAGqual: A standalone pipeline to assess the quality of metagenome-assembled genomes
> Annabel Cansdale, James P.J. Chong
> bioRxiv 2023.12.13.571510; doi: https://doi.org/10.1101/2023.12.13.571510

MAGqual would not be possible without the following software, please cite them too:
* Bakta https://doi.org/10.1099/mgen.0.000685
* CheckM https://doi.org/10.1101/gr.186072.114
* SeqKit https://doi.org/10.1371/journal.pone.0163962
