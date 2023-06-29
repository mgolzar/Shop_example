import sqlite3
class developeCode:
    def __init__(self,dbpath):
        self.cnt=sqlite3.connect(dbpath)
    
    def create_user_table(self):
        sql='''CREATE TABLE products(
            id INTEGER PRIMARY KEY,
            name CHAR(20) NOT NULL,
            username CHAR(20) NOT NULL,
            password CHAR(32) NOT NULL,
            addr text,
            aid INTEGER)'''
        self.cnt.execute(sql)
    
    def create_products_table(self):
        sql='''CREATE TABLE products(
           id INTEGER PRIMARY KEY,
           pname CHAR(20),
           qnt INTEGER,
           price INTEGER)'''
        self.cnt.execute(sql)

    def create_cart_table(self):
        sql='''CREATE TABLE cart(
           id INTEGER PRIMARY KEY,
           pid CHAR(20),
           uid INTEGER,
           qnt INTEGER)'''
        self.cnt.execute(sql)

    def crate_access_table(self):
        sql='''CREATE TABLE access(
           id INTEGER PRIMARY KEY,
           acceslvl INTEGER,
           submith BOOLEAN,
           delete BOOLEAN,
           adminpanel BOOLEAN,
           shop BOOLEAN,
           mycart BOOLEAN,
           setting BOOLEAN)'''
        self.cnt.execute(sql)

if __name__=="__main__":
    dvl=developeCode()
    dvl.create_user_table()
    dvl.create_products_table()
    dvl.create_cart_table()
    dvl.crate_access_table()
        
                