USE DigitalProject;
SELECT file_name
FROM (
    SELECT file_name, 
           SUM(IF(term_in_file_name = 1 AND term_in_file_content = 0, 1, 0)) AS count_matches
    FROM FileData
    GROUP BY file_name
) AS subquery
WHERE count_matches >= 2;



