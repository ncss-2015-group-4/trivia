from tornado.testing import AsyncHTTPTestCase

class HTTPTestCase(AsyncHTTPTestCase):
    def get_app(self):
        from trivia import server
        self.app = server.app()
        return self.app
    
    def test_00_view_homepage(self):
        url = '/'
        headers = {'method': 'GET'}
        self.check_page(url, **headers)

    def check_page(self, url, **headers):
        response = self.fetch(url, **headers)
        if response.error:
            raise Exception('{}: {} {} {}'.format(response.error, response.code, response.request.method, response.request.url))
