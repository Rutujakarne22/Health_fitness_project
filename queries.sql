MySQL queries 
-------------------------------------------------------------------------------------------------------------------------------------
create databse health_fitness_db;
use health_fitness_db;

1) user table query: 

		CREATE TABLE user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    contact VARCHAR(20) NOT NULL );

------------------------------------------------------------------------------------------------------------------------------------

2) user_profiles table query:

		CREATE TABLE user_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    name VARCHAR(255),
    age INT,
    gender VARCHAR(10),
    height FLOAT,
    weight FLOAT,
    goal_weight FLOAT,
    CONSTRAINT unique_user_profile UNIQUE (user_id));
--------------------------------------------------------------------------------------------------------------------------------------

3) set_goals table query: 

		CREATE TABLE set_goals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    goal_type VARCHAR(50),
    target_value FLOAT,
    current_value FLOAT,
    start_date DATE,
    end_date DATE,
    CONSTRAINT unique_goal UNIQUE (user_id, goal_type),
    CHECK (start_date <= end_date));



