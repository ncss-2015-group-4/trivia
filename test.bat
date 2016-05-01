@echo off
setlocal
cd /d "%~dp0"

cd db
if exist trivia.db (
	echo Existing database found, backing up.
	ren trivia.db triviaBackup.db
)

echo Initialising database...
py -3 create_db.py
cd ..
cd tests
py -3 test_data.py
cd ..

echo Running tests...
py -3 templating.py
py -3 -m db.models
py -3 -m tornado.testing tests/pages.py

echo Cleaning up...
cd db
del trivia.db
if exist triviaBackup.db ren triviaBackup.db trivia.db
pause
