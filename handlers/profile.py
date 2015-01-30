from templating import render_template
from db.models import User, Game, Category
from difficulty import difficulty
from . import template_paths


def profile_handler(request):
    u_id = request.get_secure_cookie ('user_id')
    if u_id is None:
        request.redirect("/login")
    else:
        u_id = u_id.decode("UTF-8")
        user_data = User.find(user_id=u_id)
        games = Game.find_all(user_id=u_id)
        print(games, "<-games")
        profile_page = render_template(template_paths["profile"], 
        	{"user_name": user_data.username, "email": user_data.email,
        	 "score": difficulty(int(u_id)), "games": games})
        request.write(profile_page)
