## built-in modules
from datetime import datetime

import os
import shutil
import time
import typing

## custom modules
from entities.typo import Typo as typo_blueprint
from entities.incorrect_typo import IncorrectTypo as incorrect_typo_blueprint

from entities.synonym import Synonym as synonym_blueprint
from entities.word import Word as kana_blueprint
from entities.vocab import Vocab as vocab_blueprint
from entities.reading import Reading as reading_blueprint
from entities.testing_material import TestingMaterial as testing_material_blueprint
from entities.word import Word as Kana
from entities.vocab import Vocab

from modules.file_ensurer import FileEnsurer
from modules.toolkit import Toolkit
from modules.logger import Logger

from handlers.connection_handler import ConnectionHandler
from handlers.file_handler import FileHandler

class RemoteHandler():

    """
    
    The handler that handles all interactions with the remote storage (database).

    """

    kana:typing.List[Kana] = [] 

    vocab:typing.List[Vocab] = []

##--------------------start-of-assemble_kana()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def assemble_kana() -> None:

        """

        Assembles the kana objects from the remote storage.

        """

        RemoteHandler.kana.clear()

        kana_id_list, incorrect_count_list, correct_count_list = ConnectionHandler.read_multi_column_query("select id, incorrect_count, correct_count from kana")
        typo_kana_id_list, typo_id_list, typo_list = ConnectionHandler.read_multi_column_query("select kana_id, typo_id, typo from kana_typos")
        incorrect_typo_kana_id_list, incorrect_typo_id_list, incorrect_typo_list = ConnectionHandler.read_multi_column_query("select kana_id, incorrect_typo_id, incorrect_typo from kana_incorrect_typos") 
        synonym_kana_id_list, synonym_id_list, synonym_list = ConnectionHandler.read_multi_column_query("select kana_id, synonym_id, synonym from kana_synonyms")
        testing_material_kana_id_list, testing_material_id_list, testing_material_list = ConnectionHandler.read_multi_column_query("select kana_id, testing_material_id, testing_material from kana_testing_material")
        reading_kana_id_list, reading_id_list, furigana_list, romaji_list = ConnectionHandler.read_multi_column_query("select kana_id, reading_id, furigana, romaji from kana_readings")

        ## construct typos
        kana_typos = [typo_blueprint(int(typo_kana_id_list[i]), int(typo_id_list[i]), typo_list[i]) for i in range(len(typo_kana_id_list))]
        kana_incorrect_typos = [incorrect_typo_blueprint(int(incorrect_typo_kana_id_list[i]), int(incorrect_typo_id_list[i]), incorrect_typo_list[i]) for i in range(len(incorrect_typo_kana_id_list))]

        ## construct synonyms, testing_materials, and readings
        kana_synonyms = [synonym_blueprint(int(synonym_kana_id_list[i]), int(synonym_id_list[i]), synonym_list[i]) for i in range(len(synonym_kana_id_list))]
        kana_testing_materials = [testing_material_blueprint(int(testing_material_kana_id_list[i]), int(testing_material_id_list[i]), testing_material_list[i]) for i in range(len(testing_material_kana_id_list))]
        kana_readings = [reading_blueprint(int(reading_kana_id_list[i]), int(reading_id_list[i]), furigana_list[i], romaji_list[i]) for i in range(len(reading_kana_id_list))]

        ## construct kana dummy objects
        for i in range(len(kana_id_list)):
            kana = kana_blueprint(int(kana_id_list[i]), [kana_testing_materials[0]], kana_synonyms[0], [kana_synonyms[0]], [kana_readings[0]], int(incorrect_count_list[i]), int(correct_count_list[i])) 
            RemoteHandler.kana.append(kana)

        ## fill kana objects with their respective synonyms, testing_materials, and readings
        for kana in RemoteHandler.kana:

            is_first_synonym:bool = True

            ## clear out old dummy data
            kana.testing_material_all.clear()
            kana.testing_material_answer_all.clear()
            kana.readings.clear()

            for synonym in kana_synonyms:
                if(synonym.word_id == kana.word_id):

                    if(is_first_synonym):
                        kana.testing_material_answer_main = synonym
                        is_first_synonym = False
                    
                    kana.testing_material_answer_all.append(synonym)
                    Logger.log_action("Added Synonym " + synonym.synonym_value + " to Kana " + kana.testing_material_answer_main.synonym_value)

            for testing_material in kana_testing_materials:
                if(testing_material.word_id == kana.word_id):
                    kana.testing_material_all.append(testing_material)
                    Logger.log_action("Added Testing Material " + testing_material.testing_material_value+ " to Kana " + str(kana.word_id))

            for reading in kana_readings:
                if(reading.word_id == kana.word_id):
                    kana.readings.append(reading)
                    Logger.log_action("Added Reading " + reading.furigana_value+ " to Kana " + kana.testing_material_answer_main.synonym_value)

        ## fill kana objects with their respective typos, incorrect typos
        for kana in RemoteHandler.kana:
            for typo in kana_typos:
                if(typo.word_id == kana.word_id):
                    kana.typos.append(typo)
                    Logger.log_action("Added Typo " + typo.typo_value + " to Kana " + kana.testing_material_answer_main.synonym_value)

            for incorrect_typo in kana_incorrect_typos:
                if(incorrect_typo.word_id == kana.word_id):
                    kana.incorrect_typos.append(incorrect_typo)
                    Logger.log_action("Added Incorrect Typo " + incorrect_typo.incorrect_typo_value + " to Kana " + kana.testing_material_answer_main.synonym_value)

