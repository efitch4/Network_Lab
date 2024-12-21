import sqlite3
import os

# 1. Define a base class for NetworkDevice
class NetworkDevice:
    def __init__(self, hostname, ip_address, device_type):
        self.hostname = hostname
        self.ip_address = ip_address
        self.device_type = device_type

    def display_device_info(self):
        """Display the information of the device"""
        print(f"Hostname: {self.hostname}")
        print(f"IP Address: {self.ip_address}")
        print(f"Device Type: {self.device_type}")


    def to_tuple(self):
        """Return device info as a tuple for SQL insertion"""
        return (self.hostname, self.ip_address, self.device_type)
    
# 2. Define a subclass for Router with additional properties
class Router(NetworkDevice):
    def __init__(self, hostname, ip_address, routing_protocol):
        super().__init__(hostname, ip_address, "Router")
        self.routing_protocol = routing_protocol

    def display_routing_info(self):
        """ Display router-specific info"""
        print(f"Routing Protocoll: {self.routing_protocol}")

# 3. Define a function to handle file logging
def log_to_file(message):
    """Logs messages to a text file"""
    with open('network_log.txt', 'a') as log_file:
        log_file.write(message + '\n')

# 4. Exception handling for database operations
def safe_execute(cursor, query, params=()):
    """Safley execute SQL commands with error handling"""
    try:
        cursor.execute(query, params)
    except sqlite3.Error as e:
        print(f"Database error : {e}")
        log_to_file(f"Database error{e}")

# 5. Create a database connection and a cursor
def create_connection(db_file):
    """Create a connection to the SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to {db_file}")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database {e}")
        log_to_file(f"Error connecting to database: {e}")
    return conn

# 6. Create the devices table
def create_table(conn):
    """Create the devices table if it doesn't exist"""
    try:
        sql_create_devices_table = """
        CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hostname TEXT NOT NULL, 
        ip_address TEXT NOT NULL UNIQUE,
        device_type TEXT NOT NULL,
        additional_info TEXT
        );
        """
        conn.execute(sql_create_devices_table)
        print("Devices table create.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
        log_to_file(f"Error creating table: {e}")

# 7. Insert a new device into the devices table
def insert_device(conn, device, additional_info=None):
    """Insert a new device into the dvices table"""
    sql = ''' INSERT INTO devices(hostname, ip_address, device_type, additional_info)
               VALUES(?,?,?,?)'''
    safe_execute(conn.cursor(), sql, device.to_tuple() + (additional_info))
    conn.commint()
    print(f"Inserted{device.hostname} into database.")
    log_to_file(f"Inserted {device.hostname} into database.")

# 8. Query all devices in the table 
def query_all_devices(conn):
    """Query and print all devices in the devices table"""
    cur = conn.cursor()
    safe_execute(cur, "SELECT * FROM devices")
    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No devices found.")
    log_to_file("Queried all devices.")

# 9. Update a device's IP address baed on its hostname
def update_device_ip(conn, new_ip, hostname):
    """Update the IP address of a device by hostname"""
    sql = '''UPDATE devices SET ip_address = ? WHERE hostname = ?'''
    safe_execute(conn.cursor(), sql, (new_ip, hostname))
    conn.commit()
    print(f"Updated {hostname}'s IP address to {new_ip}.")
    log_to_file(f"Updated {hostname}'s IP address to {new_ip}.")

# 10. Delete a device by hostname
def delete_device(conn, hostname):
    sql = 'DELETE FROM devices WHERE hostname = ?'
    safe_execute(conn.cursor(), sql, (hostname,))
    conn.commit()
    print(f"Deleted {hostname} from the database.")
    log_to_file(f"Deleted {hostname} from the database")

# 11. Create a function to back up the database to a file
def backup_database(conn, backup_file):
    """ Backup the current database to a file"""
    with open(backup_file, 'w') as f:
        for line in conn.interdump():
            f.write(f"{line}\n")
    print(f"Database backup saved to {backup_file}.")
    log_to_file(f"Database backup saved to {backup_file}")

# 12. Exception handling for invalid IP address formats
def validate_ip(ip_address):
    """Validate if the IP address format is correct"""
    parts = ip_address.split('.')
    if len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
        return True
    else:
        raise ValueError("Invalid IP address format")