
--Messages
CREATE INDEX idx_sender_id ON Messages (sender_id); --index for sender_id because we will search for messages by sender_id frequently

CREATE INDEX idx_chat_id ON Messages (chat_id); --index for chat_id because we will search for messages by chat_id frequently

CREATE INDEX idx_timestamp ON Messages (timestamp); --index for timestamp because we will search for messages by timestamp frequently



--Users

CREATE INDEX idx_username ON Users (username); --index for username because we will search for users by username frequently

CREATE INDEX idx_phonenumber ON Users (phonenumber); --index for phonenumber because we will search for users by phonenumber frequently

CREATE INDEX idx_datejoined ON Users (DateJoined); --index for DateJoined because we will search for users by DateJoined frequently

CREATE INDEX idx_birthdaydate ON Users (birthdaydate);


