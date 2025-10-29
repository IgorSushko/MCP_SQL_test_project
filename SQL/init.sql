CREATE SCHEMA IF NOT EXISTS sales;

CREATE TABLE IF NOT EXISTS sales.employee (
  id BIGSERIAL NOT NULL PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  gender VARCHAR(6) NOT NULL,
  email VARCHAR(150),
  date_of_birth DATE
);

INSERT INTO sales.employee (first_name, last_name, gender, email, date_of_birth) VALUES
  ('Irina','Lihoglyad','Female','testLiho@test.com','1999-05-22'),
  ('Mikola','Tverdohlib','Male','testHlib@test.com','1982-03-27'),
  ('Ivan','Bogun','Male','test@test.com','1985-11-07'),
  ('Petro','Tverdohlib','Male','testHlib@test.com','1975-01-17');
