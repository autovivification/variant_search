--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.6
-- Dumped by pg_dump version 9.6.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE IF EXISTS invitae_variant_search;
--
-- Name: invitae_variant_search; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE invitae_variant_search WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8';


ALTER DATABASE invitae_variant_search OWNER TO postgres;

\connect invitae_variant_search

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: genes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE genes (
    uid integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE genes OWNER TO postgres;

--
-- Name: genes_uid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE genes_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE genes_uid_seq OWNER TO postgres;

--
-- Name: genes_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE genes_uid_seq OWNED BY genes.uid;


--
-- Name: variant_classification; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE variant_classification (
    uid integer NOT NULL,
    assignment text NOT NULL
);


ALTER TABLE variant_classification OWNER TO postgres;

--
-- Name: variant_classification_uid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE variant_classification_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE variant_classification_uid_seq OWNER TO postgres;

--
-- Name: variant_classification_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE variant_classification_uid_seq OWNED BY variant_classification.uid;


--
-- Name: variant_source; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE variant_source (
    uid integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE variant_source OWNER TO postgres;

--
-- Name: variant_source_uid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE variant_source_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE variant_source_uid_seq OWNER TO postgres;

--
-- Name: variant_source_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE variant_source_uid_seq OWNED BY variant_source.uid;


--
-- Name: variants; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE variants (
    uid integer NOT NULL,
    gene integer,
    nucleotide_change text,
    protein_change text,
    other_mappings text,
    transcripts text,
    region text,
    reported_classification integer,
    inferred_classification integer NOT NULL,
    source integer NOT NULL,
    last_evaluated date,
    last_updated date NOT NULL,
    url text NOT NULL,
    submitter_comment text,
    assembly text,
    chr text,
    genomic_start integer,
    genomic_stop integer,
    ref text,
    alt text,
    accession text,
    reported_ref text,
    reported_alt text
);


ALTER TABLE variants OWNER TO postgres;

--
-- Name: variants_uid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE variants_uid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE variants_uid_seq OWNER TO postgres;

--
-- Name: variants_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE variants_uid_seq OWNED BY variants.uid;


--
-- Name: genes uid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY genes ALTER COLUMN uid SET DEFAULT nextval('genes_uid_seq'::regclass);


--
-- Name: variant_classification uid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY variant_classification ALTER COLUMN uid SET DEFAULT nextval('variant_classification_uid_seq'::regclass);


--
-- Name: variant_source uid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY variant_source ALTER COLUMN uid SET DEFAULT nextval('variant_source_uid_seq'::regclass);


--
-- Name: variants uid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY variants ALTER COLUMN uid SET DEFAULT nextval('variants_uid_seq'::regclass);


--
-- Name: genes genes_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY genes
    ADD CONSTRAINT genes_name_key UNIQUE (name);


--
-- Name: genes genes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY genes
    ADD CONSTRAINT genes_pkey PRIMARY KEY (uid);


--
-- Name: variant_classification variant_classification_assignment_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY variant_classification
    ADD CONSTRAINT variant_classification_assignment_key UNIQUE (assignment);


--
-- Name: variant_classification variant_classification_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY variant_classification
    ADD CONSTRAINT variant_classification_pkey PRIMARY KEY (uid);


--
-- Name: variant_source variant_source_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY variant_source
    ADD CONSTRAINT variant_source_name_key UNIQUE (name);


--
-- Name: variant_source variant_source_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY variant_source
    ADD CONSTRAINT variant_source_pkey PRIMARY KEY (uid);


--
-- Name: variants variants_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY variants
    ADD CONSTRAINT variants_pkey PRIMARY KEY (uid);


--
-- Name: variants variants_gene_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY variants
    ADD CONSTRAINT variants_gene_fkey FOREIGN KEY (gene) REFERENCES genes(uid);


--
-- Name: variants variants_inferred_classification_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY variants
    ADD CONSTRAINT variants_inferred_classification_fkey FOREIGN KEY (inferred_classification) REFERENCES variant_classification(uid);


--
-- Name: variants variants_reported_classification_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY variants
    ADD CONSTRAINT variants_reported_classification_fkey FOREIGN KEY (reported_classification) REFERENCES variant_classification(uid);


--
-- Name: variants variants_source_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY variants
    ADD CONSTRAINT variants_source_fkey FOREIGN KEY (source) REFERENCES variant_source(uid);


--
-- PostgreSQL database dump complete
--

