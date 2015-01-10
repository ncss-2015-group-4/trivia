from tornado.ncss import Server
import index_handler
import profile_handler
import game_handler
import pre_game_handler
import post_game_handler
import submit_handler
import login_handler


server = Server()
server.register('/', index_handler.index_handler)
server.register('/profile', profile_handler.profile_handler)
server.register('/game', game_handler.game_handler)
server.register('/pre_game', pre_game_handler.pre_game_handler)
server.register('/post_game', post_game_handler.post_game_handler)
server.register('/submit', submit_handler.submit_handler)
server.register('/login', login_handler.login_handler, post=login_handler.login_handler_post)

server.run()