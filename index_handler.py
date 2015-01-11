def index_handler(request):
    home_page = open('Web/Home.html')
    request.write(home_page.read())
