# Web server configuration

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

`custom_logging.py`: Config for our logger
`discovery.py`: Discovers clients
`docker-compose.yml`: You know...
`fake-response.py`: For developments purposes it fakes a _dooino_ manifest
`features_fetcher.py`: Retrieves the information from the manifests
`Procfile`: Run all the necessary for development
`register.py`: Registers a _dooino_ locally
`server.py`: Web server