##--------------------start-of-write_kana_to_disk()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def write_kana_to_disk(kana_path:str, kana_testing_material_path:str, kana_synonyms_path:str, kana_readings_path:str, kana_typos_path:str, kana_incorrect_typos_path:str) -> None:

        ## apply changes to local storage
        for kana in RemoteHandler.kana:

            kana_values = [kana.word_id, kana.incorrect_count, kana.correct_count]
            
            for testing_material in kana.testing_material_all:
                testing_material_values = [testing_material.word_id, testing_material.testing_material_id, testing_material.testing_material_value]
                FileHandler.write_seisen_line(kana_testing_material_path, testing_material_values)

            for synonym in kana.testing_material_answer_all:
                synonym_values = [synonym.word_id, synonym.synonym_id, synonym.synonym_value]
                FileHandler.write_seisen_line(kana_synonyms_path, synonym_values)

            for reading in kana.readings:
                reading_values = [reading.word_id, reading.reading_id, reading.furigana_value, reading.romaji_value]
                FileHandler.write_seisen_line(kana_readings_path, reading_values)

            for typo in kana.typos:
                typo_values = [typo.word_id, typo.typo_id, typo.typo_value]
                FileHandler.write_seisen_line(kana_typos_path, typo_values)

            for incorrect_typo in kana.incorrect_typos:
                incorrect_typo_values = [incorrect_typo.word_id, incorrect_typo.incorrect_typo_id, incorrect_typo.incorrect_typo_value]
                FileHandler.write_seisen_line(kana_incorrect_typos_path, incorrect_typo_values)

            FileHandler.write_seisen_line(kana_path, kana_values)

