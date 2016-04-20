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


### Testing

* run `docker-compose run app test`

it will run `py.test` inside of the container, you can pass
`--pdb` to enable debugger on test fail

* you can use flask fixutes (http://pytest-flask.readthedocs.org/en/latest/features.html#fixtures)
* if you need a database test you can use `db` fixture. It will create `sqlite` database
and after test end will drop it


### Installing dependencies

* run `docker-compose run app pip "package_name"`

it will install "package_name" to your `virtualenv` (if `DEBUG` is `True`)
or to the global site-package. You can pass `--save` or `--save-dev`
to save "package_name" inside of requirements file
