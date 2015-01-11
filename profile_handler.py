from templating import render_template

def profile_handler(request):
    profile_page = render_template('static/profile.html', {})
    request.write(profile_page)

