TITLE: Cloning Nominatim Repository and Downloading Country Grid (Shell)
DESCRIPTION: This snippet outlines the initial steps for setting up Nominatim: cloning the official Git repository and downloading the essential country grid SQL data file. The country grid is crucial for efficient geocoding operations within Nominatim.
SOURCE: https://github.com/osm-search/nominatim/blob/master/README.md#_snippet_0

LANGUAGE: Shell
CODE:
```
git clone https://github.com/osm-search/Nominatim.git
wget -O Nominatim/data/country_osm_grid.sql.gz https://nominatim.org/data/country_grid.sql.gz
```

----------------------------------------

TITLE: Tuning PostgreSQL Configuration for Nominatim
DESCRIPTION: Provides recommended parameter settings for the PostgreSQL configuration file (`postgresql.conf`) to optimize performance for Nominatim imports and operations. These settings adjust memory usage, transaction logging, and checkpoint behavior based on available hardware.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/admin/Installation.md#_snippet_0

LANGUAGE: Configuration
CODE:
```
shared_buffers = 2GB
maintenance_work_mem = (10GB)
autovacuum_work_mem = 2GB
work_mem = (50MB)
synchronous_commit = off
max_wal_size = 1GB
checkpoint_timeout = 60min
checkpoint_completion_target = 0.9
random_page_cost = 1.0
wal_level = minimal
max_wal_senders = 0
```

----------------------------------------

TITLE: Searching Nominatim Database (Async Python)
DESCRIPTION: Demonstrates how to perform a simple asynchronous search query using the `NominatimAPIAsync` class. It connects to the local Nominatim database, searches for 'Brugge', and prints the coordinates of the first result.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/library/Getting-Started.md#_snippet_0

LANGUAGE: python
CODE:
```
import asyncio

import nominatim_api as napi

async def search(query):
    async with napi.NominatimAPIAsync() as api:
        return await api.search(query)

results = asyncio.run(search('Brugge'))
if not results:
    print('Cannot find Brugge')
else:
    print(f'Found a place at {results[0].centroid.x},{results[0].centroid.y}')
```

----------------------------------------

TITLE: Nominatim Search API Endpoint URL
DESCRIPTION: This snippet shows the base URL format for the Nominatim Search API. Parameters are appended to this URL to specify search queries and control output. It is the primary endpoint for both free-form and structured queries.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/api/Search.md#_snippet_0

LANGUAGE: URL
CODE:
```
https://nominatim.openstreetmap.org/search?<params>
```

----------------------------------------

TITLE: Retrieving Address Details in Nominatim API (JSONv2)
DESCRIPTION: This snippet illustrates a JSON response from the Nominatim API (using `format=jsonv2`) for a search query, providing extensive address details for a 'bakery in Berlin Wedding'. It includes specific address components like shop name, road, postcode, and suburb, along with bounding box and display name.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/api/Search.md#_snippet_3

LANGUAGE: JSON
CODE:
```
[
  {
    "address": {
      "ISO3166-2-lvl4": "DE-BE",
      "borough": "Mitte",
      "city": "Berlin",
      "country": "Deutschland",
      "country_code": "de",
      "neighbourhood": "Sprengelkiez",
      "postcode": "13347",
      "road": "Lindower Straße",
      "shop": "Ditsch",
      "suburb": "Wedding"
    },
    "addresstype": "shop",
    "boundingbox": [
      "52.5427201",
      "52.5427654",
      "13.3668619",
      "13.3669442"
    ],
    "category": "shop",
    "display_name": "Ditsch, Lindower Straße, Sprengelkiez, Wedding, Mitte, Berlin, 13347, Deutschland",
    "importance": 9.99999999995449e-06,
    "lat": "52.54274275",
    "licence": "Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright",
    "lon": "13.36690305710228",
    "name": "Ditsch",
    "osm_id": 437595031,
    "osm_type": "way",
    "place_id": 204751033,
    "place_rank": 30,
    "type": "bakery"
  }
]
```

----------------------------------------

TITLE: Fitting Map Bounds with Leaflet
DESCRIPTION: This JavaScript snippet demonstrates how to use the bounding box information returned by Nominatim to pan and center a map using the Leaflet library. It takes the bounding box array (min lat, max lat, min lon, max lon) and converts it into the format required by Leaflet's fitBounds method.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/api/Output.md#_snippet_3

LANGUAGE: JavaScript
CODE:
```
map.fitBounds([[bbox[0],bbox[2]],[bbox[1],bbox[3]]], {padding: [20, 20], maxzoom: 16});
```

----------------------------------------

TITLE: Searching Nominatim Database (Sync Python)
DESCRIPTION: Shows how to perform a simple synchronous search query using the `NominatimAPI` class. It connects to the local Nominatim database, searches for 'Brugge', and prints the coordinates of the first result.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/library/Getting-Started.md#_snippet_1

LANGUAGE: python
CODE:
```
import nominatim_api as napi

with napi.NominatimAPI() as api:
    results = api.search('Brugge')

if not results:
    print('Cannot find Brugge')
else:
    print(f'Found a place at {results[0].centroid.x},{results[0].centroid.y}')
```

----------------------------------------

TITLE: Creating Acronym Variants with Python Token Analyzer
DESCRIPTION: This Python class `AcronymMaker` implements a Nominatim token analysis module. The `get_canonical_id` method returns a normalized, transliterated version of the name as a canonical ID. The `compute_variants` method generates a list of variants; it always includes the transliterated full name and, for names longer than 20 characters, it creates an acronym from the first letters of each word, adding it as a variant if the acronym is at least 3 characters long. The module interface functions `configure` and `create` handle setup and instantiation.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/develop/ICU-Tokenizer-Modules.md#_snippet_4

