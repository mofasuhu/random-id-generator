import sqlite3

def check_duplicates(db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Query to find duplicates
    query = '''
    SELECT id, COUNT(*)
    FROM ids
    GROUP BY id
    HAVING COUNT(*) > 1;
    '''

    cursor.execute(query)
    duplicates = cursor.fetchall()

    if duplicates:
        print("Duplicate IDs found:")
        for row in duplicates:
            print(f"ID: {row[0]}, Count: {row[1]}")
    else:
        print("No duplicate IDs found.")

    # Close the database connection
    conn.close()

# Specify the database file
db_file = 'random_ids.db'
check_duplicates(db_file)
