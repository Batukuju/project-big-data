### BIG_DATA PROJECT: LIBRARY SYSTEM
This project aims to create an application that will use cassandra distributed system for libraries management.

### Client actions: borrowing and returning books to the library
In our library system, the client has his favorite library, that he can borrow a book from or return one. He can return only books to the library that they were borrowed from, and vice versa. Moreover, every client has his own shelf with titles of borrowed books. 

### Library operation: book availability tracking
Every library has its own collection that contains titles and the availability of all books in this library. When the book is borrowed, the availability is set to False, and the title appears on the client's own shelf. When the client returns the book, the title is deleted from his private shelf and the availability is changed to True again.

### Database schema
![image](https://github.com/Batukuju/project-big-data/assets/75094119/63b259f4-a548-4558-95b1-8f11577d0b68)

## Project structure

### Project content
The project is divided into 2 parts:
1. Console application, whereas a client you want to return or borrow a book from one library.
2. Stress tests:
- Stress Test 1: Client borrows and returns the same book 100 times.
- Stress Test 2: Two clients select to borrow or return a random book as two separate threads. 
- Stress Test 3: Two clients tries to borrow and return consecutive books from the library.
- Stress Test 4: Two different clients fight for one book 100 times.


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
