# libkeep (A university project)

### Libkeep is an application for managing&maintaining library (with books ofc).

### Needed packages

* docker-engine >= 1.10.0 [installation guide](https://docs.docker.com/engine/)
* docker-compose >= 1.62  [installation guide](https://docs.docker.com/compose/install/)


#### Development on linux

* clone this repository
* run `ln -s docker-dev.yml docker-compose.yml`
* run `docker-compose build`
* run `docker-compose up -d`
* go to `127.0.0.1:5000`
* check logs under `./log` directory

#### Development on OSX

* clone this repo
* run docker machine `docker-machine start default`
* grab IP address of your machine `docker-machine ip default`
* run `ln -s docker-prod.yml docker-compose.yml`
* run `docker-compose build`
* run `docker-compose up -d`
* go to `[docker-machine ip default]:5000`
* check logs under `./log` directory
