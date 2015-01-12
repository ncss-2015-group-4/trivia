from templating import render_template
from db.models import Category

def pre_game_handler(request):
    pre_game_page = render_template('static/pregamelobby.html', {'categories': Category.find_all()})
    request.write(pre_game_page)