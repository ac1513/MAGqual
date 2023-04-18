import sys 
import argparse
from datetime import date

def_prefix = "MAGqual_" + str(date.today()).replace("-","")

parser = argparse.ArgumentParser(description='usage = python MAGqual.py ')
parser.add_argument('-p', '--prefix', dest='prefix', help = 'prefix for the MAGqual run', type = str, default=def_prefix)
parser.add_argument('-j', '--jobs', dest='jobs', help = 'number of jobs to be run concurrently', type = int, default=1)
parser.add_argument('-a', '--assembly', dest='assembly', required = True, help = 'location of the assembly used to generate the bins', type = str)
parser.add_argument('-b', '--binloc', dest='binloc', required = True, help = 'location of the directory containing the bins to run through MAGqual', type = str)

parser.add_argument('--cluster', dest='cluster', help = 'OPTIONAL: type of cluster (available options: slurm), leave empty if running MAGqual directly', type = str)
parser.add_argument('--checkmdb', dest='checkmdb', help = 'OPTIONAL: location of a ready installed database for CheckM', type = str)
parser.add_argument('--baktadb', dest='baktadb', help = 'OPTIONAL: location of a ready installed database for Bakta, note must be v5.0 or above', type = str)

args = parser.parse_args()

prefix = args.prefix
jobs = args.jobs
assembly = args.assembly
binloc = args.binloc

if args.checkmdb:
    checkmdb = args.checkmdb
else:
    checkmdb = ""
if args.baktadb:
    baktadb = args.baktadb
else:
    baktadb = ""

if args.cluster == "slurm":
    command = "snakemake --use-conda -j " + str(jobs) + " --config JOBID = " + prefix + " ASM_LOC = " + assembly + " BIN_LOC = " + binloc + " checkm_db = " + checkmdb + " bakta_db = " + baktadb + ' --cluster-config config/cluster.json --cluster "sbatch -A {cluster.account} -p {cluster.partition} -t {cluster.time} -c {cluster.threads} --mem-per-cpu {cluster.mem}"'
else:
    command = "snakemake --use-conda -j " + str(jobs) + " --config JOBID = " + prefix + " ASM_LOC = " + assembly + " BIN_LOC = " + binloc + " checkm_db = " + checkmdb + " bakta_db = " + baktadb

print(command)