##--------------------start-of-assemble_vocab()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    
    @staticmethod
    def assemble_vocab() -> None:

        """

        Assembles the vocab objects from the remote storage.

        """

        RemoteHandler.vocab.clear()

        vocab_id_list, incorrect_count_list, correct_count_list = ConnectionHandler.read_multi_column_query("select id, incorrect_count, correct_count from vocab")
        typo_vocab_id_list, typo_id_list, typo_list = ConnectionHandler.read_multi_column_query("select vocab_id, typo_id, typo from vocab_typos")
        incorrect_typo_vocab_id_list, incorrect_typo_id_list, incorrect_typo_list = ConnectionHandler.read_multi_column_query("select vocab_id, incorrect_typo_id, incorrect_typo from vocab_incorrect_typos")
        synonym_vocab_id_list, synonym_id_list, synonym_list = ConnectionHandler.read_multi_column_query("select vocab_id, synonym_id, synonym from vocab_synonyms")
        testing_material_vocab_id_list, testing_material_id_list, testing_material_list = ConnectionHandler.read_multi_column_query("select vocab_id, testing_material_id, testing_material from vocab_testing_material")
        reading_vocab_id_list, reading_id_list, furigana_list, romaji_list = ConnectionHandler.read_multi_column_query("select vocab_id, reading_id, furigana, romaji from vocab_readings")

        ## construct typos
        vocab_typos = [typo_blueprint(int(typo_vocab_id_list[i]), int(typo_id_list[i]), typo_list[i]) for i in range(len(typo_vocab_id_list))]
        vocab_incorrect_typos = [incorrect_typo_blueprint(int(incorrect_typo_vocab_id_list[i]), int(incorrect_typo_id_list[i]), incorrect_typo_list[i]) for i in range(len(incorrect_typo_vocab_id_list))]

        ## construct synonyms, testing_materials, and readings
        vocab_synonyms = [synonym_blueprint(int(synonym_vocab_id_list[i]), int(synonym_id_list[i]), synonym_list[i]) for i in range(len(synonym_vocab_id_list))]
        vocab_testing_materials = [testing_material_blueprint(int(testing_material_vocab_id_list[i]), int(testing_material_id_list[i]), testing_material_list[i]) for i in range(len(testing_material_vocab_id_list))]
        vocab_readings = [reading_blueprint(int(reading_vocab_id_list[i]), int(reading_id_list[i]), furigana_list[i], romaji_list[i]) for i in range(len(reading_vocab_id_list))]

        ## construct vocab dummy objects
        for i in range(len(vocab_id_list)):
            vocab = vocab_blueprint(int(vocab_id_list[i]), [vocab_testing_materials[0]], vocab_synonyms[0], [vocab_synonyms[0]], [vocab_readings[0]], int(incorrect_count_list[i]), int(correct_count_list[i])) 
            RemoteHandler.vocab.append(vocab)

        ## fill vocab objects with their respective synonyms, testing_materials, and readings
        for vocab in RemoteHandler.vocab:

            is_first_synonym:bool = True

            for synonym in vocab_synonyms:

                ## clear out old dummy data
                vocab.testing_material_all.clear()
                vocab.testing_material_answer_all.clear()
                vocab.readings.clear()

                if(synonym.word_id == vocab.word_id):

                    if(is_first_synonym):
                        vocab.testing_material_answer_main = synonym
                        is_first_synonym = False
                    
                    vocab.testing_material_answer_all.append(synonym)
                    Logger.log_action("Added Synonym " + synonym.synonym_value + " to Vocab " + vocab.testing_material_answer_main.synonym_value)

            for testing_material in vocab_testing_materials:
                if(testing_material.word_id == vocab.word_id):
                    vocab.testing_material_all.append(testing_material)
                    Logger.log_action("Added Testing Material " + testing_material.testing_material_value+ " to Vocab " + str(vocab.word_id))

            for reading in vocab_readings:
                if(reading.word_id == vocab.word_id):
                    vocab.readings.append(reading)
                    Logger.log_action("Added Reading " + reading.furigana_value+ " to Vocab " + vocab.testing_material_answer_main.synonym_value)

        ## fill vocab objects with their respective typos, incorrect typos
        for vocab in RemoteHandler.vocab:
            for typo in vocab_typos:
                if(typo.word_id == vocab.word_id):
                    vocab.typos.append(typo)
                    Logger.log_action("Added Typo " + typo.typo_value + " to Vocab " + vocab.testing_material_answer_main.synonym_value)

            for incorrect_typo in vocab_incorrect_typos:
                if(incorrect_typo.word_id == vocab.word_id):
                    vocab.incorrect_typos.append(incorrect_typo)
                    Logger.log_action("Added Incorrect Typo " + incorrect_typo.incorrect_typo_value + " to Vocab " + vocab.testing_material_answer_main.synonym_value)

