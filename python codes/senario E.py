import os
import mysql.connector

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

    # Prompt the user to input the search term
    search_term = input("Enter the search term: ")

    # Directory containing HTML files
    html_files_dir = '/Users/maedeh.farrokhzad/Desktop/my project/HTML Files'

    # Check if the directory exists
    if not os.path.isdir(html_files_dir):
        print(f"Directory {html_files_dir} does not exist.")
        exit(1)

    # Initialize variables for the search
    non_existing_string = True

    # Iterate through HTML files
    for filename in os.listdir(html_files_dir):
        if filename.endswith('.html'):
            full_path = os.path.join(html_files_dir, filename)
            print(f"Processing file: {filename}")

            # Read file content
            with open(full_path, 'r') as file:
                file_content = file.read()

            # Check if the search term is in the file content or file name
            if search_term in file_content or search_term in filename:
                non_existing_string = False
                break

    # Feature e: Snapshot of the search for a “non existing” string
    if non_existing_string:
        print(f"No occurrences of '{search_term}' found in any file content or file name.")
        print(f"There is not any file match with the term '{search_term}' in the files.")

except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")
    exit(1)
finally:
    # Close MySQL connection
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed.")