LANGUAGE: python
CODE:
```
class AcronymMaker:
    """ This class is the actual analyzer.
    """
    def __init__(self, norm, trans):
        self.norm = norm
        self.trans = trans


    def get_canonical_id(self, name):
        # In simple cases, the normalized name can be used as a canonical id.
        return self.norm.transliterate(name.name).strip()


    def compute_variants(self, name):
        # The transliterated form of the name always makes up a variant.
        variants = [self.trans.transliterate(name)]

        # Only create acronyms from very long words.
        if len(name) > 20:
            # Take the first letter from each word to form the acronym.
            acronym = ''.join(w[0] for w in name.split())
            # If that leds to an acronym with at least three letters,
            # add the resulting acronym as a variant.
            if len(acronym) > 2:
                # Never forget to transliterate the variants before returning them.
                variants.append(self.trans.transliterate(acronym))

        return variants

# The following two functions are the module interface.

def configure(rules, normalizer, transliterator):
    # There is no configuration to parse and no data to set up.
    # Just return an empty configuration.
    return None


def create(normalizer, transliterator, config):
    # Return a new instance of our token analysis class above.
    return AcronymMaker(normalizer, transliterator)
```

----------------------------------------

TITLE: Querying Place Details by OSM ID (XML URL)
DESCRIPTION: This URL format allows retrieving place details using the OpenStreetMap object type (Node, Way, Relation) and ID. The 'class' parameter is optional and helps distinguish between multiple place entries for the same OSM object.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/api/Details.md#_snippet_0

LANGUAGE: xml
CODE:
```
https://nominatim.openstreetmap.org/details?osmtype=[N|W|R]&osmid=<value>&class=<value>
```

----------------------------------------

TITLE: Test Nominatim Search Query (Shell)
DESCRIPTION: Executes a simple search query using the `nominatim` command-line tool to test the installed Nominatim instance. Searches for the location 'Berlin'.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/admin/Import.md#_snippet_8

LANGUAGE: sh
CODE:
```
nominatim search --query Berlin
```

----------------------------------------

TITLE: Installing Nominatim from PyPI
DESCRIPTION: Installs the Nominatim database and API components directly from the Python Package Index (PyPI) using pip. This method requires pre-installed dependencies like osm2pgsql, PostgreSQL/PostGIS, and libICU.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/admin/Installation.md#_snippet_1

LANGUAGE: Shell
CODE:
```
pip install nominatim-db nominatim-api
```

----------------------------------------

TITLE: Install Nominatim Python Library
DESCRIPTION: Installs the Nominatim Python library package from PyPI using pip.
SOURCE: https://github.com/osm-search/nominatim/blob/master/packaging/nominatim-api/README.md#_snippet_0

LANGUAGE: Shell
CODE:
```
pip install nominatim-api
```

----------------------------------------

TITLE: Setting Up Python Virtual Environment and Installing Nominatim Packages (Shell)
DESCRIPTION: This snippet demonstrates how to create a Python virtual environment to manage Nominatim's dependencies separately. It then installs the necessary Nominatim API and database Python packages using pip within this isolated environment.
SOURCE: https://github.com/osm-search/nominatim/blob/master/README.md#_snippet_1

LANGUAGE: Shell
CODE:
```
python3 -m venv nominatim-venv
./nominatim-venv/bin/pip install packaging/nominatim-{api,db}
```

----------------------------------------

TITLE: Nominatim Reverse Geocoding GeocodeJSON Output
DESCRIPTION: Example GeocodeJSON response structure for a reverse geocoding request using the Nominatim API with the `format=geocodejson` parameter. It provides geocoding metadata and a Feature object with detailed address properties.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/api/Reverse.md#_snippet_4

LANGUAGE: json
CODE:
```
{
  "type": "FeatureCollection",
  "geocoding": {
    "version": "0.1.0",
    "attribution": "Data © OpenStreetMap contributors, ODbL 1.0. https:\/\/osm.org\/copyright",
    "licence": "ODbL",
    "query": "60.229917843587,11.16630979382"
  },
  "features": {
    "type": "Feature",
    "properties": {
      "geocoding": {
        "place_id": "42700574",
        "osm_type": "node",
        "osm_id": "3110596255",
        "type": "house",
        "accuracy": 0,
        "label": "1, Løvenbergvegen, Mogreina, Ullensaker, Akershus, 2054, Norway",
        "name": null,
        "housenumber": "1",
        "street": "Løvenbergvegen",
        "postcode": "2054",
        "county": "Akershus",
        "country": "Norway",
        "admin": {
          "level7": "Ullensaker",
          "level4": "Akershus",
          "level2": "Norway"
        }
      }
    },
    "geometry": {
      "type": "Point",
      "coordinates": [
        11.1658572,
        60.2301296
      ]
    }
  }
}
```

----------------------------------------

TITLE: Search Nominatim Async and Format Address Python
DESCRIPTION: Demonstrates performing an asynchronous Nominatim search with address details enabled and formatting the address parts using a specified locale preference. Requires the `nominatim_api` library and asyncio.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/library/Getting-Started.md#_snippet_5

LANGUAGE: python
CODE:
```
import asyncio

import nominatim_api as napi

async def search(query):
    async with napi.NominatimAPIAsync() as api:
        return await api.search(query, address_details=True)

results = asyncio.run(search('Brugge'))

locale = napi.Locales(['fr', 'en'])
for i, result in enumerate(results):
    address_parts = result.address_rows.localize(locale)
    print(f"{i + 1}. {', '.join(address_parts)}")
```

----------------------------------------

TITLE: Request Address Details in Nominatim Search Python
DESCRIPTION: Shows how to include the `address_details=True` parameter in a Nominatim search call to receive detailed address information in the results.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/library/Getting-Started.md#_snippet_7

