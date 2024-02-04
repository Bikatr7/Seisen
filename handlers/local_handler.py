## built-in libraries
from datetime import datetime

import os
import typing
import shutil
import time

## custom modules
from entities.answer import Answer
from entities.vocab import Vocab
from entities.word import Word
from entities.reading import Reading
from entities.testing_material import TestingMaterial
from entities.typo import Typo
from entities.incorrect_typo import IncorrectTypo

from modules.toolkit import Toolkit
from modules.logger import Logger
from modules.file_ensurer import FileEnsurer

from handlers.file_handler import FileHandler


class LocalHandler():

    """
    
    The LocalHandler class is used to handle all local storage related actions.

    """

    kana:typing.List[Word] = [] 

    vocab:typing.List[Vocab] = []

##--------------------start-of-load_words_from_local_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def load_words_from_local_storage() -> None:

        """

        Loads all words from local storage into the program.

        """

        ##--------------------start-of-load_file()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        def load_file(file_path, key_index=0):

            data: typing.Dict[str, typing.List[typing.Any]] = {}

            with open(file_path, "r", encoding="utf-8") as file:

                for line in file:
                    values = FileHandler.extract_seisen_line_values(line)
                    key = values[key_index]

                    if(key not in data):
                        data[key] = []

                    data[key].append(values)

            return data
        
        ##--------------------start-of-load_entities()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        def load_words(entity_path, readings_path, answers_path, testing_material_path, typo_path, incorrect_typo_path):

            entities:typing.List[Word] = []

            entity_data = load_file(entity_path)
            readings_data = load_file(readings_path)
            answers_data = load_file(answers_path)
            testing_material_data = load_file(testing_material_path)
            typo_data = load_file(typo_path)
            incorrect_typo_data = load_file(incorrect_typo_path)

            for entity_id, entity_values in entity_data.items():
                readings = [Reading(*reading_values) for reading_values in readings_data.get(entity_id, [])]
                answers = [Answer(*answer_values) for answer_values in answers_data.get(entity_id, [])]
                testing_material = [TestingMaterial(*testing_material_values) for testing_material_values in testing_material_data.get(entity_id, [])]
                typos = [Typo(*typo_values) for typo_values in typo_data.get(entity_id, [])]
                incorrect_typos = [IncorrectTypo(*incorrect_typo_values) for incorrect_typo_values in incorrect_typo_data.get(entity_id, [])]

                correct_count = int(entity_values[0][1]) 
                incorrect_count = int(entity_values[0][2])  

                entity = Word(int(entity_id), testing_material, answers, readings, correct_count, incorrect_count)

                entity.typos = typos
                entity.incorrect_typos = incorrect_typos

                entities.append(entity)

            return entities

        def load_vocab(entity_path, readings_path, answers_path, testing_material_path, typo_path, incorrect_typo_path):

            entities:typing.List[Vocab] = []

            entity_data = load_file(entity_path)
            readings_data = load_file(readings_path)
            answers_data = load_file(answers_path)
            testing_material_data = load_file(testing_material_path)
            typo_data = load_file(typo_path)
            incorrect_typo_data = load_file(incorrect_typo_path)

            for entity_id, entity_values in entity_data.items():
                readings = [Reading(*reading_values) for reading_values in readings_data.get(entity_id, [])]
                answers = [Answer(*answer_values) for answer_values in answers_data.get(entity_id, [])]
                testing_material = [TestingMaterial(*testing_material_values) for testing_material_values in testing_material_data.get(entity_id, [])]
                typos = [Typo(*typo_values) for typo_values in typo_data.get(entity_id, [])]
                incorrect_typos = [IncorrectTypo(*incorrect_typo_values) for incorrect_typo_values in incorrect_typo_data.get(entity_id, [])]

                correct_count = int(entity_values[0][1])  
                incorrect_count = int(entity_values[0][2]) 

                entity = Vocab(int(entity_id), testing_material, answers, readings, correct_count, incorrect_count)

                entity.typos = typos
                entity.incorrect_typos = incorrect_typos

                entities.append(entity)

            return entities

        LocalHandler.kana.clear()
        LocalHandler.vocab.clear()

        Logger.log_barrier()
        Logger.log_action("Loading kana from local storage...")

        LocalHandler.kana = load_words(FileEnsurer.kana_path, FileEnsurer.kana_readings_path, FileEnsurer.kana_answers_path, FileEnsurer.kana_testing_material_path, FileEnsurer.kana_typos_path, FileEnsurer.kana_incorrect_typos_path)

        Logger.log_barrier()
        Logger.log_action("Loading vocab from local storage...")

        LocalHandler.vocab = load_vocab(FileEnsurer.vocab_path, FileEnsurer.vocab_readings_path, FileEnsurer.vocab_answers_path, FileEnsurer.vocab_testing_material_path, FileEnsurer.vocab_typos_path, FileEnsurer.vocab_incorrect_typos_path)

