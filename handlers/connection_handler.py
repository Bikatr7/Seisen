## built-in libraries
import typing
import base64

## third party modules
import mysql.connector
import mysql.connector.pooling
import mysql.connector.cursor

## custom modules
from handlers.file_handler import FileHandler

from modules.toolkit import Toolkit
from modules.file_ensurer import FileEnsurer
from modules.logger import Logger


class ConnectionHandler():

    """
    
    The ConnectionHandler class handles the connection to the database and all interactions with it.

    """
    
    connection: typing.Union[mysql.connector.connection.MySQLConnection, mysql.connector.pooling.PooledMySQLConnection, None] = None
    cursor: typing.Union[mysql.connector.cursor.MySQLCursor, None] = None

##-------------------start-of-check_connection_validity()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def check_connection_validity(reason_for_check:str) -> bool:

        """
        
        Determines if we have a valid connection.

        Parameters:
        reason_for_check (str) : Why we are checking connection validity.

        Returns:
        is_valid (bool) : True if valid, False otherwise.

        """

        log_message = "Checking connection for reason: " + reason_for_check + ", Connection is valid, continuing."
        is_valid = True

        if(ConnectionHandler.connection == None or ConnectionHandler.cursor == None):
            is_valid = False
            log_message = "Checking connection for reason: " + reason_for_check + ", Connection is invalid, skipping."
        
        Logger.log_action(log_message)

        return is_valid

##-------------------start-of-initialize_database_connection()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def initialize_database_connection() -> typing.Tuple[typing.Union[mysql.connector.connection.MySQLConnection, mysql.connector.pooling.PooledMySQLConnection, None], typing.Union[mysql.connector.cursor.MySQLCursor, None]]:

        """

        Sets up the database connection. If the user has already entered the credentials for the database, the program will use them. If not, the program will prompt the user for them.
        If connection has failed previously, the program will skip the connection initialization. You must use the start_marked_succeeded_database_connection() to reset this.

        Returns:
        connection (object - mysql.connector.connect.MySQLConnection) or (object - mysql.connector.pooling.PooledMySQLConnection) or None : The connection object to the database.
        cursor (object - mysql.connector.cursor.MySqlCursor) or None : The connection cursor.

        """

        connection = None
        cursor = None
        
        with open(FileEnsurer.has_database_connection_failed_path, "r+", encoding="utf-8") as file:
            if(file.read().strip() == "true"):
                Logger.log_action("Database connection has failed previously.... skipping connection initialization")
                return connection, cursor

        ## program assumes connection will succeed
        ConnectionHandler.start_marked_succeeded_database_connection()

        try:

            ## get saved connection credentials if exists
            with open(FileEnsurer.credentials_path, 'r', encoding='utf-8') as file:  
                credentials = file.readlines()

                database_name = base64.b64decode((credentials[0].strip()).encode('utf-8')).decode('utf-8')
                password = base64.b64decode((credentials[1].strip()).encode('utf-8')).decode('utf-8')

            connection = ConnectionHandler.create_database_connection("localhost", "root", database_name, password)
            cursor = connection.cursor()

            Logger.log_action("Used saved credentials in " + FileEnsurer.credentials_path)

        ## else try to get credentials manually
        except: 

            ## if valid save the credentials
            try:

                ## to do, adjust so user doesn't have to give root password

                database_name = Toolkit.user_confirm("Please enter the name of the database you have:")

                Toolkit.clear_console()

                password = Toolkit.user_confirm("Please enter the root password for your local database you have:")

                credentials = [
                    base64.b64encode(database_name.encode('utf-8')).decode('utf-8'),
                        base64.b64encode(password.encode('utf-8')).decode('utf-8')]
                
                connection = ConnectionHandler.create_database_connection("localhost", "root", database_name, password)
                cursor = connection.cursor()
                            
                FileHandler.standard_overwrite_file(FileEnsurer.credentials_path, credentials, omit=True)

            except Toolkit.UserCancelError:
                
                Toolkit.clear_console()

                ConnectionHandler.start_marked_failed_database_connection()

            ## if invalid break
            except Exception as e: 
                        
                Toolkit.clear_console()

                print(str(e))
                print("\nError with creating connection object, please double check your password and database name.\n")

                ConnectionHandler.start_marked_failed_database_connection()

                Toolkit.pause_console()
            
        return connection, cursor
    