##--------------------start-of-write_vocab_to_disk()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    
    @staticmethod
    def write_vocab_to_disk(vocab_path:str, vocab_testing_material_path:str, vocab_synonyms_path:str, vocab_readings_path:str, vocab_typos_path:str, vocab_incorrect_typos_path:str, vocab:typing.Union[Vocab, None]=None) -> None:

        if(vocab != None):
            old_remote_vocab = RemoteHandler.vocab
            RemoteHandler.vocab = [vocab]

        ## apply changes to local storage
        for vocab in RemoteHandler.vocab:

            vocab_values = [vocab.word_id, vocab.incorrect_count, vocab.correct_count]
            
            for testing_material in vocab.testing_material_all:
                testing_material_values = [testing_material.word_id, testing_material.testing_material_id, testing_material.testing_material_value]
                FileHandler.write_seisen_line(vocab_testing_material_path, testing_material_values)

            for synonym in vocab.testing_material_answer_all:
                synonym_values = [synonym.word_id, synonym.synonym_id, synonym.synonym_value]
                FileHandler.write_seisen_line(vocab_synonyms_path, synonym_values)

            for reading in vocab.readings:
                reading_values = [reading.word_id, reading.reading_id, reading.furigana_value, reading.romaji_value]
                FileHandler.write_seisen_line(vocab_readings_path, reading_values)

            for typo in vocab.typos:
                typo_values = [typo.word_id, typo.typo_id, typo.typo_value]
                FileHandler.write_seisen_line(vocab_typos_path, typo_values)

            for incorrect_typo in vocab.incorrect_typos:
                incorrect_typo_values = [incorrect_typo.word_id, incorrect_typo.incorrect_typo_id, incorrect_typo.incorrect_typo_value]
                FileHandler.write_seisen_line(vocab_incorrect_typos_path, incorrect_typo_values)

            FileHandler.write_seisen_line(vocab_path, vocab_values)

        if(vocab != None):
            RemoteHandler.vocab = old_remote_vocab ## type: ignore
            RemoteHandler.vocab.append(vocab)

