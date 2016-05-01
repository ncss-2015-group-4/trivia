import sqlite3

import sys
sys.path.append("../db")
import hasher

conn = sqlite3.connect('../db/trivia.db')

def add_user(username, password, email):
    salt = hasher.new_salt()
    conn.execute('INSERT INTO users VALUES(NULL, ?, ?, ?, ?);', (username, hasher.hash(password, salt), salt, email))

# Data for models.py test cases
add_user('awesomealex', 'password', 'dummy@example.com')
add_user('fantasticfeddie', 'pword', 'dummy1@example.com')


# Game Test cases:
#     < 5 questions: category 0, difficulty 0
#     5 questions: category 0, difficulty 1
#     0 questions: category 0, difficulty 2
#     > 5 questions: category 1, difficulty 0
# Note that multiple difficulties are tested with category 0

conn.executescript('''INSERT INTO categories VALUES(0, "cat0");
INSERT INTO categories VALUES(1, "cat1");

INSERT INTO questions VALUES(0, "c0_d0_q0", 0, 0, 0, 0);
INSERT INTO answers VALUES(0, 0, 1, "c0_d0_q0_A0");
INSERT INTO answers VALUES(1, 0, 0, "c0_d0_q0_a1");
INSERT INTO answers VALUES(2, 0, 0, "c0_d0_q0_a2");
INSERT INTO answers VALUES(3, 0, 0, "c0_d0_q0_a3");
INSERT INTO questions VALUES(1, "c0_d0_q1", 0, 0, 0, 0);
INSERT INTO answers VALUES(4, 1, 0, "c0_d0_q1_a0");
INSERT INTO answers VALUES(5, 1, 0, "c0_d0_q1_a1");
INSERT INTO answers VALUES(6, 1, 1, "c0_d0_q1_A2");
INSERT INTO answers VALUES(7, 1, 0, "c0_d0_q1_a3");

INSERT INTO questions VALUES(2, "c0_d1_q0", 0, 0, 0, 1);
INSERT INTO answers VALUES(8,  2, 0, "c0_d1_q0_a0");
INSERT INTO answers VALUES(9,  2, 1, "c0_d1_q0_A1");
INSERT INTO answers VALUES(10, 2, 0, "c0_d1_q0_a2");
INSERT INTO answers VALUES(11, 2, 0, "c0_d1_q0_a3");
INSERT INTO questions VALUES(3, "c0_d1_q1", 0, 0, 0, 1);
INSERT INTO answers VALUES(12, 3, 0, "c0_d1_q1_a0");
INSERT INTO answers VALUES(13, 3, 0, "c0_d1_q1_a1");
INSERT INTO answers VALUES(14, 3, 1, "c0_d1_q1_A2");
INSERT INTO answers VALUES(15, 3, 0, "c0_d1_q1_a3");
INSERT INTO questions VALUES(4, "c0_d1_q2", 0, 0, 0, 1);
INSERT INTO answers VALUES(16, 4, 1, "c0_d1_q2_A0");
INSERT INTO answers VALUES(17, 4, 0, "c0_d1_q2_a1");
INSERT INTO answers VALUES(18, 4, 0, "c0_d1_q2_a2");
INSERT INTO answers VALUES(19, 4, 0, "c0_d1_q2_a3");
INSERT INTO questions VALUES(5, "c0_d1_q3", 0, 0, 0, 1);
INSERT INTO answers VALUES(20, 5, 0, "c0_d1_q3_a0");
INSERT INTO answers VALUES(21, 5, 0, "c0_d1_q3_a1");
INSERT INTO answers VALUES(22, 5, 1, "c0_d1_q3_A2");
INSERT INTO answers VALUES(23, 5, 0, "c0_d1_q3_a3");
INSERT INTO questions VALUES(6, "c0_d1_q4", 0, 0, 0, 1);
INSERT INTO answers VALUES(24, 6, 0, "c0_d1_q4_a0");
INSERT INTO answers VALUES(25, 6, 0, "c0_d1_q4_a1");
INSERT INTO answers VALUES(26, 6, 0, "c0_d1_q4_a2");
INSERT INTO answers VALUES(27, 6, 1, "c0_d1_q4_A3");

INSERT INTO questions VALUES(7, "c1_d0_q0", 0, 0, 1, 0);
INSERT INTO answers VALUES(28, 7, 0, "c1_d0_q0_a0");
INSERT INTO answers VALUES(29, 7, 0, "c1_d0_q0_a1");
INSERT INTO answers VALUES(30, 7, 0, "c1_d0_q0_a2");
INSERT INTO answers VALUES(31, 7, 1, "c1_d0_q0_A3");
INSERT INTO questions VALUES(8, "c1_d0_q1", 0, 0, 1, 0);
INSERT INTO answers VALUES(32, 8, 0, "c1_d0_q1_a0");
INSERT INTO answers VALUES(33, 8, 1, "c1_d0_q1_A1");
INSERT INTO answers VALUES(34, 8, 0, "c1_d0_q1_a2");
INSERT INTO answers VALUES(35, 8, 0, "c1_d0_q1_a3");
INSERT INTO questions VALUES(9, "c1_d0_q2", 0, 0, 1, 0);
INSERT INTO answers VALUES(36, 9, 1, "c1_d0_q2_A0");
INSERT INTO answers VALUES(37, 9, 0, "c1_d0_q2_a1");
INSERT INTO answers VALUES(38, 9, 0, "c1_d0_q2_a2");
INSERT INTO answers VALUES(39, 9, 0, "c1_d0_q2_a3");
INSERT INTO questions VALUES(10, "c1_d0_q3", 0, 0, 1, 0);
INSERT INTO answers VALUES(40, 10, 1, "c1_d0_q3_A0");
INSERT INTO answers VALUES(41, 10, 0, "c1_d0_q3_a1");
INSERT INTO answers VALUES(42, 10, 0, "c1_d0_q3_a2");
INSERT INTO answers VALUES(43, 10, 0, "c1_d0_q3_a3");
INSERT INTO questions values(11, "c1_d0_q4", 0, 0, 1, 0);
INSERT INTO answers values(44, 11, 0, "c1_d0_q4_a0");
INSERT INTO answers values(45, 11, 0, "c1_d0_q4_a1");
INSERT INTO answers values(46, 11, 1, "c1_d0_q4_A2");
INSERT INTO answers values(47, 11, 0, "c1_d0_q4_a3");
INSERT INTO questions VALUES(12, "c1_d0_q5", 0, 0, 1, 0);
INSERT INTO answers VALUES(48, 12, 0, "c1_d0_q5_a0");
INSERT INTO answers VALUES(49, 12, 1, "c1_d0_q5_A1");
INSERT INTO answers VALUES(50, 12, 0, "c1_d0_q5_a2");
INSERT INTO answers VALUES(51, 12, 0, "c1_d0_q5_a3");
INSERT INTO questions VALUES(13, "c1_d0_q6", 0, 0, 1, 0);
INSERT INTO answers VALUES(52, 13, 0, "c1_d0_q6_a0");
INSERT INTO answers VALUES(53, 13, 0, "c1_d0_q6_a1");
INSERT INTO answers VALUES(54, 13, 1, "c1_d0_q6_A2");
INSERT INTO answers VALUES(55, 13, 0, "c1_d0_q6_a3");
''')

conn.commit()
