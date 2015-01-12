from templating import render_template
from db.models import User
from difficulty import skill_level



def profile_handler(request):
    id = request.get_secure_cookie ('user_id')
    if id is None:
        request.redirect("/login")
    else:
        id = id.decode("UTF-8")
        user_data = User.find(user_id=id)
        profile_page = render_template('static/profile.html', {"user_name": user_data.username, "email": user_data.email})
        request.write(profile_page)
     

