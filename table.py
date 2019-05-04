import sqlite3

conn = sqlite3.connect('mydatabase.db')
print ("Opened database successfully");

conn.execute('CREATE TABLE items (id INTEGER , name TEXT , price TEXT , discription TEXT , category Text , Brand Text)')
print ("Table created successfully");
conn.close()
