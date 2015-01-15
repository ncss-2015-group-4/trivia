from templating import render_template
from db.models import Category
from db.models import User
from db.models import TriviaQuestion
from . import template_paths

def category_handler(request, category_id):
    cat = Category.find(category_id=category_id)

    list_of_questions = TriviaQuestion.find_all(category=category_id)
    #print(list_of_questions)
    u_id = request.get_secure_cookie('user_id')
    u_name = ""
    if u_id is not None:
        u_id = u_id.decode("UTF-8")
        u_name = User.find(user_id=u_id)
        u_name = u_name.username

    category_page = render_template(template_paths["submit_category"], {
        "user_name": u_name,
        "category_name": cat.name,
        'list_of_questions': list_of_questions})
    request.write(category_page)

def category_list_handler(request):
    u_id = request.get_secure_cookie('user_id')
    u_name = ""
    if u_id is not None:
        u_id = u_id.decode("UTF-8")
        u_name = User.find(user_id=u_id)
        u_name = u_name.username

    list_of_categories = Category.find_all()
    print(list_of_categories)
    list_categories_page = render_template(template_paths["categories"], {
        "user_name": u_name,
        "list_of_categories": list_of_categories})
    request.write(list_categories_page)
