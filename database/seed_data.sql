-- Sample data for testing and development
-- Run this after creating the schema to populate with sample records

-- Insert customers
INSERT INTO customer (name, phone, email) VALUES
('John Smith', '555-0101', 'john.smith@email.com'),
('Jane Doe', '555-0102', 'jane.doe@email.com'),
('Michael Johnson', '555-0103', 'michael.j@email.com'),
('Sarah Williams', '555-0104', 'sarah.w@email.com'),
('David Brown', '555-0105', 'david.brown@email.com'),
('Emily Davis', '555-0106', 'emily.davis@email.com'),
('Christopher Miller', '555-0107', 'chris.miller@email.com'),
('Ashley Wilson', '555-0108', 'ashley.w@email.com'),
('Matthew Moore', '555-0109', 'matt.moore@email.com'),
('Jessica Taylor', '555-0110', 'jessica.t@email.com');

-- Insert pizzas
INSERT INTO pizza (name, size, price, cost) VALUES
('Margherita', 'Small', 8.99, 3.50),
('Margherita', 'Medium', 12.99, 5.00),
('Margherita', 'Large', 15.99, 6.50),
('Pepperoni', 'Small', 9.99, 4.00),
('Pepperoni', 'Medium', 13.99, 5.50),
('Pepperoni', 'Large', 16.99, 7.00),
('Hawaiian', 'Small', 10.99, 4.50),
('Hawaiian', 'Medium', 14.99, 6.00),
('Hawaiian', 'Large', 17.99, 7.50),
('Veggie Supreme', 'Small', 10.99, 4.50),
('Veggie Supreme', 'Medium', 14.99, 6.00),
('Veggie Supreme', 'Large', 17.99, 7.50),
('Meat Lovers', 'Small', 11.99, 5.00),
('Meat Lovers', 'Medium', 15.99, 6.50),
('Meat Lovers', 'Large', 18.99, 8.00),
('BBQ Chicken', 'Small', 11.99, 5.00),
('BBQ Chicken', 'Medium', 15.99, 6.50),
('BBQ Chicken', 'Large', 18.99, 8.00);

-- Insert employees
INSERT INTO employee (fname, lname, password, username) VALUES
('Admin', 'User', 'admin123', 'admin'),
('Manager', 'Smith', 'manager123', 'manager'),
('Employee', 'Jones', 'employee123', 'employee1'),
('Staff', 'Davis', 'staff123', 'staff1');

-- Insert orders
INSERT INTO `order` (customer_id, date) VALUES
(1, '2025-01-10 12:30:00'),
(2, '2025-01-10 13:15:00'),
(3, '2025-01-10 14:00:00'),
(4, '2025-01-11 11:45:00'),
(5, '2025-01-11 12:30:00'),
(1, '2025-01-12 18:00:00'),
(6, '2025-01-12 19:15:00'),
(7, '2025-01-13 17:30:00'),
(8, '2025-01-13 18:45:00'),
(9, '2025-01-14 12:00:00');

-- Insert order details
INSERT INTO order_detail (order_id, pizza_id, quantity) VALUES
(1, 2, 2),
(1, 5, 1),
(2, 3, 1),
(2, 6, 1),
(3, 8, 2),
(4, 1, 3),
(4, 4, 2),
(5, 14, 1),
(5, 17, 1),
(6, 9, 1),
(7, 11, 2),
(7, 15, 1),
(8, 12, 1),
(9, 6, 2),
(9, 9, 1),
(10, 18, 1),
(10, 3, 1);