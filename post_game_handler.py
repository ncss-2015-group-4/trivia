from templating import render_template
from db.models import User

def post_game_handler(request):
    u_id = request.get_secure_cookie ('user_id')
    u_name = ""
    if u_id is not None:
        u_id = u_id.decode("UTF-8")
        u_name = User.find(user_id=u_id)
        u_name = u_name.username
    post_game_page = render_template('static/postgamelobby.html', {"user_name": u_name})
    request.write(post_game_page)