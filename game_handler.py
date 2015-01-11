def game_handler(request):
    game_page = open('static/game.html')
    request.write(game_page.read())