from templating import render_template

def index_handler(request):
    home_page = render_template('static/home.html', {})
    request.write(home_page)
