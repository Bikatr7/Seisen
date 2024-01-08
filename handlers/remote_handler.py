## built-in modules
from datetime import datetime

import os
import shutil
import time

## custom modules
from entities.typo import Typo as typo_blueprint
from entities.incorrect_typo import IncorrectTypo as incorrect_typo_blueprint

from entities.synonym import Synonym as synonym_blueprint
from entities.word import Word as kana_blueprint
from entities.vocab import Vocab as vocab_blueprint

from modules.file_ensurer import FileEnsurer
from modules.toolkit import Toolkit
from modules.logger import Logger

from handlers.connection_handler import ConnectionHandler
from handlers.file_handler import FileHandler

class RemoteHandler():

    """
    
    The handler that handles all interactions with the remote storage (database).

    """

    kana = [] 
    kana_typos = []
    kana_incorrect_typos = []
    kana_synonyms = []

    vocab = []
    vocab_typos = []
    vocab_incorrect_typos = []
    vocab_synonyms = []

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

        ##----------------------------------------------------------------clear_local_vocab()----------------------------------------------------------------

        def clear_local_vocab() -> None:

            FileHandler.clear_file(FileEnsurer.vocab_path)
            FileHandler.clear_file(FileEnsurer.vocab_synonyms_path)
            FileHandler.clear_file(FileEnsurer.vocab_typos_path)
            FileHandler.clear_file(FileEnsurer.vocab_incorrect_typos_path)

        ##----------------------------------------------------------------reset_kana_relations()----------------------------------------------------------------

        def reset_kana_relations() -> None:
            
            list_of_all_accepted_answers = []

            RemoteHandler.kana.clear()
            RemoteHandler.kana_typos.clear()
            RemoteHandler.kana_incorrect_typos.clear()
            RemoteHandler.kana_synonyms.clear()

            word_id_list, kana_list, reading_list, incorrect_count_list, correct_count_list = ConnectionHandler.read_multi_column_query("select id, kana, reading, incorrect_count, correct_count from kana")
            typo_word_type_list, typo_id_list, typo_word_id_list, typo_value_list = ConnectionHandler.read_multi_column_query("select word_type, typo_id, kana_id, typo_value from kana_typos")
            incorrect_typo_word_type_list, incorrect_typo_id_list, incorrect_typo_word_id_list, incorrect_typo_value_list = ConnectionHandler.read_multi_column_query("select word_type, incorrect_typo_id, kana_id, incorrect_typo_value from kana_incorrect_typos")
            kana_id_list, synonym_id_list, synonym_value_list, word_type_list = ConnectionHandler.read_multi_column_query("select kana_id, kana_synonym_id, kana_synonym_value, word_type from kana_synonyms")

            RemoteHandler.kana = [kana_blueprint(int(word_id_list[i]), kana_list[i], reading_list[i], list_of_all_accepted_answers, int(incorrect_count_list[i]), int(correct_count_list[i])) for i in range(len(word_id_list))]
            RemoteHandler.kana_typos = [typo_blueprint(int(typo_word_id_list[i]), int(typo_id_list[i]), typo_value_list[i], typo_word_type_list[i]) for i in range(len(typo_word_id_list))]
            RemoteHandler.kana_incorrect_typos = [incorrect_typo_blueprint(int(incorrect_typo_word_id_list[i]), int(incorrect_typo_id_list[i]), incorrect_typo_value_list[i], incorrect_typo_word_type_list[i]) for i in range(len(incorrect_typo_word_id_list))]
            RemoteHandler.kana_synonyms = [synonym_blueprint(int(kana_id_list[i]), int(synonym_id_list[i]), synonym_value_list[i], word_type_list[i]) for i in range(len(kana_id_list))]


            ## resets local storage file-wise
            for kana in RemoteHandler.kana:
                word_values = [kana.word_id, kana.testing_material, kana.testing_material_answer_main, kana.incorrect_count, kana.correct_count]
                FileHandler.write_seisen_line(FileEnsurer.kana_path, word_values)

            for typo in RemoteHandler.kana_typos:
                typo_values = [typo.word_id, typo.typo_id, typo.typo_value, typo.word_type]
                FileHandler.write_seisen_line(FileEnsurer.kana_typos_path, typo_values)

            for incorrect_typo in RemoteHandler.kana_incorrect_typos:
                incorrect_typo_values = [incorrect_typo.word_id, incorrect_typo.incorrect_typo_id, incorrect_typo.incorrect_typo_value, incorrect_typo.word_type]
                FileHandler.write_seisen_line(FileEnsurer.kana_incorrect_typos_path, incorrect_typo_values)

            for synonym in RemoteHandler.kana_synonyms:
                synonym_values = [synonym.word_id, synonym.synonym_id, synonym.synonym_value, synonym.word_type]
                FileHandler.write_seisen_line(FileEnsurer.kana_synonyms_path, synonym_values)

            ## current session-wise reset
            for kana in RemoteHandler.kana:
                for typo in RemoteHandler.kana_typos:
                    if(typo.word_type == kana.word_type and typo.word_id == kana.word_id):
                        kana.typos.append(typo)
                        Logger.log_action("Added Typo " + typo.typo_value + " to Kana " + kana.testing_material)        

                for incorrect_typo in RemoteHandler.kana_incorrect_typos:
                    if(incorrect_typo.word_type == kana.word_type and incorrect_typo.word_id == kana.word_id):
                        kana.incorrect_typos.append(incorrect_typo)
                        Logger.log_action("Added Incorrect Typo " + incorrect_typo.incorrect_typo_value + " to Kana " + kana.testing_material)

                for synonym in RemoteHandler.kana_synonyms:
                    if(synonym.word_id == kana.word_id and synonym.word_type == kana.word_type):
                        kana.testing_material_answer_all.append(synonym)
                        Logger.log_action("Added Synonym " + synonym.synonym_value + " to Kana " + kana.testing_material)

        ##----------------------------------------------------------------reset_vocab_relations()----------------------------------------------------------------
                
        def reset_vocab_relations() -> None:

            RemoteHandler.vocab.clear()
            RemoteHandler.vocab_typos.clear()
            RemoteHandler.vocab_incorrect_typos.clear()
            RemoteHandler.vocab_synonyms.clear()

            word_id_list, vocab_list, romaji_list, answer_list, furigana_list, incorrect_count_list, correct_count_list, is_kanji_list = ConnectionHandler.read_multi_column_query("select id, vocab, romaji, answer, furigana, incorrect_count, correct_count, is_kanji from vocab")
            typo_word_type_list, typo_id_list, typo_word_id_list, typo_value_list = ConnectionHandler.read_multi_column_query("select word_type, typo_id, vocab_id, typo_value from vocab_typos")
            incorrect_typo_word_type_list, incorrect_typo_id_list, incorrect_typo_word_id_list, incorrect_typo_value_list = ConnectionHandler.read_multi_column_query("select word_type, incorrect_typo_id, vocab_id, incorrect_typo_value from vocab_incorrect_typos")
            vocab_id_list, synonym_id_list, synonym_value_list, word_type_list = ConnectionHandler.read_multi_column_query("select vocab_id, vocab_synonym_id, vocab_synonym_value, word_type from vocab_synonyms")

            RemoteHandler.vocab = [vocab_blueprint(int(word_id_list[i]), vocab_list[i], romaji_list[i], answer_list[i], [], furigana_list[i], int(incorrect_count_list[i]), int(correct_count_list[i]), bool(is_kanji_list[i])) for i in range(len(word_id_list))]
            RemoteHandler.vocab_typos = [typo_blueprint(int(typo_word_id_list[i]), int(typo_id_list[i]), typo_value_list[i], typo_word_type_list[i]) for i in range(len(typo_word_id_list))]
            RemoteHandler.vocab_incorrect_typos = [incorrect_typo_blueprint(int(incorrect_typo_word_id_list[i]), int(incorrect_typo_id_list[i]), incorrect_typo_value_list[i], incorrect_typo_word_type_list[i]) for i in range(len(incorrect_typo_word_id_list))]
            RemoteHandler.vocab_synonyms = [synonym_blueprint(int(vocab_id_list[i]), int(synonym_id_list[i]), synonym_value_list[i], word_type_list[i]) for i in range(len(vocab_id_list))]

            ## resets local storage file-wise
            for vocab in RemoteHandler.vocab:
                vocab_values = [vocab.word_id, vocab.testing_material, vocab.romaji, vocab.testing_material_answer_main, vocab.furigana, vocab.incorrect_count, vocab.correct_count]
                FileHandler.write_seisen_line(FileEnsurer.vocab_path, vocab_values)

            for typo in RemoteHandler.vocab_typos:
                typo_values = [typo.word_id, typo.typo_id, typo.typo_value, typo.word_type]
                FileHandler.write_seisen_line(FileEnsurer.vocab_typos_path, typo_values)

            for incorrect_typo in RemoteHandler.vocab_incorrect_typos:
                incorrect_typo_values = [incorrect_typo.word_id, incorrect_typo.incorrect_typo_id, incorrect_typo.incorrect_typo_value, incorrect_typo.word_type]
                FileHandler.write_seisen_line(FileEnsurer.vocab_incorrect_typos_path, incorrect_typo_values)

            for synonym in RemoteHandler.vocab_synonyms:
                synonym_values = [synonym.word_id, synonym.synonym_id, synonym.synonym_value, synonym.word_type]
                FileHandler.write_seisen_line(FileEnsurer.vocab_synonyms_path, synonym_values)

            ## current session-wise reset
            for vocab in RemoteHandler.vocab:

                for typo in RemoteHandler.vocab_typos:
                    if(typo.word_type == vocab.word_type and typo.word_id == vocab.word_id):
                        vocab.typos.append(typo)        
                        Logger.log_action("Added Typo" + typo.typo_value + " to Vocab " + vocab.testing_material)    

                for incorrect_typo in RemoteHandler.vocab_incorrect_typos:
                    if(incorrect_typo.word_type == vocab.word_type and incorrect_typo.word_id == vocab.word_id):
                        vocab.incorrect_typos.append(incorrect_typo)
                        Logger.log_action("Added Incorrect Typo " + incorrect_typo.incorrect_typo_value + " to Vocab " + vocab.testing_material)

                for synonym in RemoteHandler.vocab_synonyms:
                    if(synonym.word_id == vocab.word_id and synonym.word_type == vocab.word_type):
                        vocab.testing_material_answer_all.append(synonym)
                        Logger.log_action("Added Synonym " + synonym.synonym_value + " to Vocab " + vocab.testing_material)

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
        
        with open(FileEnsurer.last_local_remote_overwrite_accurate_path, 'w+', encoding="utf-8") as file:

            last_overwrite_date_accurate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            file.write(last_overwrite_date_accurate)

        Logger.log_barrier()
        Logger.log_action("Resetting Remote Storage...")

        RemoteHandler.delete_remote_storage()
        RemoteHandler.create_remote_storage()
        RemoteHandler.fill_remote_storage()

        if(not omit_print):
            print("Remote Storage Reset.\n")

