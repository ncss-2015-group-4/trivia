from templating import render_template

def leaderboard_handler(request):
    leaderboard = render_template('static/leaderboard.html', {})
    request.write(leaderboard)
