## built-in modules
from datetime import datetime

import os
import time
import typing
import shutil
import base64

## third party modules
from mysql.connector import pooling

import mysql.connector 

## custom modules
from modules.typos import typo as typo_blueprint
from modules.typos import incorrectTypo as incorrect_typo_blueprint

from modules.csep import csep as csep_blueprint

from modules.words import word as kana_blueprint
from modules.vocab import vocab as vocab_blueprint

from modules import util
from modules.ensureFileSecurity import fileEnsurer

class remoteHandler():

    """
    
    The handler that handles the connection to the database and all interactions with it.\n

    """
##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, file_ensurer:fileEnsurer) -> None:

        """
        
        Initializes the remoteHandler class.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------objects----------------------------------------------------------------

        ## the file_ensurer used for paths here
        self.fileEnsurer = file_ensurer

        ##----------------------------------------------------------------dir----------------------------------------------------------------

        ## lib files for remoteHandler.py
        self.remote_lib_dir = os.path.join(self.fileEnsurer.lib_dir, "remote")

        ## archives for previous versions of Seisen txt files
        self.archives_dir = os.path.join(self.fileEnsurer.config_dir, "Archives")

        ## archives for the local files
        self.remote_archives_dir = os.path.join(self.archives_dir, "Database")

        ## archives for the local-Database files
        self.local_remote_archives_dir = os.path.join(self.archives_dir, "LocalRemote")

        ##----------------------------------------------------------------paths----------------------------------------------------------------

        ## the path to the file that stores the password
        self.password_file = os.path.join(os.path.join(self.fileEnsurer.config_dir, "Logins"), "credentials.txt")

        ## the paths to the file that stores the kana words and its typos
        self.kana_file = os.path.join(os.path.join(self.fileEnsurer.config_dir, "Kana"), "kana.txt")
        self.kana_typos_file = os.path.join(os.path.join(self.fileEnsurer.config_dir, "Kana"), "kana typos.txt")
        self.kana_incorrect_typos_file = os.path.join(os.path.join(self.fileEnsurer.config_dir, "Kana"), "kana incorrect typos.txt")

        ## the paths for all vocab related files
        self.vocab_path = os.path.join(self.fileEnsurer.vocab_dir, "vocab.txt")
        self.vocab_csep_path = os.path.join(self.fileEnsurer.vocab_dir, "vocab csep.txt")
        self.vocab_typos_path = os.path.join(self.fileEnsurer.vocab_dir, "vocab typos.txt")
        self.vocab_incorrect_typos_path = os.path.join(self.fileEnsurer.vocab_dir, "vocab incorrect typos.txt")

        ## if remoteHandler failed to make a database connection
        self.database_connection_failed = os.path.join(self.remote_lib_dir, "isConnectionFailed.txt")

        ## contains the date of the last local backup
        self.last_remote_backup_file = os.path.join(self.remote_archives_dir, "last_remote_backup.txt")

        ## contains the date of the last time the database was overwritten with local
        self.last_local_remote_backup_file = os.path.join(self.local_remote_archives_dir, "last_local_remote_backup.txt")

        ##----------------------------------------------------------------variables----------------------------------------------------------------
        
        ## the kana that seisen will use to test the user
        self.kana = [] 

        self.kana_typos = []
        self.kana_incorrect_typos = []

        ## the vocab that will be used to test the user
        self.vocab = []

        self.vocab_typos = []
        self.vocab_incorrect_typos = []
        self.vocab_csep = []

        ##----------------------------------------------------------------functions----------------------------------------------------------------

        ## the database connection, can either be itself or none
        self.connection = self.initialize_database_connection()

##--------------------start-of-execute_query()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def execute_query(self, query:str) -> None:

        """

        Executes a query to the database\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n
        query (str) : The query to be executed.\n

        Returns:\n
        None.\n

        """
        
        cursor = self.connection.cursor()
        cursor.execute(query)
        
        self.connection.commit()

##--------------------start-of-read_single_column_query()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def read_single_column_query(self, query:str) -> typing.List[str]:

        """

        reads a single column query from the database.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n
        query (str) : The query to be executed.\n

        Returns:\n
        results_actual (list - string) : The results of the query.\n

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
        
        inserts data into a table.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n
        table_name (str) : The name of the table.\n
        data (dict) : The data to be inserted.\n

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

        reads a multi column query from the database.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n
        query (str) : The query to be executed.\n

        Returns:\n
        results_by_column (list - list) : The results of the query.\n

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
    
