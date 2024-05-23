USE DigitalProject;
CREATE TABLE IF NOT EXISTS myhtml (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_path VARCHAR(255),
    file_type VARCHAR(50),
    file_size INT,
    content TEXT
);



