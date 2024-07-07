from flask import Flask, request, jsonify, render_template
import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="ari82moh",
  database="db_project"
)

mycursor = mydb.cursor(dictionary=True)

app = Flask(__name__)



#/@ Method Groups 
#& Special Methods
#! Hazards
#Todo Uncompleted
#? Extra Wanted Scenario
#CRUD (Create,Read,Update,Delete)



#/@ User Methods

#create
@app.route('/registers', methods=['POST'])
def register_multiple():
    try:
        request_data = request.get_json()

        # Check if the request_data is a dictionary (single user) or list (multiple users)
        if isinstance(request_data, dict):
            # Convert single user dictionary to a list of one user
            request_data = [request_data]
        elif not isinstance(request_data, list):
            raise ValueError("JSON data must be a dictionary or a list of dictionaries")

        for user in request_data:
            # Parse data here
            name = user.get('name')
            lastname = user.get('lastname')
            username = user.get('username')
            phonenumber = user.get('phonenumber')
            password = user.get('password')
            birthdaydate = user.get('birthdaydate')

            if not name or not username or not password:
                return jsonify({"error": "Name, username, and password are required"}), 400

            if None in [name, lastname, username, phonenumber, password, birthdaydate]:
                raise ValueError("Missing required fields in JSON data for user: {}".format(user))

            sql = "INSERT INTO Users (name, lastname, username, phonenumber, password , birthdaydate) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (name, lastname, username, phonenumber, password, birthdaydate)

            mycursor.execute(sql, values)

        mydb.commit()
        return jsonify("Data Inserted Successfully"), 200
    except Exception as e:
        mydb.rollback()
        return jsonify({"error": str(e)}), 500

#create
@app.route('/register', methods=['POST'])
def register():
    try:
        request_data = request.get_json() #gets the data sent to the server in json format and stores it in request_data 

        #parse data here 
        name = request_data['name']
        lastname = request_data['lastname']
        username = request_data['username']
        phonenumber = request_data['phonenumber']
        password = request_data['password']
        birthdaydate = request_data['birthdaydate']

        if not name or not username or not password:
            return jsonify({"error": "Name, username, and password are required"}), 400

        
        sql = "INSERT INTO Users (name, lastname, username, phonenumber, password, birthdaydate) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (name, lastname, username, phonenumber, password,birthdaydate)

        mycursor.execute(sql, values) 
        mydb.commit()

        return jsonify("Data Inserted Succesfully") , 200
    except Exception as e:
        mydb.rollback() 
        return jsonify({"error": str(e)}) , 500 

#&login   
@app.route('/login', methods=['POST'])
def login():
    request_data = request.get_json()

    username = request_data['username']
    password = request_data['password']
    print(password)

    sql = "SELECT * FROM Users WHERE username = %s"
    values = (username,)

    mycursor.execute(sql, values)
    result = mycursor.fetchone()

    if result:
        res_password = result['password']  # Get the stored password from the result
        if res_password == password:  # Compare the stored password to the one provided by the user
            return jsonify({"message": "Login Successful", "user": result}), 200
        else:
            return jsonify({"error": "Wrong Password"}), 401
    else:
        return jsonify({"error": "Login Failed: No Data"}), 401

#read
@app.route('/read_users', methods=['GET'])
def read_users():
    try :
        mycursor.execute("SELECT * FROM Users")
        result = mycursor.fetchall()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"Empty User List": str(e)}), 500

#read
@app.route('/read_users_field', methods=['GET', 'POST'])
def read_users_input():
    try:
        request_data = request.get_json()
        field = request_data['field']
        
        
        if not field:
            return jsonify({"error": "Missing required parameters"}), 400

        # Check if the field is valid
        valid_columns = ['name', 'lastname', 'username', 'phonenumber', 'password', 'birthdaydate']
        if field not in valid_columns:
            return jsonify({"error:": "Invalid column name"}), 400
        

        sql = f"SELECT {field} FROM Users"
        mycursor.execute(sql)
        result = mycursor.fetchall()
        return jsonify(result), 200
    
    except Exception as e:
        mydb.rollback()
        return jsonify({"error": str(e)}), 500
    #

