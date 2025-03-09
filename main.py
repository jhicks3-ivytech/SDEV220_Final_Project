import tkinter as tk 
from layout import MainWindow
import pandas as pd
from database import Database


def main():
    
    db = Database('database.db')
    conn = db.conn
    curr = db.cursor

    main = MainWindow(db)

    

    
# Run the application
if __name__ == "__main__":
    app = main()
    
