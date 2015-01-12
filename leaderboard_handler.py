from templating import render_template

def leaderboard_handler(request):
    names = ["John", "Jack", "Kenni", "Ben", "Tony"]
    
    leaderboard = render_template('static/leaderboard.html', {"people": names})
    request.write(leaderboard)
