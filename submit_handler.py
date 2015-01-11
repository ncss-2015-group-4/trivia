def submit_handler(request):
    submit_page = open('static/submit.html')
    request.write(submit_page.read())