#update
@app.route('/update_user', methods=['POST'])
def update_users():
    try:
        request_data = request.get_json()
        username = request_data['username']
        field = request_data['field']
        new_value = request_data['new_value']

        
        if not username or not field or new_value is None:
            return jsonify({"error": "Missing required parameters"}), 400

        # Check if the field is valid
        valid_columns = ['name', 'lastname', 'username', 'phonenumber', 'password','birthdaydate']
        if field not in valid_columns:
            return jsonify({"error": "Invalid column name"}), 400
        
        
        sql = f"UPDATE Users SET {field} = %s WHERE username = %s"
        values = (new_value, username)

        mycursor.execute(sql, values)
        mydb.commit()

        if mycursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify("Data Updated Successfully"), 200
    
    except Exception as e:
        mydb.rollback()
        return jsonify({"error": str(e)}), 500

#delete
@app.route('/delete_user', methods=['POST'])
def delete_user():
    try:
        request_data = request.get_json()
        username = request_data['username']

        if not username:
            return jsonify({"error": "Missing required parameters"}), 400
        
        mycursor.execute("SELECT user_id FROM Users WHERE username = %s",(username,))
        user = mycursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        user_id = user['user_id']

        #first remove him from the chatmembers and delete his messages
        mycursor.execute("DELETE FROM Messages WHERE sender_id = %s",(user_id,))
        mycursor.execute("DELETE FROM ChatMembers WHERE user_id = %s",(user_id,))
      
        # Delete User
        mycursor.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
        mydb.commit()

        return jsonify("User Deleted Successfully"), 200
    
    except Exception as e:
        mydb.rollback()
        return jsonify({"error": str(e)}), 500
    




#/@ Message Methods

#create 
@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        request_data = request.get_json()

        chat_id = request_data['chat_id']
        sender_username = request_data['sender_username']
        message_content = request_data['message_content']

        mycursor.execute("SELECT user_id FROM Users WHERE username = %s",(sender_username,))
        sender_id = mycursor.fetchone()

        if not sender_id:
            return jsonify({"error":"No User Found"}) , 400

        sender_id = sender_id['user_id']

        #check null
        if not chat_id or not sender_id:
            return jsonify({"error": "Missing required parameters"}), 400
        
        # Check if chat_id exists
        mycursor.execute("SELECT chat_id FROM Chats WHERE chat_id = %s", (chat_id,))
        chat = mycursor.fetchone()
        if not chat:
            return jsonify({"error": "Invalid chat_id"}), 400
        
        sql = "INSERT INTO Messages (chat_id, sender_id, message_content) VALUES (%s, %s, %s)"
        values = (chat_id, sender_id, message_content)

        mycursor.execute(sql, values)
        mydb.commit()

        return jsonify("Message Sent Successfully"), 200
    
    except Exception as e:
        mydb.rollback()
        return jsonify({"error": str(e)}), 500
    
#read (messsages user has sent)
@app.route('/get_user_messages_sent', methods=['GET'])
def get_sent_messages():
    try:
        request_data = request.get_json()
        username = request_data['username']

        if not username:
            return jsonify({"error": "Missing required parameter: username"}), 400
        
        mycursor.execute("SELECT user_id FROM Users WHERE username = %s",(username,))
        user_id = mycursor.fetchone()

        if not user_id:
            return jsonify({"error": "User not found"}), 404
        
        user_id = user_id['user_id']

        test = """
        SELECT m.message_content , m.timestamp , m.message_id , c.chatName , c.chat_id , u.username as sender_username
        FROM Messages m 
        JOIN Users u ON m.sender_id = u.user_id 
        JOIN Chats c ON m.chat_id = c.chat_id
        WHERE u.user_id = %s;
        """
       
        mycursor.execute(test, (user_id,))
        messages = mycursor.fetchall()
        
        #test messages
        #print(messages)


        return jsonify(messages), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#read (messages sent for user)
