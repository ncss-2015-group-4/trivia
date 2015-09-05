from . import template_paths, grab_user
from templating import render_template


def error_handler(request):
    create_error(request, "404 Error!")


@grab_user
def create_error(request, message, status=404):
    request.set_status(status)

    u_name = ""
    if request.user:
        u_name = request.user.username

    error_page = render_template(template_paths["error"], {"user_name": u_name, "error": message})
    request.write(error_page)
