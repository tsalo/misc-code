# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 14:29:19 2014
Convert csv of articles to citation.
@author: tsalo
"""

import csv

csv_file = 'C:\\Users\\tsalo\\Desktop\\Carter_Articles.csv'
out_text_file = 'C:\\Users\\tsalo\\Desktop\\Carter_Citations.txt'

with open(out_text_file, 'wb') as fo:
    fo.write("Citations\n\n")

with open(csv_file, 'rb') as f:
    reader = csv.reader(f, delimiter=",")
    for line in reader:
        authors = line[0].replace("|", ",")
        year = line[1]
        title = line[2].replace("|", ",")
        if title[len(title)-1] != ".":
            title = title + "."
        journal = line[3].replace("|", ",")
        issue = line[4].replace("|", ",")
        out_string = authors + " (" + year + "). " + title + " " + journal + " " + issue + "\n\n"
        
        with open(out_text_file, 'a') as fo:
            fo.write(out_string)