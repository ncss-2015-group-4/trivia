from tornado.ncss import Server
import index_handler
from templating import render_template

import profile_handler
import game_handler
import pre_game_handler
import post_game_handler
import submit_handler
import login_handler
import question_handler
import user_handler
import error_handler
import leaderboard_handler
import category_handler

def return_404(response, *args, **kwargs):
	response.set_status(404)
	error = render_template('static/error.html', {})
	response.write(error)

def default_handler(response, method, *args, **kwargs):
	return return_404(response)

server = Server()
server.register('/', index_handler.index_handler)
server.register('/profile', profile_handler.profile_handler)
server.register('/game', game_handler.game_handler)
server.register('/pre_game', pre_game_handler.pre_game_handler)
server.register('/post_game', post_game_handler.post_game_handler)
server.register('/submit', submit_handler.submit_handler)
server.register('/leaderboard', leaderboard_handler.leaderboard_handler)
server.register('/login',
                login_handler.login_handler,
                post=login_handler.login_handler_post)
server.register('/question', question_handler.new_question_form,
                post=question_handler.new_question_hsandler)
server.register('/question/([0-9]+)',
                question_handler.get_question_handler,
                post=question_handler.edit_question_handler)
server.register('/category/([0-9]+)', category_handler.category_handler)
server.register('/user', user_handler.user_handler, post=login_handler.signup_handler_post)
server.register('/user/([0-9]+)', user_handler.edit_user_handler)
server.register('/.*', return_404)

if __name__ == '__main__':s
	server.run()
