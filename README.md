robotablet
====

## Description

* [Server Application](https://github.com/shiraco/robotablet)
* [Client Application](https://github.com/shiraco/robotablet-client)

## Requirement

* [yyuu/pyenv](https://github.com/yyuu/pyenv)
* [python 3.5.x (use pyenv)](https://github.com/shiraco/robotablet/blob/master/.python-version)
* [pypa/virtualenv](https://github.com/pypa/virtualenv)
* [python library](https://github.com/shiraco/robotablet/blob/master/rrequirements.txt)

## Install

```
$ git clone https://github.com/shiraco/robotablet.git
```

## Usage

### Setup

```
$ cd /path/to/robotablet
$ pyenv local 3.5.1
$ virtualenv .venv
$ source .venv/bin/activate
(.venv)$ pip install -r requirements.txt
```

### Run Server

```
(.venv)$ python app.py
```

## Licence

[MIT License](https://github.com/shiraco/robotablet/blob/master/LICENSE)

## Author

[shiraco](https://github.com/shiraco)
