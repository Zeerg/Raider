# Raider

## Usage
Config File
* An .env config file must be created and placed in the config/ directory
```
# App config
SLACK_API_KEY="Changeme"
BOT_ADMINS_LIST='@admin1,@admin2,@changeme' # comma delimited, cant export an array
APP_DIR='/app'
LOG_LEVEL=INFO

# VT configs
VT_API_KEY=''
```

Bring up with docker-compose

`make`

Build image 

`make build`
