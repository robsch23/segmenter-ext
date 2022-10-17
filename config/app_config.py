import os

GATEWAY = os.environ.get('GATEWAY', 'http://localhost:9999')
BASE_URL = os.path.join(GATEWAY, 'routes', 'orchestrator', 'files')
DIR_SEGMENT = os.path.join('data', 'data', 'blocchetti_segment')
DIR_SEARCHBOX = os.path.join('data', 'data', 'blocchetti_searchBox')
SERVICES_PORT = 8080
