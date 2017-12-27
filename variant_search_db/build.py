#!/usr/bin/env python
"""
Script to process the Invitae Variants Results TSV file (available for
download from: http://clinvitae.invitae.org/download) and load the genes,
their attributes, their variant locations (nucleotide and protein),
variant classifications (inferred and reported) and other relevant information,
into a backend PostgreSQL database, which will serve as the source for the
interactive client side webapp (backed by Flask mediated microservices).
"""

import os
import sys
import csv
import urllib
import zipfile
import StringIO
from .dbhandler import DbHandler


INVITAE_DATASET_URL = 'http://s3-us-west-2.amazonaws.com/clinvitae/clinvitae_download.zip'
INVITAE_DATASET_ZIP_FILENAME = 'clinvitae_download.zip'
INVITAE_DATASET_FILENAME = 'variant_results.tsv'


def download_invitae_tsv():
    """
    If not available already, download a copy of the variant_results file 
    from the Clinvitae server.

    Return a open filehandle
    """
    fname = INVITAE_DATASET_FILENAME
    zipfname = INVITAE_DATASET_ZIP_FILENAME

    # if not available, download variant_results files from clinvitae
    if not (os.path.exists(zipfname) or os.path.exists(fname)):
        print >> sys.stderr, "Downloading `{0}` file from Clinvitae".format(INVITAE_DATASET_ZIP_FILENAME)
        datafile = urllib.URLopener()
        datafile.retrieve(INVITAE_DATASET_URL, zipfname)

    if os.path.exists(zipfname):
        infh = open(zipfname, 'rb')
        inzfh = zipfile.ZipFile(infh)
        tsv_data = StringIO.StringIO(inzfh.read(fname))
    else:
        tsv_data = open(fname, 'rb')

    return tsv_data

def read_invitae_tsv(tsv_data):
    """
    Return a generator that yields rows from the Invitae Variants dataset file
    """

    tsv_reader = csv.reader(tsv_data, dialect=csv.excel, delimiter='\t')

    tsv_header = tsv_reader.next()
    tsv_header = [str(x.replace(' ', '_').lower()) for x in tsv_header]

    for tsv_row in tsv_reader:
        """
        Mimic a csv.DictReader() by converting tsv row content into
        dict with keys from the csv header column names
        """
        _tsv_row = dict()
        for i, k in enumerate(tsv_header):
            try:
                elem = tsv_row[i]
            except IndexError:
                elem = None
            _tsv_row[k] = None if not(elem and elem.strip()) or elem == "NULL" else elem
        yield _tsv_row


def main():
    """
    Process the Invitae Variants TSV file and load the data into
    backend PostgreSQL database for query by Flask app
    """
    tsv_data = download_invitae_tsv()

    dbh = DbHandler()

    seen_genes = set()
    seen_sources = set()
    seen_classfications = set()

    print >> sys.stderr, "Starting database load from `{0}`...".format(INVITAE_DATASET_FILENAME)
    for row in read_invitae_tsv(tsv_data):
        gene_name = row['gene']
        if bool(gene_name and gene_name.strip()) and gene_name not in seen_genes:
            dbh.insert_gene(gene_name)
            seen_genes.add(gene_name)

        source_name = row['source']
        if bool(source_name and source_name.strip()) and source_name not in seen_sources:
            dbh.insert_variant_source(source_name)
            seen_sources.add(source_name)

        for ctype in ('reported_classification', 'inferred_classification'):
            classification = row[ctype]
            if bool(classification and classification.strip()) \
                    and classification not in seen_classfications:
                dbh.insert_variant_classification(classification)
                seen_classfications.add(classification)

        dbh.insert_variant_details(**row)

    dbh.close(commit=True)
    print >> sys.stderr, "Database load complete!"


if __name__ == "__main__":
    main()
