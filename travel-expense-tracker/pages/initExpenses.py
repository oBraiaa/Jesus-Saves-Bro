import tkinter as tk
from tkinter import ttk
import pages.init_db as db
import pages.format_GUI as form


class InitExp(tk.Frame):
    """Tab for logging expenses to database"""
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.table = 'expenses'
        self.tree = form.add_tree(parent, "Log Expenses")
        self.tree.pack(fill="x", padx=10, pady=10, expand=1)
        form.query_database(self)

        # Label Frame for entry boxes
        self.data_frame = ttk.LabelFrame(parent, text="Record Expense")
        self.data_frame.pack(fill="x", padx=20, expand=True)

        # Trip and Category OptionMenu intialization
        self.sel_trip = tk.StringVar()
        self.sel_trip.set("Select Trip")
        self.om_trip = ttk.OptionMenu(self.data_frame, self.sel_trip,
                                      *self.populate_trips())

        self.category_list = ["Select Category", "Airfare", "Ground "
                              "Transportation", "Food",
                              "Lodging", "Attractions", "Misc", "Other"]
        self.sel_category = tk.StringVar()
        self.sel_category.set("Select Category")
        self.om_category = ttk.OptionMenu(self.data_frame, self.sel_category,
                                          *self.category_list)

        # Entry Boxes (Record Expense)
        self.id = ttk.Entry(self.data_frame)
        self.e_date = ttk.Entry(self.data_frame)
        self.e_expense = ttk.Entry(self.data_frame)
        self.e_currency = ttk.Entry(self.data_frame)
        self.e_cost = ttk.Entry(self.data_frame)
        self.e_notes = ttk.Entry(self.data_frame)

        # Labels and Buttons (Record Expense)
        self.trip = ttk.Label(self.data_frame, text="Select Trip: ")
        self.date = ttk.Label(self.data_frame, text="Date Purchased:")
        self.category = ttk.Label(self.data_frame, text="Category:")
        self.expense = ttk.Label(self.data_frame, text="Expense Name:")
        self.currency = ttk.Label(self.data_frame, text="Currency:")
        self.cost = ttk.Label(self.data_frame, text="Cost:")
        self.notes = ttk.Label(self.data_frame, text="Notes:")

        self.my_entries = (self.om_trip, self.e_date, self.om_category,
                           self.e_expense, self.e_currency, self.e_cost,
                           self.e_notes)

        self.my_labels = (self.trip, self.date, self.category, self.expense,
                          self.currency, self.cost, self.notes)

        # Format frame
        form.format_grid(self)

        self.tree['columns'] = ('Trip', 'Date', 'Category', 'Expense',
                                'Currency', 'Cost', 'Notes')
        form.format_col(self.tree)
        form.add_buttons(parent, self)

        self.tree.bind("<ButtonRelease-1>", self.select_rec)
        self.om_trip.bind('<Button-1>', self.refresh_table)

    def populate_trips(self):
        """gather list of trips recorded in trips database"""
        trip_list = ["Select Trip"]
        conn = db.conn_to_db()
        cur = conn.cursor()
        cur.execute("Select *, oid FROM trips")
        trips = cur.fetchall()
        for trip in trips:
            trip_list.append(trip[0])
        conn.commit()
        conn.close()
        return trip_list

    def refresh_table(self, e=None):
        """update trip options for trip OptionMenu"""
        trips = self.om_trip['menu']
        trips.delete(0, tk.END)
        for trip in self.populate_trips():
            trips.add_command(label=trip, command=lambda trip=trip:
            self.sel_trip.set(trip))

    def clear_entries(self):
        """clear entries from boxes"""
        self.refresh_table()
        for entry in self.my_entries:
            if entry is self.om_trip:
                self.sel_trip.set("Select Trip")
            elif entry is self.om_category:
                self.sel_category.set("Select Category")
            else:
                entry.delete(0, tk.END)

    def select_rec(self, e):
        """get information from selected row, populate into entry boxes"""
        self.clear_entries()
        self.id = self.tree.focus()
        val = self.tree.item(self.id, 'values')
        i = 0
        for entry in self.my_entries:
            if entry is self.om_trip:
                self.sel_trip.set(val[i])
            elif entry is self.om_category:
                self.sel_category.set(val[i])
            else:
                entry.insert(0, val[i])
            i += 1

    def update_rec(self):
        """update selected user input to database table"""
        up_val = """UPDATE expenses SET trip = :myTrip, date = :myDate,
                    category = :myCategory, expense_name = :myExpense, 
                    currency= :myCurrency, cost= :myCost, 
                    notes = :myNotes WHERE oid = :oid"""

        up_dict = {
                        'myTrip': self.sel_trip.get(),
                        'myDate': self.e_date.get(),
                        'myCategory': self.sel_category.get(),
                        'myExpense': self.e_expense.get(),
                        'myCurrency': self.e_currency.get(),
                        'myCost': self.e_cost.get(),
                        'myNotes': self.e_notes.get(),
                        'oid': self.id
                    }
        return up_val, up_dict

    def add_rec(self):
        """add user input to database table"""
        add_val = """INSERT INTO expenses VALUES (:myTrip, :myDate, 
                                                :myCategory, :myExpense, 
                                                :myCurrency, :myCost, 
                                                :myNotes)"""
        add_dict = {
                        'myTrip': self.sel_trip.get(),
                        'myDate': self.e_date.get(),
                        'myCategory': self.sel_category.get(),
                        'myExpense': self.e_expense.get(),
                        'myCurrency': self.e_currency.get(),
                        'myCost': self.e_cost.get(),
                        'myNotes': self.e_notes.get(),
                    }
        return add_val, add_dict
