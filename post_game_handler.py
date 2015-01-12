from templating import render_template
from db.models import Answer, Game
def post_game_handler(request, score):
    #   game = Game.find(game_id=game_id) future implementation of game object to show answered questions

    post_game_page = render_template('static/postgamelobby.html', {"score":score})
    request.write(post_game_page)