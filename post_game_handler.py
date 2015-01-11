from templating import render_template

def post_game_handler(request):
    post_game_page = render_template('static/postgamelobby.html', {})
    request.write(post_game_page)