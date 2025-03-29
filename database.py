# mysql_manager.py
import mysql.connector
from mysql.connector import Error
from typing import Optional, Tuple

class MySQLManager:
    def __init__(
        self,
        host: str = "localhost",
        user: str = "root",
        password: str = "123456",
        database: str = "atm"
    ):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection: Optional[mysql.connector.MySQLConnection] = None

    def connect(self) -> bool:
        """建立 MySQL 数据库连接"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return True
        except Error as e:
            print(f"MySQL 连接失败: {e}")
            return False

    def disconnect(self) -> None:
        """关闭数据库连接"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None

    def verify_user(self, user_id: str, password: str) -> bool:
        """验证用户身份"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT password FROM userInfo 
                WHERE id = %s
            ''', (user_id,))
            result = cursor.fetchone()
            return result and result[0] == password  # 实际应验证哈希值
        except Error as e:
            print(f"验证失败: {e}")
            return False

    def get_balance(self, user_id: str) -> float:
        """获取账户余额"""
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT money FROM accounts 
                WHERE idaccount = %s
            ''', (user_id,))
            result = cursor.fetchone()
            return result[0] if result else 0.0
        except Error as e:
            print(f"查询余额失败: {e}")
            return -1.0

    def update_balance(self, user_id: str, amount: float) -> bool:
        """更新账户余额"""
        try:
            cursor = self.connection.cursor()
            amount = float(amount)
            # 检查余额是否足够（仅限取款）
            if amount < 0:
                cursor.execute('''
                    SELECT money FROM accounts 
                    WHERE idaccount = %s
                ''', (user_id,))
                balance = cursor.fetchone()[0]
                if balance < abs(amount):
                    return False

            # 更新余额
            cursor.execute('''
                UPDATE accounts 
                SET money = money + %s 
                WHERE idaccount = %s
            ''', (amount, user_id))
            self.connection.commit()
            return cursor.rowcount > 0  # 如果更新成功返回True
        except Error as e:
            print(f"更新失败: {e}")
            self.connection.rollback()
            return False