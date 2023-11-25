import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
from datetime import datetime

class TodoList:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List")
        self.root.configure(bg='antiquewhite2')


        self.tree = ttk.Treeview(root, columns=("Tasks", "Due Date", "Importance", "Completed"), show="headings")
        self.tree.heading("Tasks", text="Tasks")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Importance", text="Importance")
        self.tree.heading("Completed", text="Completed")

        self.tree.column("Tasks", width=200)
        self.tree.column("Due Date", width=100)
        self.tree.column("Importance", width=100)
        self.tree.column("Completed", width=100)

        self.tree.grid(row=1,column=1,columnspan=3,padx=10,pady=10)

        self.task_entry = tk.Entry(root, width=50)
        self.due_date_entry = tk.Entry(root, width=20)
        self.due_date_entry.insert(0,"yyyy-mm-dd")
        self.importance_entry = tk.Entry(root, width=10)

        tk.Label(root, text="Task ID:",fg='black', bg='AntiqueWhite2').grid(row=2,column=1)
        self.task_entry.grid(row=2,column=2)

        tk.Label(root, text="Due Date:",fg='black', bg='AntiqueWhite2',anchor="center").grid(row=3,column=1)
        self.due_date_entry.grid(row=3,column=2)

        tk.Label(root, text="Importance:",fg='black', bg='AntiqueWhite2').grid(row=4,column=1)
        self.importance_entry.grid(row=4,column=2)

        tk.Button(root, text="Add Task",width=20, command=self.add_task,fg='black', bg='aquamarine2').grid(row=5,column=1,padx=10)
        tk.Button(root, text="Remove Task",width=20, command=self.remove_task,fg='black', bg='firebrick1').grid(row=5,column=2,padx=10)
        tk.Button(root, text="Save Tasks",width=20, command=self.save_tasks,fg='black', bg='bisque3').grid(row=6,column=1,padx=10)
        tk.Button(root, text="Mark Completed",width=20, command=self.mark_completed).grid(row=6,column=2,padx=10)

        self.load_tasks_from_csv()  # Load tasks from CSV file (if any)

    def add_task(self):
        task = self.task_entry.get()
        due_date = self.due_date_entry.get()
        importance = self.importance_entry.get()
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            tk.messagebox.showerror("Error", "Invalid Due Date Format (YYYY-MM-DD)")
            return
        if task and due_date and importance:
            self.tree.insert("", "end", values=(task, due_date, importance, "No"))
            self.clear_entries()

    def remove_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)

    def save_tasks(self):
        tasks = []

        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            tasks.append(values)

        with open("todo_list.csv", mode="w", newline='') as file:
            writer = csv.writer(file)
            writer.writerows(tasks)

    def load_tasks_from_csv(self):
        try:
            with open("todo_list.csv","r") as file:
                reader = csv.reader(file)
                for row in reader:
                    self.tree.insert("", "end", values=row)
        except FileNotFoundError:
            pass

    def clear_entries(self):
        self.task_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
        self.importance_entry.delete(0, tk.END)

    def mark_completed(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, 'values')
            current_completed_status = item_values[3]

            new_completed_status = "Yes" if current_completed_status == "No" else "No"

            self.tree.item(selected_item, values=(item_values[0], item_values[1], item_values[2], new_completed_status))


root = tk.Tk()
todo_list = TodoList(root)
root.mainloop()
