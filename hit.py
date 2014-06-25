#!/usr/bin/python

from Bio import Entrez, SeqIO
from Bio.SeqUtils import GC
from Bio.SeqFeature import SeqFeature, FeatureLocation

# function to retrieve genbank data from NCBI website. retrieves accession ID and nucelotide sequence
def parse(accession, filetype): # filetype can be 'gb' or 'fasta'
    Entrez.email = "aaronkgupta@gmail.com"
    handle = Entrez.efetch(db="nucleotide", id = accession, rettype = filetype, retmode="text")
    seq_record = SeqIO.read(handle,'gb') # genbank format
    return seq_record.name, seq_record.seq.translate(seq_record.seq.tostring, table = 'Standard', stop_symbol='*')

handle = parse('BC011922','gb') # sample case
print handle