##--------------------start-of-create_database_connection()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def create_database_connection(self, host_name:str, user_name:str, db_name:str, user_password:str) -> typing.Union[mysql.connector.connection.MySQLConnection, pooling.PooledMySQLConnection]:

        """

        Creates a connection to the database.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n
        host_name (str) : The host name of the database.\n
        user_name (str) : The user name of the database.\n
        db_name (str) : The name of the database.\n
        user_password (str) : The password of the database.\n

        Returns:\n
        connection (object - mysql.connector.connect.MySQLConnection) or (object - mysql.connector.pooling.PooledMySQLConnection) or None : The connection object to the database.\n

        """

        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            database= db_name,
            passwd=user_password)

        return connection

##-------------------start-of-initialize_database_connection()---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def initialize_database_connection(self) -> typing.Union[mysql.connector.connection.MySQLConnection, pooling.PooledMySQLConnection, None]:

        """

        Sets up the database connection. If the user has already entered the password for the database, the program will use the saved password. If not, the program will ask the user for the password.\n

        Parameters:\n
        None.\n

        Returns:\n
        connection (object - mysql.connector.connect.MySQLConnection) or (object - mysql.connector.pooling.PooledMySQLConnection) or None : The connection object to the database.\n

        """
        
        with open(self.database_connection_failed, "r+", encoding="utf-8") as file:
            if(file.read().strip() == "true"):
                print("Database connection has failed previously.... skipping\n")
                time.sleep(.1)
                return None
            
        self.start_marked_succeeded_database_connection()

        try:

            with open(self.password_file, 'r', encoding='utf-8') as file:  ## get saved connection credentials if exists
                credentials = file.readlines()

                database_name = base64.b64decode((credentials[0].strip()).encode('utf-8')).decode('utf-8')
                password = base64.b64decode((credentials[1].strip()).encode('utf-8')).decode('utf-8')

            connection = self.create_database_connection("localhost", "root", database_name, password)

            print("Used saved pass in " + self.password_file)

        except: ## else try to get credentials manually

            try: ## if valid save the credentials

                database_name = util.user_confirm("Please enter the name of the database you have")

                util.clear_console()

                password = util.user_confirm("Please enter the root password for your local database you have")

                credentials = [
                    base64.b64encode(database_name.encode('utf-8')).decode('utf-8'),
                        base64.b64encode(password.encode('utf-8')).decode('utf-8')]
                
                connection = self.create_database_connection("localhost", "root", database_name, password)
                            
                util.standard_create_file(self.password_file) 

                time.sleep(0.1)

                credentials = [x + '\n' for x  in credentials]

                with open(self.password_file, "w+",encoding='utf-8') as file:
                    file.writelines(credentials)

            except AssertionError:
                
                util.clear_console()

                self.start_marked_failed_database_connection()

                connection = None

            except Exception as e: ## if invalid exit
                        
                util.clear_console()

                print(str(e))
                print("Error with creating connection object, please double check your password and database name\n")

                self.start_marked_failed_database_connection()

                connection = None

                util.pause_console()
            
        return connection
    
##--------------------start-of-mark_failed_database_connection()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def start_marked_failed_database_connection(self) -> None:
         
        """
        
        Marks a file in lib that the most recently attempted database connection has failed to connect.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n

        Returns:\n
        None.\n

        """

        with open(self.database_connection_failed, "w+", encoding="utf-8") as file:
            file.write("true")

