from db.models import User, Game

def game_handler(request):
    category_id = request.get_field("category_id")
    difficulty = request.get_field("difficulty")
    user_id_cookie = request.get_secure_cookie("user_id")
    if (user_id_cookie is not None):
    	user = User.find(id=int(user_id_cookie.decode())

    	if (category_id is not None and difficulty is not None):
    		game = Game.create(user.id, category_id)

def submit_question_handler(request):
	game_id = request.get_field("game_id")
	user_id_cookie = request.get_secure_cookie("user_id")

	question_text = request.get_field("question_text")

	if (game_id is not None and user_id_cookie is not None):
		game = Game.find(id=int(game_id))
		user = User.find(id=int(user_id_cookie.decode()))

		if (game is not None and user is not None):
			if (game.user_id == user.id):
				if (game.submit_answer(question_text)):
					request.redirect('/play/{}'.format(game.question_index))
					return





