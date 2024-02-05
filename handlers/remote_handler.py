## built-in modules
from datetime import datetime

import os
import shutil
import time
import typing

## custom modules
from entities.typo import Typo
from entities.incorrect_typo import IncorrectTypo

from entities.answer import Answer
from entities.vocab import Vocab
from entities.reading import Reading
from entities.testing_material import TestingMaterial
from entities.word import Word

from modules.file_ensurer import FileEnsurer
from modules.toolkit import Toolkit
from modules.logger import Logger

from handlers.file_handler import FileHandler

## Prevents errors if mysql-connector-python is not installed
try:
    from handlers.connection_handler import ConnectionHandler

    FileEnsurer.remote_enabled = True

except ImportError:
    FileEnsurer.remote_enabled = False

class RemoteHandler():

    """
    
    The handler that handles all interactions with the mysql database (remote).

    """

    kana:typing.List[Word] = [] 

    vocab:typing.List[Vocab] = []


##--------------------start-of-is_remote_enabled()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def is_remote_enabled() -> bool:

        """

        Returns whether the remote storage is enabled or not.

        Returns:
        bool: True if remote storage is enabled, False otherwise.

        """

        return FileEnsurer.remote_enabled

##--------------------start-of-set_up_new_database()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def set_up_new_database() -> None:

        """
        
        Unlinks the current database and causes the remote handler to prompt for a new database.

        """

        if(not RemoteHandler.is_remote_enabled()):
            print("Remote storage is not enabled. Please install mysql-connector-python and restart Seisen.\n")
            Toolkit.pause_console()
            return
        
        ## forces the RemoteHandler to not skip a remote connection upon next attempt
        ConnectionHandler.start_marked_succeeded_remote_connection()
        
        ## clears the credentials file so that if a valid login exists, it's not used and prompts for a new one
        ConnectionHandler.clear_credentials_file()

        ## reinitializes the database connection 
        ConnectionHandler.initialize_database_connection()

        Logger.log_action("Database connection has been reset...")

##--------------------start-of-setup_connection_handler()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def setup_connection_handler() -> None:

        """
        
        Sets up the connection handler.

        """

        if(not RemoteHandler.is_remote_enabled()):
            return

        ConnectionHandler.connection, ConnectionHandler.cursor = ConnectionHandler.initialize_database_connection()

