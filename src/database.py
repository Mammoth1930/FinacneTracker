"""
This file contains the code which is used to setup and manipulate the SQLite3
database used to store all of the financial data for the dashboard.
"""

import sqlite3

# SQLite3 database file name
DB_FILE = "finance.db"

# Create a connection to the database
DB_CONN = sqlite3.connect(DB_FILE)

"""
Creates the database tables if they don't already exist.
"""
def db_init():

    # Create the Accounts table
    DB_CONN.execute(
        '''
        CREATE TABLE IF NOT EXISTS Accounts (
            id TEXT,
            displayName TEXT,
            accountType TEXT,
            ownershipType TEXT,
            balance INTEGER,
            created TEXT,
            PRIMARY KEY id
        )
        '''
    )

    # Create the Transactions table
    DB_CONN.execute(
        '''
        CREATE TABLE IF NOT EXISTS Transactions (
            id TEXT,
            status TEXT,
            rawText TEXT,
            description TEXT
            message TEXT,
            isCategorizable INTEGER,
            held INTEGER,
            heldAmount INTEGER,
            roundUpAmount INTEGER,
            boostProportion INTEGER,
            cashbackDesc TEXT,
            cashbackAmount INTEGER,
            foreignCurrency TEXT,
            foreignAmount INTEGER,
            cardPurchaseMethod TEXT,
            cardNumberSuffix INTEGER,
            settledAt TEXT,
            createdAt TEXT,
            account TEXT,
            transferAccount TEXT,
            category TEXT,
            parentCategory TEXT
            PRIMARY KEY id,
            FOREIGN KEY account REFERENCES Accounts(id),
            FOREIGN KEY transferAccount REFERENCES Accounts(id)
        )
        '''
    )

    # Create the Tags table
    DB_CONN.execute(
        '''
        CREATE TABLE IF NOT EXISTS Tags (
            id TEXT,
            transaction TEXT,
            PRIMARY KEY id,
            FOREIGN KEY transaction REFERENCES Transactions(id)
        )
        '''
    )