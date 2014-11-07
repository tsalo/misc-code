# -*- coding: utf-8 -*-
"""
Code based on a Gist to search Pubmed.
Dependencies: Bio, csv, datetime
Optional dependencies: time_elapsed
"""

from Bio import Entrez
from Bio import Medline
import csv
from datetime import datetime

try:
    import time_elapsed as te
    startTime = datetime.now()
    te_found = True
except ImportError:
    te_found = False

TERM = ('("Carter CS"[AUTH]) AND ("fMRI"[WORD] ' + 
        'OR "functional magnetic resonance imaging"[WORD] ' + 
        'OR "magnetic resonance imaging"[WORD] OR "MRI"[WORD] ' + 
        'OR "schizophrenia"[WORD] OR "psychosis"[WORD] OR "autism"[WORD]) ' +
        'NOT "oxytocin"[WORD]')

# Extract all publications matching term.
Entrez.email = 'tsalo90@gmail.com'
h = Entrez.esearch(db='pubmed', retmax='2', term=TERM)
result = Entrez.read(h)
print('Total number of publications containing {0}: {1}'.format(TERM, result['Count']))
h_all = Entrez.esearch(db='pubmed', retmax=result['Count'], term=TERM)
result_all = Entrez.read(h_all)
ids_all = result_all['IdList']
h = Entrez.efetch(db='pubmed', id=ids_all, rettype='medline', retmode='text')
records = Medline.parse(h)

with open('C:\\Users\\tsalo\\Documents\\find-a-mentor\\Carter_Articles.csv', 'wb') as fp:
    wr = csv.writer(fp, quoting=csv.QUOTE_ALL)
    wr.writerow(['Authors', 'Year', 'Title', 'Journal', 'Issue'])

acceptable_formats = ['journal article', 'comparative study', 'editorial',
                      'introductory journal article']
for record in records:
    if any([type_.lower() in acceptable_formats for type_ in record.get('PT')]):
        article_authors = record.get('AU')
        out_authors = "| ".join(article_authors)
        title = record.get("TI").replace(',', '|')
        journal = record.get("TA").replace(',', '|')
        full_issue = record.get('SO').replace(',', '|')
        index = full_issue.find(';')
        issue = full_issue[index+1:]
        year = record.get('DP')[:4]
        out_string = ','.join([out_authors, year, title, journal, issue])
        out_string = out_string + '\n'
        with open('C:\\Users\\tsalo\\Documents\\find-a-mentor\\Carter_Articles.csv', 'a') as fp:
            fp.write(out_string)

if te_found:
    te.main(startTime)
