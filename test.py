import subprocess

def Test_docstrings(file):
    print("Testing docstrings in "+file)
    process=subprocess.Popen(["c:/python34/python.exe",file], stderr=subprocess.PIPE)
    if process.stderr.read()==b'':
        print("OK")
    else:
        print(process.stderr.read())
    print("\n")

Test_docstrings("templating.py")
subprocess.call(["c:/python34/python.exe","-m","tornado.testing","tests/pages.py"])

input("----Press enter to continue----")