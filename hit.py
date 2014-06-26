#!/usr/bin/python

from Bio import Entrez, SeqIO
from Bio.SeqUtils import GC
from Bio.SeqFeature import SeqFeature, FeatureLocation
import requests
from requests.auth import HTTPBasicAuth
import xlrd
import csv

# converts each sheet in ORF.xls to a separate .csv
def csv_from_excel():
	wb = xlrd.open_workbook('ORF program.xls')
	sh = wb.sheet_by_name('ORF')
	sh1 = wb.sheet_by_name('RNAseq')
	c = open('ORF.csv', 'wb')
	d = open('RNAseq.csv','wb')
	wr = csv.writer(c, quoting=csv.QUOTE_ALL)
	wr1 = csv.writer(d, quoting=csv.QUOTE_ALL)
	for rownum in xrange(sh.nrows):
		try:
			wr.writerow(sh.row_values(rownum))
		except UnicodeEncodeError:
			pass	
	for rownum in xrange(sh1.nrows):
		try:
			wr1.writerow(sh1.row_values(rownum))
		except UnicodeEncodeError:
			pass
	c.close()

# extracts hit coordinates and corresponding barcodes from ORF sheet
def get_hits(csvfile):
	hits = []
	barcodes = []
	with open(csvfile, 'rU') as file:
		reader = csv.reader(file)
		arr = []
		for row in reader:
			if row[3] != "":
				hits.append(row[3].strip())
				barcodes.append(row[2].strip())
	return hits, barcodes

# gets NCBI accession number from NAR website
def get_id(x,y,barcode):
	r = requests.get('http://research.gene.com/nar',auth=HTTPBasicAuth('guptaa22','Scissor1')).text
	#find tag in html and return accession
	return accession

# retrieves GenBsank data from NCBI website: accession ID, protein seq, and gene name
def parse(accession, filetype): # filetype can be 'gb' or 'fasta'
    Entrez.email = "aaronkgupta@gmail.com"
    handle = Entrez.efetch(db="nucleotide", id = accession, rettype = filetype, retmode="text")
    seq_record = SeqIO.read(handle,'gb') # genbank format
    feats = seq_record.features
    name = []
    for feat in feats:
    	if 'gene' in feat.qualifiers:
    		name.append(feat.qualifiers['gene'])
    return seq_record.name, str(seq_record.seq.translate()), name[0]

# gets RNAseq data from RNAseq sheet
def get_rnaseq(rnaseq):
	
    
# write output file which includes GenBank data
def writefile(orf, rnaseq, name, seq, symbol):
	# add genbank data to ORF sheet
	with open(orf, 'rU') as file:
		reader = csv.reader(file)
		arr = []
		for row in reader:
			
#csv_from_excel()
#get_hits('ORF.csv')

#get_id(0,0,0)
#handle = parse('BC011922','gb') # sample case
#print handle