@app.route('/get_all_chat_messages_for_user', methods=['GET'])
def get_all_chat_messages():
    try:
        request_data = request.get_json()
        username = request_data.get('username')

        if not username:
            return jsonify({"error": "Missing required parameter: username"}), 400

        # Fetch user_id from username
        mycursor.execute("SELECT user_id FROM Users WHERE username = %s", (username,))
        user = mycursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        user_id = user['user_id']

        # Fetch messages for chats the user is a member of
        test = """
        SELECT m.message_content, m.timestamp, m.message_id, c.chatName, c.chat_id, u.username as sender_username
        FROM Messages m 
        JOIN Users u ON m.sender_id = u.user_id 
        JOIN Chats c ON m.chat_id = c.chat_id
        JOIN ChatMembers cm ON cm.chat_id = c.chat_id
        WHERE cm.user_id = %s
        ORDER BY m.timestamp ASC;
        """
       
        mycursor.execute(test, (user_id,))
        messages = mycursor.fetchall()
        
        if not messages:
            return jsonify({"Message":"No Chat Found"})

        return jsonify(messages), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#read (all messages in a chat for anyone)
@app.route('/get_messages_in_a_chat', methods=['GET'])
def get_chat_messages():
    try :
        request_data = request.get_json()
        chat_id = request_data['chat_id']

        if not chat_id:
            return jsonify({"error": "Missing required parameter: chat_id"}), 400
        
        mycursor.execute("SELECT chat_id FROM Chats WHERE chat_id = %s", (chat_id,))
        check = mycursor.fetchone()
         
        if not check:
            return jsonify({"Message":"No Chat Found"})
        
        test = """
        SELECT m.message_content, m.timestamp, m.message_id, c.chatName, c.chat_id, u.username as sender_username
        FROM Messages m
        JOIN Users u ON m.sender_id = u.user_id
        JOIN Chats c ON m.chat_id = c.chat_id
        WHERE c.chat_id = %s
        ORDER BY m.timestamp ASC;
        """
       
        mycursor.execute(test, (chat_id,))
        messages = mycursor.fetchall()

        if not messages:
            return jsonify({"Message":"No Message Sent Here Yet , Be The First One !"})

        return jsonify(messages), 200


    except Exception as e:
        mydb.rollback()
        return jsonify({"error": str(e)}), 500

#update
@app.route('/edit_message', methods=['POST'])
def edit_message():
    try:
        request_data = request.get_json()
        username = request_data['username']
        chat_id = request_data['chat_id']
        message_id = request_data['message_id']
        new_message = request_data['new_message']

        if not username or not chat_id or not message_id or not new_message:
            return jsonify({"error": "Missing required parameters"}), 400
        
        mycursor.execute("SELECT user_id FROM Users WHERE username = %s", (username,))
        user = mycursor.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404
        user_id = user['user_id']

        mycursor.execute("SELECT chat_id FROM Chats WHERE chat_id = %s", (chat_id,))
        chat_check = mycursor.fetchone()

        if not chat_check:
            return jsonify({"error":"Chat ID Does Not Exists!"}), 404
        
        #check if member is part of the given chat
        mycursor.execute("SELECT user_id FROM ChatMembers WHERE chat_id = %s AND user_id = %s",(chat_id, user_id,))
        member_check = mycursor.fetchone()

        if not member_check:
            return jsonify({"error":"You are not a member of this chat"}), 400
        
        #check if message exists
        mycursor.execute("SELECT message_id FROM Messages WHERE message_id = %s AND chat_id = %s", (message_id,chat_id,))
        message_check = mycursor.fetchone()

        if not message_check:
            return jsonify({"error":"Message Does Not Exists in the Chat!"}), 404
        
        #if the member has permission to edit (role 1 and its his message)
        mycursor.execute("SELECT sender_id FROM Messages WHERE message_id = %s", (message_id,))
        sender_id = mycursor.fetchone()
        sender_id = sender_id['sender_id']

        if sender_id != user_id:
            return jsonify({"error":"You are not the sender of this message"}), 403
        
        #update message
        mycursor.execute("UPDATE Messages SET message_content = %s WHERE message_id = %s", (new_message, message_id,))
        mydb.commit()

        return jsonify("Message Updated Successfully"), 200

    except Exception as e:
        mydb.rollback()
        return jsonify({"error": str(e)}), 500