##--------------------start-of-assemble_kana()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def assemble_kana() -> None:

        """

        Assembles the kana objects from the remote storage.

        """

        if(not RemoteHandler.is_remote_enabled()):
            return

        RemoteHandler.kana.clear()

        kana_id_list, correct_count_list, incorrect_count_list = ConnectionHandler.read_multi_column_query("select id, correct_count, incorrect_count from kana")
        typo_kana_id_list, typo_id_list, typo_list = ConnectionHandler.read_multi_column_query("select kana_id, typo_id, typo from kana_typos")
        incorrect_typo_kana_id_list, incorrect_typo_id_list, incorrect_typo_list = ConnectionHandler.read_multi_column_query("select kana_id, incorrect_typo_id, incorrect_typo from kana_incorrect_typos") 
        answer_kana_id_list, answer_id_list, answer_list = ConnectionHandler.read_multi_column_query("select kana_id, answer_id, answer from kana_answers")
        testing_material_kana_id_list, testing_material_id_list, testing_material_list = ConnectionHandler.read_multi_column_query("select kana_id, testing_material_id, testing_material from kana_testing_material")
        reading_kana_id_list, reading_id_list, furigana_list, romaji_list = ConnectionHandler.read_multi_column_query("select kana_id, reading_id, furigana, romaji from kana_readings")

        ## construct typos
        kana_typos = [Typo(int(typo_kana_id_list[i]), int(typo_id_list[i]), typo_list[i]) for i in range(len(typo_kana_id_list))]
        kana_incorrect_typos = [IncorrectTypo(int(incorrect_typo_kana_id_list[i]), int(incorrect_typo_id_list[i]), incorrect_typo_list[i]) for i in range(len(incorrect_typo_kana_id_list))]

        ## construct answers, testing_materials, and readings
        kana_answers = [Answer(int(answer_kana_id_list[i]), int(answer_id_list[i]), answer_list[i]) for i in range(len(answer_kana_id_list))]
        kana_testing_materials = [TestingMaterial(int(testing_material_kana_id_list[i]), int(testing_material_id_list[i]), testing_material_list[i]) for i in range(len(testing_material_kana_id_list))]
        kana_readings = [Reading(int(reading_kana_id_list[i]), int(reading_id_list[i]), furigana_list[i], romaji_list[i]) for i in range(len(reading_kana_id_list))]

        ## construct kana dummy objects
        for i in range(len(kana_id_list)):
            kana = Word(int(kana_id_list[i]), [kana_testing_materials[0]], [kana_answers[0]], [kana_readings[0]], int(correct_count_list[i]), int(incorrect_count_list[i])) 
            RemoteHandler.kana.append(kana)

        ## fill kana objects with their respective answers, testing_materials, and readings
        for kana in RemoteHandler.kana:

            ## clear out old dummy data
            kana.testing_material.clear()
            kana.answers.clear()
            kana.readings.clear()

            for testing_material in kana_testing_materials:
                if(testing_material.word_id == kana.id):

                    is_first_testing_material = True

                    if(is_first_testing_material):  
                        kana.main_testing_material = testing_material
                        is_first_testing_material = False

                    kana.testing_material.append(testing_material)
                    Logger.log_action("Added Testing Material " + testing_material.value + " to Kana " + str(kana.id))

            for answer in kana_answers:
                if(answer.word_id == kana.id):

                    is_first_answer = True

                    if(is_first_answer):
                        kana.main_answer = answer
                        is_first_answer = False
                    
                    kana.answers.append(answer)
                    Logger.log_action("Added Synonym " + answer.value + " to Kana " + kana.main_testing_material.value)

            for reading in kana_readings:
                if(reading.word_id == kana.id):

                    is_first_reading = True

                    if(is_first_reading):
                        kana.main_reading = reading
                        is_first_reading = False

                    kana.readings.append(reading)
                    Logger.log_action("Added Reading " + reading.furigana + " to Kana " + kana.main_testing_material.value)

        ## fill kana objects with their respective typos, incorrect typos
        for kana in RemoteHandler.kana:
            for typo in kana_typos:
                if(typo.word_id == kana.id):
                    kana.typos.append(typo)
                    Logger.log_action("Added Typo " + typo.value + " to Kana " + kana.main_testing_material.value)

            for incorrect_typo in kana_incorrect_typos:
                if(incorrect_typo.word_id == kana.id):
                    kana.incorrect_typos.append(incorrect_typo)
                    Logger.log_action("Added Incorrect Typo " + incorrect_typo.value + " to Kana " + kana.main_testing_material.value)

##--------------------start-of-write_kana_to_disk()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def write_kana_to_disk(kana_path:str, kana_testing_material_path:str, kana_answers_path:str, kana_readings_path:str, kana_typos_path:str, kana_incorrect_typos_path:str) -> None:

        """
        
        Writes the kana objects to local storage.

        Parameters:
        kana_path (str) : The path to the kana file.
        kana_testing_material_path (str) : The path to the kana testing material file.
        kana_answers_path (str) : The path to the kana answers file.
        kana_readings_path (str) : The path to the kana readings file.
        kana_typos_path (str) : The path to the kana typos file.
        kana_incorrect_typos_path (str) : The path to the kana incorrect typos file.

        """

        if(not RemoteHandler.is_remote_enabled()):
            return


        values_to_write_list = []

        ## apply changes to local storage
        for kana in RemoteHandler.kana:

            kana_values = [kana.id, kana.correct_count, kana.incorrect_count]
            FileHandler.write_seisen_line(kana_path, kana_values)
            
            for testing_material in kana.testing_material:
                testing_material_values = [testing_material.word_id, testing_material.id, testing_material.value]
                values_to_write_list.append(testing_material_values)

            FileHandler.write_seisen_lines(kana_testing_material_path, values_to_write_list)
            values_to_write_list.clear()

            for answer in kana.answers:
                answer_values = [answer.word_id, answer.id, answer.value]
                values_to_write_list.append(answer_values)

            FileHandler.write_seisen_lines(kana_answers_path, values_to_write_list)
            values_to_write_list.clear()

            for reading in kana.readings:
                reading_values = [reading.word_id, reading.id, reading.furigana, reading.romaji]
                values_to_write_list.append(reading_values)

            FileHandler.write_seisen_lines(kana_readings_path, values_to_write_list)

            for typo in kana.typos:
                typo_values = [typo.word_id, typo.id, typo.value]
                values_to_write_list.append(typo_values)

            FileHandler.write_seisen_lines(kana_typos_path, values_to_write_list)

            for incorrect_typo in kana.incorrect_typos:
                incorrect_typo_values = [incorrect_typo.word_id, incorrect_typo.id, incorrect_typo.value]
                values_to_write_list.append(incorrect_typo_values)

            FileHandler.write_seisen_lines(kana_incorrect_typos_path, values_to_write_list)
            values_to_write_list.clear()