##--------------------start-of-mark_succeeded_database_connection()---------------------------S---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def start_marked_succeeded_database_connection(self) -> None:
         
        """
        
        Marks a file in lib that the most recently attempted database connection has succeeded.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n

        Returns:\n
        None.\n

        """

        with open(self.database_connection_failed, "w+", encoding="utf-8") as file:
            file.write("false")

##--------------------start-of-reset_local_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def reset_local_storage(self) -> None:

        """
        
        loads the words from the database and replaces the local storage with it.\n
        Note that this will reset all the words locally stored on this device.\n
        Use carefully!\n

        Parameters:\n
        self (object - remoteHandler) : The handler object\n

        Returns:\n
        None\n

        """

        ##----------------------------------------------------------------clear_local_kana()----------------------------------------------------------------

        def clear_local_kana():

            with open(self.kana_file, "w", encoding="utf-8") as file:
                file.truncate(0)
                
            with open(self.kana_typos_file, "w", encoding="utf-8") as file:
                file.truncate(0)

            with open(self.kana_incorrect_typos_file, "w", encoding="utf-8") as file:
                file.truncate(0)

        ##----------------------------------------------------------------clear_local_vocab()----------------------------------------------------------------

        def clear_local_vocab():

            with open(self.vocab_path, "w", encoding="utf-8") as file:
                file.truncate(0)

            with open(self.vocab_csep_path, "w", encoding="utf-8") as file:
                file.truncate(0)

            with open(self.vocab_typos_path, "w", encoding="utf-8") as file:
                file.truncate(0)

            with open(self.vocab_incorrect_typos_path, "w", encoding="utf-8") as file:
                file.truncate(0)

        ##----------------------------------------------------------------reset_kana_relations()----------------------------------------------------------------

        def reset_kana_relations():
            
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
                    if(typo.word_type == kana.word_type and typo.word_id == kana.word_id):
                        kana.typos.append(typo)        

                for incorrect_typo in self.kana_incorrect_typos:
                    if(incorrect_typo.word_type == kana.word_type and incorrect_typo.word_id == kana.word_id):
                        kana.incorrect_typos.append(incorrect_typo)

        ##----------------------------------------------------------------reset_vocab_relations()----------------------------------------------------------------
                
        def reset_vocab_relations():

            self.vocab.clear()
            self.vocab_typos.clear()
            self.vocab_incorrect_typos.clear()

            word_id_list, vocab_list, romaji_list, answer_list, furigana_list, pValue_list, cValue_list, isKanji_list = self.read_multi_column_query("select id, vocab, romaji, answer, furigana, incorrect_count, correct_count, isKanji from vocab")
            typo_word_type_list, typo_id_list, typo_word_id_list, typo_value_list = self.read_multi_column_query("select word_type, typo_id, vocab_id, typo_value from vocab_typos")
            incorrect_typo_word_type_list, incorrect_typo_id_list, incorrect_typo_word_id_list, incorrect_typo_value_list = self.read_multi_column_query("select word_type, incorrect_typo_id, vocab_id, incorrect_typo_value from vocab_incorrect_typos")
            vocab_id_list, csep_id_list, csep_value_list, word_type_list = self.read_multi_column_query("select vocab_id, vocab_csep_id, vocab_csep_value, word_type from vocab_csep")

            self.vocab = [vocab_blueprint(int(word_id_list[i]), vocab_list[i], romaji_list[i], answer_list[i], [], furigana_list[i], int(pValue_list[i]), int(cValue_list[i]), bool(isKanji_list[i])) for i in range(len(word_id_list))]
            self.vocab_typos = [typo_blueprint(typo_word_type_list[i], int(typo_id_list[i]), int(typo_word_id_list[i]), typo_value_list[i]) for i in range(len(typo_word_id_list))]
            self.vocab_incorrect_typos = [incorrect_typo_blueprint(incorrect_typo_word_type_list[i], int(incorrect_typo_id_list[i]), int(incorrect_typo_word_id_list[i]), incorrect_typo_value_list[i]) for i in range(len(incorrect_typo_word_id_list))]
            self.vocab_csep = [csep_blueprint(int(vocab_id_list[i]), int(csep_id_list[i]), csep_value_list[i], word_type_list[i]) for i in range(len(vocab_id_list))]

            for vocab in self.vocab:
                vocab_values = [vocab.word_id, vocab.testing_material, vocab.romaji, vocab.testing_material_answer_main, vocab.furigana, vocab.incorrect_count, vocab.correct_count]
                util.write_sei_line(self.vocab_path, vocab_values)

            for typo in self.vocab_typos:
                typo_values = [typo.word_id, typo.typo_id, typo.typo_value, typo.word_type]
                util.write_sei_line(self.vocab_typos_path, typo_values)

            for incorrect_typo in self.vocab_incorrect_typos:
                incorrect_typo_values = [incorrect_typo.word_id, incorrect_typo.incorrect_typo_id, incorrect_typo.incorrect_typo_value, incorrect_typo.word_type]
                util.write_sei_line(self.vocab_incorrect_typos_path, incorrect_typo_values)

            for csep in self.vocab_csep:
                csep_values = [csep.word_id, csep.csep_id, csep.csep_value, csep.word_type]
                util.write_sei_line(self.vocab_csep_path, csep_values)

            for vocab in self.vocab:

                for typo in self.vocab_typos:
                    if(typo.word_type == vocab.word_type and typo.word_id == vocab.word_id):
                        vocab.typos.append(typo)        

                for incorrect_typo in self.vocab_incorrect_typos:
                    if(incorrect_typo.word_type == vocab.word_type and incorrect_typo.word_id == vocab.word_id):
                        vocab.incorrect_typos.append(incorrect_typo)

                for csep in self.vocab_csep:
                    if(csep.word_id == vocab.word_id and csep.word_type == vocab.word_type):
                        vocab.testing_material_answer_all.append(csep)


        ##----------------------------------------------------------------main()----------------------------------------------------------------

        ## local storage does not reset if there is no valid database connection
        if(self.connection == None): 
            return
        
        clear_local_kana()
        clear_local_vocab()

        reset_kana_relations()
        reset_vocab_relations()
      
