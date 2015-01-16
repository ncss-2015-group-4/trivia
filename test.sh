cd db
python3 create_db.py
python3 dummy_data.py
cd ..
python3 templating.py
python3 -m tornado.testing tests/pages.py
