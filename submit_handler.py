from templating import render_template

def submit_handler(request):
    submit_page = render_template('static/submit.html', {})
    request.write(submit_page)