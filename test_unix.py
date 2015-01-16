import sys
from tornado.testing import main
import subprocess

def Test_docstrings(file):
    print("Testing docstrings in "+file)
    process=subprocess.Popen(["python3",file], stderr=subprocess.PIPE)
    if process.stderr.read()==b'':
        print("OK")
    else:
        print(process.stderr.read())

Test_docstrings("templating.py")
sys.argv=["test_unix.py","tests/pages.py"]
main()
input("----Press enter to continue----")

