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

## Setup

```
$ cd /path/to/robotablet
$ pyenv local 3.5.1
$ virtualenv .venv
$ source .venv/bin/activate
(.venv)$ pip install -r requirements.txt
```

## Run Server

```
(.venv)$ python app.py
```

## Usage

Access tablet index page
http://localhost:3000/

### Action and Query

### index
GET http://localhost:3000/

### show_image
GET http://localhost:3000/q?action=show_image&image=[image_src]

* [image_src]: image_src is file_path in dir of "/static/uploads/image/[image_src]" or external src.

e.q.:
* http://localhost:3000/q?action=show_image&image=default.png
* http://localhost:3000/q?action=show_image&image=https://ja.wikipedia.org/wiki/%E3%83%A1%E3%82%A4%E3%83%B3%E3%83%9A%E3%83%BC%E3%82%B8#/media/File:Yellow_Bittern_at_Hyoko_crop.jpg

### show_menu
GET http://localhost:3000/q?action=show_menu&menu=[menu_id]

* [menu_id]: menu_id is file_path in dir of "/static/uploads/menu/[menu_id].json"

e.q.:
* http://localhost:3000/q?action=show_menu&menu=101

### hide_iframe
GET http://localhost:3000/q?action=hide_iframe

## Licence

[MIT License](https://github.com/shiraco/robotablet/blob/master/LICENSE)

## Author

[shiraco](https://github.com/shiraco)
