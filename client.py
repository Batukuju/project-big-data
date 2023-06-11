class Client():
    def __init__(self, name, surname, library, id, session):
        self.id = id
        self.session = session
        self.name = name
        self.surname = surname
        self.library = library
        # self.shelf = "shelf_" + str(id) 

    def lendBook(self, book_title):
        text = f"SELECT * FROM libraries WHERE name = '{self.library}' ALLOW FILTERING;"
        collection_id = self.getAtribute(self.session.execute(text))

        text = f"SELECT * FROM collection_{str(collection_id)} WHERE title = '{book_title}' ALLOW FILTERING;"
        isAvailable = self.getAtribute(self.session.execute(text),"availability")

        if isAvailable:
            self.session.execute(f'INSERT INTO shelf_{self.id} (title) VALUES (\'{book_title}\');')
            a = self.session.execute(f"UPDATE collection_{collection_id} SET availability = False WHERE title =  '{book_title}';")
            return a
        else:
            print(f"The book:\t{book_title} is unavailable.")

    def returnBook(self, book_title):       
        text = f"SELECT * FROM libraries WHERE name = '{self.library}' ALLOW FILTERING;"
        collection_id = self.getAtribute(self.session.execute(text), "id")
        assert collection_id is not None, f"There is no collection_{collection_id}"
        text = f"SELECT * FROM collection_{str(collection_id)} WHERE title = '{book_title}' ALLOW FILTERING;"
        q = self.session.execute(text)
        isAvailable = self.getAtribute(q,"availability")

        if isAvailable is False:
            self.session.execute(f"UPDATE collection_{collection_id} SET availability = True WHERE title =  '{book_title}';")
            self.session.execute(f"DELETE FROM shelf_{self.id} WHERE title = '{book_title}';")
        else:
            print(f"The book:\t{book_title} has never been rented")

    def getAtribute(self, sth, atribute = None):
        for i in sth:
            for name, el in zip(i._fields,i):
                if atribute is None or atribute == name:
                    return el
