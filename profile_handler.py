from templating import render_template
from db.models import User


def profile_handler(request):
    id = request.get_secure_cookie ('user_id')
    if id is None:
        request.redirect("/login")
    else:
        id = id.decode("UTF-8")
        print("WLKHGKUSDKUGLUBGS:KDJ:KV:LSKDNV:LKSND:LVK------------>", id)
        user_data = User.find(user_id=id)
        profile_page = render_template('static/profile.html', {"user_name": user_data.username})
        request.write(profile_page)

