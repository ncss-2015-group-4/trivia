from db.models import Score
from db.models import Category
EASY = 1
MEDIUM = 2
HARD = 3

BEGINNER = 1
INTERMEDIATE = 2
EXPERT = 3

def difficulty( ):
    sum = 0
    question_data = Score.find(user_id = '1')
    print(question_data.num_answered)
    print(question_data.num_correct)
    category_data = Category.find(category_id = question_data.category_id)
    print(category_data.category)
    """
	for person, correct in people_answers:
		if correct:
			if person == BEGINNER:
				sum += EASY
			elif person == INTERMEDIATE:
				sum += MEDIUM
			elif person == EXPERT:
				sum += HARD
		else:
			if person == BEGINNER:
				sum += MEDIUM	
			elif person == INTERMEDIATE:
				sum += HARD
			elif person == EXPERT:
				sum += HARD
	average = sum/len(people_answers)
	if 0 <= average < 2:
		return "Easy" 
	elif 2 <= average < 3:
		return "Medium"
	elif 3 < average:
		return "Hard"
        """

def skill_level(questions_answers): 
	''' This is findind the skill level of a user. 
	questions_answers is a list of the questions the user has answered and if they got it right or wrong. '''
	total = 0
	for question, correct in questions_answers:
		if correct:
			if question == EASY:
				total += 1
			elif question == MEDIUM:
				total += 2
			elif question == HARD:
				total += 3
		
	final = total/len(questions_answers)
	if final < 1.25:
		return 'Beginner'
	elif 1.25 <= final < 2.25:
		return 'Intermediate'	
	elif 2.25 <= final:
		return 'Expert'

difficulty()