##--------------------start-of-mark_failed_database_connection()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def start_marked_failed_database_connection() -> None:
         
        """
        
        Tells the program that the most recently attempted database connection has failed.
        This will prevent the program from attempting to connect to the database again until the user has either decided to make a new connection or the program has marked the connection as succeeded.

        """

        FileHandler.standard_overwrite_file(FileEnsurer.has_database_connection_failed_path, "true", omit=False)
            
        Logger.log_action("Database Connection Failed")

##--------------------start-of-mark_succeeded_database_connection()---------------------------S---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def start_marked_succeeded_database_connection() -> None:
         
        """
        
        Tells the program that the most recently attempted database connection has succeeded.
        This will allow the program to attempt to connect to the database automatically on the next run.

        """

        FileHandler.standard_overwrite_file(FileEnsurer.has_database_connection_failed_path, "false", omit=False)

        Logger.log_action("Database Connection Succeeded")

##--------------------start-of-create_database_connection()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def create_database_connection(host_name:str, user_name:str, db_name:str, user_password:str) -> typing.Union[mysql.connector.connection.MySQLConnection, mysql.connector.pooling.PooledMySQLConnection]:

        """

        Creates a connection to the database.

        Parameters:
        host_name (str) : The host name of the database.
        user_name (str) : The user name of the database.
        db_name (str) : The name of the database.
        user_password (str) : The password of the database.

        Returns:
        connection (object - mysql.connector.connect.MySQLConnection) or (object - mysql.connector.pooling.PooledMySQLConnection) or None : The connection object to the database.

        """

        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            database= db_name,
            passwd=user_password)

        Logger.log_action("Successfully connected to the " + db_name + " database")

        return connection
    
##--------------------start-of-clear_credentials_File()---------------------------S---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def clear_credentials_file() -> None:

        """
        
        Clears the credentials file allowing for a different database connection to be added.

        """

        FileHandler.clear_file(FileEnsurer.credentials_path)

##--------------------start-of-execute_query()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def execute_query(query:str) -> None:

        """

        Executes a query to the database.

        Parameters:
        query (str) : The query to be executed.

        """

        Logger.log_barrier()
    
        ## Never actually gonna happen, but just in case
        if(ConnectionHandler.cursor == None or ConnectionHandler.connection == None):
            raise Exception("Connection is invalid, please ensure you have a valid connection and try again")

        ConnectionHandler.cursor.execute(query) 
        
        ConnectionHandler.connection.commit()

        Logger.log_action("The following query was sent and accepted by the database : ")
        Logger.log_action(query.strip())

        Logger.log_barrier()

##--------------------start-of-read_single_column_query()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def read_single_column_query(query:str) -> typing.List[str]:

        """

        Reads a single column query from the database.

        Parameters:
        query (str) : The query to be executed.

        Returns:
        results_actual (list - str) : The results of the query.

        """
        
        results_actual = []

        ## Never actually gonna happen, but just in case
        if(ConnectionHandler.cursor == None or ConnectionHandler.connection == None):
            raise Exception("Connection is invalid, please ensure you have a valid connection and try again")

        ConnectionHandler.cursor.execute(query)
        results = ConnectionHandler.cursor.fetchall() 

        results_actual = [str(i[0]) for i in results]

        return results_actual

##--------------------start-of-read_multi_column_query()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def read_multi_column_query(query:str) -> typing.List[typing.List[str]]:

        """

        Reads a multi column query from the database.

        Parameters:
        query (str) : The query to be executed.

        Returns:
        results_by_column (list - list - str) : The results of the query.

        """
    
        results_by_column = [[]]

        ## Never actually gonna happen, but just in case
        if(ConnectionHandler.cursor == None or ConnectionHandler.connection == None):
            raise Exception("Connection is invalid, please ensure you have a valid connection and try again")

        ConnectionHandler.cursor.execute(query) 

        results = ConnectionHandler.cursor.fetchall() 

        if(len(results) == 0):
            return [[]] * ConnectionHandler.cursor.description.__len__() if ConnectionHandler.cursor.description else [[]] 

        results_by_column = [[] for i in range(len(results[0]))]
        
        for row in results:
            for i, value in enumerate(row):
                results_by_column[i].append(str(value))

        return results_by_column
    
##--------------------start-of-insert_into_table()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def insert_into_table(table_name:str, data:dict) -> None:

        """
        
        inserts data into a table.

        Parameters:
        table_name (str) : The name of the table.
        data (dict) : The data to be inserted.

        """

        columns = ", ".join(data.keys())
        values = ", ".join([f"'{value}'" for value in data.values()])

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

        ConnectionHandler.execute_query(query)