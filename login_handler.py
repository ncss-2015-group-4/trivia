#from db.models import User

def login_handler(request):
    request.write("""<!DOCTYPE html>
<html>
<body>

<h1>
Login in below -->
</h1>

<form method="post">
Email/Username:<br>
<input type="text" name="username">
<br>
Password:<br>
<input type="text" name="password">
<input type="submit" value="Submit">
</form>


<h1>
Sign up here...
</h1>

<form>
<form method="post">
Email/Username:<br>
<input type="text" name="username">
<br>
Password:<br>
<input type="text" name="password">
<input type="submit" value="Submit">
</form>

</body>
</html>
""")


def login_handler_post(request):
    username = request.get_field("username")
    password = request.get_field("password")
    if username == None or username == '' or password == None or password == '':
       request.redirect("/")
       return
    print(username)
    print(password)
    request.redirect("/")
    #gets a returned hash password from db
    #userData = User.find_by_username(username)
    #pWord = userData.password_hash
    #if pWord == hasher.hash(password):
        #userData = User.find_by_username(username)
        #pWord = userData.password_hash
        #if pWord == hasher.hash(password):
            #request.redirect("/")
