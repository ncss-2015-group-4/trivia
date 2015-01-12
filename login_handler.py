from db.models import User
from templating import render_template

def login_handler(request, **kwargs):
    error=kwargs.get("error","")
    u_id = request.get_secure_cookie('user_id')
    u_name = ""
    if u_id is not None:
        u_id = u_id.decode("UTF-8")
        u_name = User.find(user_id=u_id)
        u_name = u_name.username
    login_page = render_template('static/login.html', {"error_message": error,"user_name": u_name})
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
    if username == None or username == '' or password == None or password == '':
        request.redirect("/") #Says that the user is missing a feild
        return
    user_data = User.find(username=username) #requests a database entry with the user's username
    if user_data == None:    #checks that there is a row in the database that 
        if User.find(email=email) != None:#Says that the user email address is already in use
            error = "Email already in use!"
        else:
            User.create(username, password, email) #Creates a new entry into the db
            login_handler_post(request)
            request.redirect("/profile") #sends user a thanks pafe or profile page?
            return 
    else:
        error="Username already in use!"
    login_handler(request, error = error)
   # request.redirect("/login")