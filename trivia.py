from tornado.ncss import Server
import index_handler
import profile_handler
import game_handler
import pre_game_handler
import post_game_handler
import submit_handler
import login_handler
import question_handler


server = Server()
server.register('/', index_handler.index_handler)
server.register('/profile', profile_handler.profile_handler)
server.register('/game', game_handler.game_handler)
server.register('/pre_game', pre_game_handler.pre_game_handler)
server.register('/post_game', post_game_handler.post_game_handler)
server.register('/submit', submit_handler.submit_handler)
server.register('/login',
                login_handler.login_handler,
                post=login_handler.login_handler_post)
server.register('/question', question_handler.new_question_handler)
server.register('/question/([0-9]+)',
                question_handler.get_question_handler,
                post=question_handler.edit_question_handler)

server.run()
