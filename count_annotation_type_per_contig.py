#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File    	: count_annotation_type_per_contig.py
Author  	: Dominik R. Laetsch, dominik.laetsch at gmail dot com 
Version 	: 0.1
Description : takes an assembly file, annotation type and gff3, and returns count of type per contig
To do 		: ...
"""

from __future__ import division
import sys

def parse_contig_names(contig_file):

	contigs = set()
	contig_name = ''
	with open(contig_file) as fh:
		for line in fh:
			if line.startswith(">"):
				contig_name = line.lstrip(">").rstrip("\n")
				if contig_name in contigs:
					sys.exit('[ERROR] Repeated contig name ' + contig_name + ' in ' + contig_file)
				else:
					contigs.add(contig_name)
	return contigs

def parse_gff_and_print(gff_file, contigs, annotation_type):
	with open(gff_file) as fh:
		for line in fh:
			if not line.startswith("#"):
				field = line.split("\t")
				if field[2] == annotation_type:
					if field[0] in contigs:
						print line


if __name__ == "__main__":
	contig_file, annotation_type, gff_file = '', 'mRNA', ''
	try:
		contig_file = sys.argv[1]
		annotation_type = sys.argv[2]
		gff_file = sys.argv[3]
	except:
		sys.exit("Usage: ./count_annotation_type_per_contig.py [CONTIGFILE] [TYPE] [GFF3]")
	
	contigs = parse_contig_names(contig_file)
	parse_gff_and_print(gff_file, contigs, annotation_type)


