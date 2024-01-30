## built-in libraries
from __future__ import annotations ## Used for cheating the circular import issue that occurs when I need to type check some things

from datetime import datetime

import os
import typing
import shutil
import time

## custom modules
from entities.typo import Typo as typo_blueprint
from entities.incorrect_typo import IncorrectTypo as incorrect_typo_blueprint

from entities.word import Word as kana_blueprint
from entities.vocab import Vocab as vocab_blueprint

from entities.reading import Reading as reading_blueprint
from entities.synonym import Synonym as synonym_blueprint
from entities.testing_material import TestingMaterial as testing_material_blueprint

from modules.toolkit import Toolkit
from modules.logger import Logger
from modules.file_ensurer import FileEnsurer

from handlers.file_handler import FileHandler

if(typing.TYPE_CHECKING): ## Used for cheating the circular import issue that occurs when I need to type check some things
    from entities.synonym import Synonym
    from entities.vocab import Vocab
    from entities.word import Word as Kana
    from entities.reading import Reading
    from entities.testing_material import TestingMaterial

class LocalHandler():

    """
    
    The LocalHandler class is used to handle all local storage related actions.

    """

    kana: typing.List[Kana] = [] 

    vocab: typing.List[Vocab] = []

##--------------------start-of-load_words_from_local_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def load_words_from_local_storage() -> None:
        
        """
        
        Loads all words from local storage into the program.

        """

        ##----------------------------------------------------------------get_kana_readings()----------------------------------------------------------------

        def get_kana_readings(kana_id:str) -> typing.List[Reading]:

            readings = []

            with open(FileEnsurer.kana_readings_path, "r", encoding="utf-8") as file:

                for line in file:

                    reading_kana_id, reading_id, furigana, romaji = FileHandler.extract_seisen_line_values(line)

                    if(reading_kana_id == kana_id):

                        readings.append(reading_blueprint(int(reading_kana_id), int(reading_id), furigana, romaji))

            return readings

        ##----------------------------------------------------------------get_kana_synonyms()----------------------------------------------------------------

        def get_kana_synonyms(kana_id:str) -> typing.List[Synonym]:

            synonyms = []

            with open(FileEnsurer.kana_synonyms_path, "r", encoding="utf-8") as file:

                for line in file:

                    synonym_kana_id, synonym_id, synonym_value = FileHandler.extract_seisen_line_values(line)
                    
                    if(synonym_kana_id == kana_id):

                        synonyms.append(synonym_blueprint(int(synonym_kana_id), int(synonym_id), synonym_value))

            return synonyms
        
        ##----------------------------------------------------------------get_kana_testing_material()----------------------------------------------------------------

        def get_kana_testing_material(kana_id:str) -> typing.List[TestingMaterial]:

            testing_material = []

            with open(FileEnsurer.kana_testing_material_path, "r", encoding="utf-8") as file:

                for line in file:

                    testing_material_kana_id, testing_material_id, testing_material_value = FileHandler.extract_seisen_line_values(line)

                    if(testing_material_kana_id == kana_id):
                            
                        testing_material.append(testing_material_blueprint(int(testing_material_kana_id), int(testing_material_id), testing_material_value))


            return testing_material

        ##----------------------------------------------------------------load_kana()----------------------------------------------------------------

        def load_kana() -> None:
    
            with open(FileEnsurer.kana_path, "r", encoding="utf-8") as file:

                for line in file:

                    kana_id, correct_count, incorrect_count = FileHandler.extract_seisen_line_values(line)

                    readings = get_kana_readings(kana_id)
                    synonyms = get_kana_synonyms(kana_id)
                    testing_material = get_kana_testing_material(kana_id)

                    Logger.log_action(kana_id + " " + str(len(readings)) + " " + str(len(synonyms)) + " " + str(len(testing_material)))

                    LocalHandler.kana.append(kana_blueprint(int(kana_id), testing_material, synonyms, readings, int(correct_count), int(incorrect_count)))

                    Logger.log_action("Loaded Kana - (" + kana_id + "," + correct_count + "," + incorrect_count + ") with the following readings - " + str([reading.furigana for reading in readings]) + " and the following synonyms - " + str([synonym.value for synonym in synonyms]) + " and the following testing material - " + str([testing_material.value for testing_material in testing_material]))
            
            with open(FileEnsurer.kana_typos_path, "r", encoding="utf-8") as file:

                for line in file:
                    
                    typo_kana_id, typo_id, typo_value = FileHandler.extract_seisen_line_values(line)

                    for kana in LocalHandler.kana:
                        if(kana.id == int(typo_kana_id)):

                            kana.typos.append(typo_blueprint(int(typo_kana_id), int(typo_id), typo_value))

                            Logger.log_action("Loaded Kana Typo - (" + typo_kana_id + "," + typo_id + "," + typo_value + ",)")
            
            with open(FileEnsurer.kana_incorrect_typos_path, "r", encoding="utf-8") as file:

                for line in file:
    
                    incorrect_typo_kana_id, incorrect_typo_id, incorrect_typo_value = FileHandler.extract_seisen_line_values(line)

                    for kana in LocalHandler.kana:
                        if(kana.id == int(incorrect_typo_kana_id)):

                            kana.incorrect_typos.append(incorrect_typo_blueprint(int(incorrect_typo_kana_id), int(incorrect_typo_id), incorrect_typo_value))

                            Logger.log_action("Loaded Kana Incorrect Typo - (" + incorrect_typo_kana_id + "," + incorrect_typo_id + "," + incorrect_typo_value + ",)")

        ##----------------------------------------------------------------get_vocab_readings()----------------------------------------------------------------
                            
        def get_vocab_readings(vocab_id:str) -> typing.List[Reading]:

            readings = []

            with open(FileEnsurer.vocab_readings_path, "r", encoding="utf-8") as file:

                for line in file:

                    reading_vocab_id, reading_id, furigana, romaji = FileHandler.extract_seisen_line_values(line)

                    if(reading_vocab_id == vocab_id):

                        readings.append(reading_blueprint(int(reading_vocab_id), int(reading_id), furigana, romaji))

            return readings

        ##----------------------------------------------------------------get_vocab_synonym_values()----------------------------------------------------------------

        def get_vocab_synonym_values(vocab_id:str) -> typing.List[Synonym]:

            synonyms = []

            with open(FileEnsurer.vocab_synonyms_path, "r", encoding="utf-8") as file:

                for line in file:

                    synonym_vocab_id, synonym_id, synonym_value = FileHandler.extract_seisen_line_values(line)

                    if(synonym_vocab_id == vocab_id):

                        synonyms.append(synonym_blueprint(int(synonym_vocab_id), int(synonym_id), synonym_value))

            return synonyms
        
        ##----------------------------------------------------------------get_vocab_testing_material()----------------------------------------------------------------

        def get_vocab_testing_material(vocab_id:str) -> typing.List[TestingMaterial]:

            testing_material = []

            with open(FileEnsurer.vocab_testing_material_path, "r", encoding="utf-8") as file:

                for line in file:

                    testing_material_vocab_id, testing_material_id, testing_material_value = FileHandler.extract_seisen_line_values(line)

                    if(testing_material_vocab_id == vocab_id):
                            
                        testing_material.append(testing_material_blueprint(int(testing_material_vocab_id), int(testing_material_id), testing_material_value))


            return testing_material

        ##----------------------------------------------------------------load_vocab()----------------------------------------------------------------

        def load_vocab() -> None:


            with open(FileEnsurer.vocab_path, "r", encoding="utf-8") as file:

                for line in file:


                    vocab_id, correct_count, incorrect_count = FileHandler.extract_seisen_line_values(line)

                    readings = get_vocab_readings(vocab_id)
                    synonyms = get_vocab_synonym_values(vocab_id)
                    testing_material = get_vocab_testing_material(vocab_id)

                    LocalHandler.vocab.append(vocab_blueprint(int(vocab_id), testing_material, synonyms, readings, int(correct_count), int(incorrect_count)))

                    Logger.log_action("Loaded Vocab - (" + vocab_id + "," + correct_count + "," + incorrect_count + ") with the following readings - " + str([reading.furigana for reading in readings]) + " and the following synonyms - " + str([synonym.value for synonym in synonyms]) + " and the following testing material - " + str([testing_material.value for testing_material in testing_material]))

            with open(FileEnsurer.vocab_typos_path, "r", encoding="utf-8") as file:

                for line in file:
                    
                    typo_vocab_id, typo_id, typo_value = FileHandler.extract_seisen_line_values(line)

                    for vocab in LocalHandler.vocab:
                        if(vocab.id == int(typo_vocab_id)):

                            vocab.typos.append(typo_blueprint(int(typo_vocab_id), int(typo_id), typo_value))

                            Logger.log_action("Loaded Vocab Typo - (" + typo_vocab_id + "," + typo_id + "," + typo_value + ",)")

            with open(FileEnsurer.vocab_incorrect_typos_path, "r", encoding="utf-8") as file:

                for line in file:

                    incorrect_typo_vocab_id, incorrect_typo_id, incorrect_typo_value = FileHandler.extract_seisen_line_values(line)

                    for vocab in LocalHandler.vocab:
                        if(vocab.id == int(incorrect_typo_vocab_id)):

                            vocab.incorrect_typos.append(incorrect_typo_blueprint(int(incorrect_typo_vocab_id), int(incorrect_typo_id), incorrect_typo_value))

                            Logger.log_action("Loaded Vocab Incorrect Typo - (" + incorrect_typo_vocab_id + "," + incorrect_typo_id + "," + incorrect_typo_value + ",)")

        ##----------------------------------------------------------------functions----------------------------------------------------------------

        LocalHandler.kana.clear()
        LocalHandler.vocab.clear()

        Logger.log_barrier()
        Logger.log_action("Loading kana from local storage...")

        load_kana()

        Logger.log_barrier()
        Logger.log_action("Loading vocab from local storage...")

        load_vocab()

        Logger.log_barrier()

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

        ids = ["0"]

        i = 0

        TYPO_ID_INDEX_LOCATION = 2
        WORD_ID_INDEX_LOCATION = 1
        SYNONYM_ID_INDEX_LOCATION = 2
        READING_ID_INDEX_LOCATION = 2
        TESTING_MATERIAL_ID_INDEX_LOCATION = 2

        ## 1 = kana typo id
        if(type_of_id_to_query == "KANA TYPO ID"):
            with open(FileEnsurer.kana_typos_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_seisen_line(FileEnsurer.kana_typos_path, i+1, TYPO_ID_INDEX_LOCATION))
                    i+=1

        ## 2 = kana incorrect typo id
        elif(type_of_id_to_query == "KANA INCORRECT TYPO ID"):
            with open(FileEnsurer.kana_incorrect_typos_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_seisen_line(FileEnsurer.kana_incorrect_typos_path, i+1, TYPO_ID_INDEX_LOCATION))
                    i+=1

        ## 3 = vocab typo id
        elif(type_of_id_to_query == "VOCAB TYPO ID"):
            with open(FileEnsurer.vocab_typos_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_seisen_line(FileEnsurer.vocab_typos_path, i+1, TYPO_ID_INDEX_LOCATION))
                    i+=1

        ## 4 = vocab incorrect typo id
        elif(type_of_id_to_query == "VOCAB INCORRECT TYPO ID"):
            with open(FileEnsurer.vocab_incorrect_typos_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_seisen_line(FileEnsurer.vocab_incorrect_typos_path, i+1, TYPO_ID_INDEX_LOCATION))
                    i+=1

        ## 5 = kana id
        elif(type_of_id_to_query == "KANA ID"):
            with open(FileEnsurer.kana_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_seisen_line(FileEnsurer.kana_path, i+1, WORD_ID_INDEX_LOCATION))
                    i+=1
                    
        ## 6 = vocab id
        elif(type_of_id_to_query == "VOCAB ID"):
            with open(FileEnsurer.vocab_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_seisen_line(FileEnsurer.vocab_path, i+1, WORD_ID_INDEX_LOCATION))
                    i+=1

        ## 7 = kana synonym id
        elif(type_of_id_to_query == "KANA SYNONYM ID"):
            with open(FileEnsurer.kana_synonyms_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_seisen_line(FileEnsurer.kana_synonyms_path, i+1, SYNONYM_ID_INDEX_LOCATION))
                    i+=1

        ## 8 = vocab synonym id
        elif(type_of_id_to_query == "VOCAB SYNONYM ID"):
            with open(FileEnsurer.vocab_synonyms_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_seisen_line(FileEnsurer.vocab_synonyms_path, i+1, SYNONYM_ID_INDEX_LOCATION))
                    i+=1

        ## 9 = kana reading id
        elif(type_of_id_to_query == "KANA READING ID"):
            with open(FileEnsurer.kana_readings_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_seisen_line(FileEnsurer.kana_readings_path, i+1, READING_ID_INDEX_LOCATION))
                    i+=1

        ## 10 = vocab reading id
        elif(type_of_id_to_query == "VOCAB READING ID"):
            with open(FileEnsurer.vocab_readings_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_seisen_line(FileEnsurer.vocab_readings_path, i+1, READING_ID_INDEX_LOCATION))
                    i+=1

        ## 11 = kana testing material id
        elif(type_of_id_to_query == "KANA TESTING MATERIAL ID"):
            with open(FileEnsurer.kana_testing_material_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_seisen_line(FileEnsurer.kana_testing_material_path, i+1, TESTING_MATERIAL_ID_INDEX_LOCATION))
                    i+=1

        ## 12 = vocab testing material id
        elif(type_of_id_to_query == "VOCAB TESTING MATERIAL ID"):
            with open(FileEnsurer.vocab_testing_material_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_seisen_line(FileEnsurer.vocab_testing_material_path, i+1, TESTING_MATERIAL_ID_INDEX_LOCATION))
                    i+=1

        ids =  [int(x) for x in ids]

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

        else:
            pass

