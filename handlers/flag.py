from . import template_paths
from db.models import Question

def flag_question_handler(request, id):
	q = Question.find(question_id=id)

	if not q:
		request.write("that isnt a known question")
		return

	q.flag()

	request.write("done")

