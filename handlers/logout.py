from templating import render_template
from . import template_paths

def logout_handler(response):
    response.clear_cookie('user_id')
    page = render_template(template_paths["logout"], {"user_name":""})
    response.write(page)
    return
