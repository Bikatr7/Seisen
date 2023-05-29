## built-in modules
import os
import time

## third party modules
import mysql.connector

class mysqlHandler():

    """
    
    The handler that handles the connection to the database and all interactions with it

    """
##--------------------Start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        
        self.config_dir = os.path.join(os.environ['USERPROFILE'],"SeisenConfig")

        self.password_file = os.path.join(self.config_dir,"password.txt")

##--------------------Start-of-create_database_connection()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def create_database_connection(self, host_name, user_name, user_password,db_name):

        """

        Creates a connection to the database

        Parameters :
        self (object - mysqlHandler) : The handler object
        host_name (str) : The host name of the database
        user_name (str) : The user name of the database
        user_password (str) : The password of the database
        db_name (str) : The name of the database

        Returns :
        connection (object - mysql.connector.connect) : The connection object to the database

        """

        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database= db_name)

        return connection

##-------------------start of initialize_database_connection()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def initialize_database_connection(self):

        """

        Sets up the database connection. If the user has already entered the password for the database, the program will use the saved password. If not, the program will ask the user for the password.

        Parameters:
        None

        Returns:
        connection (object - mysql.connector.connect) The connection to the database

        """
            
        try:

            with open(self.password_file, 'r', encoding='utf-8') as file:  ## get saved connection key if exists
                logins = file.readlines()

                password = logins[0].strip()
                database_name = logins[1].strip()

            connection = self.create_database_connection("localhost","root",password,database_name)

            print("Used saved pass in " + self.password_file)

        except: ## else try to get pass manually
                
            password = input("Please enter the root password for your local database you have\n")
            database_name = input("Please enter the name of the database you have\n")

            logins = [password,
                      database_name]

            try: ## if valid save the api key

                connection = self.create_database_connection("localhost","root",password,database_name)
                            
                if(os.path.exists(self.password_file) == False):
                    print(self.password_file + " was created due to lack of the file")
                    with open(self.password_file, "w+",encoding='utf-8') as file:
                        file.truncate(0)

                time.sleep(0.1)

                with open(self.password_file, "w+",encoding='utf-8') as file:
                    file.writelines(logins)
                    
            except Exception as e: ## if invalid exit
                        
                os.system('cls')

                print(str(e))
                print("Error with creating connection object, please double check your password\n")
                os.system('pause')
                
                exit()

        return connection