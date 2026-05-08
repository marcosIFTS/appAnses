import getpass
import urllib
from sqlalchemy import create_engine

def conn():
    # creamos la varaible con los datos del server
    server = (r"Driver={SQL Server};" + "Server=10.80.5.17,21433;" +
              f"Database=HF_PPC;Trusted_Connection=yes")

    return server