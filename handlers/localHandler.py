## built-in modules
from __future__ import annotations ## used for cheating the circular import issue that occurs when i need to type check some things
from datetime import datetime

import os
import typing
import shutil
import time

## custom modules
from entities.typos import typo as typo_blueprint
from entities.typos import incorrectTypo as incorrect_typo_blueprint

from entities.words import word as kana_blueprint
from entities.vocab import vocab as vocab_blueprint

from entities.csep import csep as csep_blueprint

from modules.toolkit import Toolkit
from modules.logger import Logger
from modules.file_ensurer import FileEnsurer

from handlers.fileHandler import FileHandler

if(typing.TYPE_CHECKING): ## used for cheating the circular import issue that occurs when i need to type check some things
    from entities.csep import csep
    from entities.vocab import vocab
    from entities.words import word as kana

class LocalHandler():

    """
    
    The handler that handles the connection to local storage and all interactions with it.\n

    """

    ## the literal used in the database to flag words as Kana
    KANA_WORD_TYPE = "2"

    ## the literal used in the database to flag words as Kana
    VOCAB_WORD_TYPE = "3"

    kana: typing.List[kana] = [] 

    vocab: typing.List[vocab] = []

##--------------------start-of-load_words_local_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def load_words_from_local_storage() -> None:
        
        """
        
        Loads the words from the local storage.

        """

        ##----------------------------------------------------------------get_kana_csep_values()----------------------------------------------------------------

        def get_kana_csep_values(kana_id:str) -> typing.List[csep]:

            csep_values = []

            with open(FileEnsurer.kana_csep_actual_path, "r", encoding="utf-8") as file:

                for line in file:

                    values = line.strip().split(',')

                    if(values[0] == kana_id):
                        csep_values.append(csep_blueprint(int(values[0]), int(values[1]), values[2], values[3]))

            return csep_values

        ##----------------------------------------------------------------load_kana()----------------------------------------------------------------

        def load_kana() -> None:
    
            with open(FileEnsurer.kana_actual_path, "r", encoding="utf-8") as file:

                for line in file:

                    values = line.strip().split(',')

                    csep_values = get_kana_csep_values(values[0])

                    LocalHandler.kana.append(kana_blueprint(int(values[0]), values[1], values[2], csep_values, int(values[3]), int(values[4])))

                    Logger.log_action("Loaded Kana - (" + values[0] + "," + values[1] + "," + values[2] + "," + values[3] + "," + values[4] + ",)")

            with open(FileEnsurer.kana_typos_path, "r", encoding="utf-8") as file:

                for line in file:
                    
                    values = line.strip().split(',')

                    if(values[3] == LocalHandler.KANA_WORD_TYPE):
                        for kana in LocalHandler.kana:
                            if(kana.word_id == int(values[0])):
                                kana.typos.append(typo_blueprint(int(values[0]), int(values[1]), values[2], values[3]))

                                Logger.log_action("Loaded Kana Typo - (" + values[0] + "," + values[1] + "," + values[2] + "," + values[3] + ",)")
            
            with open(FileEnsurer.kana_incorrect_typos_path, "r", encoding="utf-8") as file:

                for line in file:

                    values = line.strip().split(',')

                    if(values[3] == LocalHandler.KANA_WORD_TYPE):
                        for kana in LocalHandler.kana:
                            if(kana.word_id == int(values[0])):
                                kana.incorrect_typos.append(incorrect_typo_blueprint(int(values[0]), int(values[1]), values[2], values[3]))

                                Logger.log_action("Loaded Kana Incorrect Typo - (" + values[0] + "," + values[1] + "," + values[2] + "," + values[3] + ",)")

        ##----------------------------------------------------------------get_vocab_csep_values()----------------------------------------------------------------

        def get_vocab_csep_values(vocab_id:str) -> typing.List[csep]:

            csep_values = []

            with open(FileEnsurer.vocab_csep_actual_path, "r", encoding="utf-8") as file:

                for line in file:

                    values = line.strip().split(',')

                    if(values[0] == vocab_id):
                        csep_values.append(csep_blueprint(int(values[0]), int(values[1]), values[2], values[3]))

            return csep_values

        ##----------------------------------------------------------------load_vocab()----------------------------------------------------------------

        def load_vocab() -> None:


            with open(FileEnsurer.vocab_actual_path, "r", encoding="utf-8") as file:

                for line in file:

                    values = line.strip().split(',')

                    if(values[4]  == "0"):
                        kanji_flag = False
                    else:
                        kanji_flag = True

                    csep_values = get_vocab_csep_values(values[0])

                    LocalHandler.vocab.append(vocab_blueprint(int(values[0]), values[1], values[2], values[3], csep_values, values[4], int(values[5]), int(values[6]), kanji_flag))

                    csep_log_value = [csep.csep_value for csep in csep_values]

                    Logger.log_action("Loaded vocab - (" + values[0] + "," + values[1] + values[2] + "," + values[3] + ","  + values[4] + "," + values[5] + "," + str(kanji_flag) + "," + ") with the following cseps - " + str(csep_log_value))

            with open(FileEnsurer.vocab_typos_path, "r", encoding="utf-8") as file:

                for line in file:
                    
                    values = line.strip().split(',')

                    if(values[3] == LocalHandler.VOCAB_WORD_TYPE):
                        for vocab in LocalHandler.vocab:
                            if(vocab.word_id == int(values[0])):
                                vocab.typos.append(typo_blueprint(int(values[0]), int(values[1]), values[2], values[3]))

                                Logger.log_action("Loaded Vocab Typo - (" + values[0] + "," + values[1] + "," + values[2] + "," + values[3] + ",)")

            with open(FileEnsurer.vocab_incorrect_typos_path, "r", encoding="utf-8") as file:

                for line in file:

                    values = line.strip().split(',')

                    if(values[3] == LocalHandler.VOCAB_WORD_TYPE):
                        for vocab in LocalHandler.vocab:
                            if(vocab.word_id == int(values[0])):
                                vocab.incorrect_typos.append(incorrect_typo_blueprint(int(values[0]), int(values[1]), values[2], values[3]))

                                Logger.log_action("Loaded Vocab Incorrect Typo - (" + values[0] + "," + values[1] + "," + values[2] + "," + values[3] + ",)")

        ##----------------------------------------------------------------functions----------------------------------------------------------------

        LocalHandler.kana.clear()
        LocalHandler.vocab.clear()

        Logger.log_action("--------------------------------------------------------------")
        Logger.log_action("Loading kana from local storage...")

        load_kana()

        Logger.log_action("--------------------------------------------------------------")
        Logger.log_action("Loading vocab from local storage...")

        load_vocab()

        Logger.log_action("--------------------------------------------------------------")