#delete
@app.route('/delete_message', methods=['GET'])
def delete_message():
    try:
        request_data = request.get_json()
        username = request_data['username']
        chat_id = request_data['chat_id']
        message_id = request_data['message_id']

        if not username or not chat_id or not message_id:
            return jsonify({"error": "Missing required parameters"}), 400
        
        mycursor.execute("SELECT user_id FROM Users WHERE username = %s", (username,))
        user = mycursor.fetchone()
        if not user:
            return jsonify({"error": "User not found"}), 404
        user_id = user['user_id']

        mycursor.execute("SELECT chat_id FROM Chats WHERE chat_id = %s", (chat_id,))
        chat_check = mycursor.fetchone()
        if not chat_check:
            return jsonify({"error":"Chat ID Does Not Exists!"}), 404
        
        #check if member is part of the given chat
        mycursor.execute("SELECT role FROM ChatMembers WHERE chat_id = %s AND user_id = %s",(chat_id, user_id,))
        member_check = mycursor.fetchone()

        if not member_check:
            return jsonify({"error":"You are not a member of this chat"}), 400
        
        user_role = member_check['role']
        
        #check if message exists
        mycursor.execute("SELECT message_id,sender_id FROM Messages WHERE message_id = %s AND chat_id = %s", (message_id,chat_id,))
        message_check = mycursor.fetchone()

        if not message_check:
            return jsonify({"error":"Message Does Not Exists in the Chat!"}), 404
        
        message_sender_id = message_check['sender_id']

        if user_role == 1 or user_id == message_sender_id:
            # User has permission to delete the message
            mycursor.execute("DELETE FROM Messages WHERE message_id = %s", (message_id,))
            mydb.commit()  # Commit the transaction to save the changes
            return jsonify("Message deleted successfully"), 200
        else:
            return jsonify({"error": "You do not have permission to delete this message"}), 403

    except Exception as e:
        mydb.rollback()
        return jsonify({"error": str(e)}), 500






#/@ Chat Methods

#create
@app.route('/create_gp', methods=['POST'])
def create_gp():
    try:
        request_data = request.get_json()

        chatName = request_data['chatName']
        owner = request_data['username']

        if not owner or not chatName:
            return jsonify({"error": "Missing required parameters"}), 400

        mycursor.execute("SELECT user_id FROM Users WHERE username = %s",(owner,))
        owner_id = mycursor.fetchone()
        owner_id = owner_id['user_id']

        if not owner_id:
            return jsonify({"error":"User Doesn't Exist"})

    
        # create gp
        mycursor.execute("INSERT INTO Chats (is_group, chatName) VALUES (%s, %s)",(1, chatName,))
        mydb.commit()


        mycursor.execute("SELECT LAST_INSERT_ID()")
        get_chat_id = mycursor.fetchone()
        get_chat_id = get_chat_id['LAST_INSERT_ID()']

        
        #add admin to the chat members
        mycursor.execute("INSERT INTO ChatMembers(chat_id, user_id , role) VALUES  (%s, %s, %s)", (get_chat_id , owner_id , 1,))
        mydb.commit()

        return jsonify("Chat Created Successfully"), 200
    
    except Exception as e:
        mydb.rollback()
        return jsonify({"error": str(e)}), 500

