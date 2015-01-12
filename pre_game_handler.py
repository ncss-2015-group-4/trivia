from templating import render_template
from db.models import User,Category

def pre_game_handler(request):
    u_id = request.get_secure_cookie ('user_id')
    u_name = ""
    if u_id is not None:
        u_id = u_id.decode("UTF-8")
        u_name = User.find(user_id=u_id)
        u_name = u_name.username

    pre_game_page = render_template('static/pregamelobby.html', {"user_name": u_name, 'categories': Category.find_all()})
    request.write(pre_game_page)