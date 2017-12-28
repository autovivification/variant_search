#!/usr/bin/env python

import unittest
from variant_search_app import app

class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_genes_autocmp(self):
        resp = self.app.get('/genes/TRPV')
        assert resp.data == b'["TRPV1", "TRPV3", "TRPV4", "TRPV5", "TRPV6"]'

    def test_gene_name_contains(self):
        resp = self.app.get('/genes/ARP/contains')
        assert resp.data == b'["ARPP21", "CBARP", "FARP2", "LARP1B", "LARP4B", "LARP6", "LARP7", "NRARP", "PARP14", "PARP4", "SHARPIN"]'

    def test_get_variants_by_gene_name(self):
        resp = self.app.get('/variants/CRY1')
        assert resp.data == b'[{"columns": ["Gene Name", "Nucleotide Change", "Protein Change", "Assembly Version", "Reported Classification", "Submitter Comment", "Last Updated Date", "Data Source", "Source URL"]}, {"results": [["CRY1", "NM_004075.4:c.1657+3A>C", null, "GRCh37", "risk factor", null, "2017-09-14", "ClinVar", "https://www.ncbi.nlm.nih.gov/clinvar/RCV000490555"]]}]'

if __name__ == '__main__':
    unittest.main()
