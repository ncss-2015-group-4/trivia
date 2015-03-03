from . import template_paths
from templating import render_template
from db.models import User

def error_handler(request):
    create_error(request, "404 Error!")
    
def create_error(request, message):
    request.set_status(404)

    u_id = request.get_secure_cookie('user_id')
    u_name = ""
    if u_id is not None:
        u_id = u_id.decode("UTF-8")
        u_name = User.find(user_id=u_id)
        u_name = u_name.username

    error_page = render_template(template_paths["error"], {"user_name": u_name, "error": message})
    request.write(error_page)