#create
@app.route('/create_pv', methods=['POST'])
def create_pv():

    try :
        request_data = request.get_json()

        First_username = request_data['First_username']
        Second_username = request_data['Second_username']

        if not First_username or not Second_username:
            return jsonify({"error": "Missing required parameters"}), 400

        #get first user id
        test1 = "SELECT user_id FROM Users WHERE username = %s"
        values = (First_username,)
        mycursor.execute(test1, values)
        user_id_1 = mycursor.fetchone()

        #get second user id
        test2 = "SELECT user_id FROM Users WHERE username = %s"
        values1 = (Second_username,)
        mycursor.execute(test2, values1)
        user_id_2 = mycursor.fetchone()

        user_id_1 = user_id_1['user_id']
        user_id_2 = user_id_2['user_id']

        if not user_id_1 or not user_id_2:
            return jsonify({"error": "User not found"}), 404
        
        

        #test to see users id
        #print(user_id_1)
        #print(user_id_2)

        # Check for existing private chat
        check_chat_query = """
            SELECT c.chat_id
            FROM ChatMembers cm
            JOIN Chats c ON cm.chat_id = c.chat_id
            WHERE c.is_group = 0 AND
            (cm.user_id = %s OR cm.user_id = %s)
            GROUP BY c.chat_id
            HAVING COUNT(DISTINCT cm.user_id) = 2
        """
        mycursor.execute(check_chat_query, (user_id_1, user_id_2))
        existing_chat = mycursor.fetchone()

        if existing_chat:
            return jsonify({"error": "Private chat between these users already exists"}), 400

        
        sql_query_toGetSecondName = "SELECT name FROM Users WHERE username = %s"
        values = (Second_username,)
        mycursor.execute(sql_query_toGetSecondName, values)
        resultname = mycursor.fetchone()

        get_Second_name = resultname['name']

        sql_query_toGetFirstName = "SELECT name FROM Users WHERE username = %s"
        values = (First_username,)
        mycursor.execute(sql_query_toGetFirstName, values)
        resultname = mycursor.fetchone()

        get_First_Name = resultname['name']

        #test to see second name
        # print(get_Second_name)
        # print(type(get_Second_name))

    
        # Create a pv Chat
        sql = "INSERT INTO Chats (is_group, chatName) VALUES (%s, %s)"
        values = (0, get_Second_name + " and " + get_First_Name)
        mycursor.execute(sql, values)
        mydb.commit()

    

        #get the created chat_id
        mycursor.execute("SELECT LAST_INSERT_ID()")
        get_chat_id = mycursor.fetchone()
        get_chat_id = get_chat_id['LAST_INSERT_ID()']
        

        sql_addUsersToChatMembers1 = "INSERT INTO ChatMembers (chat_id, user_id, role) VALUES (%s, %s, %s)"
        values = (get_chat_id, user_id_1, 1) # Both users are owner and can edit or delete
        mycursor.execute(sql_addUsersToChatMembers1, values)
        mydb.commit()

        #print(values)

        sql_addUsersToChatMembers2 = "INSERT INTO ChatMembers (chat_id, user_id, role) VALUES (%s, %s, %s)"
        values = (get_chat_id, user_id_2, 1) # Both users are owner and can edit or delete
        mycursor.execute(sql_addUsersToChatMembers2, values)
        mydb.commit()

        #print(values)


        

        return jsonify({"message":"Chat Created Successfully","Chat_id":get_chat_id}), 200
    
    except Exception as e:
        mydb.rollback()
        return jsonify({"error": str(e)}), 500

#&add user to chat
@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        request_data = request.get_json()
        owner_username = request_data['username']
        chat_id = request_data['chat_id']
        adding_username = request_data['adding_username']

        if not owner_username or not chat_id or not adding_username:
            return jsonify({"error": "Missing required parameter: username"}), 400
        
        #getting owner_id from owner_username
        mycursor.execute("SELECT user_id FROM Users WHERE username = %s", (owner_username,))
        owner = mycursor.fetchone()
        if not owner:
            return jsonify({"error": "Owner not found"}), 404
        owner_id = owner['user_id']

        
        # Check 1- if Chat exists 2- and is a gp 3- and the sent owner is in it 4- and its admin 
        mycursor.execute("""
        SELECT c.chat_id  
        FROM Chats c 
        JOIN ChatMembers cm ON c.chat_id = cm.chat_id 
        WHERE cm.chat_id = %s AND c.is_group = 1 AND cm.user_id = %s AND cm.role = 1;
        """, (chat_id, owner_id,))
    
        chat = mycursor.fetchone()
        if not chat :
            return jsonify({"error": "Chat not found or you do not have admin rights"}), 404
        chat_id = chat['chat_id']
    
        # getting adding_id from adding_username
        mycursor.execute("SELECT user_id FROM Users WHERE username = %s", (adding_username,))
        adding = mycursor.fetchone()
        if not adding:
            return jsonify({"error": "User not found"}), 404
        adding_id = adding['user_id']

        
    
        # Check if the user is already in the chat
        mycursor.execute("SELECT user_id FROM ChatMembers WHERE chat_id = %s AND user_id = %s", (chat_id, adding_id))
        existing_user = mycursor.fetchone()
        if existing_user:
            return jsonify({"error": "User is already in the chat"}), 400
    
        
        # Add user to chat
        mycursor.execute("INSERT INTO ChatMembers (chat_id, user_id, role) VALUES (%s, %s, %s)", (chat_id, adding_id, 0))
        mydb.commit()

        return jsonify({"message":"User Added Successfully","chat_id":chat_id,"added_user_id":adding_id}), 200
    
    except Exception as e:
        mydb.rollback()
        return jsonify({"error": str(e)}), 500
    
