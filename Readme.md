# Raider

An offensive and defensive chat bot for automating blue and red team tasks.

## Usage

Config File
* An .env config file must be created and placed in the config/ directory before building the container

```
# App config
SLACK_API_KEY="Changeme"
BOT_ADMINS_LIST='@admin1,@admin2,@changeme' # comma delimited, cant export an array
APP_DIR='/app'
LOG_LEVEL=INFO

# VT configs
VT_API_KEY=''

# Digital Ocean API Config
DIGITAL_OCEAN_KEY=''
MAX_VPNS=2
```

Bring up with docker-compose

`make`

Build image 

`make build`
