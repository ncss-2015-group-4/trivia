from tornado.testing import AsyncHTTPTestCase
from tornado.web import create_signed_value
import re
from db.models import User
from db.models import Category
from db.models import Question
from db.models import Answer
import html
import os
import sqlite3
#define regex patters to search for nav bar links
pre_game_pattern = re.compile(r'href\ *\=\ *\"\/pre_game\"')
submit_pattern = re.compile(r'href\ *\=\ *\"\/question\"')
#prifile will need to take into account whether the user is logged in
#profile_pattern = re.compile(r'href\ *\=\ *\"\/profile\"')
home_pattern = re.compile(r'href\ *\=\ *\"\/"')
logout_pattern = re.compile(r'href\ *\=\ *\"\/logout"')
link_patterns = {'pre_game': pre_game_pattern, 'submit': submit_pattern, 'home':home_pattern, 'logout':logout_pattern}
#Apparently some questions end with a newline.
question_pattern = re.compile(r'\<p\ id\=\"question\"\>(.+\n?)\<\/p\>')

class MissingLink(Exception):
    '''
    Exception for if a link is missing in page_html
    '''
    pass

class LoginError(Exception):
    '''
    Exception for an issue with login/register
    '''
    pass

class GameError(Exception):
    '''
    Exception for an issue with the game
    '''
    pass

class PageError(Exception):
    '''
    Exception for an error with a page
    '''
    pass

class SubmitError(Exception):
    '''
    Exception for submitting questions
    '''
    pass
    
def check_link(page_html, link, page):
    '''
    Checks if a link is in some page_html
    '''
    if not link_patterns[link].search(page_html):
        raise MissingLink("The "+link+" link is missing from the "+page+" page.")

