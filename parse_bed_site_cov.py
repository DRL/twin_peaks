#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File    	: parse_bed_site_cov.py
Author  	: 
Version 	: 0.1
Description : Parses FASTATS of assembly and bedtools genomecov output from bamfiles
To do 		: 
"""

from __future__ import division
import sys, os
import time
import multiprocessing as mp 
import subprocess
import string
import collections

class Contig():
	def __init__(self, name, length, agct, gc):
		self.name = name
		self.length = 0
		self.agct = 0
		self.gc = 0.0
		self.n = self.length - self.agct
		
def getContigStats(fastats_file):
	print "[STATUS] - Parsing FASTATS ... "
	dict_of_contigs = {}
	with open(fastats_file) as fh:
		for line in fh:
			if line.startswith("#"):
				pass
			else:
				name, length, N, agct, gc = line.rstrip("\n").split("\t")
				contig = Contig(name, length, agct, gc)
				dict_of_contigs[name] = contig

	print "[STATUS] - %s contigs found." %len(dict_of_contigs)
	return dict_of_contigs

def getGenomeCovFiles(genomecov_dir):
	dict_of_genomecovs = {}
	print "[STATUS] - Getting GenomeCovFiles ... "
	for genomecov_file in os.listdir(genomecov_dir):
		if genomecov_file.endswith("cov.hist.txt"):
			dataset = genomecov_file.split(".")[0]
			dict_of_genomecovs[dataset] = genomecov_dir + genomecov_file
	print "[STATUS] - %s GenomeCovFiles found." %len(dict_of_genomecovs)
	return dict_of_genomecovs

def parseCovSitesFromInfile(infile, max_count):
	print "[STATUS] - Parsing %s ... " %infile
	counts = {}
	with open(infile) as fh:
		for line in fh:
			name, cov, sites, length, proportion = line.rstrip("\n").split("\t")
			cov = int(cov)
			sites = int(sites)
			if cov <= max_count:
				counts[cov] = counts.get(cov, 0) + sites
			else:
				counts[max_count] = counts.get(max_count, 0) + sites

	print "[STATUS] - Finished parsing %s." %infile
	return counts

if __name__ == "__main__":
	try:
		fastats_file = sys.argv[1]
		genomecov_dir = sys.argv[2]
		max_count = int(sys.argv[3])
	except:
		sys.exit("Usage: ./parse_bed_site_cov.py [FASTATS] [GENOMECOV_DIR] [MAXCOUNT]")
	
	dict_of_contigs = getContigStats(fastats_file)	
	dict_of_genomecovs = getGenomeCovFiles(genomecov_dir)
	covered_sites = {}

	header = "# cov"
	for dataset in dict_of_genomecovs:
		header += "\t" + dataset
		covered_sites[dataset] = parseCovSitesFromInfile(dict_of_genomecovs[dataset], max_count)

	print header
	for i in range(0, max_count):		
		print str(i),
		for dataset in covered_sites:
			print "\t" + str(covered_sites[dataset][i]),
		print