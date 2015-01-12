from templating import render_template

def logout(response):
	response.clear_cookie('user_id')
	page = render_template('static/logout.html', {})
	response.write(page)
	return