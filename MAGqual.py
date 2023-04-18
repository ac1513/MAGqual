import sys 
import argparse
from datetime import date

def_prefix = "MAGqual_" + str(date.today()).replace("-","")

parser = argparse.ArgumentParser(description='usage = python MAGqual.py -a/--asm assembly.fa -b/--bins bins_dir/ (-j/--jobs 10 -p/--prefix MAGqual_run --cluster slurm --checkmdb checkm_db/ --baktadb bakta_db/)')

parser.add_argument('-a', '--asm', dest='assembly', required = True, help = 'location of the assembly used to generate the bins', type = str)
parser.add_argument('-b', '--bins', dest='binloc', required = True, help = 'location of the directory containing the bins to run through MAGqual', type = str)

parser.add_argument('-p', '--prefix', dest='prefix', help = 'prefix for the MAGqual run, default = MAGqual_YYYYMMDD', type = str, default=def_prefix)
parser.add_argument('-j', '--jobs', dest='jobs', help = 'number of jobs to be run concurrently, default = 1', type = int, default=1)

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
    checkm_com = " checkm_db=" + str(checkmdb)
else:
    checkm_com = ""
if args.baktadb:
    baktadb = args.baktadb
    bakta_com = " bakta_db=" + baktadb
else:
    bakta_com = ""

if args.cluster == "slurm":
    command = "snakemake --use-conda -j " + str(jobs) + " --config JOBID=" + prefix + " ASM_LOC=" + assembly + " BIN_LOC=" + binloc + checkm_com + bakta_com + ' --cluster-config config/cluster.json --cluster "sbatch -A {cluster.account} -p {cluster.partition} -t {cluster.time} -c {cluster.threads} --mem-per-cpu {cluster.mem}"'
else:
    command = "snakemake --use-conda -j " + str(jobs) + " --config JOBID=" + prefix + " ASM_LOC=" + assembly + " BIN_LOC=" + binloc + checkm_com + bakta_com

print(command)