#!/usr/bin/python

from Bio import Entrez, SeqIO
from Bio.SeqUtils import GC
from Bio.SeqFeature import SeqFeature, FeatureLocation
import requests
from requests.auth import HTTPBasicAuth
import xlrd
import csv

def csv_from_excel():
	wb = xlrd.open_workbook('ORF program.xls')
	sh = wb.sheet_by_name('ORF')
	your_csv_file = open('ORF.csv', 'wb')
	wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

	for rownum in xrange(sh.nrows):
		wr.writerow(sh.row_values(rownum))

	your_csv_file.close()

# function to retrieve genbank data from NCBI website. retrieves accession ID and nucelotide sequence
def parse(accession, filetype): # filetype can be 'gb' or 'fasta'
    Entrez.email = "aaronkgupta@gmail.com"
    handle = Entrez.efetch(db="nucleotide", id = accession, rettype = filetype, retmode="text")
    seq_record = SeqIO.read(handle,'gb') # genbank format
    return seq_record.name, seq_record.seq.tostring
    
def get_id(x,y,barcode):
	r = requests.get('http://research.gene.com/nar',auth=HTTPBasicAuth('guptaa22','Scissor1')).text
	#find tag in html and return accession
	return accession

csv_from_excel()

#get_id(0,0,0)
#handle = parse('BC011922','gb') # sample case
#print handle