##--------------------start-of-assemble_vocab()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    
    @staticmethod
    def assemble_vocab() -> None:

        """

        Assembles the vocab objects from the remote storage.

        """

        if(not RemoteHandler.is_remote_enabled()):
            return

        RemoteHandler.vocab.clear()

        vocab_id_list, correct_count_list, incorrect_count_list = ConnectionHandler.read_multi_column_query("select id, correct_count, incorrect_count from vocab")
        typo_vocab_id_list, typo_id_list, typo_list = ConnectionHandler.read_multi_column_query("select vocab_id, typo_id, typo from vocab_typos")
        incorrect_typo_vocab_id_list, incorrect_typo_id_list, incorrect_typo_list = ConnectionHandler.read_multi_column_query("select vocab_id, incorrect_typo_id, incorrect_typo from vocab_incorrect_typos")
        answer_vocab_id_list, answer_id_list, answer_list = ConnectionHandler.read_multi_column_query("select vocab_id, answer_id, answer from vocab_answers")
        testing_material_vocab_id_list, testing_material_id_list, testing_material_list = ConnectionHandler.read_multi_column_query("select vocab_id, testing_material_id, testing_material from vocab_testing_material")
        reading_vocab_id_list, reading_id_list, furigana_list, romaji_list = ConnectionHandler.read_multi_column_query("select vocab_id, reading_id, furigana, romaji from vocab_readings")

        ## construct typos
        vocab_typos = [Typo(int(typo_vocab_id_list[i]), int(typo_id_list[i]), typo_list[i]) for i in range(len(typo_vocab_id_list))]
        vocab_incorrect_typos = [IncorrectTypo(int(incorrect_typo_vocab_id_list[i]), int(incorrect_typo_id_list[i]), incorrect_typo_list[i]) for i in range(len(incorrect_typo_vocab_id_list))]

        ## construct answers, testing_materials, and readings
        vocab_answers = [Answer(int(answer_vocab_id_list[i]), int(answer_id_list[i]), answer_list[i]) for i in range(len(answer_vocab_id_list))]
        vocab_testing_materials = [TestingMaterial(int(testing_material_vocab_id_list[i]), int(testing_material_id_list[i]), testing_material_list[i]) for i in range(len(testing_material_vocab_id_list))]
        vocab_readings = [Reading(int(reading_vocab_id_list[i]), int(reading_id_list[i]), furigana_list[i], romaji_list[i]) for i in range(len(reading_vocab_id_list))]

        ## construct vocab dummy objects
        for i in range(len(vocab_id_list)):
            vocab = Vocab(int(vocab_id_list[i]), [vocab_testing_materials[0]], [vocab_answers[0]], [vocab_readings[0]], int(correct_count_list[i]), int(incorrect_count_list[i])) 
            RemoteHandler.vocab.append(vocab)

        ## fill vocab objects with their respective answers, testing_materials, and readings
        for vocab in RemoteHandler.vocab:

            ## clear out old dummy data
            vocab.testing_material.clear()
            vocab.answers.clear()
            vocab.readings.clear()

            for testing_material in vocab_testing_materials:
                if(testing_material.word_id == vocab.id):

                    is_first_testing_material = True

                    if(is_first_testing_material):  
                        vocab.main_testing_material = testing_material
                        is_first_testing_material = False

                    vocab.testing_material.append(testing_material)
                    Logger.log_action("Added Testing Material " + testing_material.value + " to Vocab " + str(vocab.id))

            for answer in vocab_answers:

                if(answer.word_id == vocab.id):

                    is_first_answer = True

                    if(is_first_answer):
                        vocab.main_answer = answer
                        is_first_answer = False

                    vocab.answers.append(answer)
                    Logger.log_action("Added Synonym " + answer.value + " to Vocab " + vocab.main_testing_material.value)

            for reading in vocab_readings:
                if(reading.word_id == vocab.id):

                    is_first_reading = True

                    if(is_first_reading):
                        vocab.main_reading = reading
                        is_first_reading = False

                    vocab.readings.append(reading)
                    Logger.log_action("Added Reading " + reading.furigana + " to Vocab " + vocab.main_testing_material.value)

        ## fill vocab objects with their respective typos, incorrect typos
        for vocab in RemoteHandler.vocab:
            for typo in vocab_typos:
                if(typo.word_id == vocab.id):
                    vocab.typos.append(typo)
                    Logger.log_action("Added Typo " + typo.value + " to Vocab " + vocab.main_testing_material.value)

            for incorrect_typo in vocab_incorrect_typos:
                if(incorrect_typo.word_id == vocab.id):
                    vocab.incorrect_typos.append(incorrect_typo)
                    Logger.log_action("Added Incorrect Typo " + incorrect_typo.value + " to Vocab " + vocab.main_testing_material.value)

