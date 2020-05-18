CREATE SCHEMA IF NOT EXISTS `users_db`;
CREATE TABLE IF NOT EXISTS `users_db`.`users` (
  `user_name` VARCHAR(45) NOT NULL,
  `user_password` VARCHAR(64) NOT NULL,
  `user_email` VARCHAR(45) NOT NULL,
  `user_fname` VARCHAR(45) NOT NULL,
  `user_lname` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`user_name`));