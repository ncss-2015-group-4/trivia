from templating import render_template
from db.models import Category

def category_handler(request, category_id):
	category_page = render_template('static/category.html', {})
	request.write(category_page)
	cat = Category.find(category_id=category_id)
	print(cat.name)