import tkinter as tk
from tkinter import ttk
import pages.format_GUI as form


class InitTrips(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.table = 'trips'
        self.filter = 'myTrips'
        self.tree = form.add_tree(parent, "Log Trips")
        self.tree.pack(fill="x", padx=10, pady=10, expand=True)
        form.query_database(self)

        # Label frame for entry boxes
        self.data_frame = ttk.LabelFrame(parent, text="Record Trip")
        self.data_frame.pack(fill="x", padx=20, expand=True)

        # Entry boxes (Record Trip)
        self.id = ttk.Entry(self.data_frame)
        self.e_trip = ttk.Entry(self.data_frame)
        self.e_start_date = ttk.Entry(self.data_frame)
        self.e_end_date = ttk.Entry(self.data_frame)
        self.e_trip_type = ttk.Entry(self.data_frame)
        self.e_notes = ttk.Entry(self.data_frame)

        # Labels and Buttons (Record Trip)
        self.trip = ttk.Label(self.data_frame, text="Trip Name:")
        self.start_date = ttk.Label(self.data_frame, text="Start Date:")
        self.end_date = ttk.Label(self.data_frame, text="End Date:")
        self.trip_type = ttk.Label(self.data_frame, text="Trip Type:")
        self.notes = ttk.Label(self.data_frame, text="Notes:")

        self.my_entries = (self.e_trip, self.e_start_date, self.e_end_date,
                           self.e_trip_type, self.e_notes)
        self.my_labels = (self.trip, self.start_date, self.end_date,
                          self.trip_type, self.notes)

        # Format page layout, tree, and buttons
        form.format_grid(self)
        self.tree['columns'] = ('Name', 'Start Date', 'End Date', 'Type',
                                'Notes')
        form.format_col(self.tree)
        form.add_buttons(parent, self)

        self.tree.bind("<ButtonRelease-1>", self.select_rec)

    def clear_entries(self):
        """clear entries from boxes"""
        for entry in self.my_entries:
            entry.delete(0, tk.END)

    def update_rec(self):
        """update selected user input to database table"""
        up_val = """UPDATE trips SET myTrip = :myTrip, 
                    myStartDate = :myStartDate, myEndDate = :myEndDate, 
                    myTripType = :myTripType, myNotes = :myNotes 
                    WHERE oid = :oid"""
        up_dict = {
                        'myTrip': self.e_trip.get(),
                        'myStartDate': self.e_start_date.get(),
                        'myEndDate': self.e_end_date.get(),
                        'myTripType': self.e_trip_type.get(),
                        'myNotes': self.e_notes.get(),
                        'oid': self.id}
        return [up_val, up_dict]

    def add_rec(self):
        """add user input to database table"""
        add_val = """INSERT INTO trips VALUES (:myTrip, :myStartDate, 
                                            :myEndDate, :myTripType, 
                                            :myNotes)"""
        add_dict = {
                        'myTrip': self.e_trip.get(),
                        'myStartDate': self.e_start_date.get(),
                        'myEndDate': self.e_end_date.get(),
                        'myTripType': self.e_trip_type.get(),
                        'myNotes': self.e_notes.get()
                    }
        return [add_val, add_dict]

    def select_rec(self, e):
        """get information from selected row, populate into entry boxes"""
        self.clear_entries()
        self.id = self.tree.focus()
        values = self.tree.item(self.id, 'values')
        i = 0
        for entry in self.my_entries:
            entry.insert(0, values[i])
            i += 1
