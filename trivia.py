import argparse

from tornado.ncss import Server
from templating import render_template

from handlers.index_handler import index_handler
from handlers.profile_handler import profile_handler
from handlers.game_handler import game_handler
from handlers.game_handler import get_question_handler
from handlers.game_handler import submit_question_handler
from handlers.pre_game_handler import pre_game_handler
from handlers.post_game_handler import post_game_handler
from handlers.submit_handler import submit_handler
from handlers.login_handler import login_handler
from handlers.login_handler import login_handler_post
from handlers.login_handler import signup_handler_post
from handlers.user_handler import user_handler
from handlers.error_handler import error_handler
from handlers.leaderboard_handler import leaderboard_handler
from handlers.category_handler import category_handler
from handlers.category_handler import category_list_handler
from handlers.question_handler import new_question_handler
from handlers.question_handler import new_question_form
from handlers.question_handler import edit_question_handler
from handlers.lg_handler import logout
from handlers.error_handler import error_handler

parser = argparse.ArgumentParser()
parser.add_argument("--port", help="what port do you want the server to listen on?", type=int)
parser.add_argument("--hostname", help="what host do you want the server to run on?", type=str)
args = parser.parse_args()

port = 8888
hostname = ""
if args.port:
	port = args.port

if args.hostname:
	hostname = args.hostname


server = Server(port=port, hostname=hostname)
server.register('/', index_handler)
server.register('/profile', profile_handler)
server.register('/game/([0-9]+)', get_question_handler)
server.register('/game/submit/([0-9]+)', submit_question_handler)
server.register('/game/create', game_handler)
server.register('/pre_game', pre_game_handler)
server.register('/post_game', post_game_handler)
server.register('/submit', submit_handler)
server.register('/leaderboard', leaderboard_handler)
server.register('/login',
                login_handler,
                post=login_handler_post)
server.register('/question',new_question_form,
                post=new_question_handler)
server.register('/question/([0-9]+)',
                get_question_handler,
                post=edit_question_handler)
server.register('/category/([0-9]+)', category_handler)
server.register('/user', user_handler, post=signup_handler_post)
# server.register('/user/([0-9]+)', edit_user_handler)
server.register('/categories', category_list_handler)
server.register('/logout', logout)
server.register('/.*', error_handler)


if __name__ == '__main__':
    server.run()
