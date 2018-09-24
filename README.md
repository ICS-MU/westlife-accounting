# westlife-accounting
A basic framework to gather data on usage of West-Life services

# Installation

Populate basic configuration in /etc/westlife-accounting/config.py, e.g:

CONFIG = {
    'key': 'private-key.pem',
    "cert" : 'cert',
    "db_endpoint" : "sqlite:///westlife.db",
}

Create the database using the create_db script.

Test the data retrieval using the client, e.g.:
get_accounting.py http://78.128.250.235/record.jwt
