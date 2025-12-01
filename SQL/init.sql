CREATE SCHEMA IF NOT EXISTS sales;

CREATE TABLE IF NOT EXISTS sales.employee (
  id BIGSERIAL NOT NULL PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  gender VARCHAR(6) NOT NULL,
  email VARCHAR(150),
  date_of_birth DATE
);

CREATE TABLE IF NOT EXISTS sales.product (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    employee_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    count INTEGER NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    total_sum NUMERIC(12, 2) GENERATED ALWAYS AS (count * price) STORED,

    CONSTRAINT fk_product_employee
        FOREIGN KEY (employee_id)
        REFERENCES sales.employee(id)
        ON DELETE CASCADE
);

INSERT INTO sales.employee (first_name, last_name, gender, email, date_of_birth) VALUES
  ('Irina','Lihoglyad','Female','testLiho@test.com','1999-05-22'),
  ('Mikola','Tverdohlib','Male','testHlib@test.com','1982-03-27'),
  ('Ivan','Bogun','Male','test@test.com','1985-11-07'),
  ('Petro','Tverdohlib','Male','testHlib@test.com','1975-01-17');

INSERT INTO sales.product (employee_id, name, count, price)
VALUES 
(1, 'Laptop', 2, 999.99),
(2, 'box', 2, 3.99);