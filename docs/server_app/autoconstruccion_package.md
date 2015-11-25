# Autoconstruccion app package

## App running

To run the app import create_app factory from autoconstruccion package and create the app.

``` application = create_app(config_name='DEVELOPMENT')```

you can specify a config_name to select a configuration defined in the package. 'PRODUCTION' by default.

It can be run as WSGI service.

## Configuration

The app load configuration values in order. If a config value is previously defined it wil be overwrited.

1. Package defined configurations:
The configuration can be defined passing a config_name to create_app() and create_db() functions
2. 'config.py' file inside 'instance' folder on the same path as autoconstruccion package. Config values are directly on the file.
3. Config file defined in 'AUTOCONSTRUCCION_APP_CONFIG_FILE' environment variable, config values defined same as the previous way.

If the TESTING flag is True the sqlalchemy uri will be appended with '_test' to avoid data deletion or crushing.


