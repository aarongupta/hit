#!/usr/bin/python

from Bio import Entrez, SeqIO
from Bio.SeqUtils import GC
from Bio.SeqFeature import SeqFeature, FeatureLocation

# function to retrieve genbank data from NCBI website
def parse(accession, filetype): # filetype can be 'gb' or 'fasta'
	Entrez.email = "aaronkgupta@gmail.com"     # tells NCBI who you are
	handle = Entrez.efetch(db="nucleotide", id = accession, rettype = filetype, retmode="text")
    seq_record = SeqIO.read(handle, 'gb')
	return seq_record.name, seq_record.seq

handle = parse('BC011922','gb')

print seq_record.seq