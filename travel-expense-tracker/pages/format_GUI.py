import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pages.init_db as db


def add_tree(frame, table):
    """Creates table to hold database information"""
    tree_frame = ttk.LabelFrame(frame, text=table)
    tree_frame.pack(fill="x", padx=20, expand=True)
    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side="right", fill="y")
    tree = ttk.Treeview(tree_frame,
                        yscrollcommand=tree_scroll.set,
                        selectmode='extended')
    if table == 'Converted Expenses':
        return [tree_frame, tree]
    return tree


def format_col(tree):
    """add columns and headers to tree"""
    tree.column("#0", width=0, stretch=False)
    for col in tree['columns']:
        tree.column(col, anchor='w', width=100)
    for item in tree['columns']:
        tree.heading(item, text=item)

    tree.tag_configure('oddrow', background='#e6f1ff')
    tree.tag_configure('evenrow', background='light blue')


def format_grid(frame):
    """format input boxes and labels for each page"""
    frame.data_frame.columnconfigure(0, weight=1)
    frame.data_frame.columnconfigure(1, weight=1)
    frame.data_frame.columnconfigure(2, weight=1)
    frame.data_frame.columnconfigure(3, weight=1)
    frame.data_frame.columnconfigure(4, weight=1)
    frame.data_frame.columnconfigure(5, weight=1)
    row, col, ind = 0, 0, 0
    for label in frame.my_labels:
        label.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
        frame.my_entries[ind].grid(row=row, column=col+1, padx=10, pady=10,
                                   sticky='ew')
        col += 2
        ind += 1
        if col > 5:
            col = 0
            row += 1


def add_buttons(parent, frame):
    """add buttons for database manipulation"""
    b_frame = ttk.LabelFrame(parent, text="Commands")
    b_frame.pack(fill="x", padx=20, expand=True)

    b_update = ttk.Button(b_frame, text="Update Entry",
                          command=lambda: edit_rec(frame, 'update'))
    b_add = ttk.Button(b_frame, text="Add Entry",
                       command=lambda: edit_rec(frame, 'add'))
    b_del_all = ttk.Button(b_frame, text="Delete All Entries",
                           command=lambda: delete_all(frame))
    b_del_row = ttk.Button(b_frame, text="Delete Entry",
                           command=lambda: delete_one(frame))
    b_clear = ttk.Button(b_frame, text="Clear Record Boxes",
                         command=frame.clear_entries)

    b_frame.columnconfigure(0, weight=1)
    b_frame.columnconfigure(1, weight=1)
    b_frame.columnconfigure(2, weight=1)
    b_frame.columnconfigure(3, weight=1)
    b_frame.columnconfigure(4, weight=1)
    b_add.grid(row=3, column=0, padx=10, pady=10, sticky='ew')
    b_update.grid(row=3, column=1, padx=10, pady=10, sticky='ew')
    b_del_row.grid(row=3, column=2, padx=10, pady=10, sticky='ew')
    b_del_all.grid(row=3, column=3, padx=10, pady=10, sticky='ew')
    b_clear.grid(row=3, column=4, padx=10, pady=10, sticky='ew')


def query_database(frame):
    """add content from database to tree"""
    db.create_table(frame.table)
    conn = db.conn_to_db()
    cur = conn.cursor()
    cur.execute(f"SELECT rowid, * FROM {frame.table}")
    records = cur.fetchall()
    count = 0
    for row in records:
        if count % 2 == 0:
            frame.tree.insert("", tk.END, values=row[1:], tags='evenrow',
                              iid=row[0])
        else:
            frame.tree.insert("", tk.END, values=row[1:], tags='oddrow',
                              iid=row[0])
        count += 1
    conn.commit()
    conn.close()


def edit_rec(frame, type):
    """add new record or edit and update existing record"""
    conn = db.conn_to_db()
    cur = conn.cursor()
    if type == 'add':
        items = frame.add_rec()
    else:
        items = frame.update_rec()
    cur.execute(items[0], items[1])
    conn.commit()
    conn.close()
    frame.clear_entries()
    frame.tree.delete(*frame.tree.get_children())
    query_database(frame)


def delete_one(frame):
    """warning message before deleting selected row"""
    if tk.messagebox.askokcancel(title="Delete Entry",
                                 message="Are you sure you want to delete "
                                         "this row? This cannot be undone"):
        remove_one(frame)


def remove_one(frame):
    """Remove row from database table"""
    x = frame.tree.selection()
    frame.tree.delete(x)
    conn = db.conn_to_db()
    cur = conn.cursor()
    cur.execute(f"DELETE from {frame.table} WHERE oid=" + frame.id)
    conn.commit()
    conn.close()
    frame.clear_entries()
    messagebox.showinfo("Deleted", "Row has been deleted")
    frame.tree.delete(*frame.tree.get_children())
    query_database(frame)


def delete_all(frame):
    """warning message before deleting all rows"""
    if tk.messagebox.askokcancel(title="Delete ALl",
                                 message="Are you sure you want to delete "
                                         "the entire table? This cannot be "
                                         "undone"):
        remove_all(frame)


def remove_all(frame):
    """Remove all values from tree and database table"""
    for rec in frame.tree.get_children():
        frame.tree.delete(rec)
    conn = db.conn_to_db()
    cur = conn.cursor()
    cur.execute(f"DROP TABLE {frame.table}")
    conn.commit()
    conn.close()
    db.create_table(frame.table)