LANGUAGE: python
CODE:
```
results = api.search('Brugge', address_details=True)
```

----------------------------------------

TITLE: Run Nominatim Server with Uvicorn (Falcon)
DESCRIPTION: Starts the Nominatim server using uvicorn, specifying the Falcon-based WSGI application factory.
SOURCE: https://github.com/osm-search/nominatim/blob/master/packaging/nominatim-api/README.md#_snippet_1

LANGUAGE: Shell
CODE:
```
uvicorn --factory nominatim.server.falcon.server:run_wsgi
```

----------------------------------------

TITLE: Install ASGI runner and server (sh)
DESCRIPTION: Installs the recommended packages for deploying a Python ASGI application: `falcon` (web framework), `uvicorn` (ASGI runner), and `gunicorn` (HTTP server) into the virtual environment.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/admin/Deployment-Python.md#_snippet_2

LANGUAGE: sh
CODE:
```
/srv/nominatim-venv/bin/pip install falcon uvicorn gunicorn
```

----------------------------------------

TITLE: Install virtualenv and Create Environment (Shell)
DESCRIPTION: Installs the `virtualenv` tool using apt-get on Debian/Ubuntu systems and then creates a new Python virtual environment at the specified path `/srv/nominatim-venv` to isolate Nominatim's dependencies.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/admin/Installation.md#_snippet_4

LANGUAGE: Shell
CODE:
```
sudo apt-get install virtualenv
virtualenv /srv/nominatim-venv
```

----------------------------------------

TITLE: Count rows in placex table using NominatimAPIAsync
DESCRIPTION: This Python snippet demonstrates how to establish a low-level database connection using NominatimAPIAsync, execute a simple SQLAlchemy query to count rows in the 'placex' table, and print the result. It requires the asyncio and sqlalchemy libraries.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/library/Low-Level-DB-Access.md#_snippet_0

LANGUAGE: Python
CODE:
```
import asyncio
import sqlalchemy as sa
from nominatim_api import NominatimAPIAsync

async def print_table_size():
    api = NominatimAPIAsync()

    async with api.begin() as conn:
        cnt = await conn.scalar(sa.select(sa.func.count()).select_from(conn.t.placex))
        print(f'placex table has {cnt} rows.')

asyncio.run(print_table_size())
```

----------------------------------------

TITLE: Starting Nominatim Data Import (Shell)
DESCRIPTION: Initiates the Nominatim data import process using the specified OSM data file. The command redirects standard error to standard output and pipes the combined output to the 'tee' command, which displays the output on the console and saves it to 'setup.log'.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/admin/Import.md#_snippet_6

LANGUAGE: sh
CODE:
```
nominatim import --osm-file <data file> 2>&1 | tee setup.log
```

----------------------------------------

TITLE: Example Nominatim Place Object (JSON)
DESCRIPTION: Illustrates the structure of a single place object returned by Nominatim API calls (/reverse, /search, /lookup) when the 'format' parameter is set to 'json'. It shows common fields like place_id, OSM details, coordinates, display name, importance, and nested address/extratags objects.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/api/Output.md#_snippet_0

LANGUAGE: JSON
CODE:
```
  {
    "place_id": 100149,
    "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
    "osm_type": "node",
    "osm_id": "107775",
    "boundingbox": ["51.3473219", "51.6673219", "-0.2876474", "0.0323526"],
    "lat": "51.5073219",
    "lon": "-0.1276474",
    "display_name": "London, Greater London, England, SW1A 2DU, United Kingdom",
    "class": "place",
    "type": "city",
    "importance": 0.9654895765402,
    "icon": "https://nominatim.openstreetmap.org/images/mapicons/poi_place_city.p.20.png",
    "address": {
      "city": "London",
      "state_district": "Greater London",
      "state": "England",
      "ISO3166-2-lvl4": "GB-ENG",
      "postcode": "SW1A 2DU",
      "country": "United Kingdom",
      "country_code": "gb"
    },
    "extratags": {
      "capital": "yes",
      "website": "http://www.london.gov.uk",
      "wikidata": "Q84",
      "wikipedia": "en:London",
      "population": "8416535"
    }
  }
```

----------------------------------------

TITLE: Creating Project Directory and Importing OSM Data (Shell)
DESCRIPTION: This snippet details the process of preparing a project directory and importing OpenStreetMap data into Nominatim. It creates a dedicated directory, navigates into it, and then uses the Nominatim import tool to load a specified planet file, logging the output.
SOURCE: https://github.com/osm-search/nominatim/blob/master/README.md#_snippet_2

LANGUAGE: Shell
CODE:
```
mkdir nominatim-project
cd nominatim-project
../nominatim-venv/bin/nominatim import --osm-file <your planet file> 2>&1 | tee setup.log
```

----------------------------------------

TITLE: Import OSM Data into Nominatim Database
DESCRIPTION: Initiates the process of importing OpenStreetMap data from a specified PBF file into the Nominatim database within the current project directory. Replace <downlaoded-osm-data.pbf> with the actual path to your downloaded data file.
SOURCE: https://github.com/osm-search/nominatim/blob/master/packaging/nominatim-db/README.md#_snippet_4

LANGUAGE: Shell
CODE:
```
nominatim import --osm-file <downlaoded-osm-data.pbf>
```

----------------------------------------

TITLE: Install virtualenv and create environment (sh)
DESCRIPTION: Installs the `virtualenv` package using apt-get and then creates a new Python virtual environment at `/srv/nominatim-venv`. This environment will be used to isolate the Nominatim frontend dependencies.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/admin/Deployment-Python.md#_snippet_0

