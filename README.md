# westlife-accounting
A basic framework to gather data on usage of West-Life services

# Installation

Populate basic configuration in /etc/westlife-accounting/config.py, e.g:

CONFIG = {
    # Service credentials (any IGTF certificate will do atm)
    'key': '/etc/grid-security/hostcert.pem',
    "cert" : '/etc/grid-security/hostkey.pem',
    # DB location
    "db_endpoint" : "sqlite:////var/lib/westlife-accounting/westlife.db",
    # List of service endpoints, used to get accounting records
    "services_endpoints" : "/etc/westlife-accounting/endpoints.csv",
    # URL to get all services registered with West-Life AAI
    "services_url" : "https://auth.west-life.eu/api/get_endpoints.cgi",
    # List of services (use get_endpoints.py to generate it)
    "services" : "/var/spool/westlife-accounting/endpoints.json",
}

Create the database using the create_db script.

Construct the list of services using get_endpoints.py > /var/spool/westlife-accounting/endpoints.json. You will need to provide the accounting endpoints in /etc/westlife-accounting/endpoints.csv, e.g.:

saml_entity_id,accounting_endpoint
urn:https://api-dev.scipion.ics.muni.cz/west-life,http://78.128.250.235/record.jwt
proxy-west-life.ics.muni.cz,https://proxy-west-life.ics.muni.cz/accounting/record.jwt

Test the data retrieval using the client get_accounting.py. If succesfull, the robtained records are available from the database.
