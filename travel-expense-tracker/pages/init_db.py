# Manage aspects related to the database page, functions to create tables,
#   delete tables, and edit rows

import sqlite3


def conn_to_db():
    """connect to database"""
    conn = sqlite3.connect('travel_exp.db')
    return conn


def create_table(table):
    """create table if it does not exist already"""
    conn = conn_to_db()
    if table == "trips":
        conn.execute("""CREATE TABLE IF NOT EXISTS trips (
                                'myTrip',
                                'myStartDate',
                                'myEndDate',
                                'myTripType',
                                'myNotes'
                            )""")

    elif table == "con_exp":
        conn.execute("""CREATE TABLE IF NOT EXISTS con_exp(
                trip,
                date,
                category,
                expense_name,
                cost,
                notes
                )""")

    elif table == "expenses":
        conn.execute("""CREATE TABLE IF NOT EXISTS expenses(
                    trip,
                    date,
                    category,
                    expense_name,
                    currency,
                    cost,
                    notes
                    )""")

    conn.commit()
    conn.close()


def deleteAll(table):
    """delete all contents of table"""
    conn = conn_to_db()
    cur = conn.cursor()
    cur.execute(f"delete from {table}")
    conn.commit()
    conn.close()
