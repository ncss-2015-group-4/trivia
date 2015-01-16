from db.models import User, Game
from templating import render_template
from db.models import User
from . import template_paths

import random

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

    request.redirect('/login')

def get_question_handler(request, question_index):
    u_id = request.get_secure_cookie('user_id')
    u_name = ""
    if u_id is not None:
        u_id = u_id.decode("UTF-8")
        u_name = User.find(user_id=u_id)
        u_name = u_name.username

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
        answers = game.get_answers(game.question_ids[int(question_index)])
        random.shuffle(answers)
        request.write(render_template(template_paths["questions"],
            {"question": question, "answers": answers, "question_index": str(int(question_index)+1), "user_name":u_name}))
        return
    request.redirect("/404kid")

def submit_question_handler(request, answer_id):
    game_id = request.get_secure_cookie("game_id")
    user_id_cookie = request.get_secure_cookie("user_id")

    if game_id and user_id_cookie and answer_id:
        game = Game.find(game_id=int(game_id.decode()))
        game.submit_answer(game.question_ids[game.question_index], answer_id)
        score = game.game_nextquestion()
        if game.question_index >= len(game.question_ids):
            request.redirect('/post_game')
        else:
            request.redirect('/game/{0}'.format(int(game.question_index)))

