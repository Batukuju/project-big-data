from threading import Lock
class Client():
    # table = 'Clients'
    lock = Lock()
    def __init__(self, name, surname, library, session):
        self.ID = -1
        self.shelf = "shelf_"
        self.session = session
        self.name = name
        self.surname = surname
        self.library = library

        self.createID()

    #reservation methods
    def lendBook(self, book_title):
        text = f"SELECT * FROM libraries WHERE name = '{self.library}' ALLOW FILTERING;"
        with self.lock:
            q = self.session.execute_async(text).result()
            collection_id = self.getAtribute(q)


            text = f"SELECT * FROM collection_{str(collection_id)} WHERE title = '{book_title}' ALLOW FILTERING;"
            q = self.session.execute_async(text).result()
            isAvailable = self.getAtribute(q,"availability")
            if isAvailable:
                self.addBook(book_title)
                self.session.execute_async(f"UPDATE collection_{collection_id} SET availability = False WHERE title =  '{book_title}';")

                return 1
            else:
                # print(f"The book:\t{book_title} is unavailable.")
                return 0
                #pass
    def returnBook(self, book_title):       
        text = f"SELECT * FROM libraries WHERE name = '{self.library}' ALLOW FILTERING;"
        with self.lock:
            q = self.session.execute_async(text).result()
            collection_id = self.getAtribute(q, "id")
            assert collection_id is not None, f"There is no collection_{collection_id}"


            text = f"SELECT * FROM collection_{str(collection_id)} WHERE title = '{book_title}' ALLOW FILTERING;"
            q = self.session.execute_async(text).result()
            isAvailable = self.getAtribute(q,"availability")
            if isAvailable is False:
                self.session.execute_async(f"UPDATE collection_{collection_id} SET availability = True WHERE title =  '{book_title}';")
                self.session.execute(f"DELETE FROM shelf_{self.ID} WHERE title = '{book_title}';")
                return 1
            else:
                return 0
                #print(f"The book:\t{book_title} has never been rented")

    # get books of this client
    def getShelf(self):
        books = []
        text = f"SELECT * FROM {self.shelf} ;"
        q = self.session.execute_async(text).result()
        for row in q:
            books.append(row.title)
        return books
    #add update remove
    def createID(self):
        with self.lock:
            rows =  self.session.execute(f"SELECT * from clients where name = '{self.name}' AND surname = '{self.surname}' ALLOW FILTERING;")
        
            for i in rows:
                self.ID = i.id
                self.shelf += self.ID

    def addBook(self, book_title):
        self.session.execute(f'INSERT INTO shelf_{self.ID} (title) VALUES (\'{book_title}\');')
        
    def removeBook(self, book_title):
        self.session.execute(f"DELETE FROM shelf_{self.ID} WHERE title = '{book_title}';")


    def getAtribute(self, sth, atribute = None):
        for i in sth:
            for name, el in zip(i._fields,i):
                if atribute is None or atribute == name:
                    return el