##--------------------start-of-write_vocab_to_disk()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    
    @staticmethod
    def write_vocab_to_disk(vocab_path:str, vocab_testing_material_path:str, vocab_answers_path:str, vocab_readings_path:str, vocab_typos_path:str, vocab_incorrect_typos_path:str, vocab:typing.Union[Vocab, None]=None) -> None:

        """

        Writes the vocab objects to local storage.

        Parameters:
        vocab_path (str) : The path to the vocab file.
        vocab_testing_material_path (str) : The path to the vocab testing material file.
        vocab_answers_path (str) : The path to the vocab answers file.
        vocab_readings_path (str) : The path to the vocab readings file.
        vocab_typos_path (str) : The path to the vocab typos file.
        vocab_incorrect_typos_path (str) : The path to the vocab incorrect typos file.
        vocab (Vocab) : The vocab object to write to disk.

        """

        values_to_write_list = []
        
        if(not RemoteHandler.is_remote_enabled()):
            return
        
        old_remote_vocab:typing.List[Vocab] = []

        if(vocab != None):
            old_remote_vocab = RemoteHandler.vocab
            RemoteHandler.vocab = [vocab]

        ## apply changes to local storage
        for vocab in RemoteHandler.vocab:

            vocab_values = [vocab.id, vocab.correct_count, vocab.incorrect_count]
            FileHandler.write_seisen_line(vocab_path, vocab_values)
            values_to_write_list.clear()

            for testing_material in vocab.testing_material:
                testing_material_values = [testing_material.word_id, testing_material.id, testing_material.value]
                values_to_write_list.append(testing_material_values)

            FileHandler.write_seisen_lines(vocab_testing_material_path, values_to_write_list)
            values_to_write_list.clear()

            for answer in vocab.answers:
                answer_values = [answer.word_id, answer.id, answer.value]
                values_to_write_list.append(answer_values)

            FileHandler.write_seisen_lines(vocab_answers_path, values_to_write_list)
            values_to_write_list.clear()

            for reading in vocab.readings:
                reading_values = [reading.word_id, reading.id, reading.furigana, reading.romaji]
                values_to_write_list.append(reading_values)

            FileHandler.write_seisen_lines(vocab_readings_path, values_to_write_list)
            values_to_write_list.clear()

            for typo in vocab.typos:
                typo_values = [typo.word_id, typo.id, typo.value]
                values_to_write_list.append(typo_values)

            FileHandler.write_seisen_lines(vocab_typos_path, values_to_write_list)
            values_to_write_list.clear()

            for incorrect_typo in vocab.incorrect_typos:
                incorrect_typo_values = [incorrect_typo.word_id, incorrect_typo.id, incorrect_typo.value]
                values_to_write_list.append(incorrect_typo_values)

            FileHandler.write_seisen_lines(vocab_incorrect_typos_path, values_to_write_list)
            values_to_write_list.clear()

        if(vocab != None):
            RemoteHandler.vocab = old_remote_vocab
            RemoteHandler.vocab.append(vocab)

