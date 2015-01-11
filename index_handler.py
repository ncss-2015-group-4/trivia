def index_handler(request):
    home_page = open('static/home.html')
    request.write(home_page.read())
