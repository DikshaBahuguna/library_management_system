import mysql.connector
from mysql.connector import Error
import getpass
import admin
import user

def connect_to_database():
    """Establish connection to MySQL database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Add MYSQL username here
            password='dikshamysql',  # Add MYSQL password here
            database='library_management'
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def close_connection(connection):
    """Close database connection"""
    if connection and connection.is_connected():
        connection.close()
        print("Database connection closed.")

def login(connection):
    """Handle user login"""
    print("\n=== Library Management System Login ===")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = "USE library_management"
        cursor.execute(query)
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            print(f"\nWelcome, {user['username']}!")
            return user
        else:
            print("Invalid username or password!")
            return None
    except Error as e:
        print(f"Error during login: {e}")
        return None

def logout():
    """Handle user logout"""
    print("Logged out successfully!")
    return None

def main():
    """Main function to run the library management system"""
    print("Welcome to Library Management System")
    
    # Connect to database
    connection = connect_to_database()
    if not connection:
        return
    
    try:
        current_user = None
        
        while True:
            if not current_user:
                current_user = login(connection)
                if current_user:
                    if current_user['user_type'] == 'admin':
                        current_user = admin.admin_menu(connection, current_user)
                    else:
                        current_user = user.user_menu(connection, current_user)
                
                if not current_user:
                    continue_option = input("\nDo you want to continue? (y/n): ").lower()
                    if continue_option != 'y':
                        print("Thank you for using Library Management System!")
                        break
            else:
                break
                
    finally:
        close_connection(connection)

if __name__ == "__main__":
    main()