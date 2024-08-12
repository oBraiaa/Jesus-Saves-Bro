from tkinter import *
from tkinter import ttk
from pages.initTrips import InitTrips
from pages.initExpenses import InitExp
from pages.initConvExp import InitConExp
from pages.help import Help
from pages.init_db import create_table


class Notebook(Tk):
    """Notebook for travel expense tracker app."""
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title('CS361 - Travel Expense Log')
        self.geometry("950x650")
        self.resizable(True, True)

        #colors
        light_blue = '#e6f1ff'
        blue_gray = '#68909a'
        pale_green = '#879c8b'
        main_col = pale_green
        button_col = blue_gray
        entry_col = light_blue

        # style and configure pages
        style = ttk.Style()
        style.theme_use('alt')
        style.configure("TEntry", fieldbackground=entry_col,
                        foreground='black', insertcolor='black')
        style.configure("TButton", background=button_col, foreground='white')
        style.configure("TFrame", background=main_col)
        style.configure("TLabel", background=main_col, foreground='white',
                        font=('Helvetica', 14))
        style.configure("TLabelframe", background=main_col)
        style.configure("TLabelframe.Label", background=main_col,
                        foreground='white', font=('Helvetica Bold', 18))
        style.configure("TNotebook", background=main_col)
        style.configure("TNotebook.Tab", background=button_col,
                        foreground="white", font=('Helvetica Bold', 14))
        style.map('TNotebook.Tab', background=[('selected', '#347083')])

        # Configure Treeview
        style.configure("Treeview",
                        background=main_col,
                        foreground="black",
                        rowheight=25,
                        fieldbackground=main_col)
        style.configure("Treeview.Heading", background=button_col,
                        foreground="white", font=('Helvetica', 14))
        style.map('Treeview', background=[('selected', '#347083')])

        # Create Notebook
        my_tabs = ttk.Notebook(self)
        my_tabs.pack(padx=10, pady=10, expand=1)

        trips_frame = ttk.Frame(my_tabs, width=480, height=480)
        expense_frame = ttk.Frame(my_tabs, width=480, height=480)
        con_exp_frame = ttk.Frame(my_tabs, width=480, height=480)
        help_frame = ttk.Frame(my_tabs, width=480, height=480)

        trips_frame.pack(fill="both", expand=1)
        expense_frame.pack(fill="both", expand=1)
        con_exp_frame.pack(fill="both", expand=1)
        help_frame.pack(fill="both", expand=1)

        my_tabs.add(trips_frame, text="My Trips")
        my_tabs.add(expense_frame, text="My Expenses")
        my_tabs.add(con_exp_frame, text="Convert Expenses")
        my_tabs.add(help_frame, text="Help and More Information")

        InitTrips(trips_frame)
        InitExp(expense_frame)
        InitConExp(con_exp_frame)
        Help(help_frame)


if __name__ == "__main__":
    app = Notebook()
    app.mainloop()
