from client import Client
class Library():
    lock = Client.lock
    def __init__(self, name, session):
        self.ID = -1
        self.collection = "collection_"
        self.name = name  
        self.session = session
        self.createID()

    def createID(self):
        with self.lock:
            rows =  self.session.execute(f"SELECT * from libraries where name = '{self.name}' ALLOW FILTERING;")
            for i in rows:
                self.ID = i.id
                self.collection += self.ID
        

    def addBook(self, book_title):
        with self.lock:
            self.session.execute(f'INSERT INTO collection_{self.ID} (title, availability) VALUES (\'{book_title}\', true);')
   
    def removeBook(self, book_title):
        with self.lock:
            rows =  self.session.execute(f"SELECT count(*) from collection_{self.ID} where title = '{book_title}' ALLOW FILTERING;")
            self.session.execute(f"DELETE FROM collection_{self.ID} WHERE title = '{book_title}';")
    
    def getAtribute(self, sth, atribute = None):
        for i in sth:
            for name, el in zip(i._fields,i):
                if atribute is None or atribute ==name:
                    return el
        assert("GETTING ERROR")