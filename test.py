import subprocess

#set up databases
process = subprocess.Popen(["cd", "db;", "c:/python34/python.exe", "create_db.py"], stderr=subprocess.PIPE)
if process.stderr.read() == b'':
    print("Created database")
else:
    print(process.stderr.read())
process = subprocess.Popen(["cd", "db;", "c:/python34/python.exe", "dummy_data.py"], stderr=subprocess.PIPE)
if process.stderr.read() == b'':
    print("Populated database with dummy data")
else:
    print(process.stderr.read())


def Test_docstrings(file):
    print("Testing docstrings in "+file)
    process=subprocess.Popen(["c:/python34/python.exe", file], stderr=subprocess.PIPE)
    if process.stderr.read() == b'':
        print("OK")
    else:
        print(process.stderr.read())
    print("\n")

Test_docstrings("templating.py")
subprocess.call(["c:/python34/python.exe", "-m", "tornado.testing", "tests/pages.py"])

input("----Press enter to continue----")
