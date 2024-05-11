import sqlite3
import tkinter as tk
from tkinter import messagebox

conn = sqlite3.connect('voting.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS candidates (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    votes INTEGER DEFAULT 0
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS votes (
                    id INTEGER PRIMARY KEY,
                    candidate_id INTEGER,
                    voter_id INTEGER,
                    FOREIGN KEY (candidate_id) REFERENCES candidates(id)
                )''')

def add_candidate(name):
    # Check if the candidate name already exists
    cursor.execute("SELECT id FROM candidates WHERE name = ?", (name,))
    existing_candidate = cursor.fetchone()
    if existing_candidate:
        messagebox.showerror("Error", "Candidate with this name already exists!")
        return
    # If the candidate name doesn't exist, add it to the database
    cursor.execute("INSERT INTO candidates (name) VALUES (?)", (name,))
    conn.commit()
    messagebox.showinfo("Success", "Candidate added successfully!")
    refresh_candidates()

def delete_candidate(candidate_id):
    cursor.execute("DELETE FROM candidates WHERE id = ?", (candidate_id,))
    conn.commit()
    messagebox.showinfo("Success", "Candidate deleted successfully!")
    refresh_candidates()

def update_candidate(candidate_id, new_name):
    cursor.execute("UPDATE candidates SET name = ? WHERE id = ?", (new_name, candidate_id))
    conn.commit()
    messagebox.showinfo("Success", "Candidate updated successfully!")
    refresh_candidates()

def vote(candidate_id):
    cursor.execute("INSERT INTO votes (candidate_id) VALUES (?)", (candidate_id,))
    cursor.execute("UPDATE candidates SET votes = votes + 1 WHERE id = ?", (candidate_id,))
    conn.commit()
    messagebox.showinfo("Success", "Vote casted successfully!")
    refresh_candidates()

def get_candidates():
    cursor.execute("SELECT * FROM candidates")
    return cursor.fetchall()

def get_total_votes(candidate_id):
    cursor.execute("SELECT votes FROM candidates WHERE id = ?", (candidate_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None

def view_candidates():
    candidates_window = tk.Toplevel(root)
    candidates_window.title("Candidates")

    candidates = get_candidates()
    if candidates:
        for candidate in candidates:
            candidate_frame = tk.Frame(candidates_window)
            candidate_frame.pack(padx=10, pady=5)

            label = tk.Label(candidate_frame, text=candidate[1])
            label.pack(side=tk.LEFT)

            vote_button = tk.Button(candidate_frame, text="Vote", command=lambda c_id=candidate[0]: vote(c_id))
            vote_button.pack(side=tk.RIGHT, padx=5)

    else:
        label = tk.Label(candidates_window, text="No candidates available.")
        label.pack(padx=10, pady=10)

def refresh_candidates():
    candidates_list.delete(0, tk.END)
    for candidate in get_candidates():
        candidates_list.insert(tk.END, f"{candidate[1]} - Votes: {candidate[2]}")

root = tk.Tk()
root.title("Voting Management System")

candidate_label = tk.Label(root, text="Candidate Name:")
candidate_label.grid(row=0, column=0, padx=5, pady=5)

candidate_entry = tk.Entry(root)
candidate_entry.grid(row=0, column=1, padx=5, pady=5)

add_candidate_button = tk.Button(root, text="Add Candidate", command=lambda: add_candidate(candidate_entry.get()))
add_candidate_button.grid(row=0, column=2, padx=5, pady=5)

candidates_list = tk.Listbox(root)
candidates_list.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

delete_candidate_button = tk.Button(root, text="Delete Candidate", command=lambda: delete_candidate(get_candidates()[candidates_list.curselection()[0]][0]) if candidates_list.curselection() else messagebox.showerror("Error", "Please select a candidate to delete!"))
delete_candidate_button.grid(row=2, column=0, padx=5, pady=5)

update_candidate_button = tk.Button(root, text="Update Candidate", command=lambda: update_candidate(get_candidates()[candidates_list.curselection()[0]][0], candidate_entry.get()) if candidates_list.curselection() else messagebox.showerror("Error", "Please select a candidate to update!"))
update_candidate_button.grid(row=2, column=1, padx=5, pady=5)

view_candidates_button = tk.Button(root, text="View Candidates", command=view_candidates)
view_candidates_button.grid(row=3, column=1, padx=5, pady=5)

refresh_candidates()

root.mainloop()

conn.close()
