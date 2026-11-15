from mysql.connector import Error
from datetime import datetime, timedelta

def user_menu(connection, current_user):
    """Display user menu and handle options"""
    while True:
        print("\n=== User Menu ===")
        print("1. View Available Books")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View My Transactions")
        print("5. Logout")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            view_available_books(connection)
        elif choice == '2':
            issue_book(connection, current_user)
        elif choice == '3':
            return_book(connection, current_user)
        elif choice == '4':
            view_my_transactions(connection, current_user)
        elif choice == '5':
            return None  # Logout
        else:
            print("Invalid choice! Please try again.")

def view_available_books(connection):
    """Display books available for issuing"""
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT book_id, title, author, isbn, available_quantity FROM books WHERE available_quantity > 0 ORDER BY book_id"
        cursor.execute(query)
        books = cursor.fetchall()
        
        print("\n=== Available Books ===")
        print(f"{'ID':<5} {'Title':<30} {'Author':<20} {'ISBN':<15} {'Available':<10}")
        print("-" * 80)
        for book in books:
            print(f"{book['book_id']:<5} {book['title']:<30} {book['author']:<20} {book['isbn']:<15} {book['available_quantity']:<10}")
    except Error as e:
        print(f"Error fetching available books: {e}")
    finally:
        cursor.close()

def issue_book(connection, current_user):
    """Issue a book to the current user"""
    print("\n=== Issue Book ===")
    view_available_books(connection)
    book_id = input("Enter book ID to issue: ")
    
    try:
        cursor = connection.cursor()
        
        # Check if book is available
        check_query = "SELECT available_quantity FROM books WHERE book_id = %s"
        cursor.execute(check_query, (book_id,))
        result = cursor.fetchone()
        
        if not result or result[0] <= 0:
            print("Book not available for issuing!")
            return
        
        # Calculate due date (14 days from now)
        due_date = datetime.now() + timedelta(days=14)
        
        # Create transaction
        transaction_query = """INSERT INTO transactions (user_id, book_id, transaction_type, due_date, status) 
                              VALUES (%s, %s, 'issue', %s, 'active')"""
        cursor.execute(transaction_query, (current_user['user_id'], book_id, due_date.date()))
        
        # Update book availability
        update_query = "UPDATE books SET available_quantity = available_quantity - 1 WHERE book_id = %s"
        cursor.execute(update_query, (book_id,))
        
        connection.commit()
        print("Book issued successfully!")
        print(f"Due date: {due_date.date()}")
    except Error as e:
        print(f"Error issuing book: {e}")
    finally:
        cursor.close()

def return_book(connection, current_user):
    """Return a book issued by the current user"""
    print("\n=== Return Book ===")
    view_my_transactions(connection, current_user)
    transaction_id = input("Enter transaction ID to return: ")
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Check if transaction exists and belongs to current user
        check_query = """SELECT t.transaction_id, t.book_id, b.title 
                        FROM transactions t 
                        JOIN books b ON t.book_id = b.book_id 
                        WHERE t.transaction_id = %s AND t.user_id = %s AND t.status = 'active'"""
        cursor.execute(check_query, (transaction_id, current_user['user_id']))
        transaction = cursor.fetchone()
        
        if not transaction:
            print("Invalid transaction ID or book already returned!")
            return
        
        # Update transaction status
        update_transaction = "UPDATE transactions SET status = 'completed' WHERE transaction_id = %s"
        cursor.execute(update_transaction, (transaction_id,))
        
        # Update book availability
        update_book = "UPDATE books SET available_quantity = available_quantity + 1 WHERE book_id = %s"
        cursor.execute(update_book, (transaction['book_id'],))
        
        connection.commit()
        print(f"Book '{transaction['title']}' returned successfully!")
    except Error as e:
        print(f"Error returning book: {e}")
    finally:
        cursor.close()

def view_my_transactions(connection, current_user):
    """Display current user's transactions"""
    try:
        cursor = connection.cursor(dictionary=True)
        query = """SELECT t.transaction_id, b.title, t.transaction_type, t.transaction_date, t.due_date, t.status 
                  FROM transactions t 
                  JOIN books b ON t.book_id = b.book_id 
                  WHERE t.user_id = %s 
                  ORDER BY t.transaction_date DESC"""
        cursor.execute(query, (current_user['user_id'],))
        transactions = cursor.fetchall()
        
        print("\n=== My Transactions ===")
        print(f"{'TID':<5} {'Book Title':<30} {'Type':<10} {'Date':<12} {'Due Date':<12} {'Status':<10}")
        print("-" * 80)
        for trans in transactions:
            print(f"{trans['transaction_id']:<5} {trans['title']:<30} {trans['transaction_type']:<10} {trans['transaction_date'].strftime('%Y-%m-%d'):<12} {str(trans['due_date']):<12} {trans['status']:<10}")
    except Error as e:
        print(f"Error fetching transactions: {e}")
    finally:
        cursor.close()