##--------------------start-of-reset_local_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def reset_local_storage() -> None:

        """
        
        Loads the words from remote storage into local storage.
        Note that this will reset all the words locally stored on the current device.
        Use carefully!

        """

        ##----------------------------------------------------------------clear_local_kana()----------------------------------------------------------------

        def clear_local_kana() -> None:

            FileHandler.clear_file(FileEnsurer.kana_path)
            FileHandler.clear_file(FileEnsurer.kana_answers_path)
            FileHandler.clear_file(FileEnsurer.kana_typos_path)
            FileHandler.clear_file(FileEnsurer.kana_incorrect_typos_path)
            FileHandler.clear_file(FileEnsurer.kana_readings_path)
            FileHandler.clear_file(FileEnsurer.kana_testing_material_path)

        ##----------------------------------------------------------------clear_local_vocab()----------------------------------------------------------------

        def clear_local_vocab() -> None:

            FileHandler.clear_file(FileEnsurer.vocab_path)
            FileHandler.clear_file(FileEnsurer.vocab_answers_path)
            FileHandler.clear_file(FileEnsurer.vocab_typos_path)
            FileHandler.clear_file(FileEnsurer.vocab_incorrect_typos_path)
            FileHandler.clear_file(FileEnsurer.vocab_readings_path)
            FileHandler.clear_file(FileEnsurer.vocab_testing_material_path)

        ##----------------------------------------------------------------reset_kana_relations()----------------------------------------------------------------

        def reset_kana_relations() -> None:
            
            RemoteHandler.assemble_kana()

            RemoteHandler.write_kana_to_disk(FileEnsurer.kana_path, 
                                            FileEnsurer.kana_testing_material_path,
                                            FileEnsurer.kana_answers_path,
                                            FileEnsurer.kana_readings_path,
                                            FileEnsurer.kana_typos_path,
                                            FileEnsurer.kana_incorrect_typos_path)

        ##----------------------------------------------------------------reset_vocab_relations()----------------------------------------------------------------
                
        def reset_vocab_relations() -> None:

            RemoteHandler.assemble_vocab()

            RemoteHandler.write_vocab_to_disk(FileEnsurer.vocab_path, 
                                            FileEnsurer.vocab_testing_material_path,
                                            FileEnsurer.vocab_answers_path,
                                            FileEnsurer.vocab_readings_path,
                                            FileEnsurer.vocab_typos_path,
                                            FileEnsurer.vocab_incorrect_typos_path)

        ##----------------------------------------------------------------main()----------------------------------------------------------------

        if(not RemoteHandler.is_remote_enabled()):
            return

        ## local storage does not reset if there is no valid database connection
        if(ConnectionHandler.check_connection_validity("local storage reset") == False):
            return
        
        Logger.log_barrier()
        Logger.log_action("Clearing Local Storage...")

        clear_local_kana()
        clear_local_vocab()

        Logger.log_barrier()
        Logger.log_action("Resetting Kana Relations...")

        reset_kana_relations()

        Logger.log_barrier()
        Logger.log_action("Resetting Vocab Relations...")

        reset_vocab_relations()
      
##--------------------start-of-reset_remote_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def reset_remote_storage(omit_print:bool=False) -> None:

        """
        
        Resets the remote storage with the local storage.
        Note that this will reset all the words remotely stored on the connected database.
        Use Carefully!

        """

        if(not RemoteHandler.is_remote_enabled()):
            if(not omit_print):
                print("Remote storage is not enabled. Please install mysql-connector-python, restart Seisen and set up a database to use this feature.\n")

            return

        ## we do not reset remote if there is no valid database connection
        if(ConnectionHandler.check_connection_validity("remote storage reset") == False):
            print("No valid database connection skipping remote portion.\n")
            time.sleep(Toolkit.long_sleep_constant)
            return
        
        with open(FileEnsurer.last_local_remote_overwrite_timestamp_path, 'w+', encoding="utf-8") as file:

            last_overwrite_date_accurate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            file.write(last_overwrite_date_accurate)

        Logger.log_barrier()
        Logger.log_action("Resetting Remote Storage...")

        RemoteHandler.delete_remote_storage()
        RemoteHandler.create_remote_storage()
        RemoteHandler.fill_remote_storage()

        Logger.log_action("Remote Storage Reset.")

        if(not omit_print):
            print("Remote Storage Reset.\n")

##--------------------start-of-delete_remote_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def delete_remote_storage() -> None:

        """
        
        Deletes the remote storage by dropping all the tables.

        """

        ##----------------------------------------------------------------kana----------------------------------------------------------------

        delete_kana_readings_query = """
        drop table if exists kana_readings;
        """

        delete_kana_testing_material_query = """
        drop table if exists kana_testing_material;
        """

        delete_kana_answers_query = """
        drop table if exists kana_answers;
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

        delete_vocab_readings_query = """
        drop table if exists vocab_readings;
        """

        delete_vocab_testing_material_query = """
        drop table if exists vocab_testing_material;
        """

        delete_vocab_answers_query = """
        drop table if exists vocab_answers;
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

        if(not RemoteHandler.is_remote_enabled()):
            return

        ConnectionHandler.execute_query(delete_kana_readings_query)
        ConnectionHandler.execute_query(delete_kana_testing_material_query)
        ConnectionHandler.execute_query(delete_kana_answers_query)
        ConnectionHandler.execute_query(delete_kana_typos_query)
        ConnectionHandler.execute_query(delete_kana_incorrect_typos_query)
        ConnectionHandler.execute_query(delete_kana_query)

        ConnectionHandler.execute_query(delete_vocab_readings_query)
        ConnectionHandler.execute_query(delete_vocab_testing_material_query)
        ConnectionHandler.execute_query(delete_vocab_answers_query)
        ConnectionHandler.execute_query(delete_vocab_typos_query)
        ConnectionHandler.execute_query(delete_vocab_incorrect_typos_query)
        ConnectionHandler.execute_query(delete_vocab_query)

