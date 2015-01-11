def profile_handler(request):
    profile_page = open('static/profile.html')
    request.write(profile_page.read())

