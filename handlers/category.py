from templating import render_template
from db.models import Category, Question
from .error import create_error
from . import template_paths, grab_user


@grab_user
def category_handler(request, category_id):
    cat = Category.find(category_id=category_id)
    if not cat:
        create_error(request, "That category does not exist.")
        return

    u_name = ""
    if request.user:
        u_name = request.user.username

    category_page = render_template(template_paths["submit_category"], {
        "user_name": u_name,
        "category_name": cat.name,
        'questions': Question.find_iter(category=category_id)
    })
    request.write(category_page)


@grab_user
def category_list_handler(request):
    u_name = ""
    if request.user:
        u_name = request.user.username

    list_categories_page = render_template(template_paths["categories"], {
        "user_name": u_name,
        "categories": Category.find_iter()
    })
    request.write(list_categories_page)
