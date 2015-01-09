import sys

# Generates test cases based on recorded requests
def generate_test_case(module, server, database, name="HTTPTestCase"):
	defs = """from tornado.testing import AsyncHTTPTestCase

class {}(AsyncHTTPTestCase):
	def get_app(self):
		from os import remove
		from os.path import exists

		from {} import {} as database
		from {} import {} as server

		test_database = 'test.db'
		if exists(test_database): remove(test_database)
		database(test_database)

		return server().app()
	
	def test(self):
		""".format(name, module, database, module, server)

	requests = record_requests(module, server, database)
	
	tests = ''
	for request in requests:
		args = {'method': request.method}
		if request.method in ['PUT', 'POST', 'DELETE', 'PATCH']:
			args['headers'] = request.headers
			args['body'] = request.body

		tests += """url = {!r}
		kwargs = {!r}
		response = self.fetch(url, **kwargs)
		""".format(request.uri, args)
		tests+= """if response.error:
			raise Exception('{}: {} {} {}'.format(response.error, response.code, response.request.method, response.request.url))
		
		"""

	return defs + tests


# Records the HTTP requests to the server
def record_requests(module, server, database):
	from os import remove
	from os.path import exists
	from subprocess import Popen, PIPE

	# Initialise the database
	test_database = 'test.db'
	if exists(test_database): remove(test_database)
	database = __import__(module).__dict__[database](test_database)

	# Import the server
	server = __import__(module).__dict__[server]()

	# Record server requests
	requests = record_server(server)

	# Remove the test database
	if exists(test_database): remove(test_database)

	return requests

# Takes a server and records its HTTP requests
def record_server(server):
	loop = None
	requests = []

	# Wrap each request with a logger
	def logger(handler):
		def log(response, *args, **kwargs):
			requests.append(response.request)
			handler(response, *args, **kwargs)
		
		return log

	for handler in server.handlers:
		h = handler.handler_class
		h.get = logger(h.get)
		h.post = logger(h.post)
		h.patch = logger(h.patch)
		h.delete = logger(h.delete)
		h.put = logger(h.put)

	# Create URL for ending the demo
	def end_demo(response):
		if loop:
			loop.stop()

	server.register('/end_demo', end_demo)

	# Start server
	loop = server.loop()
	loop.start()

	return requests


if __name__ == '__main__':
	this, module, server, database = sys.argv
	
	test_case = generate_test_case(module, server, database)
	print(test_case)
