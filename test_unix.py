import sys
from tornado.testing import main
import subprocess

#set up database
process = subprocess.Popen(["cd", "db", "&&", "python3", "create_db.py"], stderr=subprocess.PIPE)
if process.stderr.read() == b'':
    print("Created database")
else:
    print(process.stderr.read())
process = subprocess.Popen(["cd", "db", "&&", "python3", "dummy_data.py"], stderr=subprocess.PIPE)
if process.stderr.read() == b'':
    print("Populated database with dummy data")
else:
    print(process.stderr.read())

def Test_docstrings(file):
    print("Testing docstrings in " + file)
    process = subprocess.Popen(["python3", file], stderr=subprocess.PIPE)
    if process.stderr.read() == b'':
        print("OK")
    else:
        print(process.stderr.read())

Test_docstrings("templating.py")
sys.argv=["test_unix.py", "tests/pages.py"]
main()
input("----Press enter to continue----")

