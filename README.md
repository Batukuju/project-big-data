### BIG_DATA PROJECT: LIBRARY SYSTEM
This project aims to create an application that will use cassandra distributed system for libraries management.

### Client actions: borrowing and returning books to the library
In our library system, the client has his favorite library, that he can borrow a book from or return one. He can return only books to the library that they were borrowed from, and vice versa. Moreover, every client has his own shelf with titles of borrowed books. 

### Library operation: book availability tracking
Every library has its own collection that contains titles and the availability of all books in this library. When the book is borrowed, the availability is set to False, and the title appears on the client's own shelf. When the client returns the book, the title is deleted from his private shelf and the availability is changed to True again.

### Database schema
![image](https://github.com/Batukuju/project-big-data/assets/75094119/c171c9d5-7dc6-42bc-b6f3-1b21659c026e)

na razie do edycji https://dbdiagram.io/d/6485fa2a722eb77494c47dab

## Project structure

### Project content
The project is divided into 2 parts:
1) Console application, whereas a client you want to return or borrow a book from one library.
2) Stress tests:
2.1. Stress Test 1: The client makes the same request very quickly. -> Client want to borrow the same book all and all over again.
2.2. Stress Test 2: Two or more clients make the possible requests randomly.-> 2 clients select to borrow/return a book as two separate threads. 
2.3. Stress Test 3: Immediate occupancy of all seats/reservations on 2 clients.-> 2 clients are iteratively borrowing all books from the library.
2.4. Stress Test 4: (only for pairs) constant cancellations and seat occupancy. -> Client can return the book to the library.

### File system
- story.py -> Console Application
- main.py -> Main file to get familiar with the system
- client.py -> Client class 
- library.py -> Library class 


- data/library.csv -> Data for initial setup
- data/client.csv -> Data for initial setup
- data/books.csv -> Data for initial setup


- setup.bash -> Runs dockers with cassandra on 3 nodes and creates initial values for the system (libraries, clients, books)
- start_simple.bash -> Runs docker with cassandra and creates initial values for the system (libraries, clients, books)
- initial_setup.py -> Creates initial values for the system (libraries, clients, books)

###  How to run our project?
```bash
$ bash setup.bash 
$ python3 story.py // To get console application:
$ python3 main.py //To play around```
