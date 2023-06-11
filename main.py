from library import Library
from client import Client
import csv
from cassandra.cluster import Cluster

def show(r):
    for i in r:
        # print(i)
        for name, el in zip(i._fields,i):
            print(name, " ", el)
        print()

def getAtribute( sth, atribute = None):
    for i in sth:
        for name, el in zip(i._fields,i):
            if atribute is None or atribute ==name:
                return el
    assert("GETTING ERROR")

def returnLists(session):
    clients = []

    with open("data/clients.csv") as f:
        data = csv.DictReader(f)
        for row in (data):
            name = row["name"]
            surname = row["surname"]
            library = row["library"]
            id = getAtribute(session.execute(f"SELECT * from clients where name = '{name}' AND surname = '{surname}' ALLOW FILTERING;"), "id")
            clients.append(Client(name, surname, library, id, session))

    show(session.execute("SELECT * from clients;"))
    libraries = []

    with open("data/libraries.csv") as f:
        data = csv.DictReader(f)
        for row in (data):
            name = row["name"]
            id = getAtribute(session.execute(f"SELECT * from libraries where name = '{name}' ALLOW FILTERING;"), "id")
            libraries.append(Library(name, id, session))
    return clients, libraries

if __name__ == "__main__":
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect("libraries_system")   

    clients, libraries = returnLists(session)

    
    book_title = "Zuzanka na trawie"

    libraries[0].addBook(book_title)
    libraries[1].addBook(book_title)

    clients[1].lendBook(book_title)
    # clients[1].returnBook(book_title)

    print(clients[1].id)

    print("shelf_")
    for l in clients:
        print("client: ",l.id)
        show(session.execute(f"SELECT * FROM shelf_{l.id};"))    

    libraries[0].removeBook(book_title)
    libraries[1].removeBook(book_title)

    cluster.shutdown



  