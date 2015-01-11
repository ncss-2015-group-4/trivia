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

def edit_user_handler(request, user_id):
    request.write("""<!DOCTYPE html>
<html>
<body>
<h1>
3d!tz
</h1>
</body>
</html>
""")
