import mysql.connector

# Replace these values with your actual MySQL configuration
host = "localhost"
user = "your_username"
password = "your_password"
database = "your_database_name"

# Connect to the MySQL database
try:
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    if connection.is_connected():
        print("Connected to MySQL database")

        # Execute a query
        query = "SELECT * FROM your_table_name"
        cursor = connection.cursor()
        cursor.execute(query)

        # Fetch and print the results
        rows = cursor.fetchall()
        for row in rows:
            print(row)

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
