from db.models import User

def login_handler(request):
    request.write("""<!DOCTYPE html>
<html>
<body>

<h1>
Log-in below -->
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
Email:<br>
<input type="text" name="email">
<input type="submit" value="Submit">
</form>

</body>
</html>
""")


#--------------------------------------
# By Ben
#--------------------------------------

#======================================
# Does all the login handling:
#    - Checks for username or email in
#      databese and returns the class
#    - If there is no row:
#        - Show an error to user or redirect
#    - Else:
#        - Hashes the entered password 
#        - Grabs the hash pass from row
#        - Compares the two pass values
#======================================

def login_handler_post(request):
    username_email = request.get_field("username")
    password = request.get_field("password")
    if username_email == None or username_email == '' or password == None or password == '':
        request.redirect("/") #field isn't filled in
        return
    user_data = User.find(username=username_email) #checks db with username
    if user_data is not None: #if there is a row in the database
        if user_data.check_login(password):
            request.redirect("/") #login
            return
        else:
            request.redirect("/") #username/password is incorrect
    else: #does a second check on db with email
        user_data = User.find(email=username_email) #may 
        if user_data is not None:
            if user_data.check_login(password):
                request.redirect("/") #login
                return
            else:
                request.redirect("/") #username/password is incorrect
                return
        else:
            request.redirect("/") #username/password is incorrect
            return

#======================================
# Does all the signup handling:
#    - Takes in form data
#    - Checks that the fields are filled
#    - If not filled out:
#        - Tells the user that field empty
#    - Checks form data against db
#    - If email or username in db:
#        - Changes html to show data
#          already exists
#    - else:
#        - Creates a new row in the db
#======================================

def signup_handler_post(request):
    username = request.get_field("username")
    password = request.get_field("password")
    email = request.get_field("email")
    if username == None or username == '' or password == None or password == '':
        request.redirect("/") #Says that the user is missing a feild
        return
    
    user_data = User.find(username=username) #requests a database entry with the user's username
    if user_data == None:    #checks that there is a row in the database that 
        if user_data.find(email=email) != None:
            request.redirect("/") #Says that the user email address is already in use
            return 
        else:
            user_data.create(username, password, email) #Creates a new entry into the db
            request.redirect("/") #sends user a thanks pafe or profile page?
            return 
    else:
        request.redirect("/") #Says that the user already has a row in database
        return 
