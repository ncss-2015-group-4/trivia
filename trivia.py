import argparse

from tornado.ncss import Server
from templating import render_template

from handlers.index import index_handler
from handlers.profile import profile_handler
from handlers.game import game_handler, get_question_handler, submit_question_handler
from handlers.pre_game import pre_game_handler
from handlers.post_game import post_game_handler
from handlers.submit import submit_handler
from handlers.login import login_handler, login_handler_post, signup_handler_post
from handlers.user import user_handler
from handlers.error import error_handler
from handlers.leaderboard import leaderboard_handler
from handlers.category import category_handler, category_list_handler
from handlers.question import new_question_handler, new_question_form, edit_question_handler
from handlers.logout import logout_handler
from handlers.error import error_handler

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="what port do you want the server to listen on?", type=int)
    parser.add_argument("--hostname", help="what host do you want the server to run on?", type=str)
    args = parser.parse_args()

    server = Server(port=args.port or 8888, hostname=args.hostname or '')
else:
    server = Server()

server.register('/', index_handler)
server.register('/profile', profile_handler)
server.register('/game/([0-9]+)', get_question_handler)
server.register('/game/submit/([0-9]+)', submit_question_handler)
server.register('/game/create', game_handler)
server.register('/pre_game', pre_game_handler)
server.register('/post_game', post_game_handler)
server.register('/submit', submit_handler)
server.register('/leaderboard', leaderboard_handler)
server.register('/login', login_handler, post=login_handler_post)
server.register('/question', new_question_form, post=new_question_handler)
server.register('/question/([0-9]+)', get_question_handler, post=edit_question_handler)
server.register('/category/([0-9]+)', category_handler)
server.register('/user', user_handler, post=signup_handler_post)
# server.register('/user/([0-9]+)', edit_user_handler)
server.register('/categories', category_list_handler)
server.register('/logout', logout_handler)
server.register('/.*', error_handler)

if __name__ == '__main__':
    server.run()
