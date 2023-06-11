from library import Library
from client import Client
import csv
import uuid
from cassandra.cluster import Cluster

def showOptions(table, category):
    for row in table:
        for name, el in zip(row._fields,row):
            if name == category:
                print(f"\"{el}\"", end='    ')
    print()

def getAtribute(sth, atribute = None):
        for i in sth:
            for name, el in zip(i._fields,i):
                if atribute is None or atribute == name:
                    return el
                
        return None
def show(r):
    for i in r:
        # print(i)
        for name, el in zip(i._fields,i):
            print(name, " ", el)
        print()

def lendBook(answer, lib, collection_id, client_id, session):
    #LENDING BOOK
    while True:
        tab = '\t'
        while answer not in ("y","n"):
            print(f"{tab}Your answer '{answer}' was not correct. You need to type y or n. So once again...")
            answer = input(f"{tab}Would you like to make another reservation? (y/n): ")

        if answer == "y":
            print(f"{tab}Here is the list of all currently available books in {lib}.")
            collection_id = getAtribute(session.execute(f"SELECT * FROM libraries WHERE name = '{lib}' ALLOW FILTERING;"), "id")
            row_books = session.execute(f"SELECT * FROM collection_{collection_id} WHERE availability = True  ALLOW FILTERING;")
            print(tab, end = "")
            showOptions(row_books, "title")

            # BOOK RESERVARTION
            title = input(f"{tab}Here you can type the name of the book to make reservation: ")
            isAvailable = getAtribute(session.execute(f"SELECT * FROM collection_{str(collection_id)} WHERE title = '{title}' ALLOW FILTERING;"),"availability")
            
            while isAvailable is None or isAvailable is False:
                print(f"{tab}The book '{title}' is not in currently available collection of library '{lib}'")
                title = str(input(f"{tab}Type the title again: "))
                isAvailable = getAtribute(session.execute(f"SELECT * FROM collection_{str(collection_id)} WHERE title = '{title}' ALLOW FILTERING;"),"availability")

            # LIBRARY UPDATE
            session.execute(f"UPDATE collection_{collection_id} SET availability = False WHERE title =  '{title}';")
            
            #UPDATE CLIENT'S SHELF
            session.execute(f"INSERT INTO shelf_{str(client_id)} (title) VALUES (\'{title}\');")
            print(f"{tab}You succesfully lend the book '{title}'.")
                        
            answer = input(f"\n{tab}Would you like to make another reservation? (y/n): ")
        
        if answer =="n":
            # print("Okay!")
            return session


def returnBook(answer, lib, client_id, session):
    tab = "\t"
    client_id = str(client_id)
    #RETuRNING BOOK
    while True:
        while answer not in ("y","n"):
            print(f"{tab}Your answer '{answer}' was not correct. You need to type y or n. So once again...")
            answer = input(f"\n{tab}Would you like to return another book? (y/n): ")

        if answer == "y":
            print(f"{tab}Here is the list of all your books.", end = "\n\t")
            showOptions(session.execute(f"SELECT * FROM shelf_{client_id};"), "title")
            
            title = input(f"{tab}Type the title of the book to return: ")
            isAvailable = getAtribute(session.execute(f"SELECT * FROM shelf_{client_id} WHERE title = '{title}' ALLOW FILTERING;"),"title")
            
            while isAvailable is None:
                print(tab+"Wrong title.")
                title = str(input(f"{tab}Type the title again: "))
                isAvailable = getAtribute(session.execute(f"SELECT * FROM shelf_{client_id} WHERE title = '{title}' ALLOW FILTERING;"),"title")

            #UPDATE LIBRARY
            collection_id = getAtribute(session.execute(f"SELECT * FROM libraries WHERE name = '{lib}' ALLOW FILTERING;"), "id")
            session.execute(f"UPDATE collection_{collection_id} SET availability = True WHERE title =  '{title}';")

            #UPDATE CLIENT'S SHELF
            session.execute(f"DELETE FROM shelf_{client_id} WHERE title = '{title}';")

            print(f"{tab}You succesfully lend the book '{title}'.")     
            answer = input(f"\n{tab}Would you like to return another book? (y/n): ")
        
        if answer =="n":
            # print("Okay!")
            return session



if __name__ == "__main__":
    tab ="\t"
    #INITIALIZATION
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect("libraries_system")   

    print("Hi! Welcome in our library system!\n")
    
    print("Before we go inside, please register yourself")

    #LOGIN
    print('\nLOGIN')
    name = input(tab+"Please enter your name: ")
    surname = input(tab+"Please entre your surnaname: ")
    client_id =  getAtribute(session.execute(f"SELECT * FROM clients WHERE name = '{name}' AND surname = '{surname}' ALLOW FILTERING;"), "id")
    
    if client_id is None:
        #chose library
        print("Which library would you like to choose?")
        row_libs = session.execute("SELECT * FROM libraries;") 
        showOptions(row_libs, "name")
        lib =  input("Type the name here: ")
        collection_id = getAtribute(session.execute(f"SELECT * FROM libraries WHERE name = '{lib}' ALLOW FILTERING;"), "id")
        while None is collection_id:
            print(f"There is no such a library as '{lib}' in our system.")
            print("Available libraries: ")
            showOptions(row_libs, "name")
            lib = input("Type the library name: ")
        print(f"Great choice! Library {lib} has a great collection of various books.")

        client_id = str(uuid.uuid4().hex)
        shelf = "shelf_" + client_id
        session.execute(f'CREATE TABLE IF NOT EXISTs shelf_{client_id} (title text PRIMARY KEY);')
        session.execute(f"INSERT INTO clients (id, name, surname, library, shelf) VALUES (\'{client_id}\', \'{name}\', \'{surname}\', \'{lib}\', \'{shelf}\');")
        client = Client(name, surname, lib, session)
        print(tab+"Thank you for signing in!")
    lib =  getAtribute(session.execute(f"SELECT * FROM clients WHERE id = '{client_id}' ALLOW FILTERING;"), "library")
    collection_id =  getAtribute(session.execute(f"SELECT * FROM libraries WHERE name = '{lib}' ALLOW FILTERING;"), "id")

    print(lib)
    print("\nRESERVATION")
    answer = input(tab+"Would you like to make a reservation? (y/n): ")
    session = lendBook(answer, lib, collection_id, client_id, session)

    showOptions(session.execute(f"SELECT * FROM shelf_{client_id};"), "title")
    
    print("\nRETURNING")
    answer = input(tab+"Would you like to return any book? (y/n): ")
    session = returnBook(answer, lib, client_id, session)

    print("Thanks for a visit!")



   










    

    


















    
    # title = "Zuzanka na trawie"

    # clients[1].lendBook(title)
    # clients[1].returnBook(title)

    # print("collectioons")
    # for l in libraries:
    #     print("library: ",l.ID)
    #     show(session.execute(f"SELECT * FROM collection_{l.ID};"))    

    # libraries[0].removeBook(title)
    # libraries[1].removeBook(title)

    cluster.shutdown