from mysql.connector import Error

def admin_menu(connection, current_user):
    """Display admin menu and handle options"""
    while True:
        print("\n=== Admin Menu ===")
        print("1. Add User")
        print("2. Remove User")
        print("3. View All Users")
        print("4. Add Book")
        print("5. Remove Book")
        print("6. View All Books")
        print("7. View Transaction History")
        print("8. Logout")
        
        choice = input("Enter your choice (1-8): ")
        
        if choice == '1':
            add_user(connection)
        elif choice == '2':
            remove_user(connection, current_user)
        elif choice == '3':
            view_all_users(connection)
        elif choice == '4':
            add_book(connection)
        elif choice == '5':
            remove_book(connection)
        elif choice == '6':
            view_all_books(connection)
        elif choice == '7':
            view_transaction_history(connection)
        elif choice == '8':
            return None  # Logout
        else:
            print("Invalid choice! Please try again.")

def add_user(connection):
    """Add a new user to the system"""
    print("\n=== Add New User ===")
    username = input("Enter username: ")
    password = input("Enter password: ")
    user_type = input("Enter user type (admin/user): ").lower()
    
    if user_type not in ['admin', 'user']:
        print("Invalid user type! Must be 'admin' or 'user'")
        return
    
    try:
        cursor = connection.cursor()
        query = "INSERT INTO users (username, password, user_type) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, password, user_type))
        connection.commit()
        print(f"User '{username}' added successfully!")
    except Error as e:
        print(f"Error adding user: {e}")
    finally:
        cursor.close()

def remove_user(connection, current_user):
    """Remove a user from the system"""
    print("\n=== Remove User ===")
    view_all_users(connection)
    user_id = input("Enter user ID to remove: ")
    
    try:
        cursor = connection.cursor()
        
        # Check if user exists and is not the current user
        if int(user_id) == current_user['user_id']:
            print("Cannot remove your own account!")
            return
        
        # Check if user has active transactions
        check_query = "SELECT COUNT(*) FROM transactions WHERE user_id = %s AND status = 'active'"
        cursor.execute(check_query, (user_id,))
        active_transactions = cursor.fetchone()[0]
        
        if active_transactions > 0:
            print("Cannot remove user with active book transactions!")
            return
        
        delete_query = "DELETE FROM users WHERE user_id = %s"
        cursor.execute(delete_query, (user_id,))
        connection.commit()
        
        if cursor.rowcount > 0:
            print("User removed successfully!")
        else:
            print("User not found!")
    except Error as e:
        print(f"Error removing user: {e}")
    finally:
        cursor.close()

def view_all_users(connection):
    """Display all users in the system"""
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT user_id, username, user_type, created_at FROM users ORDER BY user_id"
        cursor.execute(query)
        users = cursor.fetchall()
        
        print("\n=== All Users ===")
        print(f"{'ID':<5} {'Username':<15} {'Type':<10} {'Created At'}")
        print("-" * 50)
        for user in users:
            print(f"{user['user_id']:<5} {user['username']:<15} {user['user_type']:<10} {user['created_at']}")
    except Error as e:
        print(f"Error fetching users: {e}")
    finally:
        cursor.close()

def add_book(connection):
    """Add a new book to the library"""
    print("\n=== Add New Book ===")
    title = input("Enter book title: ")
    author = input("Enter author: ")
    isbn = input("Enter ISBN: ")
    quantity = input("Enter quantity: ")
    
    try:
        cursor = connection.cursor()
        query = """INSERT INTO books (title, author, isbn, quantity, available_quantity) 
                   VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(query, (title, author, isbn, quantity, quantity))
        connection.commit()
        print("Book added successfully!")
    except Error as e:
        print(f"Error adding book: {e}")
    finally:
        cursor.close()

def remove_book(connection):
    """Remove a book from the library"""
    print("\n=== Remove Book ===")
    view_all_books(connection)
    book_id = input("Enter book ID to remove: ")
    
    try:
        cursor = connection.cursor()
        
        # Check if book has active transactions
        check_query = "SELECT COUNT(*) FROM transactions WHERE book_id = %s AND status = 'active'"
        cursor.execute(check_query, (book_id,))
        active_transactions = cursor.fetchone()[0]
        
        if active_transactions > 0:
            print("Cannot remove book with active transactions!")
            return
        
        delete_query = "DELETE FROM books WHERE book_id = %s"
        cursor.execute(delete_query, (book_id,))
        connection.commit()
        
        if cursor.rowcount > 0:
            print("Book removed successfully!")
        else:
            print("Book not found!")
    except Error as e:
        print(f"Error removing book: {e}")
    finally:
        cursor.close()

def view_all_books(connection):
    """Display all books in the library"""
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT book_id, title, author, isbn, quantity, available_quantity FROM books ORDER BY book_id"
        cursor.execute(query)
        books = cursor.fetchall()
        
        print("\n=== All Books ===")
        print(f"{'ID':<5} {'Title':<30} {'Author':<20} {'ISBN':<15} {'Total':<8} {'Available':<10}")
        print("-" * 90)
        for book in books:
            print(f"{book['book_id']:<5} {book['title']:<30} {book['author']:<20} {book['isbn']:<15} {book['quantity']:<8} {book['available_quantity']:<10}")
    except Error as e:
        print(f"Error fetching books: {e}")
    finally:
        cursor.close()

def view_transaction_history(connection):
    """Display all transactions (admin only)"""
    try:
        cursor = connection.cursor(dictionary=True)
        query = """SELECT t.transaction_id, u.username, b.title, t.transaction_type, 
                  t.transaction_date, t.due_date, t.status 
                  FROM transactions t 
                  JOIN users u ON t.user_id = u.user_id 
                  JOIN books b ON t.book_id = b.book_id 
                  ORDER BY t.transaction_date DESC"""
        cursor.execute(query)
        transactions = cursor.fetchall()
        
        print("\n=== All Transactions ===")
        print(f"{'TID':<5} {'User':<15} {'Book Title':<25} {'Type':<10} {'Date':<12} {'Due Date':<12} {'Status':<10}")
        print("-" * 90)
        for trans in transactions:
            print(f"{trans['transaction_id']:<5} {trans['username']:<15} {trans['title']:<25} {trans['transaction_type']:<10} {trans['transaction_date'].strftime('%Y-%m-%d'):<12} {str(trans['due_date']):<12} {trans['status']:<10}")
    except Error as e:
        print(f"Error fetching transaction history: {e}")
    finally:
        cursor.close()