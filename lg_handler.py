def logout(response):
	response.clear_cookie('user_id')
	response.redirect("/l")
	return