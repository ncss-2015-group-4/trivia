from templating import render_template

def game_handler(request):
    game_page = render_template('static/game.html', {})
    request.write(game_page)