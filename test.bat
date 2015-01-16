cd db
py -3 create_db.py
py -3 dummy_data.py
cd ..
py -3 templating.py
py -3 -m tornado.testing tests/pages.py
pause
