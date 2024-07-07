
--هر کاربر با اطلاعات کامل در چه گروه هایی عضو است
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



--کاربران یک گروه با اطلاعات کامل به ترتیب تعداد پیام های ارسال شده در آن گروه

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
    cm.chat_id = %s  AND m.chat_id = %s
GROUP BY 
    u.user_id
ORDER BY 
    message_count DESC;


--هر گروه (با اطلاعات کامل) چه تعداد کاربر دارد که با یکدیگر چت خصوصی دارند

SELECT 
    c.chat_id,
    c.chatName,
    c.is_group,
    c.CreatedTimestamp,
    COUNT(DISTINCT pv_pairs.user1_id, pv_pairs.user2_id) AS pv_chat_pairs_count
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



--کاربر هایی که در یک روز به خصوص وارد پیامرسان ما شده اند و داخل حذاقل 2 گروه بیشتر از یک پیام ارسال کرده اند

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

--کاربرانی (با اطلاعات کامل) که در یک یا چند گروه با یک کاربر خاص مشترک هستند

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