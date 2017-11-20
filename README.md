# Web server configuration

## Dependencies

```bash
gem install foreman
pip install requests
pip install zeroconf
pip install flask
pip install redis
```

## Development server

```bash
dockup-compose up
foreman start
```

### Register a service locally

```bash
python register.py
```

## Files

* `custom_logging.py`: Config for our logger
* `discovery.py`: Discovers clients
* `docker-compose.yml`: You know...
* `fake-response.py`: For developments purposes it fakes a _dooino_ manifest
* `features_fetcher.py`: Retrieves the information from the manifests
* `Procfile`: Run all the necessary for development
* `register.py`: Registers a _dooino_ locally
* `server.py`: Web server