LANGUAGE: sh
CODE:
```
sudo apt-get install virtualenv
virtualenv /srv/nominatim-venv
```

----------------------------------------

TITLE: Grant SELECT on country_osm_grid (SQL)
DESCRIPTION: Grants read permissions on the `country_osm_grid` table to the specified database user, typically the user running the web server.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/admin/Migration.md#_snippet_15

LANGUAGE: sql
CODE:
```
GRANT SELECT ON table country_osm_grid to "www-user";
```

----------------------------------------

TITLE: Setup Python Virtual Environment and Install Dependencies (Shell)
DESCRIPTION: Creates a Python virtual environment and installs all required Python packages for Nominatim development, testing, and documentation building using pip.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/develop/Development-Environment.md#_snippet_2

LANGUAGE: sh
CODE:
```
virtualenv ~/nominatim-dev-venv
~/nominatim-dev-venv/bin/pip install\
    psutil 'psycopg[binary]' PyICU SQLAlchemy \
    python-dotenv jinja2 pyYAML \
    mkdocs 'mkdocstrings[python]' mkdocs-gen-files \
    pytest pytest-asyncio pytest-bdd flake8 \
    types-jinja2 types-markupsafe types-psutil types-psycopg2 \
    types-pygments types-pyyaml types-requests types-ujson \
    types-urllib3 typing-extensions unicorn falcon starlette \
    uvicorn mypy osmium aiosqlite
```

----------------------------------------

TITLE: Install Dependencies (Ubuntu/Debian)
DESCRIPTION: Installs required dependencies osm2pgsql (>=1.8) and PostgreSQL (>=9.6) with PostGIS extensions using the apt-get package manager on Ubuntu (>=23.04) or Debian (with backports).
SOURCE: https://github.com/osm-search/nominatim/blob/master/packaging/nominatim-db/README.md#_snippet_0

LANGUAGE: Shell
CODE:
```
sudo apt-get install osm2pgsql postgresql-postgis
```

----------------------------------------

TITLE: Configuring Postcode Pattern and Output (YAML)
DESCRIPTION: Example configuration in YAML for a country (e.g., 'bm') to define a custom postcode format. The 'pattern' field uses Python-like regular expression syntax with 'd' for digits and 'l' for letters to match valid postcode variations. The optional 'output' field uses regex expand syntax to specify the canonical spelling, referring to groups captured in the pattern. This allows Nominatim to handle multiple input formats and standardize the output.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/customize/Country-Settings.md#_snippet_2

LANGUAGE: YAML
CODE:
```
bm:
    postcode:
      pattern: "(ll)[ -]?(dd)"
      output: \1 \2
```

----------------------------------------

TITLE: Resuming Nominatim Import (Indexing Stage) - Shell
DESCRIPTION: Command to resume a Nominatim import process that was interrupted after reaching the indexing stage. Check the last log output to confirm the stage. If the reported rank is 26 or higher, you can also safely add `--index-noanalyse`.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/admin/Faq.md#_snippet_0

LANGUAGE: sh
CODE:
```
nominatim import --continue indexing
```

----------------------------------------

TITLE: Start Vagrant Virtual Machine - Shell
DESCRIPTION: This command starts the Vagrant-managed virtual machine defined in the Vagrantfile, specifically the 'ubuntu24-nginx' box. It provisions the VM according to the configuration.
SOURCE: https://github.com/osm-search/nominatim/blob/master/VAGRANT.md#_snippet_1

LANGUAGE: Shell
CODE:
```
vagrant up ubuntu24-nginx
```

----------------------------------------

TITLE: Retrieving Location Data with SVG Polygon in Nominatim API (JSON)
DESCRIPTION: This snippet shows a standard JSON response from the Nominatim API for a specific address query, including detailed address components, bounding box coordinates, and an SVG polygon string representing the location's geometry. It demonstrates how to request and interpret geometric data in SVG format.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/api/Search.md#_snippet_2

LANGUAGE: JSON
CODE:
```
[
  {
    "address": {
      "ISO3166-2-lvl4": "DE-BE",
      "borough": "Mitte",
      "city": "Berlin",
      "country": "Deutschland",
      "country_code": "de",
      "historic": "Kommandantenhaus",
      "house_number": "1",
      "neighbourhood": "Friedrichswerder",
      "postcode": "10117",
      "road": "Unter den Linden",
      "suburb": "Mitte"
    },
    "boundingbox": [
      "52.5170798",
      "52.5173311",
      "13.3975116",
      "13.3981577"
    ],
    "class": "historic",
    "display_name": "Kommandantenhaus, 1, Unter den Linden, Friedrichswerder, Mitte, Berlin, 10117, Deutschland",
    "importance": 0.8135042058306902,
    "lat": "52.51720765",
    "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
    "lon": "13.397834399325466",
    "osm_id": 15976890,
    "osm_type": "way",
    "place_id": 108681845,
    "svg": "M 13.3975116 -52.5172905 L 13.397549 -52.5170798 13.397715 -52.5170906 13.3977122 -52.5171064 13.3977392 -52.5171086 13.3977417 -52.5170924 13.3979655 -52.5171069 13.3979623 -52.5171233 13.3979893 -52.5171248 13.3979922 -52.5171093 13.3981577 -52.5171203 13.398121 -52.5173311 13.3978115 -52.5173103 Z",
    "type": "house"
  }
]
```

----------------------------------------

TITLE: Configure Nginx Location for Nominatim UI Files
DESCRIPTION: Defines an Nginx `location` block for the `/ui/` path. It uses `alias` to map this path to the physical directory containing the nominatim-ui distribution files and sets `index.html` as the default file to serve.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/admin/Setup-Nominatim-UI.md#_snippet_2