##--------------------start-of-delete_remote_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def delete_remote_storage() -> None:

        """
        
        Deletes the remote storage. By dropping all the tables.

        """

        ##----------------------------------------------------------------kana----------------------------------------------------------------

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

        ConnectionHandler.execute_query(delete_kana_synonyms_query)
        ConnectionHandler.execute_query(delete_kana_typos_query)
        ConnectionHandler.execute_query(delete_kana_incorrect_typos_query)
        ConnectionHandler.execute_query(delete_kana_query)

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
            kana VARCHAR(255) NOT NULL,
            reading VARCHAR(255) NOT NULL,
            incorrect_count INT NOT NULL,
            correct_count INT NOT NULL,
            word_type VARCHAR(255) NOT NULL,
            PRIMARY KEY (id)
        );
        """

        create_kana_typos_query = """
        CREATE TABLE kana_typos (
            kana_id INT NOT NULL,
            typo_id INT NOT NULL,
            typo_value VARCHAR(255) NOT NULL,
            word_type VARCHAR(255) NOT NULL,
            PRIMARY KEY (typo_id),
            FOREIGN KEY (kana_id) REFERENCES kana(id)
        );
        """

        create_kana_incorrect_typos_query = """
        CREATE TABLE kana_incorrect_typos (
            kana_id INT NOT NULL,
            incorrect_typo_id INT NOT NULL,
            incorrect_typo_value VARCHAR(255) NOT NULL,
            word_type VARCHAR(255) NOT NULL,
            PRIMARY KEY (incorrect_typo_id),
            FOREIGN KEY (kana_id) REFERENCES kana(id)
        );
        """

        create_kana_synonyms_query = """
        CREATE TABLE kana_synonyms (
            kana_id INT NOT NULL,
            kana_synonym_id INT NOT NULL,
            kana_synonym_value VARCHAR(255) NOT NULL,
            word_type VARCHAR(255) NOT NULL,
            PRIMARY KEY (kana_synonym_id),
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
            word_type VARCHAR(255) NOT NULL,
            is_kanji TINYINT(1) NOT NULL,
            PRIMARY KEY (id)
        );

        """        
        create_vocab_typos_query = """
        CREATE TABLE vocab_typos (
            vocab_id INT NOT NULL,
            typo_id INT NOT NULL,
            typo_value VARCHAR(255) NOT NULL,
            word_type VARCHAR(255) NOT NULL,
            PRIMARY KEY (typo_id),
            FOREIGN KEY (vocab_id) REFERENCES vocab(id)
        );
        """

        create_vocab_incorrect_typos_query = """
        CREATE TABLE vocab_incorrect_typos (
            vocab_id INT NOT NULL,
            incorrect_typo_id INT NOT NULL,
            incorrect_typo_value VARCHAR(255) NOT NULL,
            word_type VARCHAR(255) NOT NULL,
            PRIMARY KEY (incorrect_typo_id),
            FOREIGN KEY (vocab_id) REFERENCES vocab(id)
        );
        """

        create_vocab_synonym_query = """
        CREATE TABLE vocab_synonyms (
            vocab_id INT NOT NULL,
            vocab_synonym_id INT NOT NULL,
            vocab_synonym_value VARCHAR(255) NOT NULL,
            word_type VARCHAR(255) NOT NULL,
            PRIMARY KEY (vocab_synonym_id),
            FOREIGN KEY (vocab_id) REFERENCES vocab(id)
        );
        """

        ##----------------------------------------------------------------queries----------------------------------------------------------------

        ConnectionHandler.execute_query(create_kana_query)
        ConnectionHandler.execute_query(create_kana_typos_query)
        ConnectionHandler.execute_query(create_kana_incorrect_typos_query)
        ConnectionHandler.execute_query(create_kana_synonyms_query)

        ConnectionHandler.execute_query(create_vocab_query)
        ConnectionHandler.execute_query(create_vocab_typos_query)
        ConnectionHandler.execute_query(create_vocab_incorrect_typos_query)
        ConnectionHandler.execute_query(create_vocab_synonym_query)

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

                    values = FileHandler.extract_seisen_line_values(line)

                    table_name = "kana"
                    insert_dict = {
                    "id": values[0],
                    "kana": values[1],
                    "reading": values[2],
                    "incorrect_count": values[3],
                    "correct_count": values[4],
                    "word_type": "kana"
                    }

                    ConnectionHandler.insert_into_table(table_name, insert_dict)

        def fill_kana_typos() -> None:

            with open(FileEnsurer.kana_typos_path, "r", encoding="utf-8") as file:

                for line in file:

                    values = FileHandler.extract_seisen_line_values(line)

                    values[2] = FileHandler.perform_database_sanitization(values[2])

                    table_name = "kana_typos"
                    insert_dict = {
                        "kana_id": values[0],
                        "typo_id": values[1],
                        "typo_value": values[2],
                        "word_type": values[3]
                    }

                    ConnectionHandler.insert_into_table(table_name, insert_dict)
        
        def fill_kana_incorrect_typos() -> None:

                with open(FileEnsurer.kana_incorrect_typos_path, "r", encoding="utf-8") as file:

                    for line in file:

                        values = FileHandler.extract_seisen_line_values(line)

                        values[2] = FileHandler.perform_database_sanitization(values[2])

                        table_name = "kana_incorrect_typos"
                        insert_dict = {
                        "kana_id": values[0],
                        "incorrect_typo_id": values[1],
                        "incorrect_typo_value": values[2],
                        "word_type": values[3]
                        }

                        ConnectionHandler.insert_into_table(table_name, insert_dict)

        def fill_kana_csep() -> None:
                                
                with open(FileEnsurer.kana_synonyms_path, "r", encoding="utf-8") as file:

                    for line in file:

                        values = FileHandler.extract_seisen_line_values(line)

                        values[2] = FileHandler.perform_database_sanitization(values[2])

                        table_name = "kana_synonyms"
                        insert_dict = {
                        "kana_id": values[0],
                        "kana_synonym_id": values[1],
                        "kana_synonym_value": values[2],
                        "word_type": values[3]
                        }

                        ConnectionHandler.insert_into_table(table_name, insert_dict)

        ##----------------------------------------------------------------vocab----------------------------------------------------------------

        def fill_vocab() -> None:

            with open(FileEnsurer.vocab_path, "r", encoding="utf-8") as file:

                for line in file:

                    values = FileHandler.extract_seisen_line_values(line)

                    ## 0 is treated as a lack of furigana, which means it's not a kanji word
                    if(values[4] == "0"):
                        is_kanji = 0
                    else:
                        is_kanji = 1
                    
                    values[3] = FileHandler.perform_database_sanitization(values[3])

                    table_name = "vocab"
                    insert_dict = {
                    "id": values[0],
                    "vocab": values[1],
                    "romaji": values[2],
                    "answer": values[3],
                    "furigana": values[4],
                    "incorrect_count": values[5],
                    "correct_count": values[6],
                    "word_type": "vocab",
                    "is_kanji": is_kanji
                    }

                    ConnectionHandler.insert_into_table(table_name, insert_dict)

        def fill_vocab_typos() -> None:

            with open(FileEnsurer.vocab_typos_path, "r", encoding="utf-8") as file:

                for line in file:

                    values = FileHandler.extract_seisen_line_values(line)

                    values[2] = FileHandler.perform_database_sanitization(values[2])

                    table_name = "vocab_typos"
                    insert_dict = {
                        "vocab_id": values[0],
                        "typo_id": values[1],
                        "typo_value": values[2],
                        "word_type": values[3]
                    }

                    ConnectionHandler.insert_into_table(table_name, insert_dict)
        
        def fill_vocab_incorrect_typos() -> None:

                with open(FileEnsurer.vocab_incorrect_typos_path, "r", encoding="utf-8") as file:

                    for line in file:

                        values = FileHandler.extract_seisen_line_values(line)

                        values[2] = FileHandler.perform_database_sanitization(values[2])

                        table_name = "vocab_incorrect_typos"
                        insert_dict = {
                        "vocab_id": values[0],
                        "incorrect_typo_id": values[1],
                        "incorrect_typo_value": values[2],
                        "word_type": values[3]
                        }

                        ConnectionHandler.insert_into_table(table_name, insert_dict)

        def fill_vocab_csep() -> None:
                                
                with open(FileEnsurer.vocab_synonyms_path, "r", encoding="utf-8") as file:

                    for line in file:

                        values = FileHandler.extract_seisen_line_values(line)

                        values[2] = FileHandler.perform_database_sanitization(values[2])

                        table_name = "vocab_synonyms"
                        insert_dict = {
                        "vocab_id": values[0],
                        "vocab_synonym_id": values[1],
                        "vocab_synonym_value": values[2],
                        "word_type": values[3]
                        }

                        ConnectionHandler.insert_into_table(table_name, insert_dict)

        ##----------------------------------------------------------------functions----------------------------------------------------------------

        fill_kana()
        fill_kana_typos()
        fill_kana_incorrect_typos()
        fill_kana_csep()

        fill_vocab()
        fill_vocab_typos()
        fill_vocab_incorrect_typos()
        fill_vocab_csep()

##--------------------start-of-create_daily_remote_backup()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def create_daily_remote_backup():

        """
        
        Creates Seisen's daily remote backup.

        """

        ##----------------------------------------------------------------kana----------------------------------------------------------------

        def backup_kana() -> None:

            list_of_all_accepted_answers = []

            remote_archive_kana_dir = os.path.join(archive_dir, "kana")

            remote_archive_kana_path = os.path.join(remote_archive_kana_dir, "kana.seisen")
            remote_archive_kana_typos_path = os.path.join(remote_archive_kana_dir, "kana_typos.seisen")
            remote_archive_kana_incorrect_typos_path = os.path.join(remote_archive_kana_dir, "kana_incorrect_typos.seisen")
            remote_archive_kana_synonyms_path = os.path.join(remote_archive_kana_dir, "kana_synonyms.seisen")

            FileHandler.standard_create_directory(remote_archive_kana_dir)

            word_id_list, kana_list, reading_list, incorrect_count_list, correct_count_list = ConnectionHandler.read_multi_column_query("select id, kana, reading, incorrect_count, correct_count from kana")
            typo_word_type_list, typo_id_list, typo_word_id_list, typo_value_list = ConnectionHandler.read_multi_column_query("select word_type, typo_id, kana_id, typo_value from kana_typos")
            incorrect_typo_word_type_list, incorrect_typo_id_list, incorrect_typo_word_id_list, incorrect_typo_value_list = ConnectionHandler.read_multi_column_query("select word_type, incorrect_typo_id, kana_id, incorrect_typo_value from kana_incorrect_typos")
            kana_id_list, synonym_id_list, synonym_value_list, word_type_list = ConnectionHandler.read_multi_column_query("select kana_id, kana_synonym_id, kana_synonym_value, word_type from kana_synonyms")

            RemoteHandler.kana = [kana_blueprint(int(word_id_list[i]), kana_list[i], reading_list[i], list_of_all_accepted_answers, int(incorrect_count_list[i]), int(correct_count_list[i])) for i in range(len(word_id_list))]
            RemoteHandler.kana_typos = [typo_blueprint(int(typo_word_id_list[i]), int(typo_id_list[i]), typo_value_list[i], typo_word_type_list[i]) for i in range(len(typo_word_id_list))]
            RemoteHandler.kana_incorrect_typos = [incorrect_typo_blueprint(int(incorrect_typo_word_id_list[i]), int(incorrect_typo_id_list[i]), incorrect_typo_value_list[i], incorrect_typo_word_type_list[i]) for i in range(len(incorrect_typo_word_id_list))]
            RemoteHandler.kana_synonyms = [synonym_blueprint(int(kana_id_list[i]), int(synonym_id_list[i]), synonym_value_list[i], word_type_list[i]) for i in range(len(kana_id_list))]

            ## backups local storage file-wise
            for kana in RemoteHandler.kana:
                word_values = [kana.word_id, kana.testing_material, kana.testing_material_answer_main, kana.incorrect_count, kana.correct_count]
                FileHandler.write_seisen_line(remote_archive_kana_path, word_values)

            for typo in RemoteHandler.kana_typos:
                typo_values = [typo.word_id, typo.typo_id, typo.typo_value, typo.word_type]
                FileHandler.write_seisen_line(remote_archive_kana_typos_path, typo_values)

            for incorrect_typo in RemoteHandler.kana_incorrect_typos:
                incorrect_typo_values = [incorrect_typo.word_id, incorrect_typo.incorrect_typo_id, incorrect_typo.incorrect_typo_value, incorrect_typo.word_type]
                FileHandler.write_seisen_line(remote_archive_kana_incorrect_typos_path, incorrect_typo_values)

            for synonym in RemoteHandler.kana_synonyms:
                synonym_values = [synonym.word_id, synonym.synonym_id, synonym.synonym_value, synonym.word_type]
                FileHandler.write_seisen_line(remote_archive_kana_synonyms_path, synonym_values)

        ##----------------------------------------------------------------vocab----------------------------------------------------------------

        def backup_vocab() -> None:

            remote_archive_vocab_dir = os.path.join(archive_dir, "vocab")

            remote_archive_vocab_path = os.path.join(remote_archive_vocab_dir, "vocab.seisen")
            remote_archive_vocab_typos_path = os.path.join(remote_archive_vocab_dir, "vocab_typos.seisen")
            remote_archive_vocab_incorrect_typos_path = os.path.join(remote_archive_vocab_dir, "vocab_incorrect_typos.seisen")
            remote_archive_vocab_synonyms_path = os.path.join(remote_archive_vocab_dir, "vocab_synonyms.seisen")

            FileHandler.standard_create_directory(remote_archive_vocab_dir)

            word_id_list, vocab_list, romaji_list, answer_list, furigana_list, incorrect_count_list, correct_count_list, is_kanji_list = ConnectionHandler.read_multi_column_query("select id, vocab, romaji, answer, furigana, incorrect_count, correct_count, is_kanji from vocab")
            typo_word_type_list, typo_id_list, typo_word_id_list, typo_value_list = ConnectionHandler.read_multi_column_query("select word_type, typo_id, vocab_id, typo_value from vocab_typos")
            incorrect_typo_word_type_list, incorrect_typo_id_list, incorrect_typo_word_id_list, incorrect_typo_value_list = ConnectionHandler.read_multi_column_query("select word_type, incorrect_typo_id, vocab_id, incorrect_typo_value from vocab_incorrect_typos")
            vocab_id_list, synonym_id_list, synonym_value_list, word_type_list = ConnectionHandler.read_multi_column_query("select vocab_id, vocab_synonym_id, vocab_synonym_value, word_type from vocab_synonyms")

            RemoteHandler.vocab = [vocab_blueprint(int(word_id_list[i]), vocab_list[i], romaji_list[i], answer_list[i], [], furigana_list[i], int(incorrect_count_list[i]), int(correct_count_list[i]), bool(is_kanji_list[i])) for i in range(len(word_id_list))]
            RemoteHandler.vocab_typos = [typo_blueprint(int(typo_word_id_list[i]), int(typo_id_list[i]), typo_value_list[i], typo_word_type_list[i]) for i in range(len(typo_word_id_list))]
            RemoteHandler.vocab_incorrect_typos = [incorrect_typo_blueprint(int(incorrect_typo_word_id_list[i]), int(incorrect_typo_id_list[i]), incorrect_typo_value_list[i], incorrect_typo_word_type_list[i]) for i in range(len(incorrect_typo_word_id_list))]
            RemoteHandler.vocab_synonyms = [synonym_blueprint(int(vocab_id_list[i]), int(synonym_id_list[i]), synonym_value_list[i], word_type_list[i]) for i in range(len(vocab_id_list))]

            ## resets local storage file-wise
            for vocab in RemoteHandler.vocab:
                vocab_values = [vocab.word_id, vocab.testing_material, vocab.romaji, vocab.testing_material_answer_main, vocab.furigana, vocab.incorrect_count, vocab.correct_count]
                FileHandler.write_seisen_line(remote_archive_vocab_path, vocab_values)

            for typo in RemoteHandler.vocab_typos:
                typo_values = [typo.word_id, typo.typo_id, typo.typo_value, typo.word_type]
                FileHandler.write_seisen_line(remote_archive_vocab_typos_path, typo_values)

            for incorrect_typo in RemoteHandler.vocab_incorrect_typos:
                incorrect_typo_values = [incorrect_typo.word_id, incorrect_typo.incorrect_typo_id, incorrect_typo.incorrect_typo_value, incorrect_typo.word_type]
                FileHandler.write_seisen_line(remote_archive_vocab_incorrect_typos_path, incorrect_typo_values)

            for synonym in RemoteHandler.vocab_synonyms:
                synonym_values = [synonym.word_id, synonym.synonym_id, synonym.synonym_value, synonym.word_type]
                FileHandler.write_seisen_line(remote_archive_vocab_synonyms_path, synonym_values)

        ##----------------------------------------------------------------main----------------------------------------------------------------

        ## we do not create a remote storage backup if there is no valid database connection
        if(ConnectionHandler.check_connection_validity("remote storage backup creation") == False):
            return
        
        with open(FileEnsurer.last_remote_backup_path, 'r+', encoding="utf-8") as file:

            last_backup_date = str(file.read().strip())
            last_backup_date = last_backup_date.strip('\x00')
        
            current_day = str(datetime.today().strftime('%Y-%m-%d'))

            if(last_backup_date != current_day):
                archive_dir = FileEnsurer.create_archive_dir(1) 

                Logger.log_action("Created Daily Remote Backup.")

                file.truncate(0)

                file.write(current_day.strip('\x00').strip(" ").strip())

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
            time.sleep(1)
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
        
        backup_to_restore_prompt += "\nPlease select a backup to restore, please keep in mind that this process is not easily reversible."

        if(len(valid_backups) == 0):
            print("No backups found.")
            time.sleep(1)
            return

        try: ## user confirm will throw an assertion/user confirm error if the user wants to cancel the backup restore.

            backup_to_restore = Toolkit.user_confirm(backup_to_restore_prompt)

            if(backup_to_restore in valid_backups):
                Toolkit.clear_console()

                shutil.rmtree(FileEnsurer.kana_dir)
                shutil.rmtree(FileEnsurer.vocab_dir)

                shutil.copytree(os.path.join(FileEnsurer.remote_archives_dir, backup_to_restore), FileEnsurer.config_dir, dirs_exist_ok=True)

                Logger.log_action("Restored the " + backup_to_restore + " remote backup.", omit_timestamp=True, output=True)

            else:
                print("Invalid Backup\n")

        except Toolkit.UserCancelError or AssertionError:
            print("Canceled.")

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

            last_backup_date = str(file.read().strip()).strip('\x00').strip()
        
            current_day = str(datetime.today().strftime('%Y-%m-%d'))

            if(last_backup_date != current_day):

                Logger.log_action("Overwriting Remote with Local.")
        
                file.truncate(0)
                
                file.write(current_day.strip('\x00').strip())

                RemoteHandler.reset_remote_storage(omit_print=True)