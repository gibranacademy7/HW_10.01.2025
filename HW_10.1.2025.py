import sqlite3

class Customer:
    def __init__(self, id, fname, lname, address, mobile):
        self.id = id
        self.fname = fname
        self.lname = lname
        self.address = address
        self.mobile = mobile

    def __str__(self):
        return f'id: {self.id}, name: {self.fname} {self.lname}, address: {self.address}, mobile: {self.mobile}'

    def __repr__(self):
        return f'Customer({self.id}, {self.fname}, {self.lname}, {self.address}, {self.mobile})'

    def __eq__(self, other):
        return (
            isinstance(other, Customer) and
            self.lname == other.lname and
            self.address == other.address
        )

    def __hash__(self):
        return hash(self.lname)


class CustomerDatabase:
    def __init__(self, db_name="customer.db"):
        self.connection = sqlite3.connect(db_name)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Customer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fname TEXT NOT NULL,
                lname TEXT NOT NULL,
                address TEXT NOT NULL,
                mobile TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def insert_customer(self, fname, lname, address, mobile):
        self.cursor.execute("""
            INSERT INTO Customer (fname, lname, address, mobile)
            VALUES (?, ?, ?, ?)
        """, (fname, lname, address, mobile))
        self.connection.commit()

    def get_all_customers(self):
        customers = self.cursor.execute("SELECT * FROM Customer")
        customers_list = [
            Customer(row['id'], row['fname'], row['lname'], row['address'], row['mobile'])
            for row in customers
        ]
        return customers_list

    def close_connection(self):
        self.connection.close()


# Example usage:

# Initialize the database and customer operations
db = CustomerDatabase()

# Insert new customers
db.insert_customer('Wisam', 'Gibran', '5 Almog st. Nof Hagalil', '054-7407016')
db.insert_customer('Hanan', 'Assad', 'Mutran 99 Nazareth', '052-2039486')
db.insert_customer('Rama', 'Hanna', 'Ben Goryon 8 Haifa', '054-3243546')
db.insert_customer('Arwa', 'Malak', 'Zion 22 Jerusalem', '054-8768576')
db.insert_customer('Moshe', 'Cohen', '33 Curcom st. Reine', '052-3645675')

# Retrieve all customers
all_customers = db.get_all_customers()

# Print all customers
for customer in all_customers:
    print(customer)

# Testing equality and hash
print(all_customers[0])
print(repr(all_customers[1]))
print(all_customers[0] == all_customers[4])  # Checking if first and fifth customer are the same

print(f'hash of customer 1: {hash(all_customers[0])}, hash of customer 5: {hash(all_customers[4])}')

# Close the database connection
db.close_connection()
