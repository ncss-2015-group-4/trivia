def login_handler(request):
    username = request.get_field("username")
    password = request.get_field("password")
    print(username)
    print(password)
    request.write("""<!DOCTYPE html>
<html>
<body>
<h1>
oginlay inway erehay!!!
<form method=post>
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
