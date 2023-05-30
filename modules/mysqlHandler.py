## built-in modules
import os
import time

## third party modules
import mysql.connector

## custom modules

class mysqlHandler():

    """
    
    The handler that handles the connection to the database and all interactions with it\n

    """
##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self):

        """
        
        The __init__() method initializes the mysqlHandler class\n

        """
        
        ## the path to the config directory
        self.config_dir = os.path.join(os.environ['USERPROFILE'],"SeisenConfig")

        ## the path to the file that stores the password
        self.password_file = os.path.join(self.config_dir,"password.txt")

        ## the database connection object
        self.connection = self.initialize_database_connection()

##--------------------start-of-load_words()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def load_words(self):

        """
        
        loads the words from the database\n

        Parameters:\n
        self (object - mysqlHandler) : The handler object\n

        Returns:\n
        words (list) : The list of words\n

        """

        words = []



##--------------------start-of-create_database_connection()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def create_database_connection(self, host_name, user_name, user_password, db_name):

        """

        Creates a connection to the database\n

        Parameters:\n
        self (object - mysqlHandler) : The handler object\n
        host_name (str) : The host name of the database\n
        user_name (str) : The user name of the database\n
        user_password (str) : The password of the database\n
        db_name (str) : The name of the database\n

        Returns:\n
        connection (object - mysql.connector.connect) : The connection object to the database\n

        """

        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database= db_name)

        return connection

##-------------------start-of-initialize_database_connection()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def initialize_database_connection(self):

        """

        Sets up the database connection. If the user has already entered the password for the database, the program will use the saved password. If not, the program will ask the user for the password.\n

        Parameters:\n
        None\n

        Returns:\n
        connection (object - mysql.connector.connect) The connection to the database\n

        """
            
        try:

            with open(self.password_file, 'r', encoding='utf-8') as file:  ## get saved connection key if exists
                logins = file.readlines()

                password = logins[0].strip()
                database_name = logins[1].strip()

            connection = self.create_database_connection("localhost", "root", password, database_name)

            print("Used saved pass in " + self.password_file)

        except: ## else try to get pass manually
                
            password = input("Please enter the root password for your local database you have\n")
            database_name = input("Please enter the name of the database you have\n")

            logins = [password,
                      database_name]

            try: ## if valid save the api key

                connection = self.create_database_connection("localhost", "root", password, database_name)
                            
                if(os.path.exists(self.password_file) == False):
                    print(self.password_file + " was created due to lack of the file")
                    with open(self.password_file, "w+",encoding='utf-8') as file:
                        file.truncate(0)

                time.sleep(0.1)

                logins = [x + '\n' for x  in logins]

                with open(self.password_file, "w+",encoding='utf-8') as file:
                    file.writelines(logins)
                    
            except Exception as e: ## if invalid exit
                        
                os.system('cls')

                print(str(e))
                print("Error with creating connection object, please double check your password\n")

                os.system('pause')
                
                exit()

        return connection
    
##--------------------start-of-execute_query()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def execute_query(self, query):

        """

        Executes a query to the database\n

        Parameters:\n
        self (object - mysqlHandler) : The handler object\n
        query (str) : The query to be executed\n

        Returns:\n
        None\n

        """
        
        cursor = self.connection.cursor()
        cursor.execute(query)
        
        self.connection.commit()

##--------------------start-of-read_single_column_query()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def read_single_column_query(self, query):

        """

        reads a single column query from the database\n

        Parameters:\n
        self (object - mysqlHandler) : The handler object\n
        query (str) : The query to be executed\n

        Returns:\n
        results_actual (list - string) : The results of the query\n

        """
        
        cursor = self.connection.cursor()
        results_actual = []

        cursor.execute(query)
        results = cursor.fetchall()

        results_actual = [str(i[0]) for i in results]

        return results_actual

##--------------------start-of-read_multi_column_query()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def read_multi_column_query(self, query):

        """

        reads a multi column query from the database\n

        Parameters:\n
        self (object - mysqlHandler) : The handler object\n
        query (str) : The query to be executed\n

        Returns:\n
        results_by_column (list - list) : The results of the query\n

        """

        cursor = self.connection.cursor()
        cursor.execute(query)

        results = cursor.fetchall()

        if(len(results) == 0):
            return [[]] * cursor.description.__len__() if cursor.description else [[]]

        results_by_column = [[] for i in range(len(results[0]))]
        
        for row in results:
            for i, value in enumerate(row):
                results_by_column[i].append(str(value))

        return results_by_column

