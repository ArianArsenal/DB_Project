

CREATE TABLE IF NOT EXISTS Users(
    user_id INT AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL,
    lastname VARCHAR(20),
    username VARCHAR(20) UNIQUE NOT NULL,
    phonenumber VARCHAR(20) UNIQUE, 
    password VARCHAR(20) NOT NULL,
    DateJoined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    birthdaydate DATE,
    PRIMARY KEY (user_id)
);



CREATE TABLE IF NOT EXISTS Contacts ( 
    user_id INT NOT NULL,
    contact_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (contact_id) REFERENCES Users(user_id),
    PRIMARY KEY (user_id, contact_id) --no duplicate contacts
);

--DROP TABLE Contacts


CREATE TABLE IF NOT EXISTS Chats (
    chat_id INT AUTO_INCREMENT PRIMARY KEY,
    is_group BOOLEAN NOT NULL,
    chatName VARCHAR(20) NOT NULL,
    CreatedTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS ChatMembers (
    chat_id INT NOT NULL,
    user_id INT NOT NULL,
    role BOOLEAN NOT NULL, --if 1= admin-owner  if 0==none
    PRIMARY KEY (chat_id, user_id), 
    FOREIGN KEY (chat_id) REFERENCES Chats(chat_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);


CREATE TABLE IF NOT EXISTS Messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    chat_id INT NOT NULL,
    sender_id INT NOT NULL,
    message_content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chat_id) REFERENCES Chats(chat_id),
    FOREIGN KEY (sender_id) REFERENCES Users(user_id)
);



--DROP TABLE Chats , ChatMembers , Messages




