#!/usr/bin/env python

import json
from flask import Response
from variant_search_app import app, dbh, mimetype, valid_search_methods, \
    JsonDateTimeEncoder


@app.route('/genes/<search_str>', defaults={'search_method': 'startswith'})
@app.route('/genes/<search_str>/<search_method>')
def genes(search_str, search_method):
    dbh.search_genes(search_str, search_method=search_method)

    gene_matches = []
    for row in dbh.fetchrows():
        gene_matches.append(row[0])

    return Response(json.dumps(gene_matches), mimetype=mimetype)


@app.route('/variants/<gene_name>')
def variants(gene_name):
    dbh.search_variants_by_gene(gene_name)

    results = []
    col_headers = ["Gene Name", "Nucleotide Change", "Protein Change",
                    "Assembly Version", "Reported Classification",
                    "Submitter Comment", "Last Updated Date",
                    "Data Source", "Source URL"]
    results.append({"columns": col_headers})

    variant_matches = []
    for row in dbh.fetchrows():
        variant_matches.append(row)

    results.append({"results": variant_matches})
    return Response(json.dumps(results, cls=JsonDateTimeEncoder), mimetype=mimetype)
