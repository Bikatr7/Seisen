## built-in modules
import os
import time
import typing

## third party modules
from mysql.connector import pooling
import mysql.connector 

## custom modules
from modules.typos import typo as typo_blueprint
from modules.typos import incorrectTypo as incorrect_typo_blueprint
from modules.words import word as kana_blueprint
from modules import util

class remoteHandler():

    """
    
    The handler that handles the connection to the database and all interactions with it.\n

    """
##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self) -> None:

        """
        
        Initializes the remoteHandler class\n

        Parameters:\n
        self (object - remoteHandler) : The handler object\n

        Returns:\n
        None\n

        """
        
        ## the path to the config directory
        self.config_dir = os.path.join(os.environ['USERPROFILE'],"SeisenConfig")

        ## the path to the file that stores the password
        self.password_file = os.path.join(os.path.join(self.config_dir, "Logins"), "credentials.txt")

        ## the paths to the file that stores the kana words and its typos
        self.kana_file = os.path.join(os.path.join(self.config_dir, "Kana"), "kana.txt")
        self.kana_typos_file = os.path.join(os.path.join(self.config_dir, "Kana"), "kana typos.txt")
        self.kana_incorrect_typos_file = os.path.join(os.path.join(self.config_dir, "Kana"), "kana incorrect typos.txt")

        ## the kana that seisen will use to test the user
        self.kana = [] 

        ## the literal used in the database to flag words as Kana
        self.KANA_WORD_TYPE = "2"

        ## the accepted typos for kana
        self.kana_typos = []

        ## the accepted incorrect typos for kana
        self.kana_incorrect_typos = []

        try:
            self.connection = self.initialize_database_connection()
        
        except:
            print("Database credentials are invalid or database does not exist")
##--------------------start-of-reset_local_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def reset_local_storage(self) -> None:

        """
        
        loads the words from the database and replaces the local storage with it\n
        Note that this will reset all the words locally stored on this device\n
        Use carefully!\n

        Parameters:\n
        self (object - remoteHandler) : The handler object\n

        Returns:\n
        None\n

        """

        def clear_local_storage():

            with open(self.kana_file, "w", encoding="utf-8") as file:
                file.truncate(0)
                
            with open(self.kana_typos_file, "w", encoding="utf-8") as file:
                file.truncate(0)

            with open(self.kana_incorrect_typos_file, "w", encoding="utf-8") as file:
                file.truncate(0)

        def reset_kana_relations():

            KANA_WORD_TYPE = "2"
            
            ##KANA_TYPO_WORD_ID_INDEX_LOCATION = 0
            ##KANA_TYPO_TYPO_ID_INDEX_LOCATION = 1
            ##KANA_TYPO_VALUE_INDEX_LOCATION = 2
            ##KANA_TYPO_WORD_TYPE_INDEX_LOCATION = 3

            list_of_all_accepted_answers = []

            self.kana.clear()
            self.kana_typos.clear()
            self.kana_incorrect_typos.clear()
            
            word_id_list, jValue_list, eValue_list, pValue_list, cValue_list = self.read_multi_column_query("select id, kana, reading, incorrect_count, correct_count from kana")
            typo_word_type_list, typo_id_list, typo_word_id_list, typo_value_list = self.read_multi_column_query("select word_type, typo_id, kana_id, typo_value from kana_typos")
            incorrect_typo_word_type_list, incorrect_typo_id_list, incorrect_typo_word_id_list, incorrect_typo_value_list = self.read_multi_column_query("select word_type, incorrect_typo_id, kana_id, incorrect_typo_value from kana_incorrect_typos")

            self.kana = [kana_blueprint(int(word_id_list[i]), jValue_list[i], eValue_list[i], list_of_all_accepted_answers, int(pValue_list[i]), int(cValue_list[i])) for i in range(len(word_id_list))]
            self.kana_typos = [typo_blueprint(typo_word_type_list[i], int(typo_id_list[i]), int(typo_word_id_list[i]), typo_value_list[i]) for i in range(len(typo_word_id_list))]
            self.kana_incorrect_typos = [incorrect_typo_blueprint(incorrect_typo_word_type_list[i], int(incorrect_typo_id_list[i]), int(incorrect_typo_word_id_list[i]), incorrect_typo_value_list[i]) for i in range(len(incorrect_typo_word_id_list))]

            for kana in self.kana:
                word_values = [kana.word_id, kana.testing_material, kana.testing_material_answer_main, kana.incorrect_count, kana.correct_count]
                util.write_sei_line(self.kana_file, word_values)

            for typo in self.kana_typos:
                typo_values = [typo.word_id, typo.typo_id, typo.typo_value, typo.word_type]
                util.write_sei_line(self.kana_typos_file, typo_values)

            for incorrect_typo in self.kana_incorrect_typos:
                incorrect_typo_values = [incorrect_typo.word_id, incorrect_typo.incorrect_typo_id, incorrect_typo.incorrect_typo_value, incorrect_typo.word_type]
                util.write_sei_line(self.kana_incorrect_typos_file, incorrect_typo_values)

            for kana in self.kana:
                for typo in self.kana_typos:
                    if(typo.word_type == int(KANA_WORD_TYPE) and typo.word_id == kana.word_id):
                        kana.typos.append(typo)        

                for incorrect_typo in self.kana_incorrect_typos:
                    if(incorrect_typo.word_type == int(KANA_WORD_TYPE) and incorrect_typo.word_id == kana.word_type):
                        kana.incorrect_typos.append(incorrect_typo)

        clear_local_storage()
        reset_kana_relations()   
        
