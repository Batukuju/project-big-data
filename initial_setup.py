from cassandra.cluster import Cluster
import csv
import uuid
KEYSPACE_NAME = "libraries_system"

# Create keyspace
cluster = Cluster()
session = cluster.connect()
session.execute(f"CREATE KEYSPACE " + KEYSPACE_NAME + " WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 1};")
cluster.shutdown()

# Create tables
cluster = Cluster()
session = cluster.connect(KEYSPACE_NAME)

session.execute("CREATE TABLE clients( \
                                    id text PRIMARY KEY, \
                                    name text, \
                                    surname text, \
                                    shelf text, \
                                    library text, \
                                    );"
                )

session.execute("CREATE TABLE libraries( \
                                    id text PRIMARY KEY, \
                                    name text, \
                                    collection_id text, \
                                    );"
                )

# populate table clients
with open(r"data/clients.csv") as f:
    data = csv.DictReader(f)
    for i, row in enumerate(data):
        name = row["name"]
        surname = row["surname"]
        library = row["library"]
        id = str(uuid.uuid4().hex)
        shelf = "shelf_" + id

        session.execute(f"INSERT INTO clients(id, name, surname, library, shelf) \
        VALUES(\'{id}\', \'{name}\', \'{surname}\', \'{library}\', \'{shelf}\');")

        query = f'CREATE TABLE IF NOT EXISTs shelf_{id} (title text PRIMARY KEY);'
        session.execute(query)
# populate libraries
with open(r"data/libraries.csv") as l:
    with open(r"data/books.csv") as b:
        libraries = list(csv.DictReader(l))
        n_lib = len (list(libraries))
        books = list(csv.DictReader(b))
        n_books = len(books)
        for i, row in enumerate(libraries):
            name = row["name"]
            id = str(uuid.uuid4().hex)
            collection_id = "collection_" + id

            session.execute(f"INSERT INTO libraries(id, name, collection_id) \
                                            VALUES(\'{id}\', \'{name}\', \'{collection_id}\');"
                            )
            #creatung collection for library
            query = f'CREATE TABLE IF NOT EXISTs collection_{id} (title text PRIMARY KEY, availability boolean);'
            session.execute(query)

            #adding books
            start = i * n_books//n_lib
            end = (i + 1) * n_books//n_lib
            for j in range(start, end):
                session.execute(f'INSERT INTO collection_{id}(title, availability) \
                                                VALUES(\'{books[j]["title"]}\', True);')
                    

cluster.shutdown()
