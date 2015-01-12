from templating import render_template
from db.models import Category
from db.models import TriviaQuestion

def category_handler(request, category_id):
    cat = Category.find(category_id=category_id)
    
    list_of_questions = TriviaQuestion.find_all(category=category_id)
    print(list_of_questions)
    category_page = render_template('static/category.html', {
        "category_name": cat.name,
        'list_of_questions': list_of_questions})
    request.write(category_page)
    
def category_list_handler(request):
    list_of_categories = Category.find_all()
    print(list_of_categories)
    list_categories_page = render_template('static/category.html', {
        "list_of_categories": list_of_categories})
    request.write(list_categories_page)