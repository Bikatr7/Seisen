## custom modules
from modules.mysqlHandler import mysqlHandler
from modules.ensureFileSecurity import ensure_files

##--------------------Start-of-load_database()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def load_database():

    handler = mysqlHandler()

    handler.initialize_database_connection()

    print("Database connection established.") 

##--------------------Start-of-main()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

ensure_files()
load_database()