LANGUAGE: Nginx
CODE:
```
server {

    # Here is the Nominatim setup as described in the Installation section

    location /ui/ {
        alias <full path to the nominatim-ui directory>/dist/;
        index index.html;
    }
}
```

----------------------------------------

TITLE: Running Initial Import for Multiple Regions with Updates - Bash
DESCRIPTION: This command executes a custom bash script (import_multiple_regions.sh) designed for the initial import of multiple regions intended for future updates. The script handles downloading data, importing it into Nominatim, and setting up the necessary state files for replication. This is part of the advanced setup for maintaining multiple regions with ongoing updates.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/admin/Advanced-Installations.md#_snippet_7

LANGUAGE: Bash
CODE:
```
bash import_multiple_regions.sh
```

----------------------------------------

TITLE: Granting Schema Create Rights to Nominatim Import User - SQL/Bash
DESCRIPTION: This command uses the psql client to connect to the 'nominatim' database and execute a SQL command. The SQL command GRANT CREATE ON SCHEMA public TO "import-user" grants the specified database user ('import-user') the necessary permissions to create tables within the 'public' schema. This is required for the import user when they do not have inherent superuser rights.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/admin/Advanced-Installations.md#_snippet_1

LANGUAGE: SQL/Bash
CODE:
```
psql -d nominatim -c 'GRANT CREATE ON SCHEMA public TO "import-user"'
```

----------------------------------------

TITLE: Nominatim Lookup Result JSON with Extratags
DESCRIPTION: Example JSON response from a Nominatim lookup query for a single OpenStreetMap Way object, including the `extratags` parameter to retrieve additional key-value pairs associated with the object.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/api/Lookup.md#_snippet_2

LANGUAGE: JSON
CODE:
```
[
   {
      "place_id": 115462561,
      "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
      "osm_type": "way",
      "osm_id": 50637691,
      "boundingbox": [
        "52.3994612",
        "52.3996426",
        "13.0479574",
        "13.0481754"
      ],
      "lat": "52.399550700000006",
      "lon": "13.048066846939687",
      "display_name": "Brandenburger Tor, Brandenburger Straße, Historische Innenstadt, Innenstadt, Potsdam, Brandenburg, 14467, Germany",
      "class": "tourism",
      "type": "attraction",
      "importance": 0.2940287400552381,
      "address": {
        "tourism": "Brandenburger Tor",
        "road": "Brandenburger Straße",
        "suburb": "Historische Innenstadt",
        "city": "Potsdam",
        "state": "Brandenburg",
        "postcode": "14467",
        "country": "Germany",
        "country_code": "de"
      },
      "extratags": {
        "image": "http://commons.wikimedia.org/wiki/File:Potsdam_brandenburger_tor.jpg",
        "heritage": "4",
        "wikidata": "Q695045",
        "architect": "Carl von Gontard;Georg Christian Unger",
        "wikipedia": "de:Brandenburger Tor (Potsdam)",
        "wheelchair": "yes",
        "description": "Kleines Brandenburger Tor in Potsdam",
        "heritage:website": "http://www.bldam-brandenburg.de/images/stories/PDF/DML%202012/04-p-internet-13.pdf",
        "heritage:operator": "bldam",
        "architect:wikidata": "Q68768;Q95223",
        "year_of_construction": "1771"
      }
   }
]
```

----------------------------------------

TITLE: Configure Nominatim Gunicorn service (systemd)
DESCRIPTION: Creates a systemd service unit file (`/etc/systemd/system/nominatim.service`) to run the Nominatim frontend via Gunicorn. It specifies the user, working directory, the command to start Gunicorn (binding to the socket, using 4 Uvicorn workers), log files, and dependencies on the socket unit.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/admin/Deployment-Python.md#_snippet_4

LANGUAGE: systemd
CODE:
```
[Unit]
Description=Nominatim running as a gunicorn application
After=network.target
Requires=nominatim.socket

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/srv/nominatim-project
ExecStart=/srv/nominatim-venv/bin/gunicorn -b unix:/run/nominatim.sock -w 4 -k uvicorn.workers.UvicornWorker "nominatim_api.server.falcon.server:run_wsgi()"
ExecReload=/bin/kill -s HUP $MAINPID
StandardOutput=append:/var/log/gunicorn-nominatim.log
StandardError=inherit
PrivateTmp=true
TimeoutStopSec=5
KillMode=mixed

[Install]
WantedBy=multi-user.target
```

----------------------------------------

TITLE: Nominatim Reverse Geocoding JSONv2 Output
DESCRIPTION: Example JSON response structure for a reverse geocoding request using the Nominatim API with the `format=jsonv2` parameter. It includes detailed address information, bounding box, and OSM identifiers.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/api/Reverse.md#_snippet_2

LANGUAGE: json
CODE:
```
{
  "place_id":"134140761",
  "licence":"Data © OpenStreetMap contributors, ODbL 1.0. https:\/\/www.openstreetmap.org\/copyright",
  "osm_type":"way",
  "osm_id":"280940520",
  "lat":"-34.4391708",
  "lon":"-58.7064573",
  "place_rank":"26",
  "category":"highway",
  "type":"motorway",
  "importance":"0.1",
  "addresstype":"road",
  "display_name":"Autopista Pedro Eugenio Aramburu, El Triángulo, Partido de Malvinas Argentinas, Buenos Aires, 1.619, Argentina",
  "name":"Autopista Pedro Eugenio Aramburu",
  "address":{
    "road":"Autopista Pedro Eugenio Aramburu",
    "village":"El Triángulo",
    "state_district":"Partido de Malvinas Argentinas",
    "state":"Buenos Aires",
    "postcode":"1.619",
    "country":"Argentina",
    "country_code":"ar"
  },
  "boundingbox":["-34.44159","-34.4370994","-58.7086067","-58.7044712"]
}
```

