from db.models import User
from templating import render_template
from . import template_paths
import re

def login_handler(request, **kwargs):
    error=kwargs.get("error","")
    u_id = request.get_secure_cookie('user_id')
    u_name = ""
    if u_id is not None:
        u_id = u_id.decode("UTF-8")
        u_name = User.find(user_id=u_id)
        u_name = u_name.username
    login_page = render_template(template_paths["login"], {"error_message": error,"user_name": u_name})
    request.write(login_page)

#--------------------------------------
# By Ben
#--------------------------------------

#======================================
# Handles cookie creation
#======================================
def login_start(response, user_id):
    print("login started")
    response.clear_cookie('user_id')
    if not response.get_secure_cookie("user_id"): #checks for cookie
        response.set_secure_cookie("user_id", str(user_id)) #creates a new cookie
    response.redirect("/profile")


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
            login_start(request, user_data.id)
            return
        else:
            error = "Password/Username is incorrect"
            #login_handler(request)
    else: #does a second check on db with email
        user_data = User.find(email=username_email) #may
        if user_data is not None:
            if user_data.check_login(password):
                login_start(request, user_data.id)
                return
            else:
               error = "Password/Username is incorrect"
        else:
            error = "User doesn't exist"
    login_handler(request, error=error) #cannot find username or email in database!
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
    error=""
    regex = r"^[a-zA-Z][a-zA-Z0-9]*[a-zA-Z]$"

    if not (username and password and email):
        login_handler(request, error="Fill in all the fields!")
        return

    if not (re.match(regex, username) and re.match(regex, password)):
        login_handler(request, error="That is not a valid username or password")
        return

    if not User.find(username=username):
        if User.find(email=email):
            error = "Email already in use!"
        else:
            User.create(username, password, email)
            login_handler_post(request)
            request.redirect("/profile")
            return
    else:
        error="Username already in use!"

    login_handler(request, error = error)
