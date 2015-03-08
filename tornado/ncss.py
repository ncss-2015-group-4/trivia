"""
NCSSbook server implementation.

Wraps tornado in a nicer interface that allows URLs to be added with a function
rather than needing to be specified to an application constructor. The task
of running the server is also abstracted into a single run() function.

Users write handler functions that accept a response object. This object is
subclassed from tornado's existing RequestHandler class, so all existing
methods from that class may be accessed as necessary. Helper functions for
accessing form fields and files in the response object are provided.

The register() function on the server is used to connect URLs with handler
functions. Regex groups can be used in URLs to capture ordered arguments; the
handler function for the URL should accept the name number of additional
arguments as there are regex groups.

For examples, see ncssbook/examples. Hello World is as follows:

from tornado.ncss import Server

def index(response):
    response.write('Hello, World!')

if __name__ == '__'main__':
    server = Server()
    server.register('/', index)

"""
import hashlib
import inspect
import logging
import random

import tornado.ioloop
import tornado.log
import tornado.web
import tornado.websocket

# Setup pretty logging for ncssbook and tornado loggers.
ncssbook_log = logging.getLogger('ncssbook')
for logger in (tornado.log.access_log, tornado.log.app_log, tornado.log.gen_log, ncssbook_log):
    logger.propagate = False
    tornado.log.enable_pretty_logging(logger=logger)


class Server:
    __slots__ = ('debug', 'handlers', 'hostname', 'port', 'static_path')

    def __init__(self, *, hostname='', port=8888, static_path='static', debug=True):
        if type(hostname) is not str:
            raise ValueError('hostname must be a string')
        if type(port) is not int or port <= 0:
            raise ValueError('port must be a positive integer')
        if type(static_path) is not str or not static_path:
            raise ValueError('static must be a non-empty string')
        if type(debug) is not bool:
            raise ValueError('debug must be a boolean')

        self.hostname = hostname
        self.port = port
        self.static_path = static_path
        self.debug = debug
        self.handlers = []

    def register(self, url_pattern, handler, *, delete=None, get=None, patch=None, post=None, put=None, url_name=None, write_error=None, **kwargs):
        if type(url_pattern) is not str:
            raise ValueError('url_pattern must be a string')

        if inspect.isroutine(handler):  # Return true if the object is a user-defined or built-in function or method.
            # Default each of the HTTP method handlers back to the default handler.
            delete_handler = delete or handler
            get_handler = get or handler
            patch_handler = patch or handler
            post_handler = post or handler
            put_handler = put or handler
            write_error_handler = write_error

            class Handler(tornado.web.RequestHandler):
                def delete(self, *args, **kwargs):
                    delete_handler(self, *args, **kwargs)

                def get(self, *args, **kwargs):
                    get_handler(self, *args, **kwargs)

                def patch(self, *args, **kwargs):
                    patch_handler(self, *args, **kwargs)

                def post(self, *args, **kwargs):
                    method = self.get_field('_method', '').lower()
                    if method == 'delete':
                        return self.delete(*args, **kwargs)
                    elif method == 'patch':
                        return self.patch(*args, **kwargs)
                    elif method == 'put':
                        return self.put(*args, **kwargs)
                    post_handler(self, *args, **kwargs)

                def put(self, *args, **kwargs):
                    put_handler(self, *args, **kwargs)

                def get_field(self, name, default=None, strip=True):
                    return self.get_argument(name, default, strip=strip)  # Normally raises a MissingArgumentError if the default value is not specified.

                def get_fields(self, strip=True):
                    return dict(self.get_arguments(strip=strip))

                def get_file(self, name, default=None):
                    if name in self.request.files:
                        field = self.request.files[name][0]
                        return field['filename'], field['content_type'], field['body']
                    else:
                        return None, None, default

                def get_files(self, name, default=None):
                    if name in self.request.files:
                        return [(f['filename'], f['content_type'], f['body']) for f in self.request.files[name]]
                    else:
                        return [(None, None, default)]

                def write_error(self, status_code, **kwargs):
                    if write_error_handler is None:
                        return super().write_error(status_code, **kwargs)
                    else:
                        return write_error_handler(self, status_code, **kwargs)

            h = Handler
        elif inspect.isclass(handler) and issubclass(handler, (tornado.web.RequestHandler, tornado.websocket.WebSocketHandler)):
            h = handler
        else:
            raise ValueError('handler must be a function or a RequestHandler class')

        # Create the URLSpec with an optional name and add it to the list of URL handlers.
        url_spec = tornado.web.URLSpec(url_pattern, h, name=url_name)
        self.handlers.append(url_spec)

    def app(self, **kwargs):
        # Randomise the cookie secret upon reload.
        if 'cookie_secret' not in kwargs:
            m = hashlib.md5()
            m.update((str(random.random()) + str(random.random())).encode('utf-8'))
            cookie_secret = m.digest()
            kwargs['cookie_secret'] = cookie_secret

        # Create the app in debug mode (autoreload)
        app = tornado.web.Application(self.handlers, static_path=self.static_path, debug=self.debug, **kwargs)
        return app

    def loop(self):
        # Initialise the app, binding to the appropriate address.
        app = self.app()
        app.listen(port=self.port, address=self.hostname)
        ncssbook_log.info('Reloading... waiting for requests on http://{}:{}'.format(self.hostname or 'localhost', self.port))
        
        # Create the ioloop.
        loop = tornado.ioloop.IOLoop.instance()
        return loop
    
    def run(self):
        loop = self.loop()
        loop.start()
