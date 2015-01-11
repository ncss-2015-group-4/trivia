def pre_game_handler(request):
    pre_game_page = open('static/pregamelobby.html')
    request.write(pre_game_page.read())