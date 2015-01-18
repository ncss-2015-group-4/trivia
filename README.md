# Quizzi 
[![Build Status](https://travis-ci.org/ncss-2015-group-4/trivia.svg?branch=master)](https://travis-ci.org/ncss-2015-group-4/trivia)

A social trivia website built by group 4 for NCSS 2015


##Is it live?
Currently you can see a reasonably up to date version of the site [here](https://quizzi.vovo.id.au/) (thanks @auscompgeek)

## How do I do this?
First, clone this repo:
```
$ git clone https://github.com/ncss-2015-group-4/trivia.git
$ cd trivia
```

Then initialise the database:
```
$ cd db
$ python3 create_db.py
$ python3 dummy_data.py
$ cd ..
```

Then run the server!
```
$ python3 trivia.py
```

`trivia.py` also takes `--host` and `--port` switches to allow for listening on different IPs and ports.
```
$ python3 trivia.py --host localhost --port 12345
```

If you are on Windows, either specify the full path to the Python 3 interpreter or use `py -3` in place of `python3`.

## Requirements
This project requires Python 3.4 or later. (`hashlib.pbkdf2_hmac()` is new in Python 3.4.)

This project currently does not have any external dependencies.
