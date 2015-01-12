def user_handler(request):
    #this is a login thingy ben needs to do here.
    pass
def edit_user_handler(request, user_id):
    pass
def user_handler_post(request):
    username = request.get_field("username")
    password = request.get_field("password")
    login_handler.login_handler(request, username, password)
