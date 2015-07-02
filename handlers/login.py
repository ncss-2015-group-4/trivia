from db.models import User
from templating import render_template
from . import template_paths, grab_user
import re


@grab_user
def login_handler(request, error=""):
    u_name = ""
    if request.user:
        u_name = request.user.username
    login_page = render_template(template_paths["login"], {
        "error_message": error, "user_name": u_name
    })
    request.write(login_page)


# Handles cookie creation
def login_start(response, user_id):
    response.set_secure_cookie("user_id", str(user_id))
    response.redirect("/profile")


# Does all the login handling:
#    - Checks for username or email in
#      databese and returns the class
#    - If there is no row:
#        - Show an error to user or redirect
#    - Else:
#        - Hashes the entered password
#        - Grabs the hash pass from row
#        - Compares the two pass values

def login_handler_post(request):
    username = request.get_field("username")
    password = request.get_field("password")

    if not (username and password): 
        login_handler(request, error="You did not provide a username or password.")
        return

    if "@" in username:
        user = User.find(email=username)
    else:
        user = User.find(username=username)

    if user:
        if user.check_login(password):
            login_start(request, user.id)
        else:
            login_handler(request, error="Incorrect password.")

    else:
        login_handler(request, error="That username does not exist.")


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

def signup_handler_post(request):
    username = request.get_field("username")
    password = request.get_field("password")
    email = request.get_field("email")

    if not (username and password and email):
        login_handler(request, error="Fill in all the fields!")
        return

    if not re.match(r"^[A-Za-z0-9_-]+$", username):
        login_handler(request, error="That is not a valid username. "
                      "Usernames may consist of alphanumeric characters, underscores, and hyphens.")
        return

    if User.find(username=username):
        login_handler(request, error="Username already in use!")
        return

    if User.find(email=email):
        login_handler(request, error="Email already in use!")
        return

    user = User.create(username, password, email)
    login_start(request, user.id)
