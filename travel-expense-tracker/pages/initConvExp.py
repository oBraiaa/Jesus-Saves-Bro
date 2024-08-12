import csv
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pages.init_db as db
import pages.format_GUI as form
import currencyConverter.currConverter as currConv

codes_csv = "./currencyConverter/FreeCurrencyAPI_codes.csv"

class InitConExp(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.table = 'con_exp'
        tree_info = form.add_tree(parent, "Converted Expenses")
        self.tree_frame = tree_info[0]
        self.tree = tree_info[1]
        self.tree.pack(fill="x", padx=10, pady=10)
        self.tree['columns'] = ('Trip', 'Date', 'Category', 'Expense', 'Cost',
                                'Notes')
        form.format_col(self.tree)
        db.create_table(self.table)

        # Frame for entering country code
        self.data_frame = ttk.LabelFrame(parent, text="Change Currency")
        self.data_frame.pack(fill="x", padx=20)
        self.curr_info = ttk.Label(self.data_frame,
                                   text="Convert all of your expenses to one "
                                        "currency! "
                                        "Enter the three-character "
                                        "alphabetic currency code or search "
                                        "for the country to get the code\n"
                                        "If searching, once you found the "
                                        "country, double click to load code "
                                        "into entry box."
                                        "Press submit to see your converted "
                                        "currency table!")

        # Entry boxes and labels (Change Currency)
        self.e_country = ttk.Entry(self.data_frame)
        self.e_code = ttk.Entry(self.data_frame)
        self.country = ttk.Label(self.data_frame, text="Search by Country",
                                 anchor='e', font=('Helvetica Bold', 16))
        self.code = ttk.Label(self.data_frame, text="Alphabetic Code",
                              anchor='e', font=('Helvetica Bold', 16))
        self.b_submit = ttk.Button(self.data_frame, text="Submit",
                                   command=self.submit)
        self.b_clear = ttk.Button(self.data_frame, text="Clear Entry",
                                  command=self.clear_entries)

        self.curr_list = tk.Listbox(self.data_frame, width=20, bg='#e6f1ff',
                                    fg='black')
        # Read in country codes
        with open(codes_csv) as csvfile:
            code_list = csv.DictReader(csvfile)
            self.codes = {}
            for row in code_list:
                self.codes[row['Entity']] = row['AlphabeticCode']

        self.refresh_filter(self.codes)
        self.e_country.bind('<KeyRelease>', self.check)
        self.curr_list.bind('<<ListboxSelect>>', self.fill_box)
        self.curr_list.bind('<ButtonRelease-1>', self.fill_box)

        # Grid Layout
        self.data_frame.columnconfigure(0, weight=1)
        self.data_frame.columnconfigure(1, weight=3)
        self.data_frame.columnconfigure(2, weight=1)

        self.curr_info.grid(row=0, columnspan=3)
        self.code.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        self.e_code.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        self.country.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        self.e_country.grid(row=2, column=1, padx=10, pady=10, sticky='ew')
        self.curr_list.grid(row=3, column=1, padx=10, pady=10, sticky='ew')
        self.b_submit.grid(row=1, column=2, padx=10, pady=10, sticky='ew')
        self.b_clear.grid(row=2, column=2, padx=10, sticky='ew')
        
    def refresh_filter(self, data):
        """insert search-matched list into listbox"""
        self.curr_list.delete(0, tk.END)
        for country in data:
            self.curr_list.insert(tk.END, country)
            
    def fill_box(self, e):
        """Update search box with selected row"""
        self.clear_entries()
        sel_country = self.curr_list.get(tk.ACTIVE)
        self.e_country.insert(0, sel_country)
        self.e_code.insert(0, self.codes[sel_country])

    def check(self, e):
        """create list of countries that match search box"""
        entered = self.e_country.get()
        if entered == '':
            data = self.codes
        else:
            data = []
            for item in self.codes:
                if entered.lower() in item.lower():
                    data.append(item)

        self.refresh_filter(data)

    def submit(self):
        """Populate converted expense table"""
        form.remove_all(self)
        if self.e_code.get().upper() not in self.codes.values():
            tk.messagebox.showerror(title="Invalid Currency Code",
                                    message="Sorry!\n "
                                            f"{self.e_code.get()} is "
                                            "invalid. Please try again.")
            self.clear_entries()
            self.refresh_filter(self.codes)
            return

        # fill converted expenses table with new values
        conn = db.conn_to_db()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM expenses")
        rows = cur.fetchall()
        for row in rows:
            cur.execute("""INSERT INTO con_exp VALUES (:myTrip, :myDate, 
                                                  :myCategory, :myExpense, 
                                                    :myCost, :myNotes)""",
                        {
                            'myTrip': row[0],
                            'myDate': row[1],
                            'myCategory': row[2],
                            'myExpense': row[3],
                            'myCost': self.edit_currency(row[4].upper(),
                                                         self.e_code.get().upper(),
                                                         row[5]),
                            'myNotes': row[6]
                        })

        conn.commit()
        conn.close()
        self.tree_frame.configure(text=f"Expenses converted to: "
                                       f" {self.e_code.get().upper()}")

        self.clear_entries()
        self.refresh_filter(self.codes)
        self.tree.delete(*self.tree.get_children())
        form.query_database(self)

    def edit_currency(self, old_curr, new_curr, cost):
        """call on microservice to convert currency to selected code"""
        user_input = [old_curr, new_curr, cost]
        conv_cost = currConv.convert(user_input)
        return round(conv_cost, 2)

    def clear_entries(self):
        """clear entries from boxes"""
        self.e_country.delete(0, tk.END)
        self.e_code.delete(0, tk.END)