----------------------------------------

TITLE: Configuring Nominatim API with Project Directory (Python)
DESCRIPTION: Demonstrates how to initialize the Nominatim API library (both async and sync versions) by providing the path to a Nominatim project directory. The library reads configuration, including database connection details, from the .env file within this directory.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/library/Getting-Started.md#_snippet_2

LANGUAGE: python
CODE:
```
import asyncio

import nominatim_api as napi

async def search(query):
    async with napi.NominatimAPIAsync('/srv/nominatim-project') as api:
        return await api.search(query)

results = asyncio.run(search('Brugge'))
if not results:
    print('Cannot find Brugge')
else:
    print(f'Found a place at {results[0].centroid.x},{results[0].centroid.y}')
```

LANGUAGE: python
CODE:
```
import nominatim_api as napi

with napi.NominatimAPI('/srv/nominatim-project') as api:
    results = api.search('Brugge')

if not results:
    print('Cannot find Brugge')
else:
    print(f'Found a place at {results[0].centroid.x},{results[0].centroid.y}')
```

----------------------------------------

TITLE: Install Core Nominatim Prerequisites (Shell)
DESCRIPTION: Installs essential system packages required for Nominatim development, including spatial database support, OSM data processing tools, and virtual environment management.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/develop/Development-Environment.md#_snippet_1

LANGUAGE: sh
CODE:
```
sudo apt install libsqlite3-mod-spatialite osm2pgsql \
                 postgresql-postgis postgresql-postgis-scripts \
                 pkg-config libicu-dev virtualenv
```

----------------------------------------

TITLE: Activate Nominatim Development Virtual Environment (Shell)
DESCRIPTION: Activates the previously created Python virtual environment, making the installed packages and scripts available in the current shell session.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/develop/Development-Environment.md#_snippet_3

LANGUAGE: sh
CODE:
```
. ~/nominatim-dev-venv/bin/activate
```

----------------------------------------

TITLE: Customizing StatusResult Text Format - Python
DESCRIPTION: This example shows how to define a custom formatter for the `StatusResult` type using the existing 'text' format. It uses the `@dispatch.format_func` decorator to register the function and demonstrates accessing result properties (`result.status`, `result.message`) to generate the output string.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/customize/Result-Formatting.md#_snippet_3

LANGUAGE: python
CODE:
```
from nominatim_api import StatusResult

@dispatch.format_func(StatusResult, 'text')
def _format_status_text(result, _):
    header = 'Status for server nominatim.openstreetmap.org'
    if result.status:
        return f"{header}\n\nERROR: {result.message}"

    return f"{header}\n\nOK"
```

----------------------------------------

TITLE: Configuring Nominatim Tokenizer with Custom Sanitizer (YAML)
DESCRIPTION: This YAML snippet shows how to integrate a custom Python sanitizer into the Nominatim `icu_tokenizer.yaml` configuration. It adds a `sanitizers` list under the `...` (presumably part of the tokenizer configuration) and specifies the custom sanitizer module by its filename (`us_streets.py`) as a `step`. This tells Nominatim to apply the logic defined in the Python file during the tokenization process.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/develop/ICU-Tokenizer-Modules.md#_snippet_3

LANGUAGE: yaml
CODE:
```
...
sanitizers:
    - step: us_streets.py
...
```

----------------------------------------

TITLE: Enable and start Nominatim systemd services (sh)
DESCRIPTION: Reloads the systemd manager configuration to recognize the new unit files, then enables and starts both the `nominatim.socket` and `nominatim.service` units. This ensures the Nominatim frontend starts automatically on boot.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/admin/Deployment-Python.md#_snippet_5

LANGUAGE: sh
CODE:
```
sudo systemctl daemon-reload
sudo systemctl enable nominatim.socket
sudo systemctl start nominatim.socket
sudo systemctl enable nominatim.service
sudo systemctl start nominatim.service
```

----------------------------------------

TITLE: Force Recomputation of Object and Dependents - Nominatim Shell
DESCRIPTION: Invalidates an OpenStreetMap object (Node, Way, or Relation specified by type and ID) and all dependent objects (like places within its area) in the Nominatim database, forcing their recomputation. This is useful when replication updates skip changes affecting many objects. Requires subsequent indexing or continuous updates to take effect.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/admin/Maintenance.md#_snippet_3

LANGUAGE: Shell
CODE:
```
nominatim refresh --data-area [NWR]<id>
```

----------------------------------------

TITLE: Configuring Nominatim Flatnode File (config)
DESCRIPTION: Sets the `NOMINATIM_FLATNODE_FILE` variable in the `.env` configuration file. This enables flatnode storage for node locations, saving import time and disk space for large datasets.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/admin/Import.md#_snippet_2

LANGUAGE: config
CODE:
```
NOMINATIM_FLATNODE_FILE="/path/to/flatnode.file"
```

----------------------------------------

TITLE: Retrieving Location Data in GeocodeJSON Format from Nominatim API
DESCRIPTION: This snippet demonstrates a GeocodeJSON `FeatureCollection` response from the Nominatim API. It provides geocoding-specific metadata under the `geocoding` object and represents the location as a `Point` geometry within a `Feature`, with a `geocoding` property containing type, label, and name.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/api/Search.md#_snippet_5

