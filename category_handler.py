from templating import render_template
from db.models import Category
from db.models import User
from db.models import TriviaQuestion

def category_handler(request, category_id):
    cat = Category.find(category_id=category_id)
    
    list_of_questions = TriviaQuestion.find_all(category=category_id)
    print(list_of_questions)
    
    id = request.get_secure_cookie('user_id')
    u_name = ""
    
    if id is not None:
        id = id.decode("UTF-8")
        u_name = User.find(user_id=id)
        u_name = User.username
    category_page = render_template('static/category.html', {
        "user_name": u_name,
        "category_name": cat.name,
        'list_of_questions': list_of_questions})
    request.write(category_page)