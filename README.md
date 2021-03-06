# blockchain-api-client

Powered by [![Blockchain]()](https://blockchain.info/api)

Client written in Python 3 for Blockchain API service:

### Features

  - Get Bitcoin blockchain charts data
  - Get Bitcoin blockchain statistical data
  - Get Bitcoin mining pools data

You can also:

  - Persist data via JSON format file pipeline
  - Persist data via [MongoDB][mongoDB] pipeline
  - Persist data via [PostgreSQL][postgreSQL] pipeline
  - Automatize data fetching with jobs scheduler
  - Deploy to [Heroku cloud platform][heroku]

### Getting Started

These instructions will get you a copy of the project on your local system.

#### Prerequisites

Blockchain API Client uses a number of open source projects to work properly:

* [apscheduler] - Advanced Python Scheduler
* [configparser] - Configuration file parser
* [psycopg2] - PostgreSQL adapter fo Python
* [pymongo] - Python driver for MongoDB
* [python-dotenv] - .env file management
* [requests] - HTTP for Humans

And of course Blockchain API Client itself is open source with a [public repository][blockchain-api-client] on GitHub.

#### Installation

#### Quick Start

A step by step series of examples:

Get historical price for Bitcoin in json format
```python
from blockchain.api import BlockchainAPIClient
api = BlockchainAPIClient('charts')
response = api.call(chart='market-price', timespan='all')
```

Get market capitalization for Bitcoin in json format
```python
from blockchain.api import BlockchainAPIClient
api = BlockchainAPIClient('charts')
response = api.call(chart='market-cap', timespan='all')
```

Get Bitcoin blockchain statistics in json format
```python
from blockchain.api import BlockchainAPIClient
api = BlockchainAPIClient('stats')
response = api.call()
```

Get Bitcoin minig pools info in json format
```python
from blockchain.api import BlockchainAPIClient
api = BlockchainAPIClient('pools')
response = api.call(timespan='5days')
```

Persist data in JSON file
```python
from blockchain.pipelines import JSONFileWriterPipeline
file = JSONFileWriterPipeline.config()
file.write(response)
```

Persist (save/update) data with MongoDB
```python
from blockchain.pipelines import MongoDBPipeline
mongo = MongoDBPipeline.config()
mongo.open_connection()
mongo.persist_data(response)
mongo.close_connection()
```

For a complete description of available parameters please check [Blockchain API documentation][official docs]

License
----

MIT


**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen.)

[apscheduler]: <https://github.com/agronholm/apscheduler>
[blockchain-api-client]: <https://github.com/sdediego/blockchain-api-client>
[configparser]: <https://github.com/python/cpython/blob/3.5/Lib/configparser.py>
[heroku]: <https://www.heroku.com>
[mongoDB]: <https://www.mongodb.com>
[postgreSQL]: <https://www.postgresql.org/>
[psycopg2]: <http://initd.org/psycopg/>
[pymongo]: <https://github.com/mongodb/mongo-python-driver>
[python-dotenv]: <https://github.com/theskumar/python-dotenv>
[requests]: <https://github.com/requests/requests>
[official docs]: <https://blockchain.info/api/charts_api>