##--------------------start-of-get_list_of_all_ids()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_list_of_all_ids(type_of_id_to_query:int) -> typing.List[int]:

        """

        Gets the list of all ids in local storage given the type of id to query.

        Parameters:
        type_of_id_to_query (int) : The type of id to query.

        Returns:
        ids (list - string) : The list of all ids in the database.

        ------------------------------

        KANA TYPO ID = 1

        KANA INCORRECT TYPO ID = 2

        VOCAB TYPO ID = 3

        VOCAB INCORRECT TYPO ID = 4

        VOCAB ID = 5

        CSEP ID = 6

        """

        ids = ["0"]

        i = 0

        KANA_TYPO_ID_IDENTIFIER = 1
        KANA_INCORRECT_TYPO_ID_IDENTIFIER = 2
        VOCAB_TYPO_ID_IDENTIFIER = 3
        VOCAB_INCORRECT_TYPO_ID_IDENTIFIER = 4
        VOCAB_ID_IDENTIFIER = 5
        CSEP_ID_IDENTIFIER = 6

        TYPO_ID_INDEX_LOCATION = 2
        VOCAB_ID_INDEX_LOCATION = 1
        CSEP_ID_INDEX_LOCATION = 2

        if(type_of_id_to_query == KANA_TYPO_ID_IDENTIFIER):
            with open(FileEnsurer.kana_typos_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_sei_file(FileEnsurer.kana_typos_path, i+1, TYPO_ID_INDEX_LOCATION))
                    i+=1

        elif(type_of_id_to_query == KANA_INCORRECT_TYPO_ID_IDENTIFIER):
            with open(FileEnsurer.kana_incorrect_typos_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_sei_file(FileEnsurer.kana_incorrect_typos_path, i+1, TYPO_ID_INDEX_LOCATION))
                    i+=1

        elif(type_of_id_to_query == VOCAB_TYPO_ID_IDENTIFIER):
            with open(FileEnsurer.vocab_typos_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_sei_file(FileEnsurer.vocab_typos_path, i+1, TYPO_ID_INDEX_LOCATION))
                    i+=1

        elif(type_of_id_to_query == VOCAB_INCORRECT_TYPO_ID_IDENTIFIER):
            with open(FileEnsurer.vocab_incorrect_typos_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_sei_file(FileEnsurer.vocab_incorrect_typos_path, i+1, TYPO_ID_INDEX_LOCATION))
                    i+=1
                    

        elif(type_of_id_to_query == VOCAB_ID_IDENTIFIER):
            with open(FileEnsurer.vocab_actual_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_sei_file(FileEnsurer.vocab_actual_path, i+1, VOCAB_ID_INDEX_LOCATION))
                    i+=1

        elif(type_of_id_to_query == CSEP_ID_IDENTIFIER):
            with open(FileEnsurer.vocab_csep_actual_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(FileHandler.read_sei_file(FileEnsurer.vocab_csep_actual_path, i+1, CSEP_ID_INDEX_LOCATION))
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
                
                archive_dir = FileHandler.create_archive_dir(2)

                Logger.log_action("Created Daily Local Backup")

                shutil.copytree(FileEnsurer.kana_dir, os.path.join(archive_dir, "kana"))
                shutil.copytree(FileEnsurer.vocab_dir, os.path.join(archive_dir, "vocab"))

                file.truncate(0)
                
                file.write(current_day.strip('\x00').strip())
            
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
        
        for item in os.listdir(FileEnsurer.local_archives_dir):
        
            full_path = os.path.join(FileEnsurer.local_archives_dir, item)
        
            if(os.path.isdir(full_path)):
                print(item)
                valid_backups.append(item)
                backup_to_restore_prompt += item + "\n"
        
        backup_to_restore_prompt += "\nPlease select a backup to restore, please keep in mind that this process is not easily reversible."

        try: ## user confirm will throw an assertion error or a user cancel error if the user cancels.

            backup_to_restore = Toolkit.user_confirm(backup_to_restore_prompt)

            if(backup_to_restore in valid_backups):
                Toolkit.clear_console()

                shutil.rmtree(FileEnsurer.kana_dir)
                shutil.rmtree(FileEnsurer.vocab_dir)

                Logger.log_action("Restored the " + backup_to_restore + " local backup")

                shutil.copytree(os.path.join(FileEnsurer.local_archives_dir, backup_to_restore), FileEnsurer.config_dir, dirs_exist_ok=True)

                LocalHandler.load_words_from_local_storage()

            else:
                print("Invalid Backup\n")
                time.sleep(1)

        except Toolkit.UserCancelError or AssertionError:
            pass
