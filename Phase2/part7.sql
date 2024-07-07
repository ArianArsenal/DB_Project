

--Function to return messages count between two users

CREATE FUNCTION count_messages_between_users(user1_id INT, user2_id INT)
RETURNS INT
BEGIN
    DECLARE message_count INT;
    
    SELECT COUNT(*) INTO message_count
    FROM Messages
    WHERE (sender_id = user1_id AND receiver_id = user2_id)
       OR (sender_id = user2_id AND receiver_id = user1_id);
    
    RETURN message_count;
END;




--Function to return the active users in the past 24 hours

CREATE FUNCTION get_recent_active_users()
RETURNS TABLE(user_id INT, name VARCHAR(50), lastname VARCHAR(50), username VARCHAR(50))
BEGIN
    RETURN (
        SELECT DISTINCT u.user_id, u.name, u.lastname, u.username
        FROM Users u
        JOIN Messages m ON u.user_id = m.sender_id OR u.user_id = m.receiver_id
        WHERE m.timestamp >= NOW() - INTERVAL 1 DAY
    );
END;




--Function to return a chat history by a given limit 

CREATE FUNCTION get_conversation_history(user1_id INT, user2_id INT, limit INT)
RETURNS TABLE(message_id INT, sender_id INT, receiver_id INT, message_text TEXT, timestamp TIMESTAMP)
BEGIN
    RETURN (
        SELECT m.message_id, m.sender_id, m.receiver_id, m.message_text, m.timestamp
        FROM Messages m
        WHERE (m.sender_id = user1_id AND m.receiver_id = user2_id)
           OR (m.sender_id = user2_id AND m.receiver_id = user1_id)
        ORDER BY m.timestamp DESC
        LIMIT limit
    );
END;





--Function to return a keyword searched for a chat

CREATE FUNCTION search_messages(keyword TEXT)
RETURNS TABLE(message_id INT, sender_id INT, receiver_id INT, message_text TEXT, timestamp TIMESTAMP)
BEGIN
    RETURN (
        SELECT m.message_id, m.sender_id, m.receiver_id, m.message_text, m.timestamp
        FROM Messages m
        WHERE m.message_text LIKE CONCAT('%', keyword, '%')
        ORDER BY m.timestamp DESC
    );
END;


