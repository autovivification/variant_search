# variant_search_app

Web application (backed by RESTful microservices and PostgreSQL DB) capable of querying 
genomic variants by Gene Name (e.g. BRCA1, CRY1, etc.) and reporting the information 
via an interactive results table.

## Installation

Dependencies:  
* PostgreSQL (>= 9.6)
* Python2.7 (Flask=0.12.2, psycopg2==2.7.3.2)
* jQuery, jQuery UI, MaterializeCSS, DataTables

Step 1: Clone repository:  
```
git clone https://github.com/autovivification/variant_search.git
cd variant_search
```

Step 2: Initialise python `virtualenv` and install necessary dependencies:  
```
$ virtualenv -p /usr/local/bin/python2 venv
$ . venv/bin/activate

(venv)$ pip install -r requirements.txt
```

Step 3: Initialize empty PostgreSQL database using schema defined in `variant_search_db/schema.sql`:  
```
(venv)$ psql -U postgres -d postgres -f variant_search_db/schema.sql
```

Step 4: Execute database loading script, which downloads the `variant_results.tsv` dataset 
from Clinvitae and uses it to build the database:  
```
(venv)$ python -m variant_search_db.build
```

Step 5: Start the Flask server:  
```
(venv)$ python runserver.py
```

## Usage

Flask webapp accessible at http://localhost:5000/

REST API endpoints (Flask routes) can be accessed as follows:
* Gene Name autocomplete (startswith): http://localhost:5000/genes/TRPV
* Gene Name autocomplete (contains): http://localhost:5000/genes/ARP/contains
* Variants by Gene Name: http://localhost:5000/variants/CRY1

## Tests

Backend:  
```
(venv)$ python -m variant_search_app.tests
```
