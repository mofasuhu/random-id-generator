import random
import csv
import sqlite3
import threading
import tkinter as tk
from tkinter import ttk

# Function to generate a random 12-digit ID
def generate_random_id():
    return int(str(random.randint(1, 9)) + ''.join([str(random.randint(0, 9)) for _ in range(11)]))

# Function to check if an ID is already in the database
def id_exists(id, cursor):
    cursor.execute('SELECT 1 FROM ids WHERE id = ?;', (id,))
    return cursor.fetchone() is not None

# Function to generate IDs and update the GUI
def generate_ids(ids_number, counter_var):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('random_ids.db')
    cursor = conn.cursor()

    # Create a table to store the IDs if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ids (
        id INTEGER PRIMARY KEY
    );
    ''')

    # Ensure indexing
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_id ON ids (id);')

    unique_ids = []

    counter = 0
    batch_size = 10000  # Adjust batch size as needed

    while counter < ids_number:
        batch_ids = []
        while len(batch_ids) < batch_size and counter < ids_number:
            N = generate_random_id()
            if (not id_exists(N, cursor)) and (N not in unique_ids):
                batch_ids.append((N,))
                unique_ids.append(N)
                counter += 1
                counter_var.set(f"Generated IDs: {counter}")
            else:
                print(f"\n{N} is present!")

        cursor.executemany('INSERT INTO ids (id) VALUES (?);', batch_ids)
        conn.commit()

    # Write the unique IDs to the CSV file
    csv_file = 'random_ids.csv'
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID'])  # Header row
        writer.writerows([[id] for id in unique_ids])

    print(f'\nGenerated {len(unique_ids)} unique 12-digit IDs and saved them in {csv_file}.')

    # Close the database connection
    conn.close()

# Function to start the ID generation in a separate thread
def start_generation():
    ids_number = int(ids_number_entry.get())
    threading.Thread(target=generate_ids, args=(ids_number, counter_var)).start()

# Setup the GUI
root = tk.Tk()
root.title("ID Generator")

frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Input field for number of IDs
ttk.Label(frame, text="Number of IDs:").grid(row=0, column=0, sticky=tk.W)
ids_number_entry = ttk.Entry(frame)
ids_number_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
ids_number_entry.insert(0, "")

# Start button
start_button = ttk.Button(frame, text="Start Generation", command=start_generation)
start_button.grid(row=1, column=0, columnspan=2, pady=10)

# Counter label
counter_var = tk.StringVar()
counter_label = ttk.Label(frame, textvariable=counter_var)
counter_label.grid(row=2, column=0, columnspan=2, pady=10)
counter_var.set("Generated IDs: 0")

root.mainloop()