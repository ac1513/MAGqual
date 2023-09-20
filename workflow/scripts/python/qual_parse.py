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
import seaborn as sns
import matplotlib.pyplot as plt

def qual_cluster(comp, cont):
    if (comp >90) and (cont<5):
        qual = "High Quality"
    elif (comp >= 50) and (cont <10):
        qual = "Medium Quality"
    elif (comp <50) and (cont <10):
        qual = "Low Quality"
    else:
        qual = "Failed"
    return qual

def gen_qual(comp, cont):
    if (comp - (cont*5)) >= 50:
        genome = "y"
    else:
        genome = "n"
    return genome

def bsearch(bakta_loc, cluster): 
    length = 0
    loc = str(bakta_loc + str(cluster) + '/' + str(cluster) + '.txt') #don't copy this bit change it !
    # loc = str(str(cluster) + '.txt') #don't copy this bit change it !
    for name in glob.glob(loc):
        bakta_file = name
        with open(bakta_file, 'r') as bakta_log:
            for line in bakta_log:
                if "Length:" in line:
                    length = int(line.split(":")[1])
                if "Count:" in line: 
                    count = int(line.split(":")[1])
                if "N50:" in line:
                    N50 = int(line.split(":")[1])
                if "Software:" in line: 
                    software = line.split(":")[1].strip()
                if "Database" in line:
                    db = line.split(":")[1].strip()
    bakta_v = "Bakta " + software + " DB " + db 
    row_dict = {"length" : length, "contigs" : count, "N50": N50, "bakta_v" : bakta_v}
    return pd.Series(row_dict)

parser = argparse.ArgumentParser(description='')
parser.add_argument('output', help='output directory for the organised bins', type=str)
parser.add_argument('checkm_log', help='checkm output log file (TAB SEPARATED', type=str)
parser.add_argument('bakta_loc', help='directory containing all bakta output for all clusters', type=str)
parser.add_argument('seqkit_log', help='file containing the seqkit output for all clusters', type=str)
parser.add_argument('bin_loc', help='directory containing fasta files for all clusters', type=str)
parser.add_argument('jobid', help='prefix for current jobs', type=str)
parser.add_argument('ext', help='file extension of MAGs', type=str)

args = parser.parse_args()
output = args.output
checkm_log = args.checkm_log
bakta_loc = args.bakta_loc
seqkit_log = args.seqkit_log
bin_loc = args.bin_loc
job_id = args.jobid
ext = args.ext

comp_software = "CheckM v.1.0.13"
comp_approach = "Marker gene"

colour_dict = dict({'High Quality':'#50C5B7',
                  'Near Complete':'#9CEC5B',
                  'Medium Quality': '#F0F465',
                  'Low Quality': "#F8333C",
                  'Failed': '#646E78'})

# =============================================================================
# CHECKM PARSE
# =============================================================================
checkm_df = pd.read_csv(checkm_log, sep = "\t")
checkm_df['Quality'] = checkm_df.apply(lambda x: qual_cluster(x['Completeness'], x['Contamination']), axis=1)
checkm_df[['Size_bp', 'No_contigs', 'N50_length', '16S_Software']] = checkm_df.apply(lambda x: bsearch(bakta_loc, x["Bin Id"]), axis = 1)

checkm_df = checkm_df.set_index("Bin Id")

high_clusters = checkm_df[checkm_df['Quality'].str.contains("High Quality")].index.values.tolist()
med_qual_clusters = checkm_df[checkm_df['Quality'].str.contains("Medium Quality")].index.values.tolist()
low_qual_clusters = checkm_df[checkm_df['Quality'].str.contains("Low Quality")].index.values.tolist()
NA = checkm_df[checkm_df['Quality'].str.contains("Failed")].index.values.tolist()
all_clusters = high_clusters + med_qual_clusters + low_qual_clusters + NA

checkm_df = checkm_df.drop(checkm_df.columns[[1, 2, 3, 4, 5, 6, 7, 8, 9]], axis=1)

# =============================================================================
# SEQKIT PARSE
# =============================================================================
seqkit_df = pd.read_csv(seqkit_log, sep = "\t")
seqkit_df = seqkit_df[["file", "max_len"]]
seqkit_df["file"] = seqkit_df["file"].str.replace(ext,'', regex=True)
seqkit_df["file"] = seqkit_df["file"].str.split("/").str[-1]
seqkit_df.set_index("file", inplace=True)
seqkit_df.rename(columns={"max_len":"Max_contig_length"}, inplace = True)
checkm_df = pd.merge(checkm_df, seqkit_df, left_index=True, right_index=True, how="left")

# =============================================================================
# BAKTA PARSE
# =============================================================================

