--Log table for user table
CREATE TABLE users_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    log_action VARCHAR(10),
    old_name VARCHAR(20),
    old_lastname VARCHAR(20),
    old_username VARCHAR(20),
    old_phonenumber VARCHAR(20),
    old_password VARCHAR(20),
    old_DateJoined TIMESTAMP,
    old_birthdaydate DATE,
    new_name VARCHAR(20),
    new_lastname VARCHAR(20),
    new_username VARCHAR(20),
    new_phonenumber VARCHAR(20),
    new_password VARCHAR(20),
    new_DateJoined TIMESTAMP,
    new_birthdaydate DATE,
    change_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


--Insert log
DELIMITER $$

CREATE TRIGGER after_users_insert
AFTER INSERT ON users
FOR EACH ROW
BEGIN
    INSERT INTO users_log (user_id, log_action, new_name, new_lastname, new_username, new_phonenumber, new_password, new_DateJoined, new_birthdaydate)
    VALUES (NEW.user_id, 'INSERT', NEW.name, NEW.lastname, NEW.username, NEW.phonenumber, NEW.password, NEW.DateJoined, NEW.birthdaydate);
END$$

DELIMITER ;


--Update log
DELIMITER $$

CREATE TRIGGER after_users_update
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    INSERT INTO users_log (user_id, log_action, old_name, old_lastname, old_username, old_phonenumber, old_password, old_DateJoined, old_birthdaydate, new_name, new_lastname, new_username, new_phonenumber, new_password, new_DateJoined, new_birthdaydate)
    VALUES (OLD.user_id, 'UPDATE', OLD.name, OLD.lastname, OLD.username, OLD.phonenumber, OLD.password, OLD.DateJoined, OLD.birthdaydate, NEW.name, NEW.lastname, NEW.username, NEW.phonenumber, NEW.password, NEW.DateJoined, NEW.birthdaydate);
END$$

DELIMITER ;



--Delete log
DELIMITER $$

CREATE TRIGGER after_users_delete
AFTER DELETE ON users
FOR EACH ROW
BEGIN
    INSERT INTO users_log (user_id, log_action, old_name, old_lastname, old_username, old_phonenumber, old_password, old_DateJoined, old_birthdaydate)
    VALUES (OLD.user_id, 'DELETE', OLD.name, OLD.lastname, OLD.username, OLD.phonenumber, OLD.password, OLD.DateJoined, OLD.birthdaydate);
END$$

DELIMITER ;
