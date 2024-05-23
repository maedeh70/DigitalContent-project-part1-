USE DigitalProject;
SELECT * FROM FileData 
WHERE term_in_file_name = 1
AND term_in_file_content = 0
AND file_name LIKE '%iran%';






