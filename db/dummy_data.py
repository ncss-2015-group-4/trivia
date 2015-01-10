import sqlite3
conn= sqlite3.connect('trivia.db')
cur= conn.cursor()
cur.execute("INSERT INTO users VALUES(NULL,'awesomealex','5f4dcc3b5aa765d61d8327deb882cf99','dummyemail@email.com');")
cur.execute("INSERT INTO users VALUES(NULL,'fantasticfeddie','25d55ad283aa400af464c76d713c07ad','dummyemail1@email.com');")
cur.execute("INSERT INTO users VALUES(NULL,'amazingaretha','d8578edf8458ce06fbc5bb76a58c5ca4','dummyemail2@email.com');")

cur.execute("INSERT INTO categories VALUES(NULL,'Harry Potter');")
cur.execute("INSERT INTO categories VALUES(NULL,'Doctor Who');")

cur.execute("INSERT INTO questions VALUES(NULL,'Which house is Harry Potter in?',10,8,1);")
cur.execute("INSERT INTO questions VALUES(NULL,'Who played the 10th Doctor?',15,13,2);")
cur.execute("INSERT INTO questions VALUES(NULL,'What is the best ranked Pokemon?',20,0,2);")

cur.execute("INSERT INTO answers VALUES(NULL,1,1,'Gryffindor');")
cur.execute("INSERT INTO answers VALUES(NULL,1,0,'Ravenclaw');")
cur.execute("INSERT INTO answers VALUES(NULL,1,0,'Hufflepuff');")
cur.execute("INSERT INTO answers VALUES(NULL,1,0,'Slytherin');")

cur.execute("INSERT INTO answers VALUES(NULL,2,1,'David Tennant');")
cur.execute("INSERT INTO answers VALUES(NULL,2,0,'Matt Smith');")
cur.execute("INSERT INTO answers VALUES(NULL,2,0,'Peter Capaldi');")
cur.execute("INSERT INTO answers VALUES(NULL,2,0,'Christopher Eccleston');")

cur.execute("INSERT INTO answers VALUES(NULL,3,1,'Kirby');")
cur.execute("INSERT INTO answers VALUES(NULL,3,0,'Donkey Kong');")
cur.execute("INSERT INTO answers VALUES(NULL,3,0,'Magic Alex');")
cur.execute("INSERT INTO answers VALUES(NULL,3,0,'Pac Man');")


cur.execute("INSERT INTO flags VALUES(NULL,3);")
cur.execute("INSERT INTO flags VALUES(NULL,3);")
cur.execute("INSERT INTO flags VALUES(NULL,3);")

cur.execute("INSERT INTO scores VALUES(1,2,20,19);")
cur.execute("INSERT INTO scores VALUES(2,1,18,4);")
cur.execute("INSERT INTO scores VALUES(3,1,20,20);")