##--------------------start-of-create_remote_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def create_remote_storage() -> None:

        """
        
        Creates the tables for remote storage.

        """

        ##----------------------------------------------------------------kana----------------------------------------------------------------

        create_kana_query = """
        CREATE TABLE kana (
            id INT NOT NULL,
            correct_count INT NOT NULL,
            incorrect_count INT NOT NULL,
            PRIMARY KEY (id)
        );
        """

        create_kana_typos_query = """
        CREATE TABLE kana_typos (
            kana_id INT NOT NULL,
            typo_id INT NOT NULL,
            typo VARCHAR(1024) NOT NULL,
            PRIMARY KEY (typo_id),
            FOREIGN KEY (kana_id) REFERENCES kana(id)
        );
        """

        create_kana_incorrect_typos_query = """
        CREATE TABLE kana_incorrect_typos (
            kana_id INT NOT NULL,
            incorrect_typo_id INT NOT NULL,
            incorrect_typo VARCHAR(1024) NOT NULL,
            PRIMARY KEY (incorrect_typo_id),
            FOREIGN KEY (kana_id) REFERENCES kana(id)
        );
        """

        create_kana_answers_query = """
        CREATE TABLE kana_answers (
            kana_id INT NOT NULL,
            answer_id INT NOT NULL,
            answer VARCHAR(1024) NOT NULL,
            PRIMARY KEY (answer_id),
            FOREIGN KEY (kana_id) REFERENCES kana(id)
        );
        """

        create_kana_testing_material_query = """
        CREATE TABLE kana_testing_material (
            kana_id INT NOT NULL,
            testing_material_id INT NOT NULL,
            testing_material VARCHAR(1024) NOT NULL,
            PRIMARY KEY (testing_material_id),
            FOREIGN KEY (kana_id) REFERENCES kana(id)
        );
        """

        create_kana_readings_query = """
        CREATE TABLE kana_readings (
            kana_id INT NOT NULL,
            reading_id INT NOT NULL,
            furigana VARCHAR(1024) NOT NULL,
            romaji VARCHAR(1024) NOT NULL,
            PRIMARY KEY (reading_id),
            FOREIGN KEY (kana_id) REFERENCES kana(id)
        );
        """

        ##----------------------------------------------------------------vocab----------------------------------------------------------------

        create_vocab_query = """
        CREATE TABLE vocab (
            id INT NOT NULL,
            correct_count INT NOT NULL,
            incorrect_count INT NOT NULL,
            PRIMARY KEY (id)
        );

        """        
        create_vocab_typos_query = """
        CREATE TABLE vocab_typos (
            vocab_id INT NOT NULL,
            typo_id INT NOT NULL,
            typo VARCHAR(1024) NOT NULL,
            PRIMARY KEY (typo_id),
            FOREIGN KEY (vocab_id) REFERENCES vocab(id)
        );
        """

        create_vocab_incorrect_typos_query = """
        CREATE TABLE vocab_incorrect_typos (
            vocab_id INT NOT NULL,
            incorrect_typo_id INT NOT NULL,
            incorrect_typo VARCHAR(1024) NOT NULL,
            PRIMARY KEY (incorrect_typo_id),
            FOREIGN KEY (vocab_id) REFERENCES vocab(id)
        );
        """

        create_vocab_answer_query = """
        CREATE TABLE vocab_answers (
            vocab_id INT NOT NULL,
            answer_id INT NOT NULL,
            answer VARCHAR(1024) NOT NULL,
            PRIMARY KEY (answer_id),
            FOREIGN KEY (vocab_id) REFERENCES vocab(id)
        );
        """

        create_vocab_testing_material_query = """
        CREATE TABLE vocab_testing_material (
            vocab_id INT NOT NULL,
            testing_material_id INT NOT NULL,
            testing_material VARCHAR(1024) NOT NULL,
            PRIMARY KEY (testing_material_id),
            FOREIGN KEY (vocab_id) REFERENCES vocab(id)
        );
        """

        create_vocab_readings_query = """
        CREATE TABLE vocab_readings (
            vocab_id INT NOT NULL,
            reading_id INT NOT NULL,
            furigana VARCHAR(1024) NOT NULL,
            romaji VARCHAR(1024) NOT NULL,
            PRIMARY KEY (reading_id),
            FOREIGN KEY (vocab_id) REFERENCES vocab(id)
        );
        """

        ##----------------------------------------------------------------queries----------------------------------------------------------------

        if(not RemoteHandler.is_remote_enabled()):
            return

        ConnectionHandler.execute_query(create_kana_query)
        ConnectionHandler.execute_query(create_kana_typos_query)
        ConnectionHandler.execute_query(create_kana_incorrect_typos_query)
        ConnectionHandler.execute_query(create_kana_answers_query)
        ConnectionHandler.execute_query(create_kana_testing_material_query)
        ConnectionHandler.execute_query(create_kana_readings_query)

        ConnectionHandler.execute_query(create_vocab_query)
        ConnectionHandler.execute_query(create_vocab_typos_query)
        ConnectionHandler.execute_query(create_vocab_incorrect_typos_query)
        ConnectionHandler.execute_query(create_vocab_answer_query)
        ConnectionHandler.execute_query(create_vocab_testing_material_query)
        ConnectionHandler.execute_query(create_vocab_readings_query)

