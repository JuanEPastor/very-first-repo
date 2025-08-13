
from pathlib import Path

import json 
import random
from datetime import datetime, timedelta


class Book:
    
    def __init__(self, id, title, author, isbn, publisher_house=None, quantity=1, year=None):
        self.id = id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publisher_house = publisher_house
        self.year = year
        self.quantity = quantity
        self.available = quantity
        
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "publisher_house": self.publisher_house,
            "year": self.year,
            "quantity": self.quantity,
            "available": self.available
        }
    
    
    def __str__(self):
        return (f"ID: ({self.id} | Title: {self.title} | Author: {self.author} | " 
                f"ISBN: {self.isbn} | Publisher_House: {self.publisher_house} | "
                f"Year: {self.year} | Available: {self.quantity}/{self.available})")
        

class User:
    
    def __init__(self, id, name, email, membership_type="standard"):
        self.id = id
        self.name = name
        self.email = email
        self.membership_type = membership_type
        self.borrowed_books = []
        
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "membership_type": self.membership_type,
            "borrowed_books": self.borrowed_books
        }
    
    def __str__(self):
        return (f"ID: {self.id} | Name: {self.name} | Email: {self.email} | "
                f"Type: {self.membership_type} | Borrowed Books: {len(self.borrowed_books)}")
        