cookies=''
class HTTPTestCase(AsyncHTTPTestCase):
    def get_app(self):
        from trivia import server
        self.app = server.app(cookie_secret='test')
        return self.app
        
    def test_00_homepage_tests(self):
        url = '/'
        headers = {'method': 'GET'}
        page_html = self.check_page(url, **headers)
        check_link(page_html, "home", "home")
        check_link(page_html, "pre_game", "home")
        check_link(page_html, "submit", "home")
        #check_link(page_html, "logout", "home")
        #check_link(page_html, "profile", "home")
         
    def test_01_register(self):
        global cookies
        url = '/user'
        headers = {'method': 'GET'}
        page_html = self.check_page(url, **headers)#test if the user page can be accessed
        '''
        check_link(page_html,"home","user")
        check_link(page_html,"pre_game","user")
        check_link(page_html,"submit","user")
        check_link(page_html, "submit", "user")
        #check_link(page_html,"profile","user")
        '''
        #test registration
        url= '/user'
        headers = {'method': 'POST', 'body': b'username=testUser&password=testPass&email=testUser%40someDomain.com'}
        page_html=self.check_page(url, **headers)
        user_id=User.find(username='testUser').id
        cookie_value = create_signed_value(self.app.settings['cookie_secret'], 'user_id', str(user_id))
        cookies = 'user_id='+cookie_value.decode('utf-8')
        #check if user name appears on homepage
        url='/'
        headers = {'method': 'GET', 'headers': {'Cookie': cookies}}
        page_html = self.check_page(url, **headers)
        if 'testUser' not in page_html:
            raise LoginError('Username not on the homepage')
        else:
            print('Logged in after registering')
    
    def test_02_login(self):
        url = '/login'
        headers = {'method': 'GET'}
        page_html = self.check_page(url, **headers)#test if the login page can be accessed
        check_link(page_html, "home", "login")
        check_link(page_html, "pre_game", "login")
        check_link(page_html, "submit", "login")
        #check_link(page_html, "logout", "login")
        #check_link(page_html, "profile", "login")

    def test_03_profile_tests(self):
        global cookies
        url = '/profile'
        headers = {'method': 'GET', 'headers': {'Cookie': cookies}}
        page_html = self.check_page(url, **headers)
        check_link(page_html, "home", "profile")
        check_link(page_html,"pre_game", "profile")
        check_link(page_html, "submit", "profile")
        #check_link(page_html, "logout", "profile")
        #check_link(page_html, "profile", "profile")
        
    def test_04_question_submission_tests(self):
        global cookies
        url = '/submit'
        headers = {'method': 'GET', 'headers': {'Cookie':cookies}}
        page_html = self.check_page(url, **headers)
        check_link(page_html, "home", "sumbission")
        check_link(page_html, "pre_game", "submission")
        check_link(page_html, "submit", "submission")

        #Try making a question in each category
        for category in Category.find_all():
            print("Making a test question for category "+str(category.id))
            url= '/question'
            headers = {'method': 'POST', 'body': b'categories='+bytes(str(category.id),'utf-8')+b'&question=testQuestion&correct_answer=correct&wrong_answer_1=wrong1&wrong_answer_2=wrong2&wrong_answer_3=wrong3'}
            page_html=self.check_page(url, **headers)
            if 'testQuestion' not in page_html:
                raise SubmitError('testQuestion was not submitted to category '+str(category.id))
        
    def test_05_category_tests(self):
        url = '/categories'
        headers = {'method': 'GET'}
        page_html = self.check_page(url, **headers)
        check_link(page_html, "home", "categories")
        check_link(page_html, "pre_game", "categories")
        check_link(page_html, "submit", "categories")
        #check if all the categories are listed
        list_of_categories = Category.find_all()
        #Checking that all the categories are listed
        for category in list_of_categories:
            print('Checking if category '+str(category.id)+' is listed on the categories page')
            if not re.search(r'\<a href\=\"\/category\/'+str(category.id)+r'\"\>\<button class\=\"category\-button\"\>'+re.escape(html.escape(category.name))+r'\<\/button\>\<\/a>\<\/br\>', page_html):
                raise PageError(category.name+' is missing from the categoties page.')
        #Check that all the questions are listed
        for category in list_of_categories:
            print('Checking question list in category '+str(category.id))
            list_of_questions = Question.find_all(category=category.id)
            url = '/category/'+str(category.id)
            page_html = self.check_page(url, **{'method': 'GET'})
            for question in list_of_questions:
                if not re.search(r'\<li\>'+re.escape(html.escape(question.question))+r'\<\/li\>', page_html):
                    raise PageError(str(question.question)+' is missing from '+url)
 
    def test_06_game_tests(self):
        #Todo: Document this mess, I am too lazy to do it right now
        global cookies
        print("Testing game")
        game_cookie=''
        game_id=0
        #there is no function in the models.Question class to get the all the question answers. As I do not want to access the game directly I will use sql
        conn = sqlite3.connect('db/trivia.db')
        cur=conn.cursor()
        #for each category
        for category in Category.find_all():
            #for each difficulty
            for difficulty in range(3):
                #Some combinations of categories and difficulties may have less than 5 questions
                #if this is the case the quiz will be shorter
                cur.execute('SELECT * FROM questions WHERE category = ? AND difficulty = ?', (category.id, difficulty))
                max_questions = len(cur.fetchall())
                if max_questions > 5:
                    max_questions = 5
                print('Max questions: {}'.format(max_questions))
                #score to test
                final_scores=[]
                if max_questions > 0:
                    final_scores.append(0)
                if max_questions > 1:
                    final_scores.append(1)
                final_scores.append(max_questions)
                for final_score in final_scores:
                    if max_questions == 0:
                        break #If there are no questions in the category there will be a 404 error when accessing /game/0
                    game_id+=1
                    url = '/game/create'
                    headers = {'method': 'POST', 'body': b'category_id='+bytes(str(category.id),'utf-8')+b'&difficulty='+bytes(str(difficulty),'utf-8'), 'headers': {'Cookie':cookies}}
                    self.fetch(url, **headers).body.decode()#Start the game, this will result in a 404 error as the redirect to /game/0 will be missing the game_id cookie. This is due to AsyncHTTPTestCase lack of cookie support (same reason why I am calculating the cookies rather then retreving them from the responce.)
                    cookie_value = create_signed_value(self.app.settings['cookie_secret'], 'game_id', str(game_id))
                    game_cookie = 'game_id='+cookie_value.decode('utf-8')
                    #for each question to get correct
                    question_number=0
                    game_headers = {'method':'GET', 'headers':{'Cookie':game_cookie+'; '+cookies}}
                    for i in range(final_score):
                        page_html = self.check_page('/game/'+str(question_number), **game_headers)
                        print("Submitting correct answer")
                        question_text = html.unescape(question_pattern.search(page_html).groups()[0])
                        question_id = Question.find(question=question_text).id
                        cur.execute('SELECT * FROM answers WHERE question_id = ?',(question_id,))#get the answers to the question
                        answers = cur.fetchall()
                        for answer in answers: #check if the answers are on the page
                            if html.escape(answer[3]) not in page_html:
                                raise GameError('Answer {} missing from question {}'.format(answer[0],question_id))
                        answers.sort(key=lambda x: x[2], reverse=True)#sort the answers so that the correct answer is first
                        url = '/game/submit/'+str(answers[0][0])
                        self.fetch(url, **game_headers)
                        question_number+=1
                    
                    for i in range(max_questions-final_score):                        
                        page_html = self.check_page('/game/'+str(question_number), **game_headers)
                        print("Submitting incorrect answer")
                        if question_pattern.search(page_html) is None:
                            print(page_html)
                        question_text = html.unescape(question_pattern.search(page_html).groups()[0])
                        question_id = Question.find(question=question_text).id
                        cur.execute('SELECT * FROM answers WHERE question_id = ?',(question_id,))
                        answers = cur.fetchall()
                        for answer in answers:
                            if html.escape(answer[3]) not in page_html:
                                raise GameError('Answer {} missing from question {}'.format(answer[0],question_id))
                        answers.sort(key=lambda x: x[2], reverse=True)
                        url = '/game/submit/'+str(answers[2][0])
                        self.fetch(url, **game_headers)
                        question_number+=1
                    print("Finished game category:{} difficulty:{} final score:{}".format(category.id,difficulty,final_score))

    def test_07_logout_tests(self):
        print("Checking logout tests")
        url = '/logout'
        headers = {'method': 'GET'}
        page_html = self.check_page(url, **headers)
        check_link(page_html, "home", "logout")
        check_link(page_html, "pre_game", "logout")
        #check_link(page_html, "submit", "logout")
        #check_link(page_html, "profile", "logout")

    def check_page(self, url, **headers):
        response = self.fetch(url, **headers)
        if response.error:
            raise Exception('{}: {} {} {} {}'.format(response.error, response.code, response.request.method, response.request.url, response.request.headers))
        else:
            return response.body.decode()

