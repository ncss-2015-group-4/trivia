from templating import render_template
from db.models import User

def logout(response):
	response.clear_cookie('user_id')
	page = render_template('static/logout.html', {"user_name"})
	response.write(page)
	return