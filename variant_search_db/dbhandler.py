#!/usr/bin/env python

from shlex import split as _split
from subprocess import Popen
import psycopg2


INVITAE_VARIANTS_DB_SCHEMA = 'db/schema.sql'
INVITAE_VARIANTS_DB_NAME = 'invitae_variant_search'


class DbHandler(object):
    """
    Connect to a specific database managed by postgres and
    return a db connection handle and cursor for executing queries
    """
    def __init__(self, db=INVITAE_VARIANTS_DB_NAME, autocommit=False):
        self.dbh = psycopg2.connect(database=db)
        self.dbh.autocommit = autocommit
        self.cur = self.dbh.cursor()

    def execute(self, query):
        self.cur.execute(query)

    def close(self, commit=False):
        if commit:
            self.dbh.commit()
        self.cur.close()
        self.dbh.close()

    def finish(self):
        self.cur.close()

    def insert_gene(self, gene_name):
        insert_gene_query = """
        INSERT INTO genes (name) VALUES ('{0}')
        """.format(gene_name)

        self.execute(insert_gene_query)

    def insert_variant_source(self, source_name):
        insert_source_query = """
        INSERT INTO variant_source (name) VALUES ('{0}')
        """.format(source_name)

        self.execute(insert_source_query)

    def insert_variant_classification(self, classfn):
        insert_classfn_query = """
        INSERT INTO variant_classification (assignment) VALUES ('{0}')
        """.format(classfn)

        self.execute(insert_classfn_query)

    def insert_variant_details(self, **kwargs):
        insert_variant_query = """
        INSERT INTO variants (gene,
            nucleotide_change, protein_change, 
            other_mappings, transcripts, region, 
            reported_classification,
            inferred_classification,
            source,
            last_evaluated, last_updated,
            url, submitter_comment,
            assembly, chr,
            genomic_start, genomic_stop,
            ref, alt, accession,
            reported_ref, reported_alt
        ) VALUES (
            (SELECT uid FROM genes WHERE name = %s),
            %s, %s,
            %s, %s, %s,
            (SELECT uid FROM variant_classification WHERE assignment = %s),
            (SELECT uid FROM variant_classification WHERE assignment = %s),
            (SELECT uid FROM variant_source WHERE name = %s),
            %s, %s,
            %s, %s,
            %s, %s,
            %s, %s,
            %s, %s, %s,
            %s, %s
        )
        """

        self.cur.execute(insert_variant_query, (
            kwargs['gene'],
            kwargs['nucleotide_change'], kwargs['protein_change'],
            kwargs['other_mappings'], kwargs['transcripts'], kwargs['region'],
            kwargs['reported_classification'],
            kwargs['inferred_classification'],
            kwargs['source'],
            kwargs['last_evaluated'], kwargs['last_updated'],
            kwargs['url'], kwargs['submitter_comment'],
            kwargs['assembly'], kwargs['chr'],
            kwargs['genomic_start'], kwargs['genomic_stop'],
            kwargs['ref'], kwargs['alt'], kwargs['accession'],
            kwargs['reported_ref'], kwargs['reported_alt']
        )
                        )

    @staticmethod
    def init_variants_db():
        """
        Initialize a PostgreSQL database to store the variant data;
        use the pre-built schema.sql file
        """
        psqlcmd = "psql -U postgres -d postgres -f {0}".format(INVITAE_VARIANTS_DB_SCHEMA)
        j = Popen(_split(psqlcmd))
        j.wait()
