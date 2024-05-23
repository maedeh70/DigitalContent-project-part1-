import os
import mysql.connector
from tabulate import tabulate


# MySQL connection parameters
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'salam88@@',
    'database': 'DigitalProject'
}

# Attempt to connect to MySQL
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    print("Connected to MySQL database.")
    
    # Create table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS FileData (
        id INT AUTO_INCREMENT PRIMARY KEY,
        full_path VARCHAR(255),
        file_name VARCHAR(255),
        file_type VARCHAR(50),
        file_size INT,
        file_content LONGTEXT,
        term_in_file_name BOOLEAN,
        term_in_file_content BOOLEAN,
        term_occurrences INT
    )
    """
    cursor.execute(create_table_query)
    connection.commit()
    print("Table 'FileData' is ready.")
    
    # Prompt the user to input the search term
    search_term = input("Enter the search term: ")

    # Function to read HTML file content
    def read_html_file(file_path):
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ""

    # Directory containing HTML files
    html_files_dir = '//Users/maedeh.farrokhzad/Desktop/my project/HTML Files'

    # Check if the directory exists
    if not os.path.isdir(html_files_dir):
        print(f"Directory {html_files_dir} does not exist.")
        exit(1)

    # Initialize variables for the different search scenarios
    non_existing_string = True
    file_name_matches = []
    content_matches = []

    # Function to insert a special record into the database
    def insert_special_record(description):
        special_record_query = """
        INSERT INTO FileData (full_path, file_name, file_type, file_size, file_content, 
                              term_in_file_name, term_in_file_content, term_occurrences)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(special_record_query, ('', description, '', 0, '', False, False, 0))
        connection.commit()
        print(f"Inserted special record: {description}")

    # Iterate through HTML files in folders and subfolders
    for root, dirs, files in os.walk(html_files_dir):
        for filename in files:
            if filename.endswith('.html'):
                full_path = os.path.join(root, filename)
                print(f"Processing file: {filename}")

                file_content = read_html_file(full_path)
                file_size = os.path.getsize(full_path)
                file_type = 'html'

                # Check if the search term is in the file name
                term_in_file_name = search_term in filename

                # Check if the search term is in the content of the file
                term_occurrences = file_content.count(search_term)
                term_in_file_content = term_occurrences > 0

                # Insert into database
                insert_query = """
                INSERT INTO FileData (full_path, file_name, file_type, file_size, file_content, 
                                      term_in_file_name, term_in_file_content, term_occurrences)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (full_path, filename, file_type, file_size, file_content, 
                                              term_in_file_name, term_in_file_content, term_occurrences))
                connection.commit()
                print(f"Inserted data for file: {filename}")

                if term_in_file_name:
                    file_name_matches.append(full_path)
                    print(f"Found '{search_term}' in file name: {filename}")

                if term_in_file_content:
                    content_matches.append((full_path, term_occurrences))
                    non_existing_string = False
                    print(f"Found '{search_term}' in content of file: {filename} with {term_occurrences} occurrences.")

    # Feature e: Snapshot of the search for a “non existing” string
    if non_existing_string:
        print(f"No occurrences of '{search_term}' found in any file content or file name.")
        insert_special_record(f"No occurrences of '{search_term}' found in any file content or file name.")

    # Feature f: Snapshot of the search for a string matching at least two file names, but not found in any searchable file
    if len(file_name_matches) >= 2 and not content_matches:
        print(f"The term '{search_term}' matches at least two file names but is not found in any file content.")
        insert_special_record(f"The term '{search_term}' matches at least two file names but is not found in any file content.")

    # Feature g: Snapshot of the search for a string matching at least one file name and contained in at least one searchable file, with the counts of occurrences in the file(s)
    if file_name_matches and content_matches:
        print(f"The term '{search_term}' matches at least one file name and is found in at least one file content.")
        for match in file_name_matches:
            print(f"Matched file name: {match}")
        for match, count in content_matches:
            print(f"Found '{search_term}' in content of file: {match} with {count} occurrences.")

    # Feature h: Snapshot of the search for a string that does not match a file name but is found in at least one searchable file, with the counts of occurrences in the file(s)
    if not file_name_matches and content_matches:
        print(f"The term '{search_term}' does not match any file name but is found in at least one file content.")
        for match, count in content_matches:
            print(f"Found '{search_term}' in content of file: {match} with {count} occurrences.")

            

except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")
    exit(1)
finally:
    # Close MySQL connection
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed.")

# Display search results
if file_name_matches or content_matches:
    for term in [search_term]:  # Adjust if you have multiple search terms
        print(f"The term '{term}' matches at least one file name and is found in at least one file content.")
        if file_name_matches:
            print("Matched file name(s):")
            for match in file_name_matches:
                print(match)
        if content_matches:
            print(f"Found '{term}' in content of file(s):")
            for match, count in content_matches:
                print(f"{match} with {count} occurrences.")
else:
    print(f"No occurrences of '{search_term}' found in any file content or file name.")

