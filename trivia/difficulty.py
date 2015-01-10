
EASY = 1
MEDIUM = 2
HARD = 3

BEGINNER = 1
INTERMEDIATE = 2
EXPERT = 3

def difficulty(people_answers):
	'''This is finding the difficulty level of a question.
	people_answers is a list of the skill level of the person and their answer to the question.'''
	sum = 0
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
		else:
			if question == EASY:
				total -= 3
			elif question == MEDIUM:
				total -= 2
			elif question == HARD:
				total -= 1
	final = total/len(questions_answers)
	if final < 2:
		return 'Beginner'
	elif 2 <= final < 3:
		return 'Intermediate'	
	elif 3 <= final:
		return 'Expert'
	
						
if __name__ == '__main__':
	print(difficulty([(INTERMEDIATE, True)]))
	print(difficulty([(INTERMEDIATE, True), (BEGINNER, True)]))
	print(difficulty([(BEGINNER, True), (INTERMEDIATE, True), (EXPERT, True)]))
	
	print(skill_level([(EASY, True)]))
	print(skill_level([(EASY, True), (MEDIUM, True), (HARD, False)]))
	print(skill_level([(EASY, True), (EASY, True), (EASY, True), (EASY, True)]))
	print(skill_level([(HARD, True), (EASY, False), (EASY, True), (MEDIUM, False), (HARD, False), (MEDIUM, True), (MEDIUM, True)]))
	print(skill_level([(EASY, False), (MEDIUM, True), (MEDIUM, True), (MEDIUM, True)]))
