from tornado.testing import AsyncHTTPTestCase
from tornado.web import create_signed_value
import re
import random
from db.models import User
from db.models import Category
from db.models import Question
import html
import sqlite3
# Define regex patters to search for nav bar links
pre_game_pattern = re.compile(r'href\ *\=\ *\"\/pre_game\"')
submit_pattern = re.compile(r'href\ *\=\ *\"\/question\"')
profile_pattern = re.compile(r'href\ *\=\ *\"\/profile\"')
home_pattern = re.compile(r'href\ *\=\ *\"\/"')
logout_pattern = re.compile(r'href\ *\=\ *\"\/logout"')
link_patterns = {'pre_game': pre_game_pattern, 'submit': submit_pattern, 'home': home_pattern, 'logout': logout_pattern, 'profile': profile_pattern}
# Apparently some questions end with a newline.
question_pattern = re.compile(r'\<p\ id\=\"question\"\>(.+\n?)\<\/p\>')
score_pattern = re.compile(r'([0-9]*)\ \/\ ([0-9]*)')
question_results_pattern = re.compile(r'<li>(.+?)&nbsp;<a\ href\=\"\/flag\/([0-9]+?)\">Flag\?<\/a>&nbsp;(.+?)\ ?<\/li>', re.DOTALL)

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

cookies = ''

