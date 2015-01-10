import sqlite3
conn= sqlite3.connect('trivia.db')
cur= conn.cursor()
cur.execute("INSERT INTO users VALUES(NULL,'awesomealex','benhash','dummyemail@email.com');")
cur.execute("INSERT INTO users VALUES(NULL,'fantasticfeddie','benhash1','dummyemail1@email.com');")
cur.execute("INSERT INTO users VALUES(NULL,'amazingaretha','benhash2','dummyemail2@email.com');")

cur.execute("INSERT INTO categories VALUES(NULL,'Harry Potter');")
cur.execute("INSERT INTO categories VALUES(NULL,'Doctor Who');")

cur.execute("INSERT INTO questions VALUES(NULL,'Which house is Harry Potter in?',10,8,1);")
cur.execute("INSERT INTO questions VALUES(NULL,'Who played the 10th Doctor?',15,13,2);")
cur.execute("INSERT INTO questions VALUES(NULL,'What is the best ranked Pokemon?',20,0,2);")

cur.execute("INSERT INTO answers VALUES(NULL,1,TRUE,'Gryffindor');")
cur.execute("INSERT INTO answers VALUES(NULL,1,FALSE,'Ravenclaw');")
cur.execute("INSERT INTO answers VALUES(NULL,1,false,'Hufflepuff');")
cur.execute("INSERT INTO answers VALUES(NULL,1,false,'Slytherin');")

cur.execute("INSERT INTO answers VALUES(NULL,2,true,'David Tennant');")
cur.execute("INSERT INTO answers VALUES(NULL,2,false,'Matt Smith');")
cur.execute("INSERT INTO answers VALUES(NULL,2,false,'Peter Capaldi');")
cur.execute("INSERT INTO answers VALUES(NULL,2,false,'Christopher Eccleston');")

cur.execute("INSERT INTO answers VALUES(NULL,3,true,'Kirby');")
cur.execute("INSERT INTO answers VALUES(NULL,3,false,'Donkey Kong');")
cur.execute("INSERT INTO answers VALUES(NULL,3,false,'Magic Alex');")
cur.execute("INSERT INTO answers VALUES(NULL,3,false,'Pac Man');")


cur.execute("INSERT INTO flags VALUES(NULL,3);")
cur.execute("INSERT INTO flags VALUES(NULL,3);")
cur.execute("INSERT INTO flags VALUES(NULL,3);")

cur.execute("INSERT INTO scores VALUES(1,2,20,19);")
cur.execute("INSERT INTO scores VALUES(2,1,18,4);")
cur.execute("INSERT INTO scores VALUES(3,1,20,20);")
