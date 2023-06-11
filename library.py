class Library():

    def __init__(self, name, id, session):
        self.id = id
        self.collection = "collection_"+str(id)
        self.name = name  
        self.session = session

    def addBook(self, book_title):
        self.session.execute(f'INSERT INTO collection_{self.id} (title, availability) VALUES (\'{book_title}\', true);')
   
    def removeBook(self, book_title):
       self.session.execute(f"DELETE FROM collection_{self.id} WHERE title = '{book_title}';")
         
