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
	return hits, barcodes

# gets NCBI accession ID from NAR website/xls (if available)
def get_id(x,y,barcode):
    
    accession = ''
    r = requests.get('http://research.gene.com/nar',auth=HTTPBasicAuth('guptaa22','Scissor1')).text
    print r
	#find tag in html and return accession
    '''
    url = 'guptaa22:Scissor1@http://research.gene.com/nar/'
    #url = 'google.com'
    xpath = '//*[@id="isc_O"]/table/tbody/tr/td/table/tbody/tr/td[2]'
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    #time.sleep(1)
    #button = browser.find_element_by_xpath(xpath)
    present = False
    try:
        try:
            button = WebDriverWait(browser, 10).until(lambda browser : browser.find_element_by_xpath(xpath))
            present = True
        except TimeoutException:
            print 'button does not exist'
    except NoSuchElementException:
        present = False
    #button = WebDriverWait(browser, 10).until(lambda browser : browser.find_element_by_xpath(xpath))
    if present == True:
        button.click()
    browser.close()
    return present
    '''
# retrieves GenBank data from NCBI website: accession ID, protein seq, and gene name
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


'''
csv_from_excel('ORF program.xls','ORF','RNAseq','ORF.csv','RNAseq.csv')
hits, barcodes = get_hits('ORF.csv')
# fills input data for writefile()
ids = []
seqs = []
symbols = []
for i in range(0,len(hits)):
    a = hits[i].split('-')
    ids.append(parse(get_id(a[0],a[1],barcodes[i]),'gb')[0])
    seqs.append(parse(get_id(a[0],a[1],barcodes[i]),'gb')[1])
    symbols.append(parse(get_id(a[0],a[1],barcodes[i]),'gb')[2])
'''
symbols =['Ap1b1','Ap2a2','Aox1']
rnas = get_rnaseq('rnaseq.csv',symbols)
ids = ['A','B','C']
seqs = ['gg','cc','aa']
writefile('ORF.csv','RNAseq.csv',ids,seqs,symbols,rnas)

#get_id(0,0,0)
#handle = parse('BC011922','gb') # sample case
#print handle