##--------------------start-of-create_database_connection()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def create_database_connection(self, host_name:str, user_name:str, user_password:str, db_name:str) -> typing.Union[mysql.connector.connection.MySQLConnection, pooling.PooledMySQLConnection]:

        """

        Creates a connection to the database\n

        Parameters:\n
        self (object - remoteHandler) : The handler object\n
        host_name (str) : The host name of the database\n
        user_name (str) : The user name of the database\n
        user_password (str) : The password of the database\n
        db_name (str) : The name of the database\n

        Returns:\n
        connection (object - mysql.connector.connect.MySQLConnection) or (object - mysql.connector.pooling.PooledMySQLConnection) : The connection object to the database\n

        """

        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database= db_name)

        return connection

##-------------------start-of-initialize_database_connection()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def initialize_database_connection(self) -> typing.Union[mysql.connector.connection.MySQLConnection, pooling.PooledMySQLConnection]:

        """

        Sets up the database connection. If the user has already entered the password for the database, the program will use the saved password. If not, the program will ask the user for the password.\n

        Parameters:\n
        None\n

        Returns:\n
        connection (object - mysql.connector.connect.MySQLConnection) or (object - mysql.connector.pooling.PooledMySQLConnection) : The connection object to the database\n

        """

        try:

            with open(self.password_file, 'r', encoding='utf-8') as file:  ## get saved connection credentials if exists
                credentials = file.readlines()

                password = credentials[0].strip()
                database_name = credentials[1].strip()

            connection = self.create_database_connection("localhost", "root", password, database_name)

            print("Used saved pass in " + self.password_file)

        except: ## else try to get credentials manually
                
            password = input("Please enter the root password for your local database you have\n")

            util.clear_console()

            database_name = input("Please enter the name of the database you have\n")

            credentials = [
                        password,
                      database_name]

            try: ## if valid save the credentials

                connection = self.create_database_connection("localhost", "root", password, database_name)
                            
                if(os.path.exists(self.password_file) == False):
                    print(self.password_file + " was created due to lack of the file")
                    with open(self.password_file, "w+",encoding='utf-8') as file:
                        file.truncate(0)

                time.sleep(0.1)

                credentials = [x + '\n' for x  in credentials]

                with open(self.password_file, "w+",encoding='utf-8') as file:
                    file.writelines(credentials)
                    
            except Exception as e: ## if invalid exit
                        
                util.clear_console()

                print(str(e))
                print("Error with creating connection object, please double check your password\n")

                util.pause_console()
                
                exit()

        return connection
    

##--------------------start-of-execute_query()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def execute_query(self, query:str) -> None:

        """

        Executes a query to the database\n

        Parameters:\n
        self (object - remoteHandler) : The handler object\n
        query (str) : The query to be executed\n

        Returns:\n
        None\n

        """
        
        cursor = self.connection.cursor()
        cursor.execute(query)
        
        self.connection.commit()

##--------------------start-of-read_single_column_query()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def read_single_column_query(self, query:str) -> typing.List[str]:

        """

        reads a single column query from the database\n

        Parameters:\n
        self (object - remoteHandler) : The handler object\n
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
    
##--------------------start-of-insert_into_table()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def insert_into_table(self, table_name, data) -> None:

        """
        
        inserts data into a table\n

        Parameters:\n
        self (object - remoteHandler) : The handler object\n
        table_name (str) : The name of the table\n
        data (dict) : The data to be inserted\n

        Returns:\n
        None\n

        """

        columns = ", ".join(data.keys())
        values = ", ".join([f"'{value}'" for value in data.values()])

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

        self.execute_query(query)

##--------------------start-of-read_multi_column_query()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def read_multi_column_query(self, query:str) -> typing.List[typing.List[str]]:

        """

        reads a multi column query from the database\n

        Parameters:\n
        self (object - remoteHandler) : The handler object\n
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