#read (all chat members in a chat)
@app.route('/get_chat_members', methods=['GET'])
def read_chat_members():
    try:
        request_data = request.get_json()
        chat_id = request_data['chat_id']

        if not chat_id:
            return jsonify({"error": "Missing required parameter: chat_id"}), 400
        
        mycursor.execute("SELECT chat_id FROM Chats WHERE chat_id = %s", (chat_id,))
        chat_check = mycursor.fetchone()
        if not chat_check:
            return jsonify({"error":"Chat Does Not Exists!"}), 404
        
        mycursor.execute("SELECT u.* , cm.role FROM Users u JOIN ChatMembers cm ON u.user_id = cm.user_id WHERE cm.chat_id = %s", (chat_id,))
        users = mycursor.fetchall()

        return jsonify(users)


    except Exception as e:
        mydb.rollback()
        return jsonify({"error": str(e)}), 500    

#delete chat  option = 1 delete for others (only work in pv chats )  option 0 = delete for me (for gp and pv chats)
@app.route('/delete_chat')
def delete_chat():
    try :
        request_data = request.get_json()
        username = request_data['username']
        chat_id = request_data['chat_id']
        option = request_data['option']
        option = int(option)

        if not username or not chat_id or option is None:
            return jsonify({"error": "Missing required parameter: chat_id"}), 400
        
        mycursor.execute("SELECT user_id FROM Users WHERE username = %s", (username,))
        user = mycursor.fetchone()

        if not user:
            return jsonify({"error":"User Does Not Exists!"}), 404

        user_id = user['user_id']

        mycursor.execute("SELECT * FROM Chats WHERE chat_id = %s", (chat_id,))
        chat_check = mycursor.fetchone()
        if not chat_check:
            return jsonify({"error":"Chat Does Not Exists!"}), 404
        
        #check if member is part of the given chat
        mycursor.execute("SELECT * FROM ChatMembers WHERE chat_id = %s AND user_id = %s",(chat_id, user_id,))
        member_check = mycursor.fetchone()

        if not member_check:
            return jsonify({"error":"You are not a member of this chat"}), 400
        
        #!
        if option == 1: #delete for both (pv only)
            if chat_check['is_group'] == 0:
                # Delete messages in the chat
                mycursor.execute("DELETE FROM Messages WHERE chat_id = %s", (chat_id,))
                mydb.commit()

                # Delete chat members
                mycursor.execute("DELETE FROM ChatMembers WHERE chat_id = %s", (chat_id,))
                mydb.commit()

                # Finally, delete the chat
                mycursor.execute("DELETE FROM Chats WHERE chat_id = %s", (chat_id,))
                mydb.commit()

                return jsonify({"message": "Chat deleted for everyone Successfully"}), 200
            else:
                return jsonify({"error": "Option 1 is only available for private chats"}), 400
    
        elif option == 0:#delete for me (pv or gp)

            mycursor.execute("DELETE FROM ChatMembers WHERE chat_id = %s AND user_id = %s ", (chat_id,user_id,))
            mydb.commit()

            return jsonify({"message":f"Left Chat :{chat_id} Successfully"}), 200
        else:
            return jsonify({"error": "Invalid option"}), 400
    
    except Exception as e:
        mydb.rollback()
        return jsonify({"error": str(e)}), 500  




#/@ Contact Methods

#create
@app.route('/add_contact', methods=['POST'])
def add_contact():
    try:
        request_data = request.get_json()
        first_username = request_data['username']
        second_username = request_data['adding_username']

        if not first_username or not second_username:
            return jsonify({"error": "Missing required parameter: username"}), 400
        
        mycursor.execute("SELECT user_id FROM Users WHERE username = %s", (first_username,))
        first_user = mycursor.fetchone()

        if not first_user:
            return jsonify({"error": "User Does not Exists"}), 400
        
        first_user_id = first_user['user_id']

        if second_username == first_username:
            return jsonify({"error": "You can't add yourself as a contact"}), 400
        
        mycursor.execute("SELECT user_id FROM Users WHERE username = %s", (second_username,))
        second_user = mycursor.fetchone()

        if not second_user:
            return jsonify({"error": "User Does not Exists"}), 400

        second_user_id = second_user['user_id']


        mycursor.execute("INSERT INTO Contacts(user_id , contact_id) VALUES(%s, %s)",(first_user_id, second_user_id) )
        mydb.commit()


        return jsonify("Contact Added Successfully"), 200
    except Exception as e:
        mydb.rollback()
        return jsonify({"error": str(e)}), 500

