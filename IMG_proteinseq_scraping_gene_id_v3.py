#!/usr/bin/env python3

#Before running this code, be sure to have requests and BeautifulSoup installed:
#Run in your command line:
#pip3 install requests
#pip3 install bs4
#pip3 install lmxl

import sys
import requests
from bs4 import BeautifulSoup

#input the gene_ids of the JGI IMG/M database here:
gene_ids = sys.argv[1:]

headers = {"User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}

for gene_id in gene_ids:
    url = 'https://img.jgi.doe.gov/cgi-bin/m/main.cgi?section=GeneDetail&page=pepstats&gene_oid={}'.format(gene_id)
    source_code = requests.get(url, headers=headers).text
    soup = BeautifulSoup(source_code, 'lxml').get_text().split('Peptide Statistics\n\nPeptide statistics are shown for the following protein.\n\n\n')[-1] #splits the text of the webpage when this pattern is matched

    #Creates text file and appends the fasta output per protein
    text_file = open("Protein_sequence_output.txt", "a+")
    text_file.write(soup.split("PEPSTATS")[0]) #splits the text of the webpage when "PEPSTATS" is matched
    text_file.close()

# Get file contents
fd = open("Protein_sequence_output.txt")
contents = fd.readlines()
fd.close()

new_contents = []
# Get rid of empty lines
for line in contents:
    # Strip whitespace, should leave nothing if empty line was just "\n"
    if not line.strip():
        continue
    # We got something, save it
    else:
        new_contents.append(line)

#Resulting pasta file will have empty lines in it:
# Make final fasta file without empty lines
text_file = open("Protein_sequence_output.txt", "w")
text_file.write("".join(new_contents))
text_file.close()
