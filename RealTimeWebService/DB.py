import mysql.connector

# Replace these values with your actual MySQL configuration
host = "localhost"
user = "root"
password = ""
database = "game_cards"


def update_users_balance(balances):
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            print("Connected to MySQL database")

            cursor = connection.cursor()

            # Iterate through the balances dictionary and update user balances
            for user_id, balance in balances.items():
                query = f"UPDATE user SET balance={balance} WHERE id={user_id}"
                cursor.execute(query)
                connection.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


import mysql.connector


def get_all_names_and_balances():
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            print("Connected to MySQL database")

            cursor = connection.cursor()

            # Execute the query to select all names and balances
            query = "SELECT name, balance FROM user"
            cursor.execute(query)

            # Fetch all name and balance pairs
            name_balance_pairs = cursor.fetchall()

            concatenated_records = []

            for name, balance in name_balance_pairs:
                concatenated_record = f"{name}: {balance}"
                concatenated_records.append(concatenated_record)

            return concatenated_records

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