class HTTPTestCase(AsyncHTTPTestCase):
    def get_app(self):
        from trivia import server
        server.set_cookie_secret('test')
        self.app = server.app()
        return self.app

    def test_00_homepage_tests(self):
        page_html = self.check_page('/', method='GET')
        self.check_link(page_html, "home", "home")
        self.check_link(page_html, "pre_game", "home")
        self.check_link(page_html, "submit", "home")

    def test_01_register(self):
        '''
        Check that a new user can register
        Note: the registration page is /login but the form is posted to /user
        '''
        global cookies
        headers = {'method': 'POST', 'body': b'username=testUser&password=testPass&email=testUser%40someDomain.com'}
        page_html = self.check_page('/user', **headers)
        # Make the cookie
        user_id = User.find(username='testUser').id  # get the user id from the database
        cookie_value = create_signed_value(self.app.settings['cookie_secret'], 'user_id', str(user_id))
        cookies = 'user_id='+cookie_value.decode('utf-8')
        # Check if username appears on the homepage
        headers = {'method': 'GET', 'headers': {'Cookie': cookies}}
        page_html = self.check_page('/', **headers)
        if 'testUser' not in page_html:
            raise LoginError('Username not on the homepage')
        # Check that the logout and profile links are now on the home page
        self.check_link(page_html, "logout", "home")
        self.check_link(page_html, "profile", "home")

    def test_02_login(self):
        '''
        Check that the login page can be accessed
        '''
        page_html = self.check_page('/login', method='GET')
        self.check_link(page_html, "home", "login")
        self.check_link(page_html, "pre_game", "login")
        self.check_link(page_html, "submit", "login")

    def test_03_profile_tests(self):
        '''
        Check that the profile page can be accessed
        '''
        global cookies
        headers = {'method': 'GET', 'headers': {'Cookie': cookies}}
        page_html = self.check_page('/profile', **headers)
        self.check_link(page_html, "home", "profile")
        self.check_link(page_html, "pre_game", "profile")
        self.check_link(page_html, "submit", "profile")

    def test_04_question_submission_tests(self):
        '''
        Check that questions can be submitted
        '''
        global cookies
        headers = {'method': 'GET', 'headers': {'Cookie': cookies}}
        page_html = self.check_page('/submit', **headers)
        self.check_link(page_html, "home", "sumbission")
        self.check_link(page_html, "pre_game", "submission")
        self.check_link(page_html, "submit", "submission")
        # Try making a question in category 1
        query = (b'categories=1'
                 + b'&question=testQuestion'
                 + b'&correct_answer=correct'
                 + b'&wrong_answer_1=wrong&wrong_answer_2=wrong2&wrong_answer_3=wrong3')
        headers = {'method': 'POST', 'body': query}
        page_html = self.check_page('/question', **headers)
        if 'testQuestion' not in page_html:
            raise SubmitError('testQuestion was not submitted to category ' + str(category.id))

    def test_05_category_tests(self):
        '''
        Check that the categories and questions are being displayed
        '''
        page_html = self.check_page('/categories', method='GET')
        self.check_link(page_html, "home", "categories")
        self.check_link(page_html, "pre_game", "categories")
        self.check_link(page_html, "submit", "categories")
        # Check that all the categories are listed
        list_of_categories = Category.find_all()
        for category in list_of_categories:
            cat = re.search(('\<a href\=\"\/category\/'
                             + str(category.id)
                             + r'\"\>\<button class\=\"category\-button\"\>'
                             + re.escape(html.escape(category.name))
                             + r'\<\/button\>\<\/a>\<\/br\>'), page_html)
            if not cat:
                raise PageError(category.name+' is missing from the categories page.')
        # Check that all the questions are listed in the category pages
        for category in list_of_categories:
            list_of_questions = Question.find_all(category=category.id)
            url = '/category/'+str(category.id)
            page_html = self.check_page(url, method='GET')
            for question in list_of_questions:
                if not re.search(r'\<li\>'+re.escape(html.escape(question.question))+r'\<\/li\>', page_html):
                    raise PageError(str(question.question)+' is missing from '+url)

    def test_06_game_tests(self):
        '''
        Check submitting questions and scoring
        '''
        global cookies
        conn = sqlite3.connect('db/trivia.db')
        cur = conn.cursor()
        # The database is reset before running the tests so the first game id should be 1
        game_id = 0
        tests = [(0, 0, 2), (0, 1, 0), (0, 1, 3), (0, 2, 5), (1, 0, 0)]
        for category, difficulty, final_score in tests:
            cur.execute('SELECT COUNT(question_id) FROM questions WHERE category = ? AND difficulty = ?', (category, difficulty))
            num_questions = cur.fetchone()
            num_questions = 5 if num_questions[0] > 5 else num_questions[0]
            url = '/game/create'
            query = (b'category_id=' + str(category).encode()
                     + b'&difficulty=' + str(difficulty).encode())
            headers = {'method': 'POST', 'body': query, 'headers': {'Cookie': cookies}}
            page_html = self.fetch(url, **headers).body.decode()
            # Test if category and difficulty is empty
            if num_questions == 0:
                if 'There are no questions in this category and difficulty. :(' not in page_html:
                    raise GameError('Message not displayed for empty category and difficulty')
                # skip to the next test case
                continue

            game_id += 1
            cookie_value = create_signed_value(self.app.settings['cookie_secret'], 'game_id', str(game_id))
            game_cookie = 'game_id='+cookie_value.decode()
            game_headers = {'method': 'GET', 'headers': {'Cookie': game_cookie+';'+cookies}}
            questions = []
            for i in range(num_questions):
                page_html = self.check_page('/game/'+str(i), **game_headers)
                question_text = html.unescape(question_pattern.search(page_html).groups()[0])
                question_id = Question.find(question=question_text).id
                cur.execute('SELECT * FROM answers WHERE question_id = ? ORDER BY correct DESC', (question_id,))
                answers = cur.fetchall()
                # Check if the answers are displayed
                # This probably doesn't need to be checked for every question
                if i == 0:
                    for answer in answers:
                        if html.escape(answer[3]) not in page_html:
                            raise GameError('Answer {} missing from question {}'.format(answer[0], question_id))

                if i < final_score:
                    questions.append((html.escape(question_text), str(question_id), "Correct!"))
                    url = '/game/submit/' + str(answers[0][0])
                else:
                    answer_index = random.randrange(1, len(answers))
                    result_text = ("Your answer: "
                                   + html.escape(answers[answer_index][3])
                                   + ", Correct answer: "
                                   + html.escape(answers[0][3]))
                    questions.append((html.escape(question_text), str(question_id), result_text))
                    url = '/game/submit/' + str(answers[answer_index][0])
                self.fetch(url, **game_headers)

            page_html = self.check_page("/post_game", **game_headers)
            returned_score = score_pattern.search(page_html)
            if int(returned_score.group(1)) != final_score:
                raise GameError(('Incorrect final game score\n'
                                 'Returned: {}\n'
                                 'Expecting: {}\n'
                                 'For category: {}, diffculty: {}').format(returned_score.group(1), final_score, category, difficulty))

            if int(returned_score.group(2)) != num_questions:
                raise GameError(('Incorrect final game score denominator\n'
                                 'Returned: {}\n'
                                 'Expecting {}\n'
                                 'For category: {}, diffculty: {}').format(returned_score.group(2), num_questions, category, difficulty))

            matches = question_results_pattern.findall(page_html)
            for question in questions:
                if question not in matches:
                    raise GameError(('Incorrect question result text.\n'
                                     'match groups found:\n{}\n'
                                     'match groups expected:\n{}\n').format(matches, questions))
            extra = [question for question in matches if question not in questions]  # Find unexpected question results
            if extra != []:
                raise GameError("Unexpected question result(s) in postgame.\nmatch groups:\n{}".format(extra))

    def test_07_logout_tests(self):
        page_html = self.check_page('/logout', method='GET')
        self.check_link(page_html, "home", "logout")
        self.check_link(page_html, "pre_game", "logout")

    def check_page(self, url, **headers):
        response = self.fetch(url, **headers)
        if response.error:
            raise Exception('{}: {} {} {} {}'.format(response.error, response.code, response.request.method, response.request.url, response.request.headers))
        else:
            return response.body.decode()

    def check_link(self, page_html, link, page):
        '''
        Checks if a link is in a page
        '''
        if not link_patterns[link].search(page_html):
            raise MissingLink("The {} link is missing from the {} page.".format(link, page))