LANGUAGE: JSON
CODE:
```
{
  "type": "FeatureCollection",
  "geocoding": {
    "version": "0.1.0",
    "attribution": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
    "licence": "ODbL",
    "query": "Αγία Τριάδα, Αδωνιδος, Athens, Greece"
  },
  "features": [
    {
      "type": "Feature",
      "properties": {
        "geocoding": {
          "type": "place_of_worship",
          "label": "Αγία Τριάδα, Αδωνιδος, Άγιος Νικόλαος, 5º Δημοτικό Διαμέρισμα Αθηνών, Athens, Municipality of Athens, Regional Unit of Central Athens, Region of Attica, Attica, 11472, Greece",
          "name": "Αγία Τριάδα",
          "admin": null
        }
      },
      "geometry": {
        "type": "Point",
        "coordinates": [
          23.72949633941,
          38.0051697
        ]
      }
    }
  ]
}
```

----------------------------------------

TITLE: Import Nominatim Data - Shell
DESCRIPTION: These commands, executed inside the VM, navigate to the project directory, download a small OSM PBF file (Monaco), and then run the Nominatim import process using that file. The output is logged to a file.
SOURCE: https://github.com/osm-search/nominatim/blob/master/VAGRANT.md#_snippet_3

LANGUAGE: Shell
CODE:
```
# inside the virtual machine:
cd nominatim-project
wget --no-verbose --output-document=monaco.osm.pbf http://download.geofabrik.de/europe/monaco-latest.osm.pbf
nominatim import --osm-file monaco.osm.pbf 2>&1 | tee monaco.$$.log
```

----------------------------------------

TITLE: Nominatim Reverse Geocoding GeoJSON Output
DESCRIPTION: Example GeoJSON response structure for a reverse geocoding request using the Nominatim API with the `format=geojson` parameter. It returns a FeatureCollection containing a Feature with properties and geometry.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/api/Reverse.md#_snippet_3

LANGUAGE: json
CODE:
```
{
  "type": "FeatureCollection",
  "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https:\/\/osm.org\/copyright",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "place_id": "18512203",
        "osm_type": "node",
        "osm_id": "1704756187",
        "place_rank": "30",
        "category": "place",
        "type": "house",
        "importance": "0",
        "addresstype": "place",
        "name": null,
        "display_name": "71, Via Guglielmo Marconi, Saragozza-Porto, Bologna, BO, Emilia-Romagna, 40122, Italy",
        "address": {
          "house_number": "71",
          "road": "Via Guglielmo Marconi",
          "suburb": "Saragozza-Porto",
          "city": "Bologna",
          "county": "BO",
          "state": "Emilia-Romagna",
          "postcode": "40122",
          "country": "Italy",
          "country_code": "it"
        }
      },
      "bbox": [
        11.3397676,
        44.5014307,
        11.3399676,
        44.5016307
      ],
      "geometry": {
        "type": "Point",
        "coordinates": [
          11.3398676,
          44.5015307
        ]
      }
    }
  ]
}
```

----------------------------------------

TITLE: Retrieving Location Data in GeoJSON Format from Nominatim API
DESCRIPTION: This snippet presents a GeoJSON `FeatureCollection` response from the Nominatim API for an address query. It encapsulates the location as a `Point` geometry within a `Feature` object, including properties like `place_id`, `osm_type`, `display_name`, and `importance`, adhering to the GeoJSON standard.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/api/Search.md#_snippet_4

LANGUAGE: JSON
CODE:
```
{
  "type": "FeatureCollection",
  "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "place_id": "35811445",
        "osm_type": "node",
        "osm_id": "2846295644",
        "display_name": "17, Strada Pictor Alexandru Romano, Bukarest, Bucharest, Sector 2, Bucharest, 023964, Romania",
        "place_rank": "30",
        "category": "place",
        "type": "house",
        "importance": 0.62025
      },
      "bbox": [
        26.1156689,
        44.4354754,
        26.1157689,
        44.4355754
      ],
      "geometry": {
        "type": "Point",
        "coordinates": [
          26.1157189,
          44.4355254
        ]
      }
    }
  ]
}
```

----------------------------------------

TITLE: Reconfiguring System Locales - Shell
DESCRIPTION: Command to reconfigure installed locales on Debian/Ubuntu systems. This can be used to generate and make UTF-8 locales available, resolving `UnicodeEncodeError` issues caused by missing or improperly configured locales.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/admin/Faq.md#_snippet_5

LANGUAGE: sh
CODE:
```
dpkg-reconfigure locales
```

----------------------------------------

TITLE: Preparing Nominatim Database with Superuser - Bash
DESCRIPTION: This command prepares the Nominatim database schema using a PostgreSQL user with superuser privileges. It sets the NOMINATIM_DATABASE_DSN environment variable to specify the database connection details before running the nominatim import --prepare-database command. This step is necessary when the user performing the main import lacks schema creation rights.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/admin/Advanced-Installations.md#_snippet_0

LANGUAGE: Bash
CODE:
```
NOMINATIM_DATABASE_DSN="pgsql:dbname=nominatim;user=dbadmin" nominatim import --prepare-database
```

----------------------------------------

TITLE: Configuring Nominatim UI Directory and Alias (Apache)
DESCRIPTION: Configures an Apache Directory block for the nominatim-ui distribution files, setting the default index file to `search.html` and granting access. It then defines an alias mapping the `/nominatim/ui` URL path to this directory, ensuring the UI is accessible. This alias must precede the main Nominatim alias.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/admin/Setup-Nominatim-UI.md#_snippet_6

LANGUAGE: apache
CODE:
```
<Directory "/home/vagrant/nominatim-ui/dist">
  DirectoryIndex search.html
  Require all granted
</Directory>

Alias /nominatim/ui /home/vagrant/nominatim-ui/dist
```

----------------------------------------

TITLE: Search Nominatim Sync and Format Address Python
DESCRIPTION: Demonstrates performing a synchronous Nominatim search with address details enabled and formatting the address parts using a specified locale preference. Requires the `nominatim_api` library.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/library/Getting-Started.md#_snippet_6

