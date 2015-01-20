#!/usr/bin/env python3

import sqlite3
import csv
import hasher

conn = sqlite3.connect('trivia.db')
cur = conn.cursor()
categories = {} 
category_files = {} 
difficulties = {"easy":0, "medium":1, "hard":2}
with open("categories.csv") as f:
    category_reader = csv.DictReader(f)
    #Get the list of categories
    for i,category in enumerate(category_reader):
        #store the category id
        categories[category["Category"]] = i+1
        #store the category csv file name
        category_files[category["Category"]] = category["CSV File"]

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
                cur.execute('INSERT INTO answers VALUES(?, ?, 0, ?)', (answer_count, question_count, question['Wrong Answer '+str(i)]))
                answer_count += 1
            question_count += 1

def add_user(username, password, email):
    salt = hasher.new_salt()
    cur.execute('INSERT INTO users VALUES(NULL, ?, ?, ?, ?);', (username, hasher.hash(password, salt), salt, email))

add_user('awesomealex', 'password', 'dummy@example.com')
add_user('fantasticfeddie', 'pword', 'dummy1@example.com')
add_user('amazingaretha', 'admin', 'dummy2@example.com')

cur.execute('INSERT INTO flags VALUES(NULL,3);')
cur.execute('INSERT INTO flags VALUES(NULL,3);')
cur.execute('INSERT INTO flags VALUES(NULL,3);')

cur.execute('INSERT INTO scores VALUES(1,2,20,19);')
cur.execute('INSERT INTO scores VALUES(2,1,18,4);')
cur.execute('INSERT INTO scores VALUES(3,1,20,20);')

conn.commit()
