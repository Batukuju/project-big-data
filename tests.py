from library import Library
from client import Client
from cassandra.cluster import Cluster
import csv
import unittest
from helpers import correctLending, correctReturning
import threading
from threading import Lock
import numpy as np

KEYSPACE_NAME = "libraries_system"
N = 100
class Test_1(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.books = []
        with open("data/books.csv") as f:
            data = csv.DictReader(f)
            for row in data:
                self.books.append(row["title"])
        self.cluster = Cluster(executor_threads=5, connect_timeout=30)
        self.session = self.cluster.connect(KEYSPACE_NAME)
        self.client = Client("Ewa", "Grzeskowiak", "Miejska", self.session)
        self.client_2 = Client("Adam", "Nowak", "Pod Wierzba", self.session)
        self.q_lib_id = self.session.prepare(f"SELECT * FROM libraries WHERE name = ? ALLOW FILTERING;")
    def test_1(self):
        """
        1 client N times reserves book and N times returns tha book (iterate over all books)
        """
        for i in range(100):
            title = self.books[i%len(self.books)]
            out_lending = self.client.lendBook(title)
            assert correctLending(out_lending, self.client, title, self.q_lib_id), f"Sth went wrong with lending {title}, {i}"
            out_returning = self.client.returnBook(title)
            assert correctReturning(out_returning, self.client, title, self.q_lib_id), f"Sth went wrong with returning {title}, {i}"

    def test_2(self):
        """
        2 different clients concurrently reserving/returning books (over all books, N times, partially random)
        """
        def target_2(client, books, id, session):
            for i in range(N):
                idx = np.random.randint(0, len(books))
                book_title = books[idx]
                coin = np.random.randint(0, 2)
                if coin:
                    #print(i, ",",id, ". Lending book:", book_title)
                    outcome_lend = client.lendBook(book_title)
                    assert correctLending(outcome_lend, client, book_title, self.q_lib_id), f"Sth went wrong with lending the book: {book_title}"
                else:
                    #print(i, ",",id, ". Returning book:", book_title)
                    outcome_return = client.returnBook(book_title)
                    assert correctReturning(outcome_return, client, book_title, self.q_lib_id), f"Sth went wrong with returning the book: {book_title}"

        threads_list = []

        x = threading.Thread(target=target_2, args=(self.client, self.books, 1, self.session))
        x.start()
        threads_list.append(x)
        y = threading.Thread(target=target_2, args=(self.client_2, self.books, 20, self.session))
        y.start()
        threads_list.append(y)

        for th in threads_list:
            th.join()

    def test_3(self):
        """
        2 different clients concurrently reserving/returning books (over all books, N times, trying to get all the books)
        """
        def target_3(client, books, id, session):
            for i in range(N):
                book_title = books[(i)%len(books)]
                #print(i, ",",id, ". Lending book:", book_title)
                outcome_lend = client.lendBook(book_title)
                assert correctLending(outcome_lend, client, book_title, self.q_lib_id), f"Sth went wrong with lending the book: {book_title}"
                #print(i, ",",id, ". Returning book:", book_title)
                outcome_return = client.returnBook(book_title)
                assert correctReturning(outcome_return, client, book_title, self.q_lib_id), f"Sth went wrong with returning the book: {book_title}"

        threads_list = []

        x = threading.Thread(target=target_3, args=(self.client, self.books, 1, self.session))
        x.start()
        threads_list.append(x)
        y = threading.Thread(target=target_3, args=(self.client_2, self.books, 20, self.session))
        y.start()
        threads_list.append(y)


        for th in threads_list:
            th.join()


    def test_4(self):
        """
        2 different clients fight for one book (reserving/returning N times)
        """
        def target_4(client, books, id, session):
            for i in range(N):
                book_title = "Władca Pierścieni"
                coin = np.random.randint(0, 2)
                if coin:
                    #print(i, ",",id, ". Lending book:", book_title)
                    outcome_lend = client.lendBook(book_title)
                    assert correctLending(outcome_lend, client, book_title, self.q_lib_id), f"Sth went wrong with lending the book: {book_title}"
                else:
                    #print(i, ",",id, ". Returning book:", book_title)
                    outcome_return = client.returnBook(book_title)
                    assert correctReturning(outcome_return, client, book_title, self.q_lib_id), f"Sth went wrong with returning the book: {book_title}"

        threads_list = []

        x = threading.Thread(target=target_4, args=(self.client, self.books, 1, self.session))
        x.start()
        threads_list.append(x)
        y = threading.Thread(target=target_4, args=(self.client_2, self.books, 20, self.session))
        y.start()
        threads_list.append(y)

        for th in threads_list:
            th.join()



unittest.main()
    