##--------------------start-of-get_list_of_all_ids()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_list_of_all_ids(type_of_id_to_query:typing.Literal["KANA TYPO ID",
                                                                "KANA INCORRECT TYPO ID",
                                                                "VOCAB TYPO ID",
                                                                "VOCAB INCORRECT TYPO ID",
                                                                "KANA ID",
                                                                "VOCAB ID",
                                                                "KANA SYNONYM ID",
                                                                "VOCAB SYNONYM ID",
                                                                "KANA READING ID",
                                                                "VOCAB READING ID",
                                                                "KANA TESTING MATERIAL ID",
                                                                "VOCAB TESTING MATERIAL ID"]) -> typing.List[int]:

        """

        Gets the list of all ids in local storage given the type of id to query.

        Parameters:
        type_of_id_to_query (typing.Literal) : The type of id to query.

        Returns:
        ids (list - int) : The list of all ids in the database.

        """

        ids = [0]

        TYPO_ID_INDEX_LOCATION = 2
        WORD_ID_INDEX_LOCATION = 1
        SYNONYM_ID_INDEX_LOCATION = 2
        READING_ID_INDEX_LOCATION = 2
        TESTING_MATERIAL_ID_INDEX_LOCATION = 2

        def read_ids_from_file(file_path: str, index_location: int):
            with open(file_path, 'r', encoding='utf-8') as file:
                file_lines = file.readlines()
                for i in range(len(file_lines)):
                    ids.append(int(FileHandler.read_seisen_line(file_path, i+1, index_location)))

        if(type_of_id_to_query == "KANA TYPO ID"):
            read_ids_from_file(FileEnsurer.kana_typos_path, TYPO_ID_INDEX_LOCATION)
        elif(type_of_id_to_query == "KANA INCORRECT TYPO ID"):
            read_ids_from_file(FileEnsurer.kana_incorrect_typos_path, TYPO_ID_INDEX_LOCATION)
        elif(type_of_id_to_query == "VOCAB TYPO ID"):
            read_ids_from_file(FileEnsurer.vocab_typos_path, TYPO_ID_INDEX_LOCATION)
        elif(type_of_id_to_query == "VOCAB INCORRECT TYPO ID"):
            read_ids_from_file(FileEnsurer.vocab_incorrect_typos_path, TYPO_ID_INDEX_LOCATION)
        elif(type_of_id_to_query == "KANA ID"):
            read_ids_from_file(FileEnsurer.kana_path, WORD_ID_INDEX_LOCATION)
        elif(type_of_id_to_query == "VOCAB ID"):
            read_ids_from_file(FileEnsurer.vocab_path, WORD_ID_INDEX_LOCATION)
        elif(type_of_id_to_query == "KANA SYNONYM ID"):
            read_ids_from_file(FileEnsurer.kana_answers_path, SYNONYM_ID_INDEX_LOCATION)
        elif(type_of_id_to_query == "VOCAB SYNONYM ID"):
            read_ids_from_file(FileEnsurer.vocab_answers_path, SYNONYM_ID_INDEX_LOCATION)
        elif(type_of_id_to_query == "KANA READING ID"):
            read_ids_from_file(FileEnsurer.kana_readings_path, READING_ID_INDEX_LOCATION)
        elif(type_of_id_to_query == "VOCAB READING ID"):
            read_ids_from_file(FileEnsurer.vocab_readings_path, READING_ID_INDEX_LOCATION)
        elif(type_of_id_to_query == "KANA TESTING MATERIAL ID"):
            read_ids_from_file(FileEnsurer.kana_testing_material_path, TESTING_MATERIAL_ID_INDEX_LOCATION)
        elif(type_of_id_to_query == "VOCAB TESTING MATERIAL ID"):
            read_ids_from_file(FileEnsurer.vocab_testing_material_path, TESTING_MATERIAL_ID_INDEX_LOCATION)

        return ids
    
##--------------------start-of-create_daily_local_backup()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def create_daily_local_backup() -> None:

        """
        
        Creates Seisen's daily local backup.

        """

        with open(FileEnsurer.last_local_backup_path, 'r+', encoding="utf-8") as file:

            strips_to_perform = " \n\x00"

            last_backup_date = file.read()

            last_backup_date = last_backup_date.strip(strips_to_perform)

            current_day = str(datetime.today().strftime('%Y-%m-%d'))

        if(last_backup_date != current_day):
            
            archive_dir = FileEnsurer.create_archive_dir(2)

            Logger.log_action("Created Daily Local Backup.")

            shutil.copytree(FileEnsurer.kana_dir, os.path.join(archive_dir, "kana"))
            shutil.copytree(FileEnsurer.vocab_dir, os.path.join(archive_dir, "vocab"))

            FileHandler.standard_delete_file(FileEnsurer.last_local_backup_path)

            FileHandler.modified_create_file(FileEnsurer.last_local_backup_path, current_day)


##--------------------start-of-restore_local_backup()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def restore_local_backup():

        """
        
        Prompts the user to restart a local backup and does so if valid.

        """

        Toolkit.clear_console()

        valid_backups = [dir for dir in os.listdir(FileEnsurer.local_archives_dir) 
                        if(os.path.isdir(os.path.join(FileEnsurer.local_archives_dir, dir)))]

        if(not valid_backups):
            print("No backups found.\n")
            time.sleep(Toolkit.long_sleep_constant)
            return

        print("Please select a backup to restore:\n")
        print('\n'.join(valid_backups))

        backup_to_restore_prompt = "\nPlease select a backup to restore, please keep in mind that this process is not easily reversible."

        try:  # user confirm will throw an assertion error or a user cancel error if the user cancels.
            backup_to_restore = Toolkit.user_confirm(backup_to_restore_prompt)

            if(backup_to_restore in valid_backups):
                Toolkit.clear_console()

                shutil.rmtree(FileEnsurer.kana_dir)
                shutil.rmtree(FileEnsurer.vocab_dir)

                shutil.copytree(os.path.join(FileEnsurer.local_archives_dir, backup_to_restore), FileEnsurer.config_dir, dirs_exist_ok=True)

                Logger.log_action(f"Restored the {backup_to_restore} local backup.", output=True, omit_timestamp=True)

                LocalHandler.load_words_from_local_storage()

            else:
                print("Invalid Backup.\n")

        except (Toolkit.UserCancelError):
            print("\nCancelled.\n")
