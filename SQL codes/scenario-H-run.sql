USE DigitalProject;
SELECT * FROM FileData 
WHERE term_in_file_name = 0 
AND term_in_file_content = 1 
AND file_content LIKE '%apple%';






