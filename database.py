import sqlite3
import hashlib
import setting

class db:
    def __init__(self):
        self.setting=setting.Setting()
        self.cnt=sqlite3.connect(self.setting.get_Stile('path')['dbpath'])
        if self.setting.get_Stile('datetime')['lastrun']=="first":
            self.__create_user_table()
            self.__create_products_table()
            self.__create_cart_table()
            self.__crate_acces_table()
            self.setting.set_last_runapp()
            self.__insert_defult_user()
            self.__insert_defult_acces()

# -------------------- Crate tabels ------------------
    def __create_user_table(self):
        sql='''CREATE TABLE users(
            id INTEGER PRIMARY KEY,
            name CHAR(20) NOT NULL,
            username CHAR(20) NOT NULL,
            password CHAR(32) NOT NULL,
            addr text,
            acceslvl CHAR(10))'''
        self.cnt.execute(sql)
    
    def __create_products_table(self):
        sql='''CREATE TABLE products(
           id INTEGER PRIMARY KEY,
           pname CHAR(20),
           qnt INTEGER,
           price INTEGER)'''
        self.cnt.execute(sql)

    def __create_cart_table(self):
        sql='''CREATE TABLE cart(
           id INTEGER PRIMARY KEY,
           pid CHAR(20),
           uid INTEGER,
           qnt INTEGER)'''
        self.cnt.execute(sql)

    def __crate_acces_table(self):    
        sql='''CREATE TABLE acces(
           id INTEGER PRIMARY KEY,
           acceslvl CHAR(10),
           submith CHAR(10),
           del CHAR(10),
           adminpanel CHAR(10),
           shop CHAR(10),
           setting CHAR(10))'''
        self.cnt.execute(sql)    
    
    def __insert_defult_user(self):
        pas="123456789"
        sql='''INSERT INTO users (name,username,password,addr,acceslvl) VALUES(?,?,?,?,?)'''
        coded_pas = hashlib.md5(pas.encode())
        self.cnt.execute(sql,("Admin","admin",coded_pas.hexdigest(),"rasht","a")) 
        self.cnt.commit()

    def __insert_defult_acces(self):
        sql='''INSERT INTO acces (acceslvl,submith,del,adminpanel,shop,setting) VALUES(?,?,?,?,?,?)'''
        self.cnt.execute(sql,("a","active","active","active","active","active")) 
        self.cnt.commit()     
        sql='''INSERT INTO acces (acceslvl,submith,del,adminpanel,shop,setting) VALUES(?,?,?,?,?,?)'''
        self.cnt.execute(sql,("b","active","active","active","active","disable")) 
        self.cnt.commit()
        sql='''INSERT INTO acces (acceslvl,submith,del,adminpanel,shop,setting) VALUES(?,?,?,?,?,?)'''
        self.cnt.execute(sql,("c","active","disable","active","active","disable")) 
        self.cnt.commit()
        sql='''INSERT INTO acces (acceslvl,submith,del,adminpanel,shop,setting) VALUES(?,?,?,?,?,?)'''
        self.cnt.execute(sql,("d","active","disable","disable","active","disable")) 
        self.cnt.commit()

    def get_acces_db(self,acceslvl):
        sql=''' SELECT * FROM acces WHERE acceslvl=? '''
        result=self.cnt.execute(sql,(acceslvl,))
        row=result.fetchone()
        dic={"acceslvl":row[1],"submith":row[2],"del":row[3],"adminpanel":row[4],"shop":row[5],"setting":row[6]}
        
        return dic




    def login_db(self,user,pas):
        coded_pas = hashlib.md5(pas.encode())
        
        sql=''' SELECT * FROM users WHERE username=? AND 
        password=? '''
        result=self.cnt.execute(sql,(user,coded_pas.hexdigest()))
        return result
    
    def isUserExist(self,user):
        sql='''SELECT * FROM users WHERE username=?'''
        result=self.cnt.execute(sql,(user,))
        row=result.fetchone()
        if row:
            return True
        else:
            return False
    
    def savetoDB(self,user,pas,name,addr,acceslvl):
        
            sql='''INSERT INTO users (name,username,password,addr,acceslvl)
                    VALUES(?,?,?,?,?)'''
            coded_pas = hashlib.md5(pas.encode())
            self.cnt.execute(sql,(name,user,coded_pas.hexdigest(),addr,acceslvl)) 
            self.cnt.commit()
            return True
    
    def deleteUser(self,user):
            try:
                sql='''DELETE FROM users WHERE username=?'''
                self.cnt.execute(sql,(user,))
                self.cnt.commit()
                return True
            except:
                return False
    
    def psavetoDB(self,pname,qnt,price):
        try:
            sql='''INSERT INTO products (pname,qnt,price)
                        VALUES(?,?,?)'''
            
            self.cnt.execute(sql,(pname,qnt,price))
            self.cnt.commit()
            return True
        except:
            return False
    
    def products_list_db(self):
        sql='''SELECT * FROM products'''
        result=self.cnt.execute(sql)
        rows=result.fetchall()
        return rows

    def __find_user_id(self,user):
        sql='''SELECT id FROM users WHERE username=?'''
        result=self.cnt.execute(sql,(user,))
        row=result.fetchone()
        return row[0]
    
    def __update_qnt(self,pid,qnt):
        sql='''UPDATE products SET qnt=(qnt - ?) WHERE id=?'''
        self.cnt.execute(sql,(qnt,pid))
        self.cnt.commit()

    def save_to_cart_db(self,pid,qnt,user):
        uid=self.__find_user_id(user)
        try:
            sql='''INSERT INTO cart (pid,uid,qnt)
                        VALUES(?,?,?)'''
            
            self.cnt.execute(sql,(pid,uid,qnt))
            self.cnt.commit()
            self.__update_qnt(pid,qnt)
            return True
        except:
            return False
               
    def get_cart_db(self,user):

        uid=self.__find_user_id(user)
        sql='''SELECT products.pname,products.price,cart.qnt
        FROM cart
        INNER JOIN products
        ON cart.pid=products.id
        WHERE cart.uid=?'''
        result=self.cnt.execute(sql,(uid,))
        rows=result.fetchall()
        return rows



        
        
        
        
        
        
        
    