##--------------------start-of-reset_remote_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def reset_remote_storage(self):

        """
        
        resets the remote storage with the local storage.\n
        Note that this will reset all the words remotely stored on the connected database.\n
        Use Carefully!\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n

        Returns:\n
        None.\n

        """

        self.delete_remote_storage()
        self.create_remote_storage()
        self.fill_remote_storage()

##--------------------start-of-delete_remote_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def delete_remote_storage(self) -> None:

        """
        
        resets the remote storage.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------kana----------------------------------------------------------------

        delete_kana_csep_query = """
        drop table if exists kana_csep;
        """

        delete_kana_typos_query = """
        drop table if exists kana_typos;
        """

        delete_kana_incorrect_typos_query = """
        drop table if exists kana_incorrect_typos;
        """

        delete_kana_query = """
        drop table if exists kana;
        """

        ##----------------------------------------------------------------vocab----------------------------------------------------------------

        delete_vocab_csep_query = """
        drop table if exists vocab_csep;
        """

        delete_vocab_typos_query = """
        drop table if exists vocab_typos;
        """

        delete_vocab_incorrect_typos_query = """
        drop table if exists vocab_incorrect_typos;
        """

        delete_vocab_query = """
        drop table if exists vocab;
        """

        ##----------------------------------------------------------------calls----------------------------------------------------------------

        self.execute_query(delete_kana_csep_query)
        self.execute_query(delete_kana_typos_query)
        self.execute_query(delete_kana_incorrect_typos_query)
        self.execute_query(delete_kana_query)

        self.execute_query(delete_vocab_csep_query)
        self.execute_query(delete_vocab_typos_query)
        self.execute_query(delete_vocab_incorrect_typos_query)
        self.execute_query(delete_vocab_query)

##--------------------start-of-create_remote_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def create_remote_storage(self) -> None:

        """
        
        creates the tables for the remote storage.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------kana----------------------------------------------------------------

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
        CREATE TABLE kana_csep (
            kana_id INT NOT NULL,
            kana_csep_id INT NOT NULL,
            kana_csep_value VARCHAR(255) NOT NULL,
            word_type INT NOT NULL,
            PRIMARY KEY (kana_csep_id),
            FOREIGN KEY (kana_id) REFERENCES kana(id)
        );
        """

        ##----------------------------------------------------------------vocab----------------------------------------------------------------

        create_vocab_query = """
        CREATE TABLE vocab (
            id INT NOT NULL,
            vocab VARCHAR(255) NOT NULL,
            romaji VARCHAR(255) NOT NULL,
            answer VARCHAR(255) NOT NULL,
            furigana VARCHAR(255) NOT NULL,
            incorrect_count INT NOT NULL,
            correct_count INT NOT NULL,
            word_type INT NOT NULL,
            isKanji TINYINT(1) NOT NULL,
            PRIMARY KEY (id)
        );

        """        
        create_vocab_typos_query = """
        CREATE TABLE vocab_typos (
            vocab_id INT NOT NULL,
            typo_id INT NOT NULL,
            typo_value VARCHAR(255) NOT NULL,
            word_type INT NOT NULL,
            PRIMARY KEY (typo_id),
            FOREIGN KEY (vocab_id) REFERENCES vocab(id)
        );
        """

        create_vocab_incorrect_typos_query = """
        CREATE TABLE vocab_incorrect_typos (
            vocab_id INT NOT NULL,
            incorrect_typo_id INT NOT NULL,
            incorrect_typo_value VARCHAR(255) NOT NULL,
            word_type INT NOT NULL,
            PRIMARY KEY (incorrect_typo_id),
            FOREIGN KEY (vocab_id) REFERENCES vocab(id)
        );
        """

        create_vocab_csep_query = """
        CREATE TABLE vocab_csep (
            vocab_id INT NOT NULL,
            vocab_csep_id INT NOT NULL,
            vocab_csep_value VARCHAR(255) NOT NULL,
            word_type INT NOT NULL,
            PRIMARY KEY (vocab_csep_id),
            FOREIGN KEY (vocab_id) REFERENCES vocab(id)
        );
        """

        ##----------------------------------------------------------------queries----------------------------------------------------------------

        self.execute_query(create_kana_query)
        self.execute_query(create_kana_typos_query)
        self.execute_query(create_kana_incorrect_typos_query)
        self.execute_query(create_kana_csep_query)

        self.execute_query(create_vocab_query)
        self.execute_query(create_vocab_typos_query)
        self.execute_query(create_vocab_incorrect_typos_query)
        self.execute_query(create_vocab_csep_query)

##--------------------start-of-fill_remote_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def fill_remote_storage(self) -> None:

        """
        
        fills the tables in remote storage with the local data.\n

        Parameters:\n
        self (object - remoteHandler) : The handler object.\n

        Returns\n
        None.\n

        """


        ##----------------------------------------------------------------kana----------------------------------------------------------------

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

        ##----------------------------------------------------------------vocab----------------------------------------------------------------

        def fill_vocab():

            with open(self.vocab_path, "r", encoding="utf-8") as file:

                for line in file:

                    values = line.strip().split(',')

                    if(values[4] == "0"):
                        isKanji = 0
                    else:
                        isKanji = 1
                    

                    table_name = "vocab"
                    insert_dict = {
                    "id": values[0],
                    "vocab": values[1],
                    "romaji": values[2],
                    "answer": values[3],
                    "furigana": values[4],
                    "incorrect_count": values[5],
                    "correct_count": values[6],
                    "word_type": 2,
                    "isKanji": isKanji
                    }

                    self.insert_into_table(table_name, insert_dict)

        def fill_vocab_typos():

            with open(self.vocab_typos_path, "r", encoding="utf-8") as file:

                for line in file:

                    values = line.strip().split(',')

                    values[2] = values[2].replace('\\', '\\\\')  ## Replace single backslash with double backslash
                    values[2] = values[2].replace("'", "\\'")    ## Escape single quotes with a backslash

                    table_name = "vocab_typos"
                    insert_dict = {
                        "vocab_id": values[0],
                        "typo_id": values[1],
                        "typo_value": values[2],
                        "word_type": values[3]
                    }
                    self.insert_into_table(table_name, insert_dict)
        
        def fill_vocab_incorrect_typos():

                with open(self.vocab_incorrect_typos_path, "r", encoding="utf-8") as file:

                    for line in file:

                        values = line.strip().split(',')

                        values[2] = values[2].replace('\\', '\\\\')  ## Replace single backslash with double backslash
                        values[2] = values[2].replace("'", "\\'")    ## Escape single quotes with a backslash

                        table_name = "vocab_incorrect_typos"
                        insert_dict = {
                        "vocab_id": values[0],
                        "incorrect_typo_id": values[1],
                        "incorrect_typo_value": values[2],
                        "word_type": values[3]
                        }

                        self.insert_into_table(table_name, insert_dict)

        def fill_vocab_csep():
                                
                with open(self.vocab_csep_path, "r", encoding="utf-8") as file:

                    for line in file:

                        values = line.strip().split(',')

                        values[2] = values[2].replace('\\', '\\\\')  ## Replace single backslash with double backslash
                        values[2] = values[2].replace("'", "\\'")    ## Escape single quotes with a backslash

                        table_name = "vocab_csep"
                        insert_dict = {
                        "vocab_id": values[0],
                        "vocab_csep_id": values[1],
                        "vocab_csep_value": values[2],
                        "word_type": values[3]
                        }

                        self.insert_into_table(table_name, insert_dict)

        ##----------------------------------------------------------------functions----------------------------------------------------------------

        fill_kana()
        fill_kana_typos()
        fill_kana_incorrect_typos()

        fill_vocab()
        fill_vocab_typos
        fill_vocab_incorrect_typos()
        fill_vocab_csep()

##--------------------start-of-create_daily_remote_backup()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def create_daily_remote_backup(self):

        """
        
        Creates Seisen's daily remote backup.\n

        Parameters:\n
        self (object - Seisen) : the Seisen object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------kana----------------------------------------------------------------

        def backup_kana():

            list_of_all_accepted_answers = []

            remote_archive_kana_dir = os.path.join(archive_dir, "Kana")

            remote_archive_kana_path = os.path.join(remote_archive_kana_dir, "kana.txt")
            remote_archive_kana_typos_path = os.path.join(remote_archive_kana_dir, "kana typos.txt")
            remote_archive_kana_incorrect_typos_path = os.path.join(remote_archive_kana_dir, "kana incorrect typos.txt")

            util.standard_create_directory(remote_archive_kana_dir)

            word_id_list, jValue_list, eValue_list, pValue_list, cValue_list = self.read_multi_column_query("select id, kana, reading, incorrect_count, correct_count from kana")
            typo_word_type_list, typo_id_list, typo_word_id_list, typo_value_list = self.read_multi_column_query("select word_type, typo_id, kana_id, typo_value from kana_typos")
            incorrect_typo_word_type_list, incorrect_typo_id_list, incorrect_typo_word_id_list, incorrect_typo_value_list = self.read_multi_column_query("select word_type, incorrect_typo_id, kana_id, incorrect_typo_value from kana_incorrect_typos")

            self.kana = [kana_blueprint(int(word_id_list[i]), jValue_list[i], eValue_list[i], list_of_all_accepted_answers, int(pValue_list[i]), int(cValue_list[i])) for i in range(len(word_id_list))]
            self.kana_typos = [typo_blueprint(typo_word_type_list[i], int(typo_id_list[i]), int(typo_word_id_list[i]), typo_value_list[i]) for i in range(len(typo_word_id_list))]
            self.kana_incorrect_typos = [incorrect_typo_blueprint(incorrect_typo_word_type_list[i], int(incorrect_typo_id_list[i]), int(incorrect_typo_word_id_list[i]), incorrect_typo_value_list[i]) for i in range(len(incorrect_typo_word_id_list))]

            for kana in self.kana:
                word_values = [kana.word_id, kana.testing_material, kana.testing_material_answer_main, kana.incorrect_count, kana.correct_count]
                util.write_sei_line(remote_archive_kana_path, word_values)

            for typo in self.kana_typos:
                typo_values = [typo.word_id, typo.typo_id, typo.typo_value, typo.word_type]
                util.write_sei_line(remote_archive_kana_typos_path, typo_values)

            for incorrect_typo in self.kana_incorrect_typos:
                incorrect_typo_values = [incorrect_typo.word_id, incorrect_typo.incorrect_typo_id, incorrect_typo.incorrect_typo_value, incorrect_typo.word_type]
                util.write_sei_line(remote_archive_kana_incorrect_typos_path, incorrect_typo_values)

        ##----------------------------------------------------------------vocab----------------------------------------------------------------

        def backup_vocab():

            remote_archive_vocab_dir = os.path.join(archive_dir, "Vocab")

            remote_archive_vocab_path = os.path.join(remote_archive_vocab_dir, "vocab.txt")
            remote_archive_vocab_typos_path = os.path.join(remote_archive_vocab_dir, "vocab typos.txt")
            remote_archive_vocab_incorrect_typos_path = os.path.join(remote_archive_vocab_dir, "vocab incorrect typos.txt")
            remote_archive_vocab_csep_path = os.path.join(remote_archive_vocab_dir, "vocab csep.txt")

            util.standard_create_directory(remote_archive_vocab_dir)

            word_id_list, vocab_list, romaji_list, answer_list, furigana_list, pValue_list, cValue_list, isKanji_list = self.read_multi_column_query("select id, vocab, romaji, answer, furigana, incorrect_count, correct_count, isKanji from vocab")
            typo_word_type_list, typo_id_list, typo_word_id_list, typo_value_list = self.read_multi_column_query("select word_type, typo_id, vocab_id, typo_value from vocab_typos")
            incorrect_typo_word_type_list, incorrect_typo_id_list, incorrect_typo_word_id_list, incorrect_typo_value_list = self.read_multi_column_query("select word_type, incorrect_typo_id, vocab_id, incorrect_typo_value from vocab_incorrect_typos")
            vocab_id_list, csep_id_list, csep_value_list, word_type_list = self.read_multi_column_query("select vocab_id, vocab_csep_id, vocab_csep_value, word_type from vocab_csep")

            self.vocab = [vocab_blueprint(int(word_id_list[i]), vocab_list[i], romaji_list[i], answer_list[i], [], furigana_list[i], int(pValue_list[i]), int(cValue_list[i]), bool(isKanji_list[i])) for i in range(len(word_id_list))]
            self.vocab_typos = [typo_blueprint(typo_word_type_list[i], int(typo_id_list[i]), int(typo_word_id_list[i]), typo_value_list[i]) for i in range(len(typo_word_id_list))]
            self.vocab_incorrect_typos = [incorrect_typo_blueprint(incorrect_typo_word_type_list[i], int(incorrect_typo_id_list[i]), int(incorrect_typo_word_id_list[i]), incorrect_typo_value_list[i]) for i in range(len(incorrect_typo_word_id_list))]
            self.vocab_csep = [csep_blueprint(int(vocab_id_list[i]), int(csep_id_list[i]), csep_value_list[i], word_type_list[i]) for i in range(len(vocab_id_list))]

            for vocab in self.vocab:
                vocab_values = [vocab.word_id, vocab.testing_material, vocab.romaji, vocab.testing_material_answer_main, vocab.furigana, vocab.incorrect_count, vocab.correct_count]
                util.write_sei_line(remote_archive_vocab_path, vocab_values)

            for typo in self.vocab_typos:
                typo_values = [typo.word_id, typo.typo_id, typo.typo_value, typo.word_type]
                util.write_sei_line(remote_archive_vocab_typos_path, typo_values)

            for incorrect_typo in self.vocab_incorrect_typos:
                incorrect_typo_values = [incorrect_typo.word_id, incorrect_typo.incorrect_typo_id, incorrect_typo.incorrect_typo_value, incorrect_typo.word_type]
                util.write_sei_line(remote_archive_vocab_incorrect_typos_path, incorrect_typo_values)

            for csep in self.vocab_csep:
                csep_values = [csep.word_id, csep.csep_id, csep.csep_value, csep.word_type]
                util.write_sei_line(remote_archive_vocab_csep_path, csep_values)

        ##----------------------------------------------------------------main----------------------------------------------------------------


        if(self.connection is None):
            return

        with open(self.last_remote_backup_file, 'r+', encoding="utf-8") as file:

            last_backup_date = str(file.read().strip())
            last_backup_date = last_backup_date.strip('\x00')
        
            current_day = str(datetime.today().strftime('%Y-%m-%d'))

            if(last_backup_date != current_day):
                archive_dir = util.create_archive_dir(1)

                file.truncate(0)

                file.write(current_day.strip())

                backup_kana()
                backup_vocab()

            else:
                pass
  
