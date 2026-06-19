import json
import os

FILE_NAME = "library_books.json"


class Book:
    def __init__(self, book_id, title, author, issued=False):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.issued = issued

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "issued": self.issued
        }


class Library:
    def __init__(self):
        self.books = {}
        self.load_books()

    def load_books(self):
        if os.path.exists(FILE_NAME):
            try:
                with open(FILE_NAME, "r") as file:
                    data = json.load(file)

                    for book in data:
                        self.books[book["book_id"]] = Book(
                            book["book_id"],
                            book["title"],
                            book["author"],
                            book["issued"]
                        )
            except:
                self.books = {}

    def save_books(self):
        data = [book.to_dict() for book in self.books.values()]

        with open(FILE_NAME, "w") as file:
            json.dump(data, file, indent=4)

    def add_book(self):
        book_id = input("Enter Book ID: ")

        if book_id in self.books:
            print("Book ID already exists!")
            return

        title = input("Enter Title: ")
        author = input("Enter Author: ")

        self.books[book_id] = Book(
            book_id,
            title,
            author
        )

        self.save_books()
        print("Book Added Successfully!")

    def search_book(self):
        keyword = input(
            "Enter Title or Author: "
        ).lower()

        found = False

        for book in self.books.values():

            if (keyword in book.title.lower()
                    or keyword in book.author.lower()):

                print("\n--------------------")
                print("Book ID :", book.book_id)
                print("Title   :", book.title)
                print("Author  :", book.author)

                if book.issued:
                    print("Status  : Issued")
                else:
                    print("Status  : Available")

                found = True

        if not found:
            print("No matching books found.")

    def issue_book(self):
        book_id = input(
            "Enter Book ID to Issue: "
        )

        if book_id not in self.books:
            print("Book not found.")
            return

        if self.books[book_id].issued:
            print("Book already issued.")
            return

        self.books[book_id].issued = True

        self.save_books()

        print("Book Issued Successfully!")

    def return_book(self):
        book_id = input(
            "Enter Book ID to Return: "
        )

        if book_id not in self.books:
            print("Book not found.")
            return

        if not self.books[book_id].issued:
            print("Book already available.")
            return

        self.books[book_id].issued = False

        self.save_books()

        print("Book Returned Successfully!")

    def display_books(self):

        if not self.books:
            print("No books available.")
            return

        print("\n========== BOOK LIST ==========")

        for book in self.books.values():

            status = (
                "Issued"
                if book.issued
                else "Available"
            )

            print(
                f"{book.book_id:<10}"
                f"{book.title:<25}"
                f"{book.author:<20}"
                f"{status}"
            )

    def generate_report(self):

        total_books = len(self.books)

        issued_books = sum(
            1 for book in self.books.values()
            if book.issued
        )

        available_books = (
            total_books - issued_books
        )

        print("\n===== LIBRARY REPORT =====")
        print("Total Books     :", total_books)
        print("Issued Books    :", issued_books)
        print("Available Books :", available_books)


def main():

    library = Library()

    while True:

        print("\n===== LIBRARY BOOK INVENTORY =====")
        print("1. Add Book")
        print("2. Search Book")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Display Books")
        print("6. Generate Report")
        print("7. Exit")

        choice = input(
            "Enter Your Choice: "
        )

        if choice == "1":
            library.add_book()

        elif choice == "2":
            library.search_book()

        elif choice == "3":
            library.issue_book()

        elif choice == "4":
            library.return_book()

        elif choice == "5":
            library.display_books()

        elif choice == "6":
            library.generate_report()

        elif choice == "7":
            print("Thank You!")
            break

        else:
            print("Invalid Choice!")


if __name__ == "__main__":
    main()