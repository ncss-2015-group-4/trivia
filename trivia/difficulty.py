
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
	totalC = 0
	totalW = 0
	count_correct = 0 
	count_wrong = 0
	
	for question, correct in questions_answers:
		if correct:
			if question == EASY:
				totalC += 1
			elif question == MEDIUM:
				totalC += 2
			elif question == HARD:
				totalC += 3
			count_correct += 1 
		else:
			if question == EASY:
				totalW -= 3
			elif question == MEDIUM:
				totalW -= 2
			elif question == HARD:
				totalW -= 1
			count_wrong = 0
	average_correct = totalC/count_correct
	if count_wrong != 0:
		average_wrong = totalW/count_wrong
	else:
		average_wrong = 0
	#final = total/len(questions_answers)
	final = average_correct + average_wrong
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
	print(skill_level([(HARD, True), (HARD, True), (HARD, True)]))
