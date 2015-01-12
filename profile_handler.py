from templating import render_template
from db.models import User

def profile_handler(request):
    profile_page = render_template('static/profile.html', {})
    request.write(profile_page)

