from templating import render_template
from db.models import User

def leaderboard_handler(request):
    names = ["John", "Jack", "Kenni", "Ben", "Tony"]
    
    id = request.get_secure_cookie ('user_id')
    u_name = ""
    if id is not None:
        id = id.decode("UTF-8")
        u_name = User.find(user_id=id)
        u_name = u_name.username
    leaderboard = render_template('static/leaderboard.html', {"user_name": u_name, "people": names})
    request.write(leaderboard)
