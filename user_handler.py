def user_handler(request):
    request.write("""<!DOCTYPE html>
<html>
<body>
<h1>
<h1>
Change stuff here
</h1>

<form method="post">
Username:<br>
<input type="text" name="username">
<br>
Password:<br>
<input type="text" name="password">
<br>
Email:<br>
<input type="text" name="Email">
<br>
<input type="submit" value="Submit">
</form>
</h1>
</body>
</html>
""")
    
def user_handler_post(request):
    username = request.get_field("username")
    password = request.get_field("password")
    email = request.get_field("email")
    if username != '' and password != '' and email != '':
        request.redirect('/user/8829')


def edit_user_handler(request, user_id):
    request.write("""<!DOCTYPE html>
<html>
<body>
<h1>
""" + user_id + """
</h1>
</body>
</html>
""")
