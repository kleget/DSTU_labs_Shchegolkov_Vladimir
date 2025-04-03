class Cover: # обожка
    def __init__(self, cover_type):
        self.cover_type = cover_type


class Author:
    def __init__(self, name):
        self.name = name


class Book:
    def __init__(self, title, author, isbn, year, cover_type):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.cover = Cover(cover_type)

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author.name}, Year: {self.year}"


class Publisher:
    def __init__(self, name):
        self.name = name
        self.books = []

    def add_book(self, book):
        self.books.append(book)


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def list_books(self):
        for book in self.books:
            print(book)

    def search_by_author(self, author_name):
        return [book for book in self.books if book.author.name == author_name]

    def search_by_year(self, year):
        return [book for book in self.books if book.year == year]


# Демонстрационная программа
author1 = Author("Лев Толстой")
author2 = Author("Федор Достоевский")

book1 = Book("Война и мир", author1, "123456789", 1869, "Твердая")
book2 = Book("Преступление и наказание", author2, "987654321", 1866, "Мягкая")

publisher = Publisher("Русские классики")
publisher.add_book(book1)
publisher.add_book(book2)

library = Library()
library.add_book(book1)
library.add_book(book2)

print("Все книги в библиотеке:")
library.list_books()

print("\nПоиск книг по автору 'Лев Толстой':")
for book in library.search_by_author("Лев Толстой"):
    print(book)

print("\nПоиск книг по году издания 1866:")
for book in library.search_by_year(1866):
    print(book)