##--------------------start-of-restore_local_backup()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def restore_local_backup():

        """
        
        Prompts the user to restart a local backup and does so if valid.

        """

        valid_backups = []

        backup_to_restore_prompt = ""
        
        Toolkit.clear_console()
        
        print("Please select a backup to restore:\n")
        
        for dir in os.listdir(FileEnsurer.local_archives_dir):
        
            full_path = os.path.join(FileEnsurer.local_archives_dir, dir)
        
            if(os.path.isdir(full_path)):
                print(dir)
                valid_backups.append(dir)
                backup_to_restore_prompt += dir + "\n"
        
        backup_to_restore_prompt += "\nPlease select a backup to restore, please keep in mind that this process is not easily reversible."

        if(len(valid_backups) == 0):
            print("No backups found.\n")
            time.sleep(Toolkit.sleep_constant)
            return

        try: ## user confirm will throw an assertion error or a user cancel error if the user cancels.

            backup_to_restore = Toolkit.user_confirm(backup_to_restore_prompt)

            if(backup_to_restore in valid_backups):
                Toolkit.clear_console()

                shutil.rmtree(FileEnsurer.kana_dir)
                shutil.rmtree(FileEnsurer.vocab_dir)

                shutil.copytree(os.path.join(FileEnsurer.local_archives_dir, backup_to_restore), FileEnsurer.config_dir, dirs_exist_ok=True)

                Logger.log_action("Restored the " + backup_to_restore + " local backup.", output=True, omit_timestamp=True)

                LocalHandler.load_words_from_local_storage()

            else:
                print("Invalid Backup.\n")

        except Toolkit.UserCancelError or AssertionError:
            print("\nCancelled.\n")