class Library:
    def __init__(self):
        self.books = {}
        self.users = {}
        self.transactions = []
        self.next_book_id = 1
        self.next_user_id = 1
        self.data_file = self.get_data_file()
    def get_data_file(self):
        """Returns the path to the data file."""
        script_dir = Path(__file__).parent.absolute()
        return script_dir / "library_Alexandria.json"
        
    def add_book(self, title, author, isbn, publisher_house=None, quantity=1, year=None):
        book = Book(self.next_book_id, title, author, isbn, publisher_house, quantity, year)
        self.books[book.id] = book
        self.next_book_id += 1
        messages=[
            f"📜 '{title}' added to our sacred collection. Gogol's flames cannot reach it here",
            f"The wisdom of '{title}' now graces our halls...",
            f"Another treasure added: '{title}' to our inmmortal library",
            f"📖 '{title}' enshrined in our eternal library"
        ]
        msg = random.choice(messages)
        self.log_transaction("ADD_BOOK", msg)
        return msg
        
    def find_book(self, **criteria):
        results = []
        for book in self.books.values():
            match = True
            for key, value in criteria.items():
                if key == "title" and value.lower() not in book.title.lower():
                    match = False
                elif key == "author" and value.lower() not in book.author.lower():
                    match = False
                elif key == "isbn" and value != book.isbn:
                    match = False
                elif key == "publisher_house" and value.lower() not in (book.publisher_house or "").lower():
                    match = False
                elif key == "year" and value != book.year:
                    match = False
                elif key == "id" and value != book.id:
                    match = False
                elif key == "available" and value > book.available:
                    match = False
            if match:
                results.append(book)
        return results

    def register_user(self, name, email, membership_type="standard"):
        user = User(self.next_user_id, name, email, membership_type)
        self.users[user.id] = user
        self.next_user_id += 1
        self.log_transaction("ADD_USER", f"Registered user {name}")
        return user

    def borrow_book(self, user_id, book_id, days= 14):
        if user_id not in self.users:
            return "User not found."
        if book_id not in self.books:
            return "Book not found."
    
        book = self.books[book_id]
        user= self.users[user_id]
    
        if book.available <= 0:
            return "No copies available."
    
        if len(user.borrowed_books) >= 7:
            return "User has reached the maximum number of borrowed books."
        
        book.available -= 1
    
        due_date = datetime.now() + timedelta(days=days)
        loan = {
            "user_id": user.id,
            "book_id": book.id,
            "borrow_date": datetime.now().strftime("%Y-%m-%d"),
            "due_date": due_date.strftime("%Y-%m-%d"),
            "returned": False
    }

        user.borrowed_books.append(loan)
        self.log_transaction("BORROW", f"User {user.id} borrowed book {book.title}")
        
        phrases =[
            "Guard this knowledge as the ancients guarded the flame",
            "Protect this wisdom from Gogol's destructive fire",
            "This book/scroll contains truths thaT no flame can erase"
            
        ]
        success_msg = f"Borrowed successfully. Due date: {due_date.strftime('%Y-%m-%d')}"
        return f"📖 {success_msg}\n{random.choice(phrases)}"

    def return_book(self, user_id, book_id):
        if user_id not in self.users:
            return "User not found."
        if book_id not in self.books:
            return "Book not found."
    
        user = self.users[user_id]
        book = self.books[book_id]
    
        for loan in user.borrowed_books:
            if loan["book_id"] == book_id and not loan["returned"]:
                loan["returned"] = True
                book.available += 1
                self.log_transaction("RETURN", f"User {user.id} returned book {book.title}")
                return f"📚 The Book/Scroll returns safely to our protection.\n" \
                        "The knowledge within has survived another journey."
        
        return "This book was not borrowed by the user."

    def log_transaction(self, action, details):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        action_titles = {
            "ADD_BOOK": "BOOK/ SCROLL ENTOMBED",
            "ADD_USER": "NEW SCHOLAR REGISTERED",
            "BORROW": "WISDOM LOANED",
            "RETURN": "KNOWLEDGE RESTORED"
        }
        action = action_titles.get(action, action)          
        self.transactions.append({
            "timestamp": timestamp,
            "action": action,
            "details": details
    })
    
    def save_data(self):
        data = {
            "books": [book.to_dict() for book in self.books.values()],
            "users": [user.to_dict() for user in self.users.values()],
            "transactions": self.transactions,
            "next_book_id": self.next_book_id,
            "next_user_id": self.next_user_id
    }
        try:
        
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return f"Data saved to {self.data_file}"
        except Exception as e:
            return f"Error saving data: {str(e)}"
        
        
    def load_data(self):
        try:
            if not self.data_file.exists():
                print("No data file found at {self.data_file}")
                return False
            
            
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
            self.books= {}
            for book_data in data["books"]:
                book = Book(
                    book_data["id"],
                    book_data["title"],
                    book_data["author"],
                    book_data["isbn"],
                    book_data.get("publisher_house"),
                    book_data.get("quantity"),
                    book_data.get("year")
            )
                book.available = book_data["available"]
                self.books[book.id] = book
        
            self.users = {}
            for user_data in data["users"]:
                user = User(
                    user_data["id"],
                    user_data["name"],
                    user_data["email"],
                    user_data.get("membership_type")
            )
                user.borrowed_books = user_data["borrowed_books"]
                self.users[user.id] = user
        
            self.transactions = data["transactions"]
            self.next_book_id = data["next_book_id"]    
            self.next_user_id = data["next_user_id"]
            
            print(f"📜Loaded: {len(self.books)} books, {len(self.users)} users from the archives.")
            return True
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return False

def display_menu():
    """It displays the main menu options"""
    print("\n" + "="*50)
    print("Welcome to the Great Library of Alexandria")
    print("Where the wisdom of the ages is preserved")
    print("against the ravages of time and ignorance.")
    print("Gógol!!, Why!?, Why did you do it?")
    print("="*50)
    print("1. Add Book")
    print("2. Register new User")
    print("3. Search Books")
    print("4. Borrow Book")
    print("5. Return Book")
    print("6. View all Users")
    print("7. View Records of Transactions")
    print("8. Save Data")
    print("9. Load Data")
    print("0. Exit")
    print("="*50)
    
