#!/bin/sh

status=0

cleanup_exit() {
	echo 'Cleaning up...'
	cd db
	rm trivia.db
	if [ -f triviaBackup.db ]; then
		mv triviaBackup.db trivia.db
	fi

	exit $status
}

cd "$(dirname "$0")"

cd db
if [ -e trivia.db ]; then
	echo 'Existing database found, backing up.'
	mv trivia.db triviaBackup.db
fi

# make sure we clean up the test database afterwards
trap cleanup_exit EXIT HUP INT TERM

echo 'Initialising database...'
python3 create_db.py
python3 dummy_data.py
cd ..

echo 'Running tests...'
python3 templating.py || status=$?
python3 -m db.models || status=$?
python3 -m tornado.testing tests/pages.py || status=$?
