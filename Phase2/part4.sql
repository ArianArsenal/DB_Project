--a constraint to ensure that the phonenumber column in the Users table is unique
ALTER TABLE Users
ADD CONSTRAINT unique_phonenumber UNIQUE (phonenumber);



--Check Group Admin for insert
DELIMITER $$

CREATE TRIGGER check_single_group_admin
BEFORE INSERT ON ChatMembers
FOR EACH ROW
BEGIN
    IF NEW.role = 1 THEN
        DECLARE admin_count INT;
        SELECT COUNT(*)
        INTO admin_count
        FROM ChatMembers
        WHERE chat_id = NEW.chat_id AND role = 1;
        
        IF admin_count > 0 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'A group can only have one admin.';
        END IF;
    END IF;
END$$

DELIMITER ;


--Check Group Admin for update

DELIMITER $$

CREATE TRIGGER check_single_group_admin_update
BEFORE UPDATE ON ChatMembers
FOR EACH ROW
BEGIN
    IF NEW.role = 1 AND OLD.role != 1 THEN
        DECLARE admin_count INT;
        SELECT COUNT(*)
        INTO admin_count
        FROM ChatMembers
        WHERE chat_id = NEW.chat_id AND role = 1;
        
        IF admin_count > 0 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'A group can only have one admin.';
        END IF;
    END IF;
END$$

DELIMITER ;
