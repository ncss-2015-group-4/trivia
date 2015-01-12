import subprocess

print("Testing templating docstrings")
x=subprocess.Popen(["c:/python34/python.exe","templating.py"], stderr=subprocess.PIPE)
if x.stderr.read()==b'':
    print("OK")
else:
    print(x.stderr.read())
print("Finished testing templating docstrings")
print("\n")

subprocess.call(["c:/python34/python.exe","-m","tornado.testing","tests/pages.py"])

input("----Press enter to continue----")