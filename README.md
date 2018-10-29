# Automation process of deploy using Gitlab API

## Features
* Create/Accept Merge Requests
* Add tag by branch name

## Run on host

### Install python2.7 and pip
<https://pip.pypa.io/en/stable/installing/>

### Install dependencies
`pip install --no-cache-dir -r requirements.txt` 

### Set environment variables
`export AUTOMR_ASS_ID=`  
`export AUTOMR_TOKEN=`  
`export AUTOMR_API_VERSION=`  
`export AUTOMR_URL=`  

### Create folder src/projects
`mkdir src/projects`

Create yaml file in this folder, by example _projects-list.yaml.dist_

### Run
`python main.py --help`

## Run in Docker
`docker build -t glmr .`  
`docker run -e AUTOMR_ASS_ID= -e AUTOMR_TOKEN= -e AUTOMR_API_VERSION= -e AUTOMR_URL= --rm glmr python main.py -a accept-mr -f projects/projects-list.yaml`

## Example of accept MR
`python main.py -a accept-mr -f projects/projects-list.yaml`  
_-a - action (create-mr, accept-mr, new-tag)_  
_-f - filename (use custom project.yml)_  
