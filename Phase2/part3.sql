


--user_message
CREATE VIEW user_message AS
SELECT 
    m.message_id,
    m.chat_id,
    m.sender_id,
    u.name AS sender_name,
    u.lastname AS sender_lastname,
    u.username AS sender_username,
    m.message_content,
    m.timestamp
FROM 
    Messages m
JOIN 
    Users u ON m.sender_id = u.user_id;



--user_contacts
CREATE VIEW user_contacts AS
SELECT 
    u1.user_id AS user_id,
    u1.name AS user_name,
    u1.lastname AS user_lastname,
    u1.username AS user_username,
    u2.user_id AS contact_id,
    u2.name AS contact_name,
    u2.lastname AS contact_lastname,
    u2.username AS contact_username
FROM 
    Contacts c
JOIN 
    Users u1 ON c.user_id = u1.user_id
JOIN 
    Users u2 ON c.contact_id = u2.user_id;



--user_message_group
CREATE VIEW user_message_group AS
SELECT 
    u.user_id,
    u.name AS user_name,
    u.lastname AS user_lastname,
    u.username AS user_username,
    c.chat_id,
    c.chatName,
    m.message_id,
    m.message_content,
    m.timestamp
FROM 
    Users u
JOIN 
    ChatMembers cm ON u.user_id = cm.user_id
JOIN 
    Chats c ON cm.chat_id = c.chat_id
JOIN 
    Messages m ON c.chat_id = m.chat_id
WHERE 
    c.is_group = 1;
