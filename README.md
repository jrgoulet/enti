# enti  
  
A user interface that provides an easy way to manage External Entities for Knowledge Graphs.  

## Features

 - Import External Entities from XML
 - Create, Update, and Remove Entities from the UI
 - Export Entities to XML
 - Ingest Entities directly into Synthesys

  
## Requirements
  
 - Docker CE, Docker-Compose
	 - Installation Instructions: https://docs.docker.com/install/

## Quickstart

### Set up the Env File

Modify the following file and save it with the name `.env`.
```
# Reserved for deployment options
export DEPLOYMENT_MODE=development

# Secret key used for AES encyption (32 chars recommended)  
export SECRET_KEY=secret

# Don't change this, ever
export SERVER_HOST=0.0.0.0

# Server port for the UI
export SERVER_PORT=5100

# The default value for the "source" field of the Entity XML file
export ENTITIES_SRC=enti

# Whether Synthesys is co-located on the same machine
export SYNTHESYS_LOCAL=true

# Synthesys Host (Exclude http[s]:// and any suffixes)
export SYNTHESYS_HOST=0.0.0.0

# Synthesys Port
export SYNTHESYS_PORT=8999

# If Synthesys instance uses HTTPS, set to true
export SYNTHESYS_SSL=false

# Synthesys Username
export SYNTHESYS_USER=admin

# Synthesys Password  
export SYNTHESYS_PASS=1234

# Install Directory
# Nothing actually has to go here, but the folder does need to exist
# This is the directory that is mounted between the container and host,
# allowing for interaction with Synthesys pipelines
# Note: Not used currently, refer to MOUNT_DIR
export INSTALL_DIR=/mnt/enti

# This folder needs to exist
# The permissions need to be set to 777 (easy way)
export MOUNT_DIR=/mnt/enti/export

# Database Options
# Changing the values below is the only database initialization that
# needs to be done. Everything else is automatic

# Don't change this, nothing else is currently supported
export DATABASE_TYPE=mysql

# Name of the database
export DATABASE_NAME=enti

# Don't change these, unless you're not using the MySQL container
export DATABASE_HOST=mysql
export DATABASE_PORT=3306

# Change these  
export DATABASE_USER=enti
export DATABASE_PASS=pass  
export DATABASE_ROOT_PW=root
```

### Start the Server

Run it!
```
./enti.sh start
```

## Commands

These are all the commands needed to manage the application

| Command | Description |
|--|--|
| ./enti.sh start | Starts the server |
| ./enti.sh stop | Stops the server |
| ./enti.sh update | Download the latest image |
| ./enti.sh down | Remove the server (Deletes all stored data) |
| ./enti.sh restart | Restart the server |
| ./enti.sh logs | Stream server logs