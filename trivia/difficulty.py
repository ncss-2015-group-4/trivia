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
	if average == 1:
		print("Easy")
	elif average == 2:
		print("Average")
	elif average == 3:
		print("Hard")
	
if __name__ == '__main__':
	print(difficulty([(INTERMEDIATE, True)]))
	