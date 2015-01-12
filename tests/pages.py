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
    
    def test_01_view_login(self):
        url = '/login'
        headers = {'method': 'GET'}
        self.check_page(url, **headers)
        
    def test_02_view_user(self):
        url = '/user'
        headers = {'method': 'GET'}
        self.check_page(url, **headers)
        
    def test_03_view_profile(self):
        url = '/profile'
        headers = {'method': 'GET'}
        self.check_page(url, **headers)
        
    def test_04_view_submit(self):
        url = '/submit'
        headers = {'method': 'GET'}
        self.check_page(url, **headers)
        
    def test_05_view_question(self):
        url = '/question'
        headers = {'method': 'GET'}
        self.check_page(url, **headers)
        
    def test_06_view_pre_game(self):
        url = '/pre_game'
        headers = {'method': 'GET'}
        self.check_page(url, **headers)
        
    def test_07_view_game(self):
        url = '/game'
        headers = {'method': 'GET'}
        self.check_page(url, **headers)
        
    def test_08_view_post_game(self):
        url = '/post_game'
        headers = {'method': 'GET'}
        self.check_page(url, **headers)
    
    def check_page(self, url, **headers):
        response = self.fetch(url, **headers)
        if response.error:
            raise Exception('{}: {} {} {}'.format(response.error, response.code, response.request.method, response.request.url))
