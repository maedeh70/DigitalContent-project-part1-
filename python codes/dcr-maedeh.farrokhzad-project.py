import os
import mysql.connector

# MySQL connection parameters
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'salam88@@',
    'database': 'DigitalProject'
}

try:
    # Establish connection to MySQL
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Check if the columns exist before adding them
    check_column_query = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'FileData' AND COLUMN_NAME IN ('file_names_with_search_term', 'term_only_in_file_names')"
    cursor.execute(check_column_query)
    existing_columns = cursor.fetchall()

    # Check if both columns are not already present
    if len(existing_columns) < 2:
        # ALTER TABLE statement to add new columns
        alter_table_query = """
        ALTER TABLE FileData
        ADD COLUMN file_names_with_search_term INT DEFAULT 0,
        ADD COLUMN term_only_in_file_names BOOLEAN DEFAULT FALSE
        """

        cursor.execute(alter_table_query)
        connection.commit()
        print("Columns added to the table.")
    else:
        print("Columns already exist in the table.")

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
    html_files_dir = '/Users/maedeh.farrokhzad/Desktop/my project/HTML Files'

    # Check if the directory exists
    if not os.path.isdir(html_files_dir):
        print(f"Directory {html_files_dir} does not exist.")
        exit(1)

    # Initialize variables for the different search scenarios
    file_name_matches = []
    content_matches = []

    # Function to insert a special record into the database
    def insert_special_record(description):
        special_record_query = """
        INSERT INTO FileData (full_path, file_name, file_type, file_size, file_content, 
                              term_in_file_name, term_in_file_content, term_occurrences,
                              file_names_with_search_term, term_only_in_file_names)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(special_record_query, ('', description, '', 0, '', False, False, 0, 0, True))
        connection.commit()
        print(f"Inserted special record: {description}")

    # Recursive function to process files in directory and subdirectories
    def process_files(directory):
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.html'):
                    full_path = os.path.join(root, filename)
                    print(f"Processing file: {full_path}")

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
                                          term_in_file_name, term_in_file_content, term_occurrences,
                                          file_names_with_search_term, term_only_in_file_names)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (full_path, filename, file_type, file_size, file_content, 
                                                  term_in_file_name, term_in_file_content, term_occurrences, 0, False))
                    connection.commit()
                    print(f"Inserted data for file: {filename}")

                    # Track file name matches
                    if term_in_file_name:
                        file_name_matches.append(full_path)
                        print(f"Found '{search_term}' in file name: {filename}")

                    # Track content matches
                    if term_in_file_content:
                        content_matches.append((full_path, term_occurrences))
                        print(f"Found '{search_term}' in content of file: {filename} with {term_occurrences} occurrences.")

    # Call the recursive function to process files in the directory
    process_files(html_files_dir)

    # Calculate total occurrences
    total_occurrences = sum(count for _, count in content_matches)

    # Insert total occurrences into the SQL table
    insert_total_query = """
    INSERT INTO TotalOccurrences (search_term, total_occurrences)
    VALUES (%s, %s)
    """
    cursor.execute(insert_total_query, (search_term, total_occurrences))
    connection.commit()
    print(f"Inserted total occurrences for search term '{search_term}': {total_occurrences}")

    # Additional logic: Update the count of file names with the search term and set the flag if the term is only found in file names
    if file_name_matches and content_matches:
        print(f"The term '{search_term}' matches at least one file name and is found in at least one file content.")
        for match in file_name_matches:
            print(f"Matched file name: {match}")
        for match, count in content_matches:
            print(f"Found '{search_term}' in content of file: {match} with {count} occurrences.")
        
        # Update occurrences of the search term in file content
        for match, count in content_matches:
            cursor.execute("UPDATE FileData SET term_occurrences = %s WHERE full_path = %s", (count, match))
            connection.commit()
            print(f"Updated occurrences of '{search_term}' in content of file: {match} to {count}.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed.")
