from library import Library
from client import Client
import csv
from cassandra.cluster import Cluster

def show(r):
    for i in r:
        print(i)
        for name, el in zip(i._fields,i):
            print(name, " ", el)
        print()

def returnLists(session):
    clients = []

    with open("data/clients.csv") as f:
        data = csv.DictReader(f)
        for i, row in enumerate(data):
            name = row["name"]
            surname = row["surname"]
            library = row["library"]
            clients.append(Client(name, surname, library, session))

    show(session.execute("SELECT * from clients;"))
    libraries = []


    with open("data/libraries.csv") as f:
        data = csv.DictReader(f)
        for i, row in enumerate(data):
            name = row["name"]
            libraries.append(Library(name, session))

    return clients, libraries

if __name__ == "__main__":
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect("libraries_system")   

    clients, libraries = returnLists(session)
    

    book_title = "Pan Tadeusz"
    show(session.execute('SELECT * FROM libraries;'))
    libraries[0].removeBook(book_title)

    libraries[0].addBook(book_title)
    libraries[1].addBook(book_title)

    clients[1].lendBook(book_title)
    clients[1].returnBook(book_title)
    
    libraries[0].removeBook(book_title)

    cluster.shutdown