LANGUAGE: python
CODE:
```
import nominatim_api as napi

with napi.NominatimAPI() as api:
    results = api.search('Brugge', address_details=True)

locale = napi.Locales(['fr', 'en'])
for i, result in enumerate(results):
    address_parts = result.address_rows.localize(locale)
    print(f"{i + 1}. {', '.join(address_parts)}")
```

----------------------------------------

TITLE: Nominatim Reverse Geocoding API Endpoint (URL)
DESCRIPTION: This snippet shows the base URL format for accessing the Nominatim Reverse Geocoding API. It requires 'lat' and 'lon' parameters for the coordinate and accepts additional parameters.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/api/Reverse.md#_snippet_0

LANGUAGE: URL
CODE:
```
https://nominatim.openstreetmap.org/reverse?lat=<value>&lon=<value>&<params>
```

----------------------------------------

TITLE: Nominatim Lookup API Endpoint URL
DESCRIPTION: The base URL and required `osm_ids` parameter format for querying the Nominatim lookup API. `osm_ids` must be a comma-separated list of OSM object IDs, each prefixed with its type (N, W, or R). Up to 50 IDs are allowed per request.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/api/Lookup.md#_snippet_0

LANGUAGE: URL
CODE:
```
https://nominatim.openstreetmap.org/lookup?osm_ids=[N|W|R]<value>,…,…,&<params>
```

----------------------------------------

TITLE: Run All Nominatim Tests (Shell)
DESCRIPTION: Executes the default make target to run the complete Nominatim test suite, including linting, mypy checks, pytest unit tests, and pytest-bdd behavioral tests.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/develop/Development-Environment.md#_snippet_5

LANGUAGE: sh
CODE:
```
make tests
```

----------------------------------------

TITLE: Clean Large Deleted Objects - Nominatim Shell
DESCRIPTION: Removes large areas that were deleted in OpenStreetMap but kept in the Nominatim database's import_polygon_delete table because they were too large for automatic deletion. The command requires a PostgreSQL time interval argument to specify the minimum age of deletions to clean.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/admin/Maintenance.md#_snippet_4

LANGUAGE: Shell
CODE:
```
nominatim admin --clean-deleted <PostgreSQL Time Interval>
```

----------------------------------------

TITLE: Example Nominatim Rank Configuration JSON
DESCRIPTION: This JSON snippet shows the structure of the configuration file used to assign search and address ranks. It consists of an array of entries, each defining ranks for specific tags, optionally limited to certain countries. Ranks can be a single number (both search and address) or an array [search, address].
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/customize/Ranking.md#_snippet_0

LANGUAGE: JSON
CODE:
```
[
  {
    "tags" : {
      "place" : {
        "county" : 12,
        "city" : 16
      },
      "landuse" : {
        "residential" : 22,
        "" : 30
      }
    }
  },
  {
    "countries" : [ "ca", "us" ],
    "tags" : {
      "boundary" : {
        "administrative8" : 18,
        "administrative9" : 20
      },
      "landuse" : {
        "residential" : [22, 0]
      }
    }
  }
]
```

----------------------------------------

TITLE: Formatter Function Signature - Python
DESCRIPTION: This snippet illustrates the required signature for a formatter function used with the `FormatDispatcher`. A formatter function takes the result object (of a specific `ResultType`) and an options dictionary as input and must return a string representing the formatted output.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/customize/Result-Formatting.md#_snippet_2

LANGUAGE: python
CODE:
```
def format_func(result: ResultType, options: Mapping[str, Any]) -> str
```

----------------------------------------

TITLE: Configure Nominatim Gunicorn socket (systemd)
DESCRIPTION: Creates a systemd socket unit file (`/etc/systemd/system/nominatim.socket`) that defines a Unix domain socket (`/run/nominatim.sock`) for Gunicorn to listen on. It sets the socket owner to `www-data`.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/admin/Deployment-Python.md#_snippet_3

LANGUAGE: systemd
CODE:
```
[Unit]
Description=Gunicorn socket for Nominatim

[Socket]
ListenStream=/run/nominatim.sock
SocketUser=www-data

[Install]
WantedBy=multi-user.target
```

----------------------------------------

TITLE: Update Nominatim SQL Functions (Full, Shell)
DESCRIPTION: Runs the Nominatim setup script with flags to recreate all SQL functions, enable differential updates, and create partition functions.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/admin/Migration.md#_snippet_6

LANGUAGE: sh
CODE:
```
./utils/setup.php --create-functions --enable-diff-updates --create-partition-functions
```

----------------------------------------

TITLE: Successful Status Response (JSON)
DESCRIPTION: This JSON object represents a successful response from the Nominatim status endpoint when the 'format' parameter is set to 'json'. It includes the status code, message, data update timestamp, and software/database versions.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/api/Status.md#_snippet_0

LANGUAGE: json
CODE:
```
{
      "status": 0,
      "message": "OK",
      "data_updated": "2020-05-04T14:47:00+00:00",
      "software_version": "3.6.0-0",
      "database_version": "3.6.0-0"
  }
```

----------------------------------------

TITLE: Stop and Monitor Nominatim Update Service (Shell)
DESCRIPTION: Shell commands to stop the nominatim-updates systemd timer, check the active status of the associated service, and view the service's output logs using journalctl.
SOURCE: https://github.com/osm-search/nominatim/blob/master/docs/admin/Update.md#_snippet_4

LANGUAGE: Shell
CODE:
```
sudo systemctl stop nominatim-updates.timer
sudo systemctl is-active nominatim-updates.service
journalctl -u nominatim-updates.service
```