from db.models import User, Game
from templating import render_template

def game_handler(request):
    category_id = request.get_field("category_id")
    difficulty = request.get_field("difficulty")
    print(category_id, difficulty)
    user_id_cookie = request.get_secure_cookie("user_id")

    if user_id_cookie:
        user = User.find(user_id=int(user_id_cookie.decode()))
        if category_id is not None and difficulty is not None:
            game = Game.create(user.id, int(category_id), float(difficulty))
            request.set_secure_cookie("game_id", str(game.id))
            print('game_id set to', game.id)
            request.redirect('/game/0')

def get_question_handler(request, question_index):
    game_id = request.get_secure_cookie('game_id')
    if not game_id:
        request.redirect("/404punk")
        return

    game_id = game_id.decode()
    game = Game.find(game_id=int(game_id))
    if game:
        question = game.get_question(int(question_index))
        if not question:
            request.write("that question does not exist")
            return
        answers = game.get_answers(int(question_index) + 1)

        request.write(render_template('static/question.html',
                    {"question": question, "answers": answers, "question_index": question_index}))
        return
    request.redirect("/404kid")

def submit_question_handler(request):
    game_id = request.get_field("game_id")
    user_id_cookie = request.get_secure_cookie("user_id")

    question_id = request.get_field("question_id")
    answer_id = request.get_field("answer_id")

    if game_id and user_id_cookie and question_id and answer_id:
        game = Game.find(game_id=int(game_id))
        user = User.find(user_id=int(user_id_cookie.decode()))

        if game and user:
            if game.user_id == user.id:
                if game.submit_answer(question_id):
                    request.redirect('/game/{0}'.format(game.question_index))
                    return

    request.redirect("/404")
