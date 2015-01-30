@echo off
cd db
echo Backing up database (If one exists)
if exist trivia.db ren trivia.db triviaBackup.db
echo Creating new database (in case one does not already exist)
py -3 create_db.py
py -3 dummy_data.py
cd ..
echo Running tests
py -3 templating.py
py -3 -m tornado.testing tests/pages.py
echo Restoring database from backup
cd db
del trivia.db
if exist triviaBackup.db ren triviaBackup.db trivia.db
pause
