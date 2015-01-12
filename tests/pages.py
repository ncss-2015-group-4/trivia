from tornado.testing import AsyncHTTPTestCase
import re
#define regex patters to search for nav bar links
pre_game_pattern = re.compile(r'href\ *\=\ *\"\/pre_game\"')
submit_pattern = re.compile(r'href\ *\=\ *\"\/question\"')
#prifile will need to take into account whether the user is logged in
#profile_pattern = re.compile(r'href\ *\=\ *\"\/profile\"')
home_pattern = re.compile(r'href\ *\=\ *\"\/"')
logout_pattern = re.compile(r'href\ *\=\ *\"\/logout"')
link_patterns = {'pre_game': pre_game_pattern, 'submit': submit_pattern, 'home':home_pattern, 'logout':logout_pattern}

class MissingLink(Exception):
    '''
    Exception for if a link is missing in html
    '''
    pass
    
def check_link(html, link, page):
    '''
    Checks if a link is in some html
    '''
    if not link_patterns[link].search(html):
        raise MissingLink("The "+link+" link is missing from the "+page+" page.")
    
class HTTPTestCase(AsyncHTTPTestCase):
    def get_app(self):
        from trivia import server
        self.app = server.app()
        return self.app
        
    def test_00_homepage_tests(self):
        url = '/'
        headers = {'method': 'GET'}
        html = self.check_page(url, **headers).decode()
        check_link(html, "home", "home")
        check_link(html, "pre_game", "home")
        check_link(html, "submit", "home")
        #check_link(html, "logout", "home")
        #check_link(html, "profile", "home")
        
    def test_01_login(self):
        url = '/login'
        headers = {'method': 'GET'}
        html = self.check_page(url, **headers).decode()#test if the login page can be accessed
        check_link(html, "home", "login")
        check_link(html, "pre_game", "login")
        check_link(html, "submit", "login")
        #check_link(html, "logout", "login")
        #check_link(html, "profile", "login")
        
    def test_02_register(self):
        url = '/user'
        headers = {'method': 'GET'}
        html = self.check_page(url, **headers).decode()#test if the user page can be accessed
        '''
        check_link(html,"home","user")
        check_link(html,"pre_game","user")
        check_link(html,"submit","user")
        check_link(html, "submit", "user")
        #check_link(html,"profile","user")
        '''
        
        #the databases are not currently finished. I will uncomment the following when they are
        #url = '/user'
        #headers = {'method': 'POST', 'body': b'username=someUser&password=pass&email=someUser@someDomain.com'}
        #self.check_page(url, **headers)#test if the registration form works
        
        #url = '/login'
        #headers = {'method': 'POST', 'body': b'username=someUser&password=pass'}
        #self.check_page(url, **headers)#test if the login form works
        
    def test_03_profile_tests(self):
        url = '/profile'
        headers = {'method': 'GET'}
        html = self.check_page(url, **headers).decode()
        check_link(html, "home", "profile")
        check_link(html,"pre_game", "profile")
        check_link(html, "submit", "profile")
        #check_link(html, "logout", "profile")
        #check_link(html, "profile", "profile")
        
    def test_04_question_submission_tests(self):
        url = '/submit'
        headers = {'method': 'GET'}
        html = self.check_page(url, **headers).decode()
        check_link(html, "home", "sumbission")
        check_link(html, "pre_game", "submission")
        check_link(html, "submit", "submission")
        #check_link(html, "logout", "submission")
        #check_link(html, "profile", "submission")
        
    def test_05_pre_game_tests(self):
        url = '/pre_game'
        headers = {'method': 'GET'}
        html = self.check_page(url, **headers).decode()
        check_link(html, "home", "pre_game")
        check_link(html, "pre_game", "pre_game")
        check_link(html, "submit", "pre_game")
        #check_link(html, "logout", "pre_game")
        #check_link(html, "profile", "pre_game")
        
    def test_06_game_tests(self):
        pass
        '''
        url = '/game'
        headers = {'method': 'GET'}
        html = self.check_page(url, **headers).decode()
        check_link(html, "home", "game")
        check_link(html, "pre_game", "game")
        check_link(html, "submit", "game")
        check_link(html, "logout", "game")
        #check_link(html, "profile", "game")
        '''
        
    def test_07_post_game_tests(self):
        url = '/post_game'
        headers = {'method': 'GET'}
        html = self.check_page(url, **headers).decode()
        check_link(html, "home", "login")
        check_link(html, "pre_game", "login")
        check_link(html, "submit", "login")
        #check_link(html, "logout", "login")
        #check_link(html, "profile", "login")
        
    def test_07_logout_tests(self):
        url = '/logout'
        headers = {'method': 'GET'}
        html = self.check_page(url, **headers).decode()
        check_link(html, "home", "logout")
        check_link(html, "pre_game", "logout")
        #check_link(html, "submit", "logout")
        #check_link(html, "profile", "logout")
    
    def check_page(self, url, **headers):
        response = self.fetch(url, **headers)
        if response.error:
            raise Exception('{}: {} {} {}'.format(response.error, response.code, response.request.method, response.request.url))
        else:
            return response.body