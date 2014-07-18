#!/usr/bin/python

from Bio import Entrez, SeqIO
from Bio.SeqUtils import GC
from Bio.SeqFeature import SeqFeature, FeatureLocation
import requests
from requests.auth import HTTPBasicAuth
import xlrd
import csv
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import xlsxwriter
import json
import urllib2

# converts each sheet in ORF.xls to a separate .csv
def csv_from_excel(ixls,sheet1,sheet2, ocsv1, ocsv2):
	wb = xlrd.open_workbook(ixls)
	sh = wb.sheet_by_name(sheet1) # 'ORF'
	sh1 = wb.sheet_by_name(sheet2) # 'RNAseq'
	c = open(ocsv1,'wb')
	d = open(ocsv2,'wb')
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
def get_hits(orf):
	hits = [] # filled in the format 'x-y'
	barcodes = [] # barcode string
	with open(orf, 'rU') as file:
		reader = csv.reader(file)
		arr = []
		for row in reader:
			if row[3] != "":
				hits.append(row[3].strip())
				barcodes.append(row[2].strip())
	return hits, barcodes # separate arrays with coordinates and barcodes

def convert_coordinate(s):
    a = ['A','B','C','D','E','F','G','H']
    row = a.index(s[0])
    col = ''
    if s[1] == '0':
        col = s[2]
    else:
        col = s[1:3]
    return str(col)+'-'+str(row)

def get_dnaids(hits, barcodes):
    dnaids = []
    with open('Plate map NK.csv', 'rU') as file:
        reader = csv.reader(file)
        arr = []
        for i in range(0,len(hits)):
            for row in reader:
                print row[2].strip()
                hit = convert_coordinate(row[2].strip())
                if row[1].strip() == barcodes[i] and hit == hits[i]:
                    dnaids.append(row[4])
    return dnaids



def retrieve_annotation(id_list):
    
    """Annotates Entrez Gene IDs using Bio.Entrez, in particular epost (to
        submit the data to NCBI) and esummary to retrieve the information.
        Returns a list of dictionaries with the annotations."""
    
    request = Entrez.epost("gene",id=",".join(id_list))
    try:
        result = Entrez.read(request)
    except RuntimeError as e:
        #FIXME: How generate NAs instead of causing an error with invalid IDs?
        print "An error occurred while retrieving the annotations."
        print "The error returned was %s" % e
        sys.exit(-1)
    
    webEnv = result["WebEnv"]
    queryKey = result["QueryKey"]
    data = Entrez.esummary(db="gene", webenv=webEnv, query_key =
                           queryKey)
    annotations = Entrez.read(data)
    
    print "Retrieved %d annotations for %d genes" % (len(annotations),
                                                     len(id_list))
                                                     
    return annotations

def print_data(annotations):
    for gene_data in annotations:
        print '\n\n\n\n\n\n\n\n'
        print gene_data
        #gene_id = gene_data["Id"]
        #gene_symbol = gene_data["NomenclatureSymbol"]
        #gene_name = gene_data["Description"]
        #print "ID: %s - Gene Symbol: %s - Gene Name: %s" % (gene_id, gene_symbol, gene_name)
'''
Entrez.email = "aaronkgupta@gmail.com"
id_list = ['5348','28972','27436']
annotations = retrieve_annotation(id_list)
print_data(annotations)
'''
# retrieves GenBank data from NCBI website: accession ID, protein seq, and gene name
def ncbi(accession, filetype): # filetype can be 'gb' or 'fasta'
    Entrez.email = "aaronkgupta@gmail.com"
    handle = Entrez.efetch(db="nucleotide", id = accession, rettype = filetype, retmode="text")
    seq_record = SeqIO.read(handle,'gb') # genbank format
    feats = seq_record.features
    name = []
    for feat in feats:
    	if 'gene' in feat.qualifiers:
    		name.append(feat.qualifiers['gene'])
    return seq_record.name, str(seq_record.seq.translate()), name[0]

# gets RNAseq data from RNAseq sheet (saved as .csv). Pass through all symbols.
def get_rnaseq(rnaseq, symbols):
    rnas = []
    with open(rnaseq, 'rU') as file:
        reader = csv.reader(file)
        arr = []
        for row in reader:
            for s in symbols:
                if row[1].strip() == s and row[3] > 1 and row[4] > 1:
                    rna = [0,0]
                    rna[0:2] = row[3:5]
                    rnas.append(rna)
    return rnas

# write output file which includes GenBank data + Pfam
def writefile(orf, rnaseq, ids, seqs, symbols,rnas):
    workbook = xlsxwriter.Workbook('output.xlsx',{'strings_to_numbers': True})
    ws1 = workbook.add_worksheet('ORF')
    ws2 = workbook.add_worksheet('RNAseq')
	# write genbank data to ORF sheet
    i = 0
    k = 0
    with open(orf, 'rU') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[3] != '':
                row[4] = ids[i]
                row[5] = symbols[i]
                row[6] = seqs[i]
                row[7:9] = rnas[i]
                i+=1
            k+= 1
            ws1.write_row('A'+str(k+1),row)
    j = 0
    with open(rnaseq, 'rU') as file2:
        reader = csv.reader(file2)
        for row in reader:
            ws2.write_row('A'+str(j+1),row)
            j+=1


# TEST CASE

csv_from_excel('ORF program.xls','ORF','RNAseq','ORF.csv','RNAseq.csv') # turns sheets in separate csvs
hits, barcodes = get_hits('ORF.csv') # extract hits and barcodes
print hits
print barcodes
print get_dnaids(hits,barcodes)
# fills input data for writefile()
'''
ids = []
seqs = []
symbols = []
for i in range(0,len(hits)): # loop through to get all accession ids, seqs, and symbols from NCBI
    a = hits[i].split('-')
    ids.append(ncbi(get_id(a[0],a[1],barcodes[i]),'gb')[0])
    seqs.append(ncbi(get_id(a[0],a[1],barcodes[i]),'gb')[1])
    symbols.append(ncbi(get_id(a[0],a[1],barcodes[i]),'gb')[2])

symbols =['Ap1b1','Ap2a2','Aox1']
rnas = get_rnaseq('rnaseq.csv',symbols) # get those hits that have high enough expression (>1)
ids = ['A','B','C']
seqs = ['gg','cc','aa']
writefile('ORF.csv','RNAseq.csv',ids,seqs,symbols,rnas) # write all gathered data to new xlsx file
'''

#get_id(0,0,0)
