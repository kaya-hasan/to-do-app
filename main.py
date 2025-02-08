import sqlite3
import tkinter as tk
from tkinter import messagebox


conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)")
conn.commit()


def add_task():
    task = entry_task.get()
    if task:
        cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()
        list_tasks()
        entry_task.delete(0, tk.END)
    else:
        messagebox.showwarning("Uyarı", "Boş görev eklenemez!")


def list_tasks():
    listbox_tasks.delete(0, tk.END)
    cursor.execute("SELECT * FROM tasks")
    for row in cursor.fetchall():
        listbox_tasks.insert(tk.END, row[1])


def delete_task():
    try:
        selected_task = listbox_tasks.get(listbox_tasks.curselection())
        cursor.execute("DELETE FROM tasks WHERE task = ?", (selected_task,))
        conn.commit()
        list_tasks()
    except:
        messagebox.showwarning("Uyarı", "Lütfen bir görev seçin!")

root = tk.Tk()
root.title("To-Do List App")

frame = tk.Frame(root)
frame.pack(pady=10)

entry_task = tk.Entry(frame, width=40)
entry_task.pack(side=tk.LEFT, padx=10)

btn_add = tk.Button(frame, text="Ekle", command=add_task)
btn_add.pack(side=tk.LEFT)

listbox_tasks = tk.Listbox(root, width=50, height=10)
listbox_tasks.pack(pady=10)

btn_delete = tk.Button(root, text="Sil", command=delete_task)
btn_delete.pack(pady=5)

list_tasks()
root.mainloop()

conn.close()