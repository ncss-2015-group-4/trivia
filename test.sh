#!/bin/sh

cd db
echo Backing up database \(If one exists\)
if [ -a trivia.db  ]; then mv trivia.db triviaBackup.db; fi
echo Creating new database \(in case one does not already exist\)
python3 create_db.py
python3 dummy_data.py
cd ..
echo running tests
python3 templating.py
python3 -m tornado.testing tests/pages.py
echo Restoring database from backup
cd db
rm trivia.db
if [ -a triviaBackup.db  ]; then mv triviaBackup.db trivia.db; fi