##--------------------start-of-reset_local_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def reset_local_storage() -> None:

        """
        
        Loads the words from remote storage into local storage.
        Note that this will reset all the words locally stored on this device.
        Use carefully!

        """

        ##----------------------------------------------------------------clear_local_kana()----------------------------------------------------------------

        def clear_local_kana() -> None:

            FileHandler.clear_file(FileEnsurer.kana_path)
            FileHandler.clear_file(FileEnsurer.kana_synonyms_path)
            FileHandler.clear_file(FileEnsurer.kana_typos_path)
            FileHandler.clear_file(FileEnsurer.kana_incorrect_typos_path)
            FileHandler.clear_file(FileEnsurer.kana_readings_path)
            FileHandler.clear_file(FileEnsurer.kana_testing_material_path)

        ##----------------------------------------------------------------clear_local_vocab()----------------------------------------------------------------

        def clear_local_vocab() -> None:

            FileHandler.clear_file(FileEnsurer.vocab_path)
            FileHandler.clear_file(FileEnsurer.vocab_synonyms_path)
            FileHandler.clear_file(FileEnsurer.vocab_typos_path)
            FileHandler.clear_file(FileEnsurer.vocab_incorrect_typos_path)
            FileHandler.clear_file(FileEnsurer.vocab_readings_path)
            FileHandler.clear_file(FileEnsurer.vocab_testing_material_path)

        ##----------------------------------------------------------------reset_kana_relations()----------------------------------------------------------------

        def reset_kana_relations() -> None:
            
            RemoteHandler.assemble_kana()

            RemoteHandler.write_kana_to_disk(FileEnsurer.kana_path, 
                                            FileEnsurer.kana_testing_material_path,
                                            FileEnsurer.kana_synonyms_path,
                                            FileEnsurer.kana_readings_path,
                                            FileEnsurer.kana_typos_path,
                                            FileEnsurer.kana_incorrect_typos_path)

        ##----------------------------------------------------------------reset_vocab_relations()----------------------------------------------------------------
                
        def reset_vocab_relations() -> None:

            RemoteHandler.assemble_vocab()

            RemoteHandler.write_vocab_to_disk(FileEnsurer.vocab_path, 
                                            FileEnsurer.vocab_testing_material_path,
                                            FileEnsurer.vocab_synonyms_path,
                                            FileEnsurer.vocab_readings_path,
                                            FileEnsurer.vocab_typos_path,
                                            FileEnsurer.vocab_incorrect_typos_path)

        ##----------------------------------------------------------------main()----------------------------------------------------------------

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

        ## we do not reset remote if there is no valid database connection
        if(ConnectionHandler.check_connection_validity("remote storage reset") == False):
            print("No valid database connection skipping remote portion.\n")
            time.sleep(1)
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
        
        Deletes the remote storage. By dropping all the tables.

        """

        ##----------------------------------------------------------------kana----------------------------------------------------------------

        delete_kana_readings_query = """
        drop table if exists kana_readings;
        """

        delete_kana_testing_material_query = """
        drop table if exists kana_testing_material;
        """

        delete_kana_synonyms_query = """
        drop table if exists kana_synonyms;
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

        delete_vocab_synonyms_query = """
        drop table if exists vocab_synonyms;
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

        ConnectionHandler.execute_query(delete_kana_readings_query)
        ConnectionHandler.execute_query(delete_kana_testing_material_query)
        ConnectionHandler.execute_query(delete_kana_synonyms_query)
        ConnectionHandler.execute_query(delete_kana_typos_query)
        ConnectionHandler.execute_query(delete_kana_incorrect_typos_query)
        ConnectionHandler.execute_query(delete_kana_query)

        ConnectionHandler.execute_query(delete_vocab_readings_query)
        ConnectionHandler.execute_query(delete_vocab_testing_material_query)
        ConnectionHandler.execute_query(delete_vocab_synonyms_query)
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
            incorrect_count INT NOT NULL,
            correct_count INT NOT NULL,
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

        create_kana_synonyms_query = """
        CREATE TABLE kana_synonyms (
            kana_id INT NOT NULL,
            synonym_id INT NOT NULL,
            synonym VARCHAR(1024) NOT NULL,
            PRIMARY KEY (synonym_id),
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
            incorrect_count INT NOT NULL,
            correct_count INT NOT NULL,
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

        create_vocab_synonym_query = """
        CREATE TABLE vocab_synonyms (
            vocab_id INT NOT NULL,
            synonym_id INT NOT NULL,
            synonym VARCHAR(1024) NOT NULL,
            PRIMARY KEY (synonym_id),
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

        ConnectionHandler.execute_query(create_kana_query)
        ConnectionHandler.execute_query(create_kana_typos_query)
        ConnectionHandler.execute_query(create_kana_incorrect_typos_query)
        ConnectionHandler.execute_query(create_kana_synonyms_query)
        ConnectionHandler.execute_query(create_kana_testing_material_query)
        ConnectionHandler.execute_query(create_kana_readings_query)

        ConnectionHandler.execute_query(create_vocab_query)
        ConnectionHandler.execute_query(create_vocab_typos_query)
        ConnectionHandler.execute_query(create_vocab_incorrect_typos_query)
        ConnectionHandler.execute_query(create_vocab_synonym_query)
        ConnectionHandler.execute_query(create_vocab_testing_material_query)
        ConnectionHandler.execute_query(create_vocab_readings_query)

##--------------------start-of-fill_remote_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def fill_remote_storage()-> None:

        """
        
        Fills the tables in remote storage with the local data.

        """


        ##----------------------------------------------------------------kana----------------------------------------------------------------

        def fill_kana() -> None:

            with open(FileEnsurer.kana_path, "r", encoding="utf-8") as file:

                for line in file:

                    id, correct_count, incorrect_count = FileHandler.extract_seisen_line_values(line)

                    table_name = "kana"
                    insert_dict = {
                    "id": id,
                    "correct_count": correct_count,
                    "incorrect_count": incorrect_count
                    }

                    ConnectionHandler.insert_into_table(table_name, insert_dict)

        def fill_kana_typos() -> None:

            with open(FileEnsurer.kana_typos_path, "r", encoding="utf-8") as file:

                for line in file:

                    kana_id, typo_id, typo = FileHandler.extract_seisen_line_values(line)

                    table_name = "kana_typos"
                    insert_dict = {
                        "kana_id": kana_id,
                        "typo_id": typo_id,
                        "typo": typo,
                    }

                    ConnectionHandler.insert_into_table(table_name, insert_dict)
        
        def fill_kana_incorrect_typos() -> None:

            with open(FileEnsurer.kana_incorrect_typos_path, "r", encoding="utf-8") as file:

                for line in file:

                    kana_id, incorrect_typo_id, incorrect_typo = FileHandler.extract_seisen_line_values(line)

                    table_name = "kana_incorrect_typos"
                    insert_dict = {
                    "kana_id": kana_id,
                    "incorrect_typo_id": incorrect_typo_id,
                    "incorrect_typo": incorrect_typo,
                    }

                    ConnectionHandler.insert_into_table(table_name, insert_dict)

        def fill_kana_synonyms() -> None:
                            
            with open(FileEnsurer.kana_synonyms_path, "r", encoding="utf-8") as file:

                for line in file:

                    kana_id, synonym_id, synonym = FileHandler.extract_seisen_line_values(line)

                    table_name = "kana_synonyms"
                    insert_dict = {
                    "kana_id": kana_id,
                    "synonym_id": synonym_id,
                    "synonym": synonym,
                    }

                    ConnectionHandler.insert_into_table(table_name, insert_dict)

        def fill_kana_testing_material() -> None:

            with open(FileEnsurer.kana_testing_material_path, "r", encoding="utf-8") as file:

                for line in file:

                    kana_id, testing_material_id, testing_material = FileHandler.extract_seisen_line_values(line)

                    table_name = "kana_testing_material"
                    insert_dict = {
                    "kana_id": kana_id,
                    "testing_material_id": testing_material_id,
                    "testing_material": testing_material,
                    }

                    ConnectionHandler.insert_into_table(table_name, insert_dict)

        def fill_kana_readings() -> None:

            with open(FileEnsurer.kana_readings_path, "r", encoding="utf-8") as file:

                for line in file:

                    kana_id, reading_id, furigana, romaji = FileHandler.extract_seisen_line_values(line)

                    table_name = "kana_readings"
                    insert_dict = {
                    "kana_id": kana_id,
                    "reading_id": reading_id,
                    "furigana": furigana,
                    "romaji": romaji
                    }

                    ConnectionHandler.insert_into_table(table_name, insert_dict)

        ##----------------------------------------------------------------vocab----------------------------------------------------------------

        def fill_vocab() -> None:

            with open(FileEnsurer.vocab_path, "r", encoding="utf-8") as file:

                for line in file:

                    id, correct_count, incorrect_count = FileHandler.extract_seisen_line_values(line)

                    table_name = "vocab"
                    insert_dict = {
                    "id": id,
                    "correct_count": correct_count,
                    "incorrect_count": incorrect_count
                    }

                    ConnectionHandler.insert_into_table(table_name, insert_dict)

        def fill_vocab_typos() -> None:

            with open(FileEnsurer.vocab_typos_path, "r", encoding="utf-8") as file:

                for line in file:

                    vocab_id, typo_id, typo = FileHandler.extract_seisen_line_values(line)

                    table_name = "vocab_typos"
                    insert_dict = {
                    "vocab_id": vocab_id,
                    "typo_id": typo_id,
                    "typo": typo,
                    }

                    ConnectionHandler.insert_into_table(table_name, insert_dict)
        
        def fill_vocab_incorrect_typos() -> None:

            with open(FileEnsurer.vocab_incorrect_typos_path, "r", encoding="utf-8") as file:

                for line in file:

                    vocab_id, incorrect_typo_id, incorrect_typo = FileHandler.extract_seisen_line_values(line)

                    table_name = "vocab_incorrect_typos"
                    insert_dict = {
                    "vocab_id": vocab_id,
                    "incorrect_typo_id": incorrect_typo_id,
                    "incorrect_typo": incorrect_typo,
                    }

                    ConnectionHandler.insert_into_table(table_name, insert_dict)

        def fill_vocab_csep() -> None:
                                
            with open(FileEnsurer.vocab_synonyms_path, "r", encoding="utf-8") as file:

                for line in file:

                    vocab_id, synonym_id, synonym = FileHandler.extract_seisen_line_values(line)

                    table_name = "vocab_synonyms"
                    insert_dict = {
                    "vocab_id": vocab_id,
                    "synonym_id": synonym_id,
                    "synonym": synonym,
                    }

                    ConnectionHandler.insert_into_table(table_name, insert_dict)

        def fill_vocab_testing_material() -> None:

            with open(FileEnsurer.vocab_testing_material_path, "r", encoding="utf-8") as file:

                for line in file:

                    vocab_id, testing_material_id, testing_material = FileHandler.extract_seisen_line_values(line)

                    table_name = "vocab_testing_material"
                    insert_dict = {
                    "vocab_id": vocab_id,
                    "testing_material_id": testing_material_id,
                    "testing_material": testing_material,
                    }

                    ConnectionHandler.insert_into_table(table_name, insert_dict)

        def fill_vocab_readings() -> None:

            with open(FileEnsurer.vocab_readings_path, "r", encoding="utf-8") as file:

                for line in file:

                    vocab_id, reading_id, furigana, romaji = FileHandler.extract_seisen_line_values(line)

                    table_name = "vocab_readings"
                    insert_dict = {
                    "vocab_id": vocab_id,
                    "reading_id": reading_id,
                    "furigana": furigana,
                    "romaji": romaji
                    }

                    ConnectionHandler.insert_into_table(table_name, insert_dict)

        ##----------------------------------------------------------------functions----------------------------------------------------------------

        fill_kana()
        fill_kana_typos()
        fill_kana_incorrect_typos()
        fill_kana_synonyms()
        fill_kana_testing_material()
        fill_kana_readings()

        fill_vocab()
        fill_vocab_typos()
        fill_vocab_incorrect_typos()
        fill_vocab_csep()
        fill_vocab_testing_material()
        fill_vocab_readings()

##--------------------start-of-create_daily_remote_backup()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def create_daily_remote_backup():

        """
        
        Creates Seisen's daily remote backup.

        """

        ##----------------------------------------------------------------kana----------------------------------------------------------------

        def backup_kana() -> None:

            remote_archive_kana_dir = os.path.join(archive_dir, "kana")

            remote_archive_kana_path = os.path.join(remote_archive_kana_dir, "kana.seisen")
            remote_archive_kana_typos_path = os.path.join(remote_archive_kana_dir, "kana_typos.seisen")
            remote_archive_kana_incorrect_typos_path = os.path.join(remote_archive_kana_dir, "kana_incorrect_typos.seisen")
            remote_archive_kana_synonyms_path = os.path.join(remote_archive_kana_dir, "kana_synonyms.seisen")
            remote_archive_kana_readings_path = os.path.join(remote_archive_kana_dir, "kana_readings.seisen")
            remote_archive_kana_testing_material_path = os.path.join(remote_archive_kana_dir, "kana_testing_material.seisen")

            FileHandler.standard_create_directory(remote_archive_kana_dir)

            RemoteHandler.assemble_kana()

            RemoteHandler.write_kana_to_disk(remote_archive_kana_path, 
                                            remote_archive_kana_testing_material_path,
                                            remote_archive_kana_synonyms_path,
                                            remote_archive_kana_readings_path,
                                            remote_archive_kana_typos_path,
                                            remote_archive_kana_incorrect_typos_path)

        ##----------------------------------------------------------------vocab----------------------------------------------------------------

        def backup_vocab() -> None:

            remote_archive_vocab_dir = os.path.join(archive_dir, "vocab")

            remote_archive_vocab_path = os.path.join(remote_archive_vocab_dir, "vocab.seisen")
            remote_archive_vocab_typos_path = os.path.join(remote_archive_vocab_dir, "vocab_typos.seisen")
            remote_archive_vocab_incorrect_typos_path = os.path.join(remote_archive_vocab_dir, "vocab_incorrect_typos.seisen")
            remote_archive_vocab_synonyms_path = os.path.join(remote_archive_vocab_dir, "vocab_synonyms.seisen")
            remote_archive_vocab_readings_path = os.path.join(remote_archive_vocab_dir, "vocab_readings.seisen")
            remote_archive_vocab_testing_material_path = os.path.join(remote_archive_vocab_dir, "vocab_testing_material.seisen")

            FileHandler.standard_create_directory(remote_archive_vocab_dir)

            RemoteHandler.assemble_vocab()

            RemoteHandler.write_vocab_to_disk(remote_archive_vocab_path,
                                            remote_archive_vocab_testing_material_path,
                                            remote_archive_vocab_synonyms_path,
                                            remote_archive_vocab_readings_path,
                                            remote_archive_vocab_typos_path,
                                            remote_archive_vocab_incorrect_typos_path)

        ##----------------------------------------------------------------main----------------------------------------------------------------

        ## we do not create a remote storage backup if there is no valid database connection
        if(ConnectionHandler.check_connection_validity("remote storage backup creation") == False):
            return
        
        with open(FileEnsurer.last_remote_backup_path, 'r+', encoding="utf-8") as file:

            strips_to_perform = " \n\x00"

            last_backup_date = file.read()

            last_backup_date = last_backup_date.strip(strips_to_perform)
        
            current_day = str(datetime.today().strftime('%Y-%m-%d'))

        if(last_backup_date != current_day):
            archive_dir = FileEnsurer.create_archive_dir(1) 

            Logger.log_action("Created Daily Remote Backup.")

            FileHandler.standard_delete_file(FileEnsurer.last_remote_backup_path)

            FileHandler.modified_create_file(FileEnsurer.last_remote_backup_path, current_day)

            backup_kana()
            backup_vocab()

        else:
            pass
  
##--------------------start-of-restore_remote_backup()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def restore_remote_backup() -> None:

        """
        
        Prompts a user to restore a remote backup and does so if valid.

        """

        ## we do not fuck w/ remote if there is no valid database connection
        if(ConnectionHandler.check_connection_validity("restore remote storage backup") == False):
            print("No valid database connection skipping remote portion.\n")
            time.sleep(Toolkit.sleep_constant)
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

        try: ## user confirm will throw an UserConfirm error if the user wants to cancel the backup restore.

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

        except Toolkit.UserCancelError or AssertionError:
            print("Canceled.\n")

##--------------------start-of-local_remote_overwrite()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def local_remote_overwrite() -> None:
        
        """

        Overwrites the remote storage with the local storage.

        """

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