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

from entities.synonym import Synonym as synonym_blueprint

from modules.toolkit import Toolkit
from modules.logger import Logger
from modules.file_ensurer import FileEnsurer

from handlers.file_handler import FileHandler

if(typing.TYPE_CHECKING): ## Used for cheating the circular import issue that occurs when I need to type check some things
    from entities.synonym import Synonym
    from entities.vocab import Vocab
    from entities.word import Word as Kana

class LocalHandler():

    """
    
    The LocalHandler class is used to handle all local storage related actions.

    """

    KANA_WORD_TYPE = "kana"

    VOCAB_WORD_TYPE = "vocab"

    kana: typing.List[Kana] = [] 

    vocab: typing.List[Vocab] = []

##--------------------start-of-load_words_local_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def load_words_from_local_storage() -> None:
        
        """
        
        Loads all words from local storage into the program.

        """

        ##----------------------------------------------------------------get_kana_synonyms()----------------------------------------------------------------

        def get_kana_synonyms(kana_id:str) -> typing.List[Synonym]:

            synonyms = []

            with open(FileEnsurer.kana_synonyms_path, "r", encoding="utf-8") as file:

                for line in file:

                    synonym_kana_id, synonym_id, synonym_value, synonym_word_type, _ = line.strip().split(',')
                    
                    if(synonym_kana_id == kana_id):

                        synonym_value = synonym_value.replace('*', ',')        ## Reversing comma to asterisk replacement
                        synonym_value = synonym_value.replace("\\'", "'")      ## Reversing escaping of single quotes
                        synonym_value = synonym_value.replace('\\\\', '\\')    ## Reversing double backslash to single backslash replacement

                        synonyms.append(synonym_blueprint(int(synonym_kana_id), int(synonym_id), synonym_value, synonym_word_type))

            return synonyms

        ##----------------------------------------------------------------load_kana()----------------------------------------------------------------

        def load_kana() -> None:
    
            with open(FileEnsurer.kana_path, "r", encoding="utf-8") as file:

                for line in file:

                    kana_id, testing_material, testing_material_answer_main, incorrect_count, correct_count, _ = line.strip().split(',')

                    synonyms = get_kana_synonyms(kana_id)

                    LocalHandler.kana.append(kana_blueprint(int(kana_id), testing_material, testing_material_answer_main, synonyms, int(incorrect_count), int(correct_count)))

                    Logger.log_action("Loaded Kana - (" + kana_id + "," + testing_material + "," + testing_material_answer_main + "," + incorrect_count + "," + correct_count + ") with the following synonyms - " + str([synonym.synonym_value for synonym in synonyms]))

            with open(FileEnsurer.kana_typos_path, "r", encoding="utf-8") as file:

                for line in file:
                    
                    typo_kana_id, typo_id, typo_value, typo_word_type, _ = line.strip().split(',')

                    if(typo_word_type == LocalHandler.KANA_WORD_TYPE):
                        for kana in LocalHandler.kana:
                            if(kana.word_id == int(typo_kana_id)):

                                typo_value = typo_value.replace('*', ',')        ## Reversing comma to asterisk replacement
                                typo_value = typo_value.replace("\\'", "'")      ## Reversing escaping of single quotes
                                typo_value = typo_value.replace('\\\\', '\\')    ## Reversing double backslash to single backslash replacement


                                kana.typos.append(typo_blueprint(int(typo_kana_id), int(typo_id), typo_value, typo_word_type))

                                Logger.log_action("Loaded Kana Typo - (" + typo_kana_id + "," + typo_id + "," + typo_value + "," + typo_word_type + ")")
            
            with open(FileEnsurer.kana_incorrect_typos_path, "r", encoding="utf-8") as file:

                for line in file:
    
                    incorrect_typo_kana_id, incorrect_typo_id, incorrect_typo_value, incorrect_typo_word_type, _ = line.strip().split(',')

                    if(incorrect_typo_word_type == LocalHandler.KANA_WORD_TYPE):
                        for kana in LocalHandler.kana:
                            if(kana.word_id == int(incorrect_typo_kana_id)):

                                incorrect_typo_value = incorrect_typo_value.replace('*', ',')        ## Reversing comma to asterisk replacement
                                incorrect_typo_value = incorrect_typo_value.replace("\\'", "'")      ## Reversing escaping of single quotes
                                incorrect_typo_value = incorrect_typo_value.replace('\\\\', '\\')    ## Reversing double backslash to single backslash replacement

                                kana.incorrect_typos.append(incorrect_typo_blueprint(int(incorrect_typo_kana_id), int(incorrect_typo_id), incorrect_typo_value, incorrect_typo_word_type))

                                Logger.log_action("Loaded Kana Incorrect Typo - (" + incorrect_typo_kana_id + "," + incorrect_typo_id + "," + incorrect_typo_value + "," + incorrect_typo_word_type + ")")

        ##----------------------------------------------------------------get_vocab_synonym_values()----------------------------------------------------------------

        def get_vocab_synonym_values(vocab_id:str) -> typing.List[Synonym]:

            synonyms = []

            with open(FileEnsurer.vocab_synonyms_path, "r", encoding="utf-8") as file:

                for line in file:

                    synonym_vocab_id, synonym_id, synonym_value, synonym_word_type, _ = line.strip().split(',')

                    if(synonym_vocab_id == vocab_id):

                        synonym_value = synonym_value.replace('*', ',')        ## Reversing comma to asterisk replacement
                        synonym_value = synonym_value.replace("\\'", "'")      ## Reversing escaping of single quotes
                        synonym_value = synonym_value.replace('\\\\', '\\')    ## Reversing double backslash to single backslash replacement

                        synonyms.append(synonym_blueprint(int(synonym_vocab_id), int(synonym_id), synonym_value, synonym_word_type))

            return synonyms

        ##----------------------------------------------------------------load_vocab()----------------------------------------------------------------

        def load_vocab() -> None:


            with open(FileEnsurer.vocab_path, "r", encoding="utf-8") as file:

                for line in file:

                    vocab_id, testing_material, romaji, testing_material_answer_main, furigana, incorrect_count, correct_count, _ = line.strip().split(',')

                    if(furigana == "0"):
                        kanji_flag = False
                    else:
                        kanji_flag = True

                    synonyms = get_vocab_synonym_values(vocab_id)

                    testing_material_answer_main = testing_material_answer_main.replace('*', ',')        ## Reversing comma to asterisk replacement
                    testing_material_answer_main = testing_material_answer_main.replace("\\'", "'")      ## Reversing escaping of single quotes
                    testing_material_answer_main = testing_material_answer_main.replace('\\\\', '\\')    ## Reversing double backslash to single backslash replacement

                    LocalHandler.vocab.append(vocab_blueprint(int(vocab_id), testing_material, romaji, testing_material_answer_main, synonyms, furigana, int(incorrect_count), int(correct_count), kanji_flag))

                    Logger.log_action("Loaded Vocab - (" + vocab_id + "," + testing_material + "," + romaji + "," + testing_material_answer_main + "," + furigana + "," + incorrect_count + "," + correct_count + "," + str(kanji_flag) + ") with the following synonyms - " + str([synonym.synonym_value for synonym in synonyms]))

            with open(FileEnsurer.vocab_typos_path, "r", encoding="utf-8") as file:

                for line in file:
                    
                    typo_vocab_id, typo_id, typo_value, typo_word_type, _ = line.strip().split(',')

                    if(typo_word_type == LocalHandler.VOCAB_WORD_TYPE):
                        for vocab in LocalHandler.vocab:
                            if(vocab.word_id == int(typo_vocab_id)):

                                typo_value = typo_value.replace('*', ',')        ## Reversing comma to asterisk replacement
                                typo_value = typo_value.replace("\\'", "'")      ## Reversing escaping of single quotes
                                typo_value = typo_value.replace('\\\\', '\\')    ## Reversing double backslash to single backslash replacement

                                vocab.typos.append(typo_blueprint(int(typo_vocab_id), int(typo_id), typo_value, typo_word_type))

                                Logger.log_action("Loaded Vocab Typo - (" + typo_vocab_id + "," + typo_id + "," + typo_value + "," + typo_word_type + ")")

            with open(FileEnsurer.vocab_incorrect_typos_path, "r", encoding="utf-8") as file:

                for line in file:

                    incorrect_typo_vocab_id, incorrect_typo_id, incorrect_typo_value, incorrect_typo_word_type, _ = line.strip().split(',')

                    if(incorrect_typo_word_type == LocalHandler.VOCAB_WORD_TYPE):
                        for vocab in LocalHandler.vocab:
                            if(vocab.word_id == int(incorrect_typo_vocab_id)):

                                incorrect_typo_value = incorrect_typo_value.replace('*', ',')        # Reversing comma to asterisk replacement
                                incorrect_typo_value = incorrect_typo_value.replace("\\'", "'")      # Reversing escaping of single quotes
                                incorrect_typo_value = incorrect_typo_value.replace('\\\\', '\\')    # Reversing double backslash to single backslash replacement

                                vocab.incorrect_typos.append(incorrect_typo_blueprint(int(incorrect_typo_vocab_id), int(incorrect_typo_id), incorrect_typo_value, incorrect_typo_word_type))

                                Logger.log_action("Loaded Vocab Incorrect Typo - (" + incorrect_typo_vocab_id + "," + incorrect_typo_id + "," + incorrect_typo_value + "," + incorrect_typo_word_type + ")")

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
    def get_list_of_all_ids(type_of_id_to_query:int) -> typing.List[int]:

        """

        Gets the list of all ids in local storage given the type of id to query.

        Parameters:
        type_of_id_to_query (int) : The type of id to query.

        Returns:
        ids (list - int) : The list of all ids in the database.

        ------------------------------

        KANA TYPO ID = 1

        KANA INCORRECT TYPO ID = 2

        VOCAB TYPO ID = 3

        VOCAB INCORRECT TYPO ID = 4

        KANA ID = 5

        VOCAB ID = 6

        KANA SYNONYM ID = 7
        
        VOCAB SYNONYM ID = 8

        """

        ids = ["0"]

        i = 0

        KANA_TYPO_ID_IDENTIFIER = 1
        KANA_INCORRECT_TYPO_ID_IDENTIFIER = 2
        VOCAB_TYPO_ID_IDENTIFIER = 3
        VOCAB_INCORRECT_TYPO_ID_IDENTIFIER = 4
        KANA_ID_IDENTIFIER = 5
        VOCAB_ID_IDENTIFIER = 6
        KANA_SYNONYM_ID_IDENTIFIER = 7
        VOCAB_SYNONYM_ID_IDENTIFIER = 8

        TYPO_ID_INDEX_LOCATION = 2
        WORD_ID_INDEX_LOCATION = 1
        SYNONYM_ID_INDEX_LOCATION = 2

        ## 1 = kana typo id
        if(type_of_id_to_query == KANA_TYPO_ID_IDENTIFIER):
            with open(FileEnsurer.kana_typos_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_seisen_line(FileEnsurer.kana_typos_path, i+1, TYPO_ID_INDEX_LOCATION))
                    i+=1

        ## 2 = kana incorrect typo id
        elif(type_of_id_to_query == KANA_INCORRECT_TYPO_ID_IDENTIFIER):
            with open(FileEnsurer.kana_incorrect_typos_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_seisen_line(FileEnsurer.kana_incorrect_typos_path, i+1, TYPO_ID_INDEX_LOCATION))
                    i+=1

        ## 3 = vocab typo id
        elif(type_of_id_to_query == VOCAB_TYPO_ID_IDENTIFIER):
            with open(FileEnsurer.vocab_typos_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_seisen_line(FileEnsurer.vocab_typos_path, i+1, TYPO_ID_INDEX_LOCATION))
                    i+=1

        ## 4 = vocab incorrect typo id
        elif(type_of_id_to_query == VOCAB_INCORRECT_TYPO_ID_IDENTIFIER):
            with open(FileEnsurer.vocab_incorrect_typos_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_seisen_line(FileEnsurer.vocab_incorrect_typos_path, i+1, TYPO_ID_INDEX_LOCATION))
                    i+=1

        ## 5 = kana id
        elif(type_of_id_to_query == KANA_ID_IDENTIFIER):
            with open(FileEnsurer.kana_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_seisen_line(FileEnsurer.kana_path, i+1, WORD_ID_INDEX_LOCATION))
                    i+=1
                    
        ## 6 = vocab id
        elif(type_of_id_to_query == VOCAB_ID_IDENTIFIER):
            with open(FileEnsurer.vocab_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_seisen_line(FileEnsurer.vocab_path, i+1, WORD_ID_INDEX_LOCATION))
                    i+=1

        ## 7 = kana synonym id
        elif(type_of_id_to_query == KANA_SYNONYM_ID_IDENTIFIER):
            with open(FileEnsurer.kana_synonyms_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_seisen_line(FileEnsurer.kana_synonyms_path, i+1, SYNONYM_ID_INDEX_LOCATION))
                    i+=1

        ## 8 = vocab synonym id
        elif(type_of_id_to_query == VOCAB_SYNONYM_ID_IDENTIFIER):
            with open(FileEnsurer.vocab_synonyms_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_seisen_line(FileEnsurer.vocab_synonyms_path, i+1, SYNONYM_ID_INDEX_LOCATION))
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

            last_backup_date = str(file.read().strip())
            last_backup_date = last_backup_date.strip('\x00')
        
            current_day = str(datetime.today().strftime('%Y-%m-%d').strip())

            if(last_backup_date != current_day):
                
                archive_dir = FileEnsurer.create_archive_dir(2)

                Logger.log_action("Created Daily Local Backup.")

                shutil.copytree(FileEnsurer.kana_dir, os.path.join(archive_dir, "kana"))
                shutil.copytree(FileEnsurer.vocab_dir, os.path.join(archive_dir, "vocab"))

                file.truncate(0)
                
                file.write(current_day.strip('\x00').strip(" ").strip())
            
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
            print("No backups found.")
            time.sleep(1)
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
            print("Cancelled.\n")
