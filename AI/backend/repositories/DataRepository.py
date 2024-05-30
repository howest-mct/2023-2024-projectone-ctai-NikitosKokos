from .Database import Database


class DataRepository:
    #########  Customer  #########
    @staticmethod
    def read_users():
        # tblKlant is the name of the table in the database. (klant = customer in dutch)
        sql = "SELECT * FROM users"
        return Database.get_rows(sql)

    @staticmethod
    def create_user(firstname, lastname, password, type, honorific=""):
        # tblKlant is the name of the table in the database. (klant = customer in dutch)
        # FNaam, VNaam, Straat, Nummer, Postcode, Gemeente are the names of the columns in the table.
        sql = "INSERT into users (firstname, lastname, password, type, honorific) VALUES (%s, %s, %s, %s, %s)"
        params = [firstname, lastname, password, type, honorific]
        return Database.execute_sql(sql, params)