def main():
    """Main function to run the library management system."""
    library = Library()
    print("Data file location: {library.data_file}")
   
    if library.load_data():
        print("Ancient books and scrolls have been recovered from the archives...")
        
    while True:
        display_menu()
        choice = input("Select an option: ")
        
        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            isbn = input("Enter book ISBN: ")
            publisher_house = input("Enter publisher house (optional): ") or None
            year = input("Enter publication year (optional): ") or None
            quantity = int(input("Enter quantity of copies: ") or 1)
            book = library.add_book(title, author, isbn, publisher_house, quantity, year)
            print(f"Book added successfully: {book}")
        
        elif choice == "2":
            name = input("Enter user name: ")
            email = input("Enter user email: ")
            membership_type = input("Enter membership type (standard/premium): ") or "standard"
            user = library.register_user(name, email, membership_type)
            print(f"User registered successfully: {user}")
        
        elif choice == "3":
            print("\nSearch Books")
            print("1. By Title")
            print("2. By Author")
            print("3. By ISBN")
            print("4. By Publisher House")
            print("5. By Year")
            print("6. By ID")
            print("7. By Available Copies")
            print("8. Back to Main Menu")
            search_choice = input("Select an option: ")
            
            if search_choice == "8":
                continue

            books = []

            if search_choice == "1":
                term = input("Enter title to search: ")
                books = library.find_book(title=term)
            elif search_choice == "2":
                term = input("Enter author to search: ")
                books = library.find_book(author=term)
            elif search_choice == "3":
                term = input("Enter ISBN to search: ")
                books = library.find_book(isbn=term)
            elif search_choice == "4":
                term = input("Enter publisher house to search: ")
                books = library.find_book(publisher_house=term)
            elif search_choice == "5":
                term = input("Enter year to search: ")
                books = library.find_book(year=term)
            elif search_choice == "6":
                term = int(input("Enter ID to search: "))
                books = library.find_book(id=term)
            elif search_choice == "7":
                min_available= int(input("Enter minimum available copies: "))
                books = library.find_book(available=min_available)
            else:
                print("invalid option.")
                books = []
            
            if books:
                print(f"\nFound {len(books)} book(s):")
                for book in books:
                    print(book)
                print("\n" + "="*50)
                print(f"🌌 {len(books)} fragments of eternity found")
                print("Remember: These truths survived Gogol's fire")
                print("="*50)
            else:
                print("No books found matching the criteria.")
        
        elif choice == "4":
            try:
                user_input = input("User ID: ")
                book_input = input("Book ID: ")
                
                if not user_input or not book_input or not user_input.isdigit() or not book_input.isdigit():
                     print("Error: IDs cannot be empty or non-numeric.")
                     continue
                
                user_id = int(input(user_input))
                book_id = int(input(book_input)) 
                result = library.borrow_book(user_id, book_id)
                print(result)
            except ValueError:
                print("Error: IDs must be numeric.")           
        
        elif choice == "5":
            try:
                user_input = input("User ID: ")
                book_input = input("Book ID: ")
                
                if not user_input or not book_input or not user_input.isdigit() or not book_input.isdigit():
                     print("Error: IDs cannot be empty or non-numeric.")
                     continue
                 
                user_id = int(input(user_input))
                book_id = int(input(book_input)) 
                result = library.return_book(user_id, book_id)
                print(result)
            except ValueError:
                print("Error: IDs must be numeric.")
        
        elif choice == "6":
            if library.users:
                print("\nRegistered Users:")
                for user in library.users.values():
                    print(user)
            else:
                print("No users registered.")

        elif choice == "7":
            print("\nTransaction Records:")
            for trans in library.transactions:
                print(f"{trans['timestamp']} - {trans['action']}: {trans['details']}")
        
        elif choice == "8":
            library.save_data()
            print("Data saved successfully.")   
        
        elif choice == "9":
            if library.load_data():
                print("Data loaded successfully!")
            else:
                print("No saved data found.")
        
        elif choice == "0":
            if input("Do you want to save data before exiting? (y/n): ").lower() == 'y':
                library.save_data()
                print("Data saved successfully.")
            print("\n" + "="*50)            
            print("="*50)
            print("You depat the Great Library of Alexandria, but its wisdom travel with you.")
            print("Remember: No flame can burn what lives in the mind")
            print("The books are safe with us, Gogol cannot touch them here.")
            print("Farewell, keeper of Infinite Worlds")
            print("="*50)
            break
        else:
            print("Invalid option. Please try again.")
    
if __name__ == "__main__":
    main()
        
    
   