from templating import render_template
from db.models import User

def logout(response):
    id = request.get_secure_cookie ('user_id')
    u_name = ""
    if id is not None:
        id = id.decode("UTF-8")
        u_name = User.find(user_id=id)
        u_name = u_name.username
    response.clear_cookie('user_id')
    page = render_template('static/logout.html', {"user_name": u_name})
    response.write(page)
    return