##--------------------start-of-fill_remote_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def fill_remote_storage()-> None:

        """
        
        Fills the tables in remote storage with the local data.

        """

        def fill_table(file_path, table_name, keys):
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    values = FileHandler.extract_seisen_line_values(line)
                    insert_dict = dict(zip(keys, values))
                    ConnectionHandler.insert_into_table(table_name, insert_dict)

        if(not RemoteHandler.is_remote_enabled()):
            return

        fill_table(FileEnsurer.kana_path, "kana", ["id", "correct_count", "incorrect_count"])
        fill_table(FileEnsurer.kana_typos_path, "kana_typos", ["kana_id", "typo_id", "typo"])
        fill_table(FileEnsurer.kana_incorrect_typos_path, "kana_incorrect_typos", ["kana_id", "incorrect_typo_id", "incorrect_typo"])
        fill_table(FileEnsurer.kana_answers_path, "kana_answers", ["kana_id", "answer_id", "answer"])
        fill_table(FileEnsurer.kana_testing_material_path, "kana_testing_material", ["kana_id", "testing_material_id", "testing_material"])
        fill_table(FileEnsurer.kana_readings_path, "kana_readings", ["kana_id", "reading_id", "furigana", "romaji"])

        fill_table(FileEnsurer.vocab_path, "vocab", ["id", "correct_count", "incorrect_count"])
        fill_table(FileEnsurer.vocab_typos_path, "vocab_typos", ["vocab_id", "typo_id", "typo"])
        fill_table(FileEnsurer.vocab_incorrect_typos_path, "vocab_incorrect_typos", ["vocab_id", "incorrect_typo_id", "incorrect_typo"])
        fill_table(FileEnsurer.vocab_answers_path, "vocab_answers", ["vocab_id", "answer_id", "answer"])
        fill_table(FileEnsurer.vocab_testing_material_path, "vocab_testing_material", ["vocab_id", "testing_material_id", "testing_material"])
        fill_table(FileEnsurer.vocab_readings_path, "vocab_readings", ["vocab_id", "reading_id", "furigana", "romaji"])

