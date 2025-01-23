from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Book class to represent each book
class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.checked_out = False

    def __str__(self):
        return f"{self.title} by {self.author}"

# Library class to manage the collection of books
class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title, author, isbn):
        book = Book(title, author, isbn)
        self.books.append(book)

    def list_books(self):
        return self.books

    def check_out(self, book_index):
        if 0 <= book_index < len(self.books):
            book = self.books[book_index]
            if not book.checked_out:
                book.checked_out = True
                return f"You have checked out {book.title}."
            else:
                return f"{book.title} is already checked out."
        return "Invalid book index."

    def return_book(self, book_index):
        if 0 <= book_index < len(self.books):
            book = self.books[book_index]
            if book.checked_out:
                book.checked_out = False
                return f"Thank you for returning {book.title}."
            else:
                return f"{book.title} was not checked out."
        return "Invalid book index."

# Initialize the library
library = Library()

@app.route('/')
def index():
    return render_template('index.html', books=library.list_books())

@app.route('/add', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    isbn = request.form['isbn']
    library.add_book(title, author, isbn)
    return redirect(url_for('index'))

@app.route('/checkout/<int:book_index>')
def check_out(book_index):
    message = library.check_out(book_index)
    return render_template('index.html', books=library.list_books(), message=message)

@app.route('/return/<int:book_index>')
def return_book(book_index):
    message = library.return_book(book_index)
    return render_template('index.html', books=library.list_books(), message=message)

if __name__ == '__main__':
    app.run(debug=True)
