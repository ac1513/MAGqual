#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 11:58:34 2020

@author: ac1513
Script that calculates the quality of MAGs when given a prokka and a checkm output.
Outputs a file containing the quality and copies the MAGs into a new directory depending on their quality.
"""

import pandas as pd
import glob
import argparse
import os
from shutil import copyfile

def qual_cluster(comp, cont):
    if (comp >90) and (cont<5):
        qual = "high"
    elif (comp >= 50) and (cont <10):
        qual = "med"
    elif (comp <50) and (cont <10):
        qual = "low"
    else:
        qual = "NA"
    return qual

parser = argparse.ArgumentParser(description='')
parser.add_argument('output', help='output directory for the organised bins', type=str)
parser.add_argument('checkm_log', help='checkm output log file (TAB SEPARATED', type=str)
parser.add_argument('prok_loc', help='directory containing all prokka output for all clusters', type=str)
parser.add_argument('bin_loc', help='directory containing fasta files for all clusters', type=str)
parser.add_argument('jobid', help='prefix for current jobs', type=str)

args = parser.parse_args()
output = args.output
checkm_log = args.checkm_log
prok_loc = args.prok_loc
bin_loc = args.bin_loc
job_id = args.jobid

# =============================================================================
# CHECKM STUFF HERE
# =============================================================================

checkm_df = pd.read_csv(checkm_log, sep = "\t", index_col = 0)
checkm_df['qual'] = checkm_df.apply(lambda x: qual_cluster(x['Completeness'], x['Contamination']), axis=1)

high_clusters = checkm_df[checkm_df['qual'].str.contains("high")].index.values.tolist()
med_qual_clusters = checkm_df[checkm_df['qual'].str.contains("med")].index.values.tolist()
low_qual_clusters = checkm_df[checkm_df['qual'].str.contains("low")].index.values.tolist()
NA = checkm_df[checkm_df['qual'].str.contains("NA")].index.values.tolist()
# =============================================================================
# PROKKA PARSE HERE
# =============================================================================

high_qual_clusters= []
near_comp_clusters = []
for cluster in high_clusters:
    loc = str(prok_loc + cluster + '/*.tsv')
    for name in glob.glob(loc):
        prok_file = name
        with open(prok_file, 'r') as prokka_in:
            trna_set = set()
            rna_set = set()
            for line in prokka_in:
                if "tRNA-Ala" in line:
                    trna_set.add("tRNA-Ala")
                if "tRNA-Arg" in line:
                    trna_set.add("tRNA-Arg")
                if "tRNA-Asn" in line:
                    trna_set.add("tRNA-Asn")
                if "tRNA-Asp" in line:
                    trna_set.add("tRNA-Asp")
                if "tRNA-Cys" in line:
                    trna_set.add("tRNA-Cys")
                if "tRNA-Gln" in line:
                    trna_set.add("tRNA-Gln")
                if "tRNA-Glu" in line:
                    trna_set.add("tRNA-Glu")
                if "tRNA-Gly" in line:
                    trna_set.add("tRNA-Gly")
                if "tRNA-His" in line:
                    trna_set.add("tRNA-His")
                if "tRNA-Ile" in line:
                    trna_set.add("tRNA-Ile")
                if "tRNA-Leu" in line:
                    trna_set.add("tRNA-Leu")
                if "tRNA-Lys" in line:
                    trna_set.add("tRNA-Lys")
                if "tRNA-Met" in line:
                    trna_set.add("tRNA-Met")
                if "tRNA-Phe" in line:
                    trna_set.add("tRNA-Phe")
                if "tRNA-Pro" in line:
                    trna_set.add("tRNA-Pro")
                if "tRNA-Ser" in line:
                    trna_set.add("tRNA-Ser")
                if "tRNA-Thr" in line:
                    trna_set.add("tRNA-Thr")
                if "tRNA-Trp" in line:
                    trna_set.add("tRNA-Trp")
                if "tRNA-Tyr" in line:
                    trna_set.add("tRNA-Tyr")
                if "tRNA-Val" in line:
                    trna_set.add("tRNA-Val")
                if ("5S ribosomal RNA" in line) and ("partial" not in line):
                    rna_set.add('5S')
                if ("16S ribosomal RNA" in line) and ("partial" not in line):
                    rna_set.add('16S')
                if ("23S ribosomal RNA" in line) and ("partial" not in line):
                    rna_set.add('23s')
    if (len(trna_set) >= 18) and (len(rna_set) == 3):
        high_qual_clusters.append(cluster)
    else:
        near_comp_clusters.append(cluster) # adds high qual that fail trna/rna
# =============================================================================
# COPYING FILES INTO QUAL DIRECTORIES
# =============================================================================

location = bin_loc
new_loc = output + "/" + job_id + "/"
os.makedirs(new_loc + "high_qual", exist_ok=True)
os.makedirs(new_loc + "near_comp", exist_ok=True)
os.makedirs(new_loc + "med_qual", exist_ok=True)
os.makedirs(new_loc + "low_qual", exist_ok=True)
os.makedirs(new_loc + "failed", exist_ok=True)

for high in high_qual_clusters:
    file = location + high + ".fasta"
    copyfile(file, new_loc +"high_qual/"+high+".fasta")

for nc in near_comp_clusters:
    file = location + nc + ".fasta"
    copyfile(file, new_loc +"near_comp/"+nc+".fasta")

for med in med_qual_clusters:
    file = location + med + ".fasta"
    copyfile(file, new_loc+"med_qual/"+med+".fasta")

for low in low_qual_clusters:
    file = location + low + ".fasta"
    copyfile(file, new_loc+"low_qual/"+low+".fasta")

for NA_bin in NA:
    file = location + NA_bin + ".fasta"
    copyfile(file, new_loc+"failed/"+nc+".fasta")

# =============================================================================
# OUTPUT CREATED HERE
# =============================================================================

print("-" * 12)
print(" NUMBER MAGs")
print("-" * 12)
print("High Qual:", len(high_qual_clusters))
print("Near Comp:", len(near_comp_clusters))
print("Med Qual:", len(med_qual_clusters))
print("Low Qual:", len(low_qual_clusters))
print("Failed:", len(NA), "\n")
print("-" * 12)
print(" MAG IDs")
print("-" * 12)
print("High Qual:")
print(*high_qual_clusters, sep=", ")
print("\nNear Comp:")
print(*near_comp_clusters, sep=", ")
print("\nMed Qual:")
print(*med_qual_clusters, sep=", ")
print("\nLow Qual:")
print(*low_qual_clusters, sep=", ")
print("\nFailed:")
print(*NA, sep=", ")
