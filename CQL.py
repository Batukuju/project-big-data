from cassandra.cluster import Cluster

class CQL():
    ID = 0
    table = ""
    def __init__(self):
        self.cluster = Cluster(['172.17.0.2'])
        self.session = self.cluster.connect("libraries_system")   

    # def insert(self, table, values):
    #     text = f"INSERT INTO {table} VALUES {tuple([values])}"
    #     print(text)
    #     self.session.execute(text)
        
    # def create(self, newTableName, column, column2 = None ):
        # text = f'CREATE TABLE IF NOT EXISTs "{newTableName}" ({column} text PRIMARY KEY);'
        # print(text)
        # self.session.execute(text)
    
    # def update(self, table, updated, category, ID): 
    #     text = f"UPDATE  {table} SET {category} = {updated} WHERE ID = {ID};"
    #     print(text)
    #     self.session.execute(text)

    # def remove(self, table, categoryValue = ID, category = "ID"):
    #     text = f"DELETE FROM  {table} WHERE {category} = {categoryValue};"
    #     print(text)
    #     self.session.execute(text)

    # def select(self, table, category, categoryValue):
    #     text = f"SELECT * FROM {table} WHERE {category} = '{categoryValue}' ALLOW FILTERING;"
    #     print(text)
    #     return self.session.execute(text)

    # def apply(self, text):
    #     print(text)
    #     self.session.execute(text)
    
    def getSession(self):
        return self.session

    def closeCluster(self):
        self.cluster.shutdown
