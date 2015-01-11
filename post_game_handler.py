def post_game_handler(request):
    post_game_page = open('static/postgamelobby.html')
    request.write(post_game_page.read())