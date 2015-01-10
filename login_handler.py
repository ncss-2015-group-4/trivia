def login_handler(request):
    request.write("""<!DOCTYPE html>
<html>
<body>
<h1>
oginlay inway erehay!!!
<form>
Email/Username:<br>
<input type="text" name="firstname">
<br>
Password:<br>
<input type="text" name="lastname">
<input type="submit" value="Submit">
</form>
</h1>
</body>
</html>
""")
