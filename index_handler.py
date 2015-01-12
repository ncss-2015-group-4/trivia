from templating import render_template
from db.models import User

def index_handler(request):
    id = request.get_secure_cookie('user_id')
    u_name = ""
    if id is not None:
        id = id.decode("UTF-8")
        u_name = User.find(user_id=id)
        u_name = u_name.username
    home_page = render_template('static/home.html', {'user_name': u_name})
    request.write(home_page)
