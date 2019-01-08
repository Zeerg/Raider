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

wip

# ToDo
* Add some kind of plugin manager system so it doesn't bloat the image, maybe an env
* Add GCE integration
* queue system for concurrent testing - spot instances in gce cluster or something
* Add better slack messaging (message when scanning, then delete and send pretty logs when done + mention) (user configurable)
* Add more tools
* firecracker integration eventually maybe
* move api keys to some param store
* Add ability to use public proxys for sites that block tor
* elasticsearch integration

## Tools to add

* https://github.com/woj-ciech/Danger-zone
* Massscan
* nfosec news crawler from riskdiscovery.com
* Some kind of dos/load tool? Maybe vegeta 
