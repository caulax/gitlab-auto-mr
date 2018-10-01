# Automation process of deploy using Gitlab API #

## Features ##
* Create/Accept Merge Requests
* Add tag by branch name

## Run on host ##

### Install python2.7 and pip ###
<https://pip.pypa.io/en/stable/installing/>

### Install dependencies ###
`pip install --no-cache-dir -r requirements.txt` 

## Run ##
`python main.py --help`

### Example of accept MR ###
`python main.py -a accept-mr -f projects-list.yaml`
_-a - action (create-mr, accept-mr, new-tag)_
_-f - filename (use custom project.yml)_

## Run in Docker ##

`docker build -t glmr .`
`docker run --rm glmr python main.py -a accept-mr -f projects-list.yaml`

_Will build and run docker-container with command_
