import mysql.connector


mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="ari82moh",
  database="db_project"
)

mycursor = mydb.cursor(dictionary=True)
#mycursor = mydb.cursor()   #!TypeError: tuple indices must be integers or slices, not str


#mycursor.execute("SHOW DATABASES")



# mycursor.execute("""CREATE TABLE IF NOT EXISTS Users(
#     user_id INT AUTO_INCREMENT,
#     name VARCHAR(20) NOT NULL,
#     lastname VARCHAR(20),
#     username VARCHAR(20) UNIQUE NOT NULL,
#     phonenumber VARCHAR(20) UNIQUE, 
#     password VARCHAR(20) NOT NULL,
#     DateJoined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     PRIMARY KEY (user_id)
# );
# """)


# mycursor.execute("SELECT LAST_INSERT_ID()")
# get_chat_id = mycursor.fetchone()
# print(get_chat_id)
# get_chat_id = get_chat_id['LAST_INSERT_ID()']
# print(get_chat_id)


mycursor.execute("ALTER TABLE Users ADD birthdaydate DATE;")
        


# mycursor.execute("SHOW DATABASES")

# database_list = mycursor.fetchall()

# for x in database_list:
#     print(x)


# mycursor.execute("SHOW TABLES")

# table_list = mycursor.fetchall()

# for x in table_list:
#     print(x)




# mycursor.execute("SELECT * FROM users")

# myresult = mycursor.fetchall()

# for x in myresult:

#   print(x)

# mycursor.execute("SELECT * FROM messages")

# myresult = mycursor.fetchall()

# for x in myresult:

#   print(x)