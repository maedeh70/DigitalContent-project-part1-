Project Overview: 

This project is designed to process and analyze HTML files stored in a specified directory, identify occurrences of a user-defined search term within the file names and their content, and store the results in a MySQL database.
The project also manages database schema updates and maintains detailed records of the search term occurrences.


Features :

Connects to a MySQL database to store results.
Automatically adds necessary columns to the database table if they do not already exist.
Recursively processes HTML files in a specified directory.
Tracks occurrences of the search term in both file names and file content.
Inserts detailed records into the database for each processed file.
Calculates and stores the total occurrences of the search term across all files.
Provides special handling for files where the search term is only found in the file name.

Requirements:

Python 3.x 
python packages library : mysql-connector-python 


Setup installation :

1. Install Python 3.x on your system.(my os was mac)
2. Install the required library
```ruby
pip install mysql-connector-python

```
3. Set up a MySQL database and create a table named "FileData" with an appropriate schema.
4. Adjust the database configuration in the script to match your MySQL setup.

Set up SQL Data Base: 
1. Create a new database (for this project that was ```DigitalProject```)
2. Create a Table (for this project that was ```FileData```)
```ruby
CREATE TABLE IF NOT EXISTS myhtml (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_path VARCHAR(255) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size INT NOT NULL,
    file_content LONGTEXT,
    term_in_file_name BOOLEAN,
    term_in_file_content BOOLEAN,
    term_occurrences INT
);
```
Finall Setup for Data Base with MySQL connection parameters:
```ruby
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'your_password',
    'database': 'DigitalProject'
}
```
Run :

1. Place your HTML files in a directory on your system.

2. Modify the ```html_files_dir``` variable in the script to point to your HTML files directory:
```ruby
html_files_dir = '/path/to/your/html_files'
```
3. Run the python code:
   ```pythonCode.py```

4. Insert your search string
5. See your results
   
Directory and File Processing:

* The script verifies the existence of the specified directory.
* It recursively processes each HTML file, reading its content and checking for the search term in both the file name and content.
* It stores detailed records in the FileData table for each processed file.
   
Future Enhancements:

* Add support for other file types.
* Implement more advanced text search algorithms.
* Improve performance for large datasets.
* 
Error Handling and Cleanup:

The script includes error handling to manage MySQL connection issues and ensures that the database connection is closed properly after processing. 

Some of Functions Used in this Project: 

```read_html_file(file_path)```

* Purpose: Reads the content of an HTML file.
* Usage: Used to read the content of each HTML file being processed.
Returns: The content of the HTML file as a string.

```insert_special_record(description)```

* Purpose: Inserts a special record into the myhtml table when the search term is found only in file names and not in the content.
* Usage: Called when a special condition is met during file processing.


```process_files(directory)```

* Purpose: Recursively processes files in the given directory and its subdirectories.
* Usage: Main function to handle file processing logic.



   
   



