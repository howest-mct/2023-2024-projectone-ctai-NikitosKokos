from .Database import Database


class DataRepository:
    @staticmethod
    def read_users():
        sql = "SELECT * FROM users"
        return Database.get_rows(sql)

    @staticmethod
    def create_user(firstname, lastname, password, type, honorific="", recorded=0):
        sql = "INSERT into users (firstname, lastname, password, type, honorific, recorded) VALUES (%s, %s, %s, %s, %s, %s)"
        params = [firstname, lastname, password, type, honorific, recorded]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def is_recorded(user_id):
        sql = "SELECT recorded FROM users WHERE userId=%s"
        params = [user_id]
        return Database.get_rows(sql, params)
    
    @staticmethod
    def get_password(user_id):
        sql = "SELECT password FROM users WHERE userId=%s"
        params = [user_id]
        return Database.get_rows(sql, params)
    
    @staticmethod
    def set_recorded(user_id):
        sql = "UPDATE users SET recorded = 1 WHERE userId = %s"
        params = [user_id]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def get_name(user_id):
        sql = "SELECT firstname, honorific FROM users WHERE userId=%s"
        params = [user_id]
        return Database.get_rows(sql, params)
