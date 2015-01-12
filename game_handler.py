from db.models import User, Game
from templating import render_template

def game_handler(request):
    category_id = request.get_field("category_id")
    difficulty = request.get_field("difficulty")
    user_id_cookie = request.get_secure_cookie("user_id")

    if user_id_cookie is not:
    	user = User.find(id=int(user_id_cookie.decode()))

    	if category_id and difficulty:
    		game = Game.create(user.id, category_id)

def get_question(request, game_id, question_index):
	game = Game.find(id=int(game_id))
	if game:
		question = game.get_question(int(question_index))
		answers = game.get_answers(int(question_index))

		request.write(render_template('static/question.html',
					{question: question, answers: answers, question_index: question_index}))
		return
	request.redirect("/404kid")

def submit_question_handler(request):
	game_id = request.get_field("game_id")
	user_id_cookie = request.get_secure_cookie("user_id")

	question_id = request.get_field("question_id")
	answer_id = request.get_field("answer_id")

	if game_id and user_id_cookie and question_id and answer_id:
		game = Game.find(id=int(game_id))
		user = User.find(id=int(user_id_cookie.decode()))

		if game and user:
			if game.user_id == user.id:
				if game.submit_answer(question_id)):
					request.redirect('/play/{0}'.format(game.question_index))
					return

	request.redirect("/404")
