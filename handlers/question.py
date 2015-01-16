from db.models import Question
from db.models import Answer
from db.models import Category
from templating import render_template
from db.models import User
from . import template_paths


def new_question_handler(request):
    question = request.get_field("question")
    correct_answer = request.get_field("correct_answer")
    wrong_answer_1 = request.get_field("wrong_answer_1")
    wrong_answer_2 = request.get_field("wrong_answer_2")
    wrong_answer_3 = request.get_field("wrong_answer_3")
    category = request.get_field("categories")

    #print(question, correct_answer, wrong_answer_1, wrong_answer_2, wrong_answer_3, category)
    question = Question.create(question, category)
    Answer.create(question.id, True, correct_answer)
    Answer.create(question.id, False, wrong_answer_1)
    Answer.create(question.id, False, wrong_answer_2)
    Answer.create(question.id, False, wrong_answer_3)
    request.redirect('/category/' + category)

def new_question_form(request):
    u_id = request.get_secure_cookie ('user_id')
    u_name = ""
    if u_id is not None:
        u_id = u_id.decode("UTF-8")
        u_name = User.find(user_id=u_id)
        u_name = u_name.username
    list_of_categories = Category.find_all()
    question_new = render_template(template_paths["submit"], {"list_of_categories": list_of_categories,"user_name":u_name})
    request.write(question_new)

def get_question_handler(request, question_id):
  request.write("""<!DOCTYPE html>
<html>
<body>
<h1>
Edit Question Form
</h1>
<form method="post">
Question:<br>
<input type="text" name="question">
<br>
Correct answer:<br>
<input type="text" name="correct_answer">
<br>
Wrong answer 1:<br>
<input type="text" name="wrong_answer_1">
<br>
Wromg answer 2:<br>
<input type="text" name="wrong_answer_2">
<br>
Wrong answer 3:<br>
<input type="text" name="wrong_answer_3">
<br><br>
<input type="submit" value="Submit">
</form>
</body>
</html>
""")


def edit_question_handler(request, question_id):
  print("Edit Question Handler")
  pass
