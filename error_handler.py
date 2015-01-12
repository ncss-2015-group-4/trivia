from templating import render_template

def error_handler(request):
    error_page = render_template('static/error.html', {})
    request.write(error_page)
