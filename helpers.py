def correctLending(outcome_lend, client, book_title, q_lib_id):
    with client.lock:
        q = client.session.execute_async(q_lib_id, (client.library, )).result()
        collection_id = client.getAtribute(q)
        text = f"SELECT * FROM collection_{str(collection_id)} WHERE title = '{book_title}' ALLOW FILTERING;"
        q = client.session.execute_async(text).result()
        isAvailable = client.getAtribute(q,"availability")

        isInShelf = book_title in client.getShelf()
        books = []
        text = f"SELECT title FROM collection_{str(collection_id)}" 
        q = client.session.execute_async(text).result()
        for row in q:
            books.append(row.title)
        isInCollection = book_title in books

    # 1 --> lending sucessful --> check if book is not available and if the book is in users shelf
        if outcome_lend:
            if not isAvailable and isInShelf and isInCollection:
                return 1
    # 0 --> lending unsuccesfull --> check if book is not available or if book is not in collection 
        else:
            if not isAvailable:
                return 1
        print(f"Lending: {client.name} vs {book_title}: {isAvailable=}, {isInShelf=}, {isInCollection=}")
        return 0

def correctReturning(outcome_lend, client, book_title, q_lib_id):
    with client.lock:
        q = client.session.execute_async(q_lib_id, (client.library, )).result()
        collection_id = client.getAtribute(q)
        text = f"SELECT * FROM collection_{str(collection_id)} WHERE title = '{book_title}' ALLOW FILTERING;"
        q = client.session.execute_async(text).result()
        isAvailable = client.getAtribute(q,"availability")

        books = []
     
        text = f"SELECT title FROM collection_{str(collection_id)}" 
        q = client.session.execute_async(text).result()
        for row in q:
            books.append(row.title)
        isInCollection = book_title in books

        isInShelf = book_title in client.getShelf()
        # 1 --> returning succesful --> check if this book is not in clients shelf and if it is available
        if outcome_lend:
            if isAvailable and not isInShelf and isInCollection:
                return 1
        # 0 --> returning unsuccesful --> check if this book is not in collection of library or user does not have it
        else:
            if (not isInCollection and not isAvailable) or (not isInShelf and isInCollection):
                return 1
        print(f"Returning: {client.name} vs {book_title}: {isAvailable=}, {isInShelf=}, {isInCollection=}")
        return 0
