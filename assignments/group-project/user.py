from data.mysql_sample_db import *


class User(object):

    def __init__(self, *args, **kwargs):
        self.username = kwargs.get("username", "test_user")
        self.password = kwargs.get("password", "test_password")
        self.host = kwargs.get("host", "localhost")
        self.global_privs = kwargs.get("global_privs", [])
        self.table_privs = kwargs.get("table_privs", {})

    def name_and_host(self) -> str:
        return f"""'{self.username}'@'{self.host}'"""

    def create_statement(self) -> str:
        return f"""CREATE USER {self.name_and_host()} IDENTIFIED BY '{self.password}';"""

    def grant_global_priv(self) -> str:
        allprivs = ', '.join(self.global_privs)

        return f"GRANT {allprivs} ON *.* TO {self.name_and_host()};"

    def grant_table_priv(self) -> str:
        ret = ""

        table_name: str
        priviledges: [str]

        for table_name, priviledges in self.table_privs.items():
            ret = ret + f"GRANT {', '.join(priviledges)} ON {table_name} TO {self.name_and_host()};\n"

        return ret


ALL_USERS = [
    User(username=f'{DATABASE_NAME}_admin', password='totallysecure',
         table_privs={
             f"{DATABASE_NAME}.*": ["ALL"]
         }),

    User(username=f'{DATABASE_NAME}_farmer_payment', password='iamafarmer',
         table_privs={
             f"{DATABASE_NAME}.{FarmerDatabase.name}": ["UPDATE", "CREATE"]
         }),

    User(username=f'{DATABASE_NAME}_product_manager', password='icannotmanage',
         table_privs={
             f"{DATABASE_NAME}.{ProductLinesData.table_name}": ["CREATE", "UPDATE", "DELETE"],
             f"{DATABASE_NAME}.{ProductsData.table_name}": ["CREATE", "UPDATE", "DELETE"],
         }),
]