#read
@app.route('/get_contacts', methods=['GET'])
def get_contacts():
    try :
        request_data = request.get_json()
        username = request_data['username']

        if not username :
            return jsonify({"error": "Missing required parameter: username"}), 400

        mycursor.execute("SELECT user_id FROM Users WHERE username = %s",(username,))
        user_id = mycursor.fetchone()

        if not user_id:
            return jsonify({"error": "No User Found"}), 400
        
        user_id = user_id['user_id']
        

        mycursor.execute("""
                         
        SELECT u.name , u.lastname , u.username , u.user_id , u.DateJoined , u.phonenumber 
        FROM Users u JOIN Contacts c ON u.user_id = c.contact_id 
        WHERE c.user_id = %s
        """,(user_id,))

        result = mycursor.fetchall()

        if not result:
            return jsonify({"message":"No Contact Found"}) 

        return jsonify(result)
        

    
    except Exception as e:
        mydb.rollback()
        return jsonify({"error": str(e)}), 500

#delete
@app.route('/delete_contact', methods=['GET'])
def delete_contact():
    try:
        request_data = request.get_json()
        first_username = request_data['username']
        second_username = request_data['removing_username']
    
        if not first_username or not second_username:
            return jsonify({"error": "Missing required parameter: username"}), 400
        
        mycursor.execute("SELECT user_id FROM Users WHERE username = %s", (first_username,))
        first_user = mycursor.fetchone()

        if not first_user:
            return jsonify({"error": "User Does not Exists"}), 400
        
        first_user_id = first_user['user_id']

        mycursor.execute("SELECT user_id FROM Users WHERE username = %s", (second_username,))
        second_user = mycursor.fetchone()

        if not second_user:
            return jsonify({"error": "User Does not Exists"}), 400

        second_user_id = second_user['user_id']

        mycursor.execute("DELETE FROM Contacts WHERE user_id = %s AND contact_id = %s",(first_user_id, second_user_id) )
        mydb.commit()


        return jsonify("Contact Removed Successfully"), 200

    except Exception as e:
        mydb.rollback()
        return jsonify({"error": str(e)}), 500



#?Extra Scenario

@app.route('/delete_if_no_gp',methods=['GET'])
def delete_no_gp():
    try:
        
        mycursor.execute("SELECT user_id FROM Users")
        users = mycursor.fetchall()
        
        # iterate over each user and check if they are part of any chat
        for user in users:
            user_id = user['user_id']
            
            mycursor.execute("SELECT * FROM ChatMembers WHERE user_id = %s", (user_id,))
            chat_membership = mycursor.fetchall()
            
            if not chat_membership:
                

                #first check for any refernce in contacts table and delete them
                mycursor.execute("DELETE FROM Contacts WHERE user_id = %s OR contact_id = %s", (user_id, user_id))
                mydb.commit()

                mycursor.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
                mydb.commit()
                
        return jsonify({"message": "Users who are not part of any chat have been deleted"}), 200

    except Exception as e:
        mydb.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/full_info_which_chats',methods=['GET'])
def full_info_which_chats():
    try:
        sql = """
        SELECT 
            u.user_id, u.name, u.lastname, u.username, u.phonenumber, u.password, u.DateJoined, u.birthdaydate,
            c.chat_id, c.chatName, c.is_group, c.CreatedTimestamp
        FROM 
            Users u
        JOIN 
            ChatMembers cm ON u.user_id = cm.user_id
        JOIN 
            Chats c ON cm.chat_id = c.chat_id
        ORDER BY 
            u.user_id, c.chat_id;
        """

        mycursor.execute(sql)
        result = mycursor.fetchall()
        return jsonify(result)
    
    except Exception as e:
        mydb.rollback()
        return jsonify({"error": str(e)}), 500
    