high_qual_clusters= []
near_comp_clusters = []
r16s_comp_clusters = []ß
trna_num = {}
for cluster in all_clusters:
    cluster = str(cluster)
    loc = str(bakta_loc + str(cluster) + '/' + str(cluster) + '.tsv') #change this too 
    # loc = str(str(cluster) + '.tsv') #don't copy this bit change it !
    for name in glob.glob(loc):
        bakta_file = name
        with open(bakta_file, 'r') as bakta_in:
            trna_set = set()
            rna_set = set()
            rrna_16S = "N"
            for line in bakta_in:
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
                    rrna_16S = "Y"
                if ("23S ribosomal RNA" in line) and ("partial" not in line):
                    rna_set.add('23s')
        if rrna_16S == "Y":
            r16s_comp_clusters.append(cluster)
        if cluster in high_clusters:
            if (len(trna_set) >= 18) and (len(rna_set) == 3):
                high_qual_clusters.append(cluster)
            else:
                near_comp_clusters.append(cluster) # adds high qual that fail trna/rna
        trna_num.update({cluster : len(trna_set)})

            
# =============================================================================
# Add these new qualities to the checkm dataframe        
# =============================================================================

checkm_df.loc[checkm_df.index.isin(near_comp_clusters), "Quality"] = "Near Complete"

checkm_df.loc[checkm_df.index.isin(r16s_comp_clusters), "16S_Recovered"] = "Y"
checkm_df["16S_Recovered"] = checkm_df["16S_Recovered"].fillna("N")

# Sort out legend order
label_order = ["High Quality", "Near Complete", "Medium Quality", "Low Quality", "Failed"]
labels_all = checkm_df["Quality"].unique().tolist()

for item in label_order:
    if item not in labels_all:
        label_order.remove(item)

labels_list = label_order

# =============================================================================
# Basic plot
# =============================================================================

checkm_df["Purity"] = 100 - checkm_df["Contamination"]
plt.figure(figsize=(15, 10))
ax = sns.scatterplot(data = checkm_df, x="Completeness", y="Purity",
                hue='Quality', size = 'Size_bp', sizes=(20, 800), alpha = 0.6, 
                palette=colour_dict, hue_order= labels_list)
sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))

plt.xlabel('Completeness (%)', size = 24)
plt.ylabel('Purity (%)', size = 24)
plt.xlim(0)
plt.legend(prop={'size': 20})
plt.tight_layout()
plt.tick_params(labelsize=18)

plt.savefig(job_id + '_mag_qual.png')
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
    file = location + high + ext
    copyfile(file, new_loc +"high_qual/"+high+ext)

for nc in near_comp_clusters:
    file = location + nc + ext
    copyfile(file, new_loc +"near_comp/"+nc+ext)

for med in med_qual_clusters:
    file = location + med + ext
    copyfile(file, new_loc+"med_qual/"+med+ext)

for low in low_qual_clusters:
    file = location + low + ext
    copyfile(file, new_loc+"low_qual/"+low+ext)

for NA_bin in NA:
    file = location + NA_bin + ext
    copyfile(file, new_loc+"failed/"+NA_bin+ext)

# =============================================================================
# OUTPUT CREATED HERE
# =============================================================================

magqual_df = checkm_df[["Quality", "Completeness", "Contamination", "16S_Recovered", "16S_Software", "Size_bp", "No_contigs", "N50_length", "Max_contig_length"]].copy()
magqual_df["tRNA_Extracted"] = pd.Series(trna_num)
magqual_df["tRNA_Software"] = magqual_df["16S_Software"]
magqual_df["Completeness_Approach"] = comp_approach
magqual_df["Completeness_Software"] = comp_software

magqual_df = magqual_df.reindex(columns=["Quality", "Completeness", "Contamination", "Completeness_Software","Completeness_Approach", "16S_Recovered", "16S_Software", "tRNA_Extracted", "tRNA_Software", "Size_bp", "No_contigs", "N50_length", "Max_contig_length"])

magqual_df.to_csv("analysis/" + job_id + "_mag_qual_statistics.csv")

print("-" * 12)
print(" NUMBER MAGs")
print("-" * 12)
print("High Quality:", len(high_qual_clusters))
print("Near Complete:", len(near_comp_clusters))
print("Med Quality:", len(med_qual_clusters))
print("Low Quality:", len(low_qual_clusters))
print("Failed:", len(NA), "\n")
print("-" * 12)
print(" MAG IDs")
print("-" * 12)
print("High Quality: " , ", ".join([str(x) for x in high_qual_clusters]))
print("Near Complete: ", ", ".join([str(x) for x in near_comp_clusters]))
print("Med Quality: ", ", ".join([str(x) for x in med_qual_clusters]))
print("Low Quality: ", ", ".join([str(x) for x in low_qual_clusters]))
print("Failed: ", ", ".join([str(x) for x in NA]))