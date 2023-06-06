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

class dataHandler():

    """
    
    The handler that handles the connection to the database and all interactions with it. As well as all interactions with local storage.\n

    """
##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self) -> None:

        """
        
        The __init__() method initializes the dataHandler class\n

        Parameters:\n
        self (object - dataHandler) : The handler object\n

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

        ## the database connection object
        self.connection = self.initialize_database_connection()

        ## the kana that seisen will use to test the user
        self.kana = [] 

        ## the literal used in the database to flag words as Kana
        self.KANA_WORD_TYPE = "2"

        ## the accepted typos for kana
        self.kana_typos = []

        ## the accepted incorrect typos for kana
        self.kana_incorrect_typos = []

##--------------------start-of-load_words_local_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def load_words_from_local_storage(self) -> None:
        
        """
        
        loads the words from the local storage\n

        Parameters:\n
        self (object - dataHandler) : The handler object\n

        Returns:\n
        None\n

        """

        KANA_TYPO_WORD_ID_INDEX_LOCATION = 0
        KANA_TYPO_TYPO_ID_INDEX_LOCATION = 1
        KANA_TYPO_VALUE_INDEX_LOCATION = 2
        KANA_TYPO_WORD_TYPE_INDEX_LOCATION = 3
        


        self.kana.clear()

        with open(self.kana_file, "r", encoding="utf-8") as file:

            for line in file:

                values = line.strip().split(',')

                self.kana.append(kana_blueprint(int(values[0]), values[1], values[2], [], int(values[3]), int(values[4])))

        with open(self.kana_typos_file, "r", encoding="utf-8") as file:

            for line in file:
                
                values = line.strip().split(',')

                if(int(values[0]) == self.KANA_WORD_TYPE):
                    for kana in self.kana:
                        if(kana.word_id == int(values[1])):
                            kana.typos.append(typo_blueprint(int(values[0]), int(values[1]), int(values[2]), values[4]))

        with open(self.kana_incorrect_typos_file, "r", encoding="utf-8") as file:

            for line in file:

                values = line.strip().split(',')

                if(int(values[0]) == self.KANA_WORD_TYPE):
                    for kana in self.kana:
                        if(kana.word_id == int(values[1])):
                            kana.incorrect_typos.append(incorrect_typo_blueprint(int(values[0]), int(values[1]), int(values[2]), values[4]))

##--------------------start-of-load_words()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def reset_words_from_database(self) -> None:

        """
        
        loads the words from the database and replaces the local storage with it\n
        Note that this will reset all the words locally stored on this device\n
        Use carefully!\n

        Parameters:\n
        self (object - dataHandler) : The handler object\n

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
            
            word_id_list, jValue_list, eValue_list, pValue_list, cValue_list = self.read_multi_column_query("select word_id, jValue, eValue, pValue, cValue from words where word_type = " + KANA_WORD_TYPE)
            typo_word_type_list, typo_id_list, typo_word_id_list, typo_value_list = self.read_multi_column_query("select word_type, typo_id, word_id, typo from typos where word_type = " + KANA_WORD_TYPE)
            incorrect_typo_word_type_list, incorrect_typo_id_list, incorrect_typo_word_id_list, incorrect_typo_value_list = self.read_multi_column_query("select word_type, itypo_id, word_id, itypo from itypos where word_type = " + KANA_WORD_TYPE)

            self.kana = [kana_blueprint(int(word_id_list[i]), jValue_list[i], eValue_list[i], list_of_all_accepted_answers, int(pValue_list[i]), int(cValue_list[i])) for i in range(len(word_id_list))]
            self.kana_typos = [typo_blueprint(int(typo_word_type_list[i]), int(typo_id_list[i]), int(typo_word_id_list[i]), typo_value_list[i]) for i in range(len(typo_word_id_list))]
            self.kana_incorrect_typos = [incorrect_typo_blueprint(int(incorrect_typo_word_type_list[i]), int(incorrect_typo_id_list[i]), int(incorrect_typo_word_id_list[i]), incorrect_typo_value_list[i]) for i in range(len(incorrect_typo_word_id_list))]

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
        self (object - dataHandler) : The handler object\n
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
                        
                os.system('cls')

                print(str(e))
                print("Error with creating connection object, please double check your password\n")

                os.system('pause')
                
                exit()

        return connection
    
##--------------------start-of-execute_query()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def execute_query(self, query:str) -> None:

        """

        Executes a query to the database\n

        Parameters:\n
        self (object - dataHandler) : The handler object\n
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
        self (object - dataHandler) : The handler object\n
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

    def read_multi_column_query(self, query:str) -> typing.List[typing.List[str]]:

        """

        reads a multi column query from the database\n

        Parameters:\n
        self (object - dataHandler) : The handler object\n
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
    
##--------------------start-of-get_list_of_all_ids()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_list_of_all_ids(self, type_of_id_to_query:int) -> typing.List[int]:

        """

        Gets the list of all ids in the database\n

        Parameters:\n
        self (object - dataHandler) : The handler object\n

        Returns:\n
        ids (list - string) : The list of all ids in the database\n

        """

        ids = []

        TYPO_ID_IDENTIFIER = 1

        if(type_of_id_to_query == TYPO_ID_IDENTIFIER):
            ids = self.read_single_column_query("select typo_id from typos order by typo_id")

        ids =  [int(x) for x in ids]


        return ids