@app.route('/message_sent_in_chat_ordered', methods=['GET'])
def message_sent_in_chat_ordered():
    try:
        request_data = request.get_json()
        chat_id = request_data.get('chat_id')

        if not chat_id:
            return jsonify({"error": "Missing required parameter: chat_id"}), 400

        sql = """
        SELECT 
            u.user_id, u.name, u.lastname, u.username, u.phonenumber, u.password, u.DateJoined, u.birthdaydate,
            COUNT(m.message_id) AS message_count
        FROM 
            Users u
        JOIN 
            ChatMembers cm ON u.user_id = cm.user_id
        JOIN 
            Messages m ON u.user_id = m.sender_id
        WHERE 
            cm.chat_id = %s AND m.chat_id = %s
        GROUP BY 
            u.user_id
        ORDER BY 
            message_count DESC;
        """

        mycursor.execute(sql, (chat_id, chat_id))
        result = mycursor.fetchall()
        return jsonify(result)
    
    except Exception as e:
        mydb.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/gp_with_pv_chat_count_of_users', methods=['GET'])
def gp_with_pv_chat_count_of_users():
    try:
        sql = """
        SELECT 
            c.chat_id,
            c.chatName,
            c.is_group,
            c.CreatedTimestamp,
            COUNT(DISTINCT CONCAT(pv_pairs.user1_id, '-', pv_pairs.user2_id)) AS pv_chat_pairs_count
        FROM 
            Chats c
        JOIN 
            ChatMembers cm1 ON c.chat_id = cm1.chat_id
        JOIN 
            ChatMembers cm2 ON c.chat_id = cm2.chat_id
        JOIN (
            SELECT 
                cm1.user_id AS user1_id,
                cm2.user_id AS user2_id,
                cm1.chat_id
            FROM 
                ChatMembers cm1
            JOIN 
                ChatMembers cm2 ON cm1.chat_id = cm2.chat_id
            JOIN 
                Chats c ON c.chat_id = cm1.chat_id
            WHERE 
                c.is_group = 0
                AND cm1.user_id < cm2.user_id
        ) AS pv_pairs ON cm1.user_id = pv_pairs.user1_id AND cm2.user_id = pv_pairs.user2_id
        WHERE 
            c.is_group = 1
        GROUP BY 
            c.chat_id, c.chatName, c.is_group, c.CreatedTimestamp;
        """

        mycursor.execute(sql)
        result = mycursor.fetchall()
        return jsonify(result)
    
    except Exception as e:
        mydb.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/same_date_joined_sent_over_2_ms',methods=['GET'])
def same_date_joined_sent_over_2_ms():
    try:
        sql = """
        SELECT 
    u.user_id,
    u.name,
    u.lastname,
    u.username,
    u.phonenumber,
    u.DateJoined,
    u.birthdaydate
FROM 
    Users u
JOIN 
    (
        SELECT 
            m.sender_id,
            COUNT(DISTINCT m.chat_id) AS groups_count
        FROM 
            Messages m
        JOIN 
            Chats c ON m.chat_id = c.chat_id
        WHERE 
            c.is_group = 1
        GROUP BY 
            m.sender_id
        HAVING 
            COUNT(DISTINCT m.chat_id) >= 2 
            AND COUNT(m.message_id) > 1
    ) msg_counts ON u.user_id = msg_counts.sender_id
WHERE 
    DATE(u.DateJoined) = (
        SELECT 
            DATE(u1.DateJoined)
        FROM 
            Users u1
        WHERE 
            u1.user_id = u.user_id
    );

        """

        mycursor.execute(sql)
        result = mycursor.fetchall()
        return jsonify(result)
    
    except Exception as e:
        mydb.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/users_who_share_gp_with_user',methods=['GET'])
def users_who_share_gp_with_user():
    try:

        request_data = request.get_json()
        username = request_data['username']

        sql = """
        SELECT DISTINCT
            u.user_id,
            u.name,
            u.lastname,
            u.username,
            u.phonenumber,
            u.DateJoined,
            u.birthdaydate
        FROM
            Users u
        JOIN
            ChatMembers cm1 ON u.user_id = cm1.user_id
        JOIN
            (
                SELECT
                    cm2.chat_id
                FROM
                    Users u2
                JOIN
                    ChatMembers cm2 ON u2.user_id = cm2.user_id
                JOIN
                    Chats c ON cm2.chat_id = c.chat_id
                WHERE
                    u2.username = %s
                    AND c.is_group = 1
            ) shared_chats ON cm1.chat_id = shared_chats.chat_id
        WHERE
            u.username != %s;
        """

        mycursor.execute(sql, (username, username))
        result = mycursor.fetchall()
        return jsonify(result)
    
    except Exception as e:
        mydb.rollback()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

    