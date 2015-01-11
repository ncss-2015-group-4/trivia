from templating import render_template

def pre_game_handler(request):
    pre_game_page = render_template('static/pregamelobby.html', {})
    request.write(pre_game_page)