import functools
from db.models import User

template_paths = {
    "submit": 'templates/submit.html',
    "profile": 'templates/profile.html',
    "pre_game": 'templates/pregamelobby.html',
    "post_game": 'templates/postgamelobby.html',
    "login": 'templates/login.html',
    "register": 'templates/register.html',
    "logout": 'templates/logout.html',
    "leaderboard": 'templates/leaderboard.html',
    "index":"templates/home.html",
    "questions": "templates/question.html",
    "error": "templates/error.html",
    "submit_category": "templates/category.html",
    "categories":"templates/categories.html"
}


def get_template(name):
    """Get the path of a template given by the provided name."""
    if name in template_paths:
        return template_paths[name]
    return 'templates/{}.html'.format(name)


def grab_user(f):
    """Decorator to provide the current user as request.user if logged in."""
    @functools.wraps(f)
    def wrapped(request, *args, **kwargs):
        if not hasattr(request, 'user'):
            user = get_uid(request)
            if user is not None:
                user = User.find(id=user)
            request.user = user
        return f(request, *args, **kwargs)
    return wrapped


def require_user(f):
    """Decorator to require a logged-in user, providing request.user."""
    @functools.wraps(f)
    def wrapped(request, *args, **kwargs):
        if hasattr(request, 'user') and request.user:
            return f(request, *args, **kwargs)
        user_id = get_uid(request)
        if user_id is not None:
            request.user = User.find(id=user_id)
            if request.user:
                return f(request, *args, **kwargs)
        request.redirect('/login')
    return wrapped


def get_uid(request):
    user_id = request.get_secure_cookie("user_id")
    if user_id:
        return int(user_id.decode())