##--------------------start-of-create_daily_remote_backup()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def create_daily_remote_backup() -> None:

        """
        
        Creates Seisen's daily remote backup.

        """

        def backup_data(data_type, assemble_func, write_func):
            remote_archive_data_dir = os.path.join(archive_dir, data_type)

            remote_archive_data_paths = {
                f"{data_type}.seisen": os.path.join(remote_archive_data_dir, f"{data_type}.seisen"),
                f"{data_type}_typos.seisen": os.path.join(remote_archive_data_dir, f"{data_type}_typos.seisen"),
                f"{data_type}_incorrect_typos.seisen": os.path.join(remote_archive_data_dir, f"{data_type}_incorrect_typos.seisen"),
                f"{data_type}_answers.seisen": os.path.join(remote_archive_data_dir, f"{data_type}_answers.seisen"),
                f"{data_type}_readings.seisen": os.path.join(remote_archive_data_dir, f"{data_type}_readings.seisen"),
                f"{data_type}_testing_material.seisen": os.path.join(remote_archive_data_dir, f"{data_type}_testing_material.seisen"),
            }

            FileHandler.standard_create_directory(remote_archive_data_dir)

            assemble_func()

            write_func(*remote_archive_data_paths.values())

        if(not RemoteHandler.is_remote_enabled()):
            return

        if(ConnectionHandler.check_connection_validity("remote storage backup creation") == False):
            return

        with open(FileEnsurer.last_remote_backup_path, 'r+', encoding="utf-8") as file:
            strips_to_perform = " \n\x00"
            last_backup_date = file.read().strip(strips_to_perform)
            current_day = str(datetime.today().strftime('%Y-%m-%d'))

        if(last_backup_date != current_day):
            archive_dir = FileEnsurer.create_archive_dir(1) 

            Logger.log_action("Created Daily Remote Backup.")

            FileHandler.standard_delete_file(FileEnsurer.last_remote_backup_path)
            FileHandler.modified_create_file(FileEnsurer.last_remote_backup_path, current_day)

            backup_data("kana", RemoteHandler.assemble_kana, RemoteHandler.write_kana_to_disk)
            backup_data("vocab", RemoteHandler.assemble_vocab, RemoteHandler.write_vocab_to_disk)

##--------------------start-of-restore_remote_backup()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def restore_remote_backup() -> None:

        """
        
        Prompts a user to restore a remote backup and does so if valid.

        """

        if(not RemoteHandler.is_remote_enabled()):
            return

        ## we do not fuck w/ remote if there is no valid database connection
        if(ConnectionHandler.check_connection_validity("restore remote storage backup") == False):
            print("No valid database connection skipping remote portion.\n")
            time.sleep(Toolkit.long_sleep_constant)
            return

        valid_backups = []

        backup_to_restore_prompt = ""
        
        Toolkit.clear_console()
        
        print("Please select a backup to restore:\n")
        
        for item in os.listdir(FileEnsurer.remote_archives_dir):
        
            full_path = os.path.join(FileEnsurer.remote_archives_dir, item)
        
            if(os.path.isdir(full_path)):
                print(item)
                valid_backups.append(item)
                backup_to_restore_prompt += item + "\n"
        
        backup_to_restore_prompt += "\nPlease select a backup to restore, please keep in mind that this process is not easily reversible. (This resets local with a remote backup)"

        if(len(valid_backups) == 0):
            print("No backups found.")
            time.sleep(1)
            return

        try: ## user confirm will throw an UserCancelError if the user cancels

            backup_to_restore = Toolkit.user_confirm(backup_to_restore_prompt)

            if(backup_to_restore in valid_backups):
                Toolkit.clear_console()

                shutil.rmtree(FileEnsurer.kana_dir)
                shutil.rmtree(FileEnsurer.vocab_dir)

                shutil.copytree(os.path.join(FileEnsurer.remote_archives_dir, backup_to_restore), FileEnsurer.config_dir, dirs_exist_ok=True)

                Logger.log_action("Restored the " + backup_to_restore + " remote backup.", omit_timestamp=True, output=True)

                print("\nNote that if you wish to see changes in remote, you need to reset remote with local.\n")

            else:
                print("Invalid Backup.\n")

        except Toolkit.UserCancelError:
            print("Canceled.\n")

##--------------------start-of-local_remote_overwrite()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def local_remote_overwrite() -> None:
        
        """

        Overwrites the remote storage with the local storage.

        """

        if(not RemoteHandler.is_remote_enabled()):
            return

        ## we do not overwrite remote with local if there is no valid database connection
        if(ConnectionHandler.check_connection_validity("local-remote overwrite") == False):
            return
        
        with open(FileEnsurer.last_local_remote_backup_path, 'r+', encoding="utf-8") as file:

            strips_to_perform = " \n\x00"

            last_backup_date = file.read()

            last_backup_date = last_backup_date.strip(strips_to_perform)
        
            current_day = str(datetime.today().strftime('%Y-%m-%d'))

        if(last_backup_date != current_day):

            Logger.log_action("Overwriting Remote with Local.")
    
            FileHandler.standard_delete_file(FileEnsurer.last_local_remote_backup_path)

            FileHandler.modified_create_file(FileEnsurer.last_local_remote_backup_path, current_day)

            RemoteHandler.reset_remote_storage(omit_print=True)