##--------------------start-of-delete_remote_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def delete_remote_storage(self) -> None:

        """
        
        resets the remote storage\n

        Parameters:\n
        self (object - remoteHandler) : The handler object\n

        Returns:\n
        None\n

        """

        delete_kana_query = """
        drop table if exists kana;
        """

        delete_kana_typos_query = """
        drop table if exists kana_typos;
        """

        delete_kana_incorrect_typos_query = """
        drop table if exists kana_incorrect_typos;
        """

        delete_kana_csep_query = """
        drop table if exists kana_csep;
        """

        self.execute_query(delete_kana_csep_query)
        self.execute_query(delete_kana_typos_query)
        self.execute_query(delete_kana_incorrect_typos_query)
        self.execute_query(delete_kana_query)

##--------------------start-of-create_remote_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def create_remote_storage(self) -> None:

        """
        
        creates the tables for the remote storage\n

        Parameters:\n
        self (object - remoteHandler) : The handler object\n

        Returns:\n
        None\n

        """

        create_kana_query = """
        CREATE TABLE kana (
            id INT NOT NULL,
            kana VARCHAR(255) NOT NULL,
            reading VARCHAR(255) NOT NULL,
            incorrect_count INT NOT NULL,
            correct_count INT NOT NULL,
            word_type INT NOT NULL,
            PRIMARY KEY (id)
        );
        """

        create_kana_typos_query = """
        CREATE TABLE kana_typos (
            kana_id INT NOT NULL,
            typo_id INT NOT NULL,
            typo_value VARCHAR(255) NOT NULL,
            word_type INT NOT NULL,
            PRIMARY KEY (typo_id),
            FOREIGN KEY (kana_id) REFERENCES kana(id)
        );
        """

        create_kana_incorrect_typos_query = """
        CREATE TABLE kana_incorrect_typos (
            kana_id INT NOT NULL,
            incorrect_typo_id INT NOT NULL,
            incorrect_typo_value VARCHAR(255) NOT NULL,
            word_type INT NOT NULL,
            PRIMARY KEY (incorrect_typo_id),
            FOREIGN KEY (kana_id) REFERENCES kana(id)
        );
        """

        create_kana_csep_query = """
        create table kana_csep (
        kana_id INT NOT NULL,
        kana_csep_id INT NOT NULL,
        kana_csep_value VARCHAR(255) NOT NULL,
        word_type INT NOT NULL,
        PRIMARY KEY (kana_csep_id),
        FOREIGN KEY (kana_id) REFERENCES kana(id)
        );
        """

        self.execute_query(create_kana_query)
        self.execute_query(create_kana_typos_query)
        self.execute_query(create_kana_incorrect_typos_query)
        self.execute_query(create_kana_csep_query)

##--------------------start-of-fill_remote_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def fill_remote_storage(self) -> None:

        """
        
        fills the tables in remote storage with the local data\n

        Parameters:\n
        self (object - remoteHandler) : The handler object\n

        Returns\n
        None\n

        """

        def fill_kana():

            with open(self.kana_file, "r", encoding="utf-8") as file:

                for line in file:

                    values = line.strip().split(',')

                    table_name = "kana"
                    insert_dict = {
                    "id": values[0],
                    "kana": values[1],
                    "reading": values[2],
                    "incorrect_count": values[3],
                    "correct_count": values[4],
                    "word_type": 2
                    }

                    self.insert_into_table(table_name, insert_dict)

        def fill_kana_typos():

            with open(self.kana_typos_file, "r", encoding="utf-8") as file:

                for line in file:

                    values = line.strip().split(',')

                    values[2] = values[2].replace('\\', '\\\\')  ## Replace single backslash with double backslash
                    values[2] = values[2].replace("'", "\\'")    ## Escape single quotes with a backslash

                    table_name = "kana_typos"
                    insert_dict = {
                        "kana_id": values[0],
                        "typo_id": values[1],
                        "typo_value": values[2],
                        "word_type": values[3]
                    }
                    self.insert_into_table(table_name, insert_dict)
        
        def fill_kana_incorrect_typos():

                with open(self.kana_incorrect_typos_file, "r", encoding="utf-8") as file:

                    for line in file:

                        values = line.strip().split(',')

                        values[2] = values[2].replace('\\', '\\\\')  ## Replace single backslash with double backslash
                        values[2] = values[2].replace("'", "\\'")    ## Escape single quotes with a backslash

                        table_name = "kana_incorrect_typos"
                        insert_dict = {
                        "kana_id": values[0],
                        "incorrect_typo_id": values[1],
                        "incorrect_typo_value": values[2],
                        "word_type": values[3]
                        }

                        self.insert_into_table(table_name, insert_dict)


        fill_kana()
        fill_kana_typos()
        fill_kana_incorrect_typos()