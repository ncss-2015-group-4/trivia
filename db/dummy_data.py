import sqlite3
conn= sqlite3.connect('trivia.db')
cur= conn.cursor()
cur.execute("INSERT INTO users VALUES(NULL,'awesomealex','5f4dcc3b5aa765d61d8327deb882cf99','dummyemail@email.com');")
cur.execute("INSERT INTO users VALUES(NULL,'fantasticfeddie','25d55ad283aa400af464c76d713c07ad','dummyemail1@email.com');")
cur.execute("INSERT INTO users VALUES(NULL,'amazingaretha','d8578edf8458ce06fbc5bb76a58c5ca4','dummyemail2@email.com');")

cur.execute("INSERT INTO categories VALUES(NULL,'Harry Potter');")
cur.execute("INSERT INTO categories VALUES(NULL,'Doctor Who');")

cur.execute("INSERT INTO questions VALUES(NULL,'Which house is Harry Potter in?',20,8,1);")
cur.execute("INSERT INTO questions VALUES(NULL,'Who played the 10th Doctor?',20,18,2);")
cur.execute("INSERT INTO questions VALUES(NULL,'What year was Doctor Who first aired?',20,6,2);")
cur.execute("INSERT INTO questions VALUES(NULL,'Who was the 9th Doctor's companion?',20,17,2);")
cur.execute("INSERT INTO questions VALUES(NULL,'Who played the first Doctor?',20,17,2);")
cur.execute("INSERT INTO questions VALUES(NULL,'Who is RTD??',20,8,2);")
cur.execute("INSERT INTO questions VALUES(NULL,'What is John Hurt's Doctor refered to as?',20,17,2);")
cur.execute("INSERT INTO questions VALUES(NULL,'Which of these is a spin off series from Doctor Who?',20,4,2);")
cur.execute("INSERT INTO questions VALUES(NULL,'What planet is The Doctor from?',20,14,2);")
cur.execute("INSERT INTO questions VALUES(NULL,'What species is The Doctor?',20,20,2);")
cur.execute("INSERT INTO questions VALUES(NULL,'What is the best ranked Pokemon?',20,0,2);")
cur.execute("INSERT INTO questions VALUES(NULL,'Who killed Snape',20,17,1);")
cur.execute("INSERT INTO questions VALUES(NULL,'How many Horcru?',10,8,1);")

cur.execute("INSERT INTO answers VALUES(NULL,1,1,'Gryffindor');")
cur.execute("INSERT INTO answers VALUES(NULL,1,0,'Ravenclaw');")
cur.execute("INSERT INTO answers VALUES(NULL,1,0,'Hufflepuff');")
cur.execute("INSERT INTO answers VALUES(NULL,1,0,'Slytherin');")

cur.execute("INSERT INTO answers VALUES(NULL,2,1,'David Tennant');")
cur.execute("INSERT INTO answers VALUES(NULL,2,0,'Matt Smith');")
cur.execute("INSERT INTO answers VALUES(NULL,2,0,'Peter Capaldi');")
cur.execute("INSERT INTO answers VALUES(NULL,2,0,'Christopher Eccleston');")

cur.execute("INSERT INTO answers VALUES(NULL,3,1,'1963');")
cur.execute("INSERT INTO answers VALUES(NULL,3,0,'2005');")
cur.execute("INSERT INTO answers VALUES(NULL,3,0,'1960');")
cur.execute("INSERT INTO answers VALUES(NULL,3,0,'1986');")

cur.execute("INSERT INTO answers VALUES(NULL,4,1,'Rose Tyler');")
cur.execute("INSERT INTO answers VALUES(NULL,4,0,'Donna Noble');")
cur.execute("INSERT INTO answers VALUES(NULL,4,0,'Amy Pond');")
cur.execute("INSERT INTO answers VALUES(NULL,4,0,'Clara Oswald');")

cur.execute("INSERT INTO answers VALUES(NULL,5,1,'William Hartnell');")
cur.execute("INSERT INTO answers VALUES(NULL,5,0,'Tom Baker');")
cur.execute("INSERT INTO answers VALUES(NULL,5,0,'Christopher Eccleston');")
cur.execute("INSERT INTO answers VALUES(NULL,5,0,'Jimmy Murran');")

cur.execute("INSERT INTO answers VALUES(NULL,6,1,'Russel T. Davis');")
cur.execute("INSERT INTO answers VALUES(NULL,6,0,'R. Tennant David');")
cur.execute("INSERT INTO answers VALUES(NULL,6,0,'Robert Tennant Daniels');")
cur.execute("INSERT INTO answers VALUES(NULL,6,0,'R. Tom Donald');")

cur.execute("INSERT INTO answers VALUES(NULL,7,1,'The War Doctor');")
cur.execute("INSERT INTO answers VALUES(NULL,7,0,'The 9th Doctor');")
cur.execute("INSERT INTO answers VALUES(NULL,7,0,'The Other Doctor');")
cur.execute("INSERT INTO answers VALUES(NULL,7,0,'No More');")

cur.execute("INSERT INTO answers VALUES(NULL,8,1,'Torchwood');")
cur.execute("INSERT INTO answers VALUES(NULL,8,0,'The Daleks');")
cur.execute("INSERT INTO answers VALUES(NULL,8,0,'The Angels Have The Phonebox');")
cur.execute("INSERT INTO answers VALUES(NULL,8,0,'Sherlock');")

cur.execute("INSERT INTO answers VALUES(NULL,9,1,'Gallifrey');")
cur.execute("INSERT INTO answers VALUES(NULL,9,0,'Earth');")
cur.execute("INSERT INTO answers VALUES(NULL,9,0,'Mars');")
cur.execute("INSERT INTO answers VALUES(NULL,9,0,'Raxacoricofallapatorious');")

cur.execute("INSERT INTO answers VALUES(NULL,10,1,'Time Lord');")
cur.execute("INSERT INTO answers VALUES(NULL,10,0,'Human');")
cur.execute("INSERT INTO answers VALUES(NULL,10,0,'Slitheen');")
cur.execute("INSERT INTO answers VALUES(NULL,10,0,'Dalek');")

cur.execute("INSERT INTO answers VALUES(NULL,11,1,'Kirby');")
cur.execute("INSERT INTO answers VALUES(NULL,11,0,'Donkey Kong');")
cur.execute("INSERT INTO answers VALUES(NULL,11,0,'Magic Alex');")
cur.execute("INSERT INTO answers VALUES(NULL,11,0,'Pac Man');")


cur.execute("INSERT INTO flags VALUES(NULL,3);")
cur.execute("INSERT INTO flags VALUES(NULL,3);")
cur.execute("INSERT INTO flags VALUES(NULL,3);")

cur.execute("INSERT INTO scores VALUES(1,2,20,19);")
cur.execute("INSERT INTO scores VALUES(2,1,18,4);")
cur.execute("INSERT INTO scores VALUES(3,1,20,20);")

conn.commit()
