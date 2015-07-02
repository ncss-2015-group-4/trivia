from templating import render_template
from db.models import Game
# from difficulty import difficulty
from . import template_paths, require_user


@require_user
def profile_handler(request):
    user = request.user
    profile_page = render_template(template_paths["profile"], {
        "user_name": user.username,
        "email": user.email,
        # "score": difficulty(user.id),
        "games": Game.find_iter(user_id=user.id)
    })
    request.write(profile_page)
