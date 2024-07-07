--user access creation
CREATE USER 'Aroushe_Azad'@'localhost' IDENTIFIED BY 'Aroushe2000azad';

-- Grant SELECT privilege on all tables and views in the database to the user
GRANT SELECT ON db_project.* TO 'Aroushe_Azad'@'localhost';

--Confrim changes
FLUSH PRIVILEGES;