##--------------------start-of-restore_remote_backup()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def restore_remote_backup(self) -> None:

        """
        
        Prompts a user to restore a remote backup and does so if valid.\n

        Parameters:\n
        self (object - remoteHandler) : the handler object\n

        Returns:\n
        None.\n

        """

        valid_backups = []

        backup_to_restore_prompt = ""
        
        util.clear_console()
        
        print("Please select a backup to restore:\n")
        
        for item in os.listdir(self.remote_archives_dir):
        
            full_path = os.path.join(self.remote_archives_dir, item)
        
            if(os.path.isdir(full_path)):
                print(item)
                valid_backups.append(item)
                backup_to_restore_prompt += item + "\n"
        
        backup_to_restore_prompt += "\nPlease select a backup to restore, please keep in mind that this process is not easily reversible.\n\n"

        backup_to_restore = util.user_confirm(backup_to_restore_prompt)

        try: ## user confirm will throw an assertion error if  the user wants to cancel the backup restore.

            if(backup_to_restore in valid_backups):
                util.clear_console()

                shutil.rmtree(self.fileEnsurer.kana_dir)
                shutil.rmtree(self.fileEnsurer.vocab_dir)

                shutil.copytree(os.path.join(self.remote_archives_dir, backup_to_restore), self.fileEnsurer.config_dir, dirs_exist_ok=True)

            else:
                print("Invalid Backup\n")
                time.sleep(1)

        except AssertionError:
            pass

##--------------------start-of-local_remote_overwrite()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def local_remote_overwrite(self) -> None:

        if(self.connection is None):
            return
        
        with open(self.last_local_remote_backup_file, 'r+', encoding="utf-8") as file:

            last_backup_date = str(file.read().strip())
            last_backup_date = last_backup_date.strip('\x00')
        
            current_day = str(datetime.today().strftime('%Y-%m-%d'))

            if(last_backup_date != current_day):
                print("Overwriting Remote with Local")
                time.sleep(1)

                file.truncate(0)
                
                file.write(current_day.strip())

                self.reset_remote_storage()