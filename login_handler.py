from hasher.hasher import hasher
from db.models import User
import hasher.hasher  as hasher

def login_handler(request):
    request.write("""<!DOCTYPE html>
<html>
<body>
<h1>
oginlay inway erehay!!!
<form method="post">
Email/Username:<br>
<input type="text" name="username">
<br>
Password:<br>
<input type="text" name="password">
<input type="submit" value="Submit">
</form>
</h1>
</body>
</html>
""")


def login_handler_post(request):
    username = request.get_field("username")
    password = request.get_field("password")
    if username == None or username == '' or password == None or password == '':
       request.redirect("/login")
       return
    print(username)
    #gets a returned hash password from db
    userData == User.find_by_username(username)
    pWord == userData.password_hash
    if pWord == hasher.hash(password):
        userData = User.find_by_username(username)
        pWord = userData.password_hash
        if pWord = hasher.hash(password):
            request.redirect("/")


