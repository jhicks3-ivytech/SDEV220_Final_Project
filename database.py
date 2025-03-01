import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tools_table()
        self.create_employee_table()
        

    def create_tools_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tools (
                                id INTEGER PRIMARY KEY,
                                tool TEXT,
                                serial_number INTEGER,
                                available INTEGER
                              )''')
        self.conn.commit()

    def add_tool(self, id, tool, serial_number, available=1):
        self.cursor.execute("INSERT INTO tools (id, tool, serial_number, available) VALUES (?, ?, ?, ?)",
                            (id, tool, serial_number, available))
        self.conn.commit()

    def add_tools_bulk(self, tools):
        #tools param should be a list of tuples
        self.cursor.executemany("INSERT INTO tools (id, tool, serial_number, available) VALUES (?, ?, ?, ?)", tools)
        self.conn.commit()

    def fetch_tools(self):
        self.cursor.execute("SELECT * FROM tools")
        return self.cursor.fetchall()
    
    def fetch_available(self):
        self.cursor.execute('''
                            SELECT * 
                            FROM tools
                            WHERE available = 1;
                            ''')
        return self.cursor.fetchall()
    
    def fetch_not_available(self):
        self.cursor.execute('''
                            SELECT * 
                            FROM tools
                            WHERE available = 0;
                            ''')
        return self.cursor.fetchall()

    def update_status(self, id, available):
        self.cursor.execute('''
                            UPDATE tools 
                            SET available = ? 
                            WHERE id = ?;
                            ''', (available, id))
        self.conn.commit()

    def delete_tool(self, id):
        self.cursor.execute('''
                            DELETE FROM tools 
                            WHERE id = ?;
                            ''', (id,))
        self.conn.commit()

    def create_employee_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                department TEXT,
                                shift INTEGER
                              )''')
        self.conn.commit()

    def add_employee(self, id, name, department, shift):
        self.cursor.execute("INSERT INTO employees (id, name, department, shift) VALUES (?, ?, ?, ?)",
                            (id, name, department, shift))
        self.conn.commit()

    def add_employees_bulk(self, employees):
        #employees param should be a list of tuples
        self.cursor.executemany("INSERT INTO employees (id, name, department, shift) VALUES (?, ?, ?, ?)", employees)
        self.conn.commit()

    def fetch_employees(self):
        self.cursor.execute("SELECT * FROM employees")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()