from templating import render_template
from db.models import User
from difficulty import difficulty

def profile_handler(request):
    u_id = request.get_secure_cookie ('user_id')
    if u_id is None:
        request.redirect("/login")
    else:
        u_id = u_id.decode("UTF-8")
        user_data = User.find(user_id=u_id)
        profile_page = render_template('static/profile.html', {"user_name": user_data.username, "email": user_data.email, "score": difficulty(int(u_id))})
        request.write(profile_page)
     

