
import database


class logDataBase:
    def __init__(self):
        
        self.id = ''
        self.password= ''
        self.logFlag = False
        self.db_manager = database.MySQLManager(
            host="localhost",
            user="root",
            password="123456",
            database="atm"
        )

    def setID(self,value):
        self.id = value
        return
    
    def setPass(self,value):
        self.password = value
        return
    
    def login (self):
        if self.db_manager.connect() is True:
            if self.db_manager.verify_user(self.id,self.password):
                self.logFlag = True
                return '525 OK!'
            else:
                return '401 ERROR!'
        else:
            return 'Database Fault'

    def getAmount(self):
        if self.logFlag is False:
            return -1
        if self.logFlag is True:
            amount = self.db_manager.get_balance(self.id)
            
            return amount

    def withdraw(self,value):
        return self.db_manager.update_balance(self.id,value)
            
    def byeDatabase(self):
        self.db_manager.disconnect()