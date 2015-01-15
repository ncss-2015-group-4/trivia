import sqlite3
import csv
from hasher import new_salt

conn = sqlite3.connect('trivia.db')
cur = conn.cursor()
categories = {"Harry Potter":1, "Doctor Who":2, "Star Trek":3, "Legue of Lengends":4}
category_files = {"Harry Potter":"harry_potter_questions.csv", "Doctor Who":"doctor_who_questions.csv", "Star Trek":"star_trek_questions.csv", "Legue of Lengends":"league_of_lengends_questions.csv"}
difficulties = {"easy":0, "medium":1, "hard":2}
for category in categories:
    #category id, category name
    cur.execute("INSERT INTO categories VALUES(?, ?)", (categories[category], category))

question_count = 1
answer_count = 1
for category, category_file in category_files.items():
    with open(category_file) as f:
        reader = csv.DictReader(f)
        #for each question in the category
        for question in reader:
            #add the question
            #question id, question text, times answered, times correct, category id, difficulty
            cur.execute('INSERT INTO questions VALUES(?, ?, 0, 0, ?, ?)', (question_count, question['Question'], categories[category], difficulties[question['Difficulty']]))
            #answer id, qyestion id, is the correct answer, answer text
            #add the correct answer
            cur.execute('INSERT INTO answers VALUES(?, ?, 1, ?)', (answer_count, question_count, question['Correct Answer']))
            answer_count += 1
            #add the incorrect answers
            for i in range(1, 4):
                cur.execute('INSERT INTO answers VALUES(?, ?, 1, ?)', (answer_count, question_count, question['Wrong Answer '+str(i)]))
                answer_count += 1
            question_count+=1

cur.execute('INSERT INTO users VALUES(NULL,"awesomealex","5f4dcc3b5aa765d61d8327deb882cf99", ?,"dummyemail@email.com");', (new_salt(),))
cur.execute('INSERT INTO users VALUES(NULL,"fantasticfeddie","25d55ad283aa400af464c76d713c07ad", ?, "dummyemail1@email.com");', (new_salt(),))
cur.execute('INSERT INTO users VALUES(NULL,"amazingaretha","d8578edf8458ce06fbc5bb76a58c5ca4", ?, "dummyemail2@email.com");', (new_salt(),))

cur.execute('INSERT INTO flags VALUES(NULL,3);')
cur.execute('INSERT INTO flags VALUES(NULL,3);')
cur.execute('INSERT INTO flags VALUES(NULL,3);')

cur.execute('INSERT INTO scores VALUES(1,2,20,19);')
cur.execute('INSERT INTO scores VALUES(2,1,18,4);')
cur.execute('INSERT INTO scores VALUES(3,1,20,20);')

conn.commit()
