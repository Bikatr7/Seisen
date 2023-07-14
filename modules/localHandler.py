## built-in modules
from datetime import datetime

import os
import typing
import shutil
import time

## custom modules
from modules.typos import typo as typo_blueprint
from modules.typos import incorrectTypo as incorrect_typo_blueprint

from modules.words import word as kana_blueprint
from modules.vocab import vocab as vocab_blueprint

from modules import util
from modules.ensureFileSecurity import fileEnsurer

class localHandler():

    """
    
    The handler that handles the connection to local storage and all interactions with it.\n

    """

##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, file_ensurer:fileEnsurer) -> None:

        """
        
        Initializes the localHandler class.\n

        Parameters:\n
        self (object - localHandler) : The handler object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------objects----------------------------------------------------------------

        ## the file_ensurer used for paths here
        self.fileEnsurer = file_ensurer

        ##----------------------------------------------------------------dirs----------------------------------------------------------------

        ## archives for previous versions of Seisen txt files
        self.archives_dir = os.path.join(self.fileEnsurer.config_dir, "Archives")

        ## archives for the local files
        self.local_archives_dir = os.path.join(self.archives_dir, "Local")

        ##----------------------------------------------------------------paths----------------------------------------------------------------

        ## the path to the file that stores the password
        self.password_path = os.path.join(os.path.join(self.fileEnsurer.config_dir, "Logins"), "credentials.txt")

        ## the paths for all kana related files
        self.kana_path = os.path.join(self.fileEnsurer.kana_dir, "kana.txt")
        self.kana_typos_path = os.path.join(self.fileEnsurer.kana_dir, "kana typos.txt")
        self.kana_incorrect_typos_path = os.path.join(self.fileEnsurer.kana_dir, "kana incorrect typos.txt")

        ## the paths for all vocab related files
        self.vocab_path = os.path.join(self.fileEnsurer.vocab_dir, "vocab.txt")
        self.vocab_csep_path = os.path.join(self.fileEnsurer.vocab_dir, "vocab csep.txt")
        self.vocab_typos_path = os.path.join(self.fileEnsurer.vocab_dir, "vocab typos.txt")
        self.vocab_incorrect_typos_path = os.path.join(self.fileEnsurer.vocab_dir, "vocab incorrect typos.txt")

        ## contains the date of the last local backup
        self.last_local_backup_path = os.path.join(self.local_archives_dir, "last_local_backup.txt")

        ##----------------------------------------------------------------variables----------------------------------------------------------------

        ## the literal used in the database to flag words as Kana
        self.KANA_WORD_TYPE = "2"

        ## the literal used in the database to flag words as Kana
        self.VOCAB_WORD_TYPE = "3"

        ## the kana that seisen will use to test the user
        self.kana = [] 

        ## the vocab that will be used to test the user
        self.vocab = []
        
##--------------------start-of-load_words_local_storage()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def load_words_from_local_storage(self) -> None:
        
        """
        
        loads the words from the local storage.\n

        Parameters:\n
        self (object - localHandler) : The handler object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------load_kana()----------------------------------------------------------------

        def load_kana():
    
            with open(self.kana_path, "r", encoding="utf-8") as file:

                for line in file:

                    values = line.strip().split(',')

                    self.kana.append(kana_blueprint(int(values[0]), values[1], values[2], [], int(values[3]), int(values[4])))

            with open(self.kana_typos_path, "r", encoding="utf-8") as file:

                for line in file:
                    
                    values = line.strip().split(',')

                    if(values[3] == self.KANA_WORD_TYPE):
                        for kana in self.kana:
                            if(kana.word_id == int(values[0])):
                                kana.typos.append(typo_blueprint(int(values[0]), int(values[1]), values[2], values[3]))
            
            with open(self.kana_incorrect_typos_path, "r", encoding="utf-8") as file:

                for line in file:

                    values = line.strip().split(',')

                    if(values[3] == self.KANA_WORD_TYPE):
                        for kana in self.kana:
                            if(kana.word_id == int(values[0])):
                                kana.incorrect_typos.append(incorrect_typo_blueprint(int(values[0]), int(values[1]), values[2], values[3]))

        ##----------------------------------------------------------------get_csep_values()----------------------------------------------------------------

        def get_csep_values(vocab_id:str) -> typing.List[str]:

            csep_values = []

            with open(self.vocab_csep_path, "r", encoding="utf-8") as file:

                for line in file:

                    values = line.strip().split(',')

                    if(values[0] == vocab_id):
                        csep_values.append(values[2])

            return csep_values

        ##----------------------------------------------------------------load_vocab()----------------------------------------------------------------

        def load_vocab():


            with open(self.vocab_path, "r", encoding="utf-8") as file:

                for line in file:

                    values = line.strip().split(',')

                    if(values[4]  == "0"):
                        kanji_flag = False
                    else:
                        kanji_flag = True

                    csep_values = get_csep_values(values[0])

                    print(csep_values)

                    util.pause_console()

                    self.vocab.append(vocab_blueprint(int(values[0]), values[1], values[2], values[3], csep_values, values[4], int(values[5]), int(values[6]), kanji_flag))

            with open(self.vocab_typos_path, "r", encoding="utf-8") as file:

                for line in file:
                    
                    values = line.strip().split(',')

                    if(values[3] == self.VOCAB_WORD_TYPE):
                        for vocab in self.vocab:
                            if(vocab.word_id == int(values[0])):
                                vocab.typos.append(typo_blueprint(int(values[0]), int(values[1]), values[2], values[3]))

            with open(self.vocab_incorrect_typos_path, "r", encoding="utf-8") as file:

                for line in file:

                    values = line.strip().split(',')

                    if(values[3] == self.VOCAB_WORD_TYPE):
                        for vocab in self.vocab:
                            if(vocab.word_id == int(values[0])):
                                vocab.incorrect_typos.append(incorrect_typo_blueprint(int(values[0]), int(values[1]), values[2], values[3]))

        ##----------------------------------------------------------------functions----------------------------------------------------------------

        self.kana.clear()
        self.vocab.clear()

        load_kana()
        load_vocab()

##--------------------start-of-get_list_of_all_ids()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def get_list_of_all_ids(self, type_of_id_to_query:int) -> typing.List[int]:

        """

        Gets the list of all ids in local storage.\n

        Parameters:\n
        self (object - localHandler) : The handler object.\n

        Returns:\n
        ids (list - string) : The list of all ids in the database.\n

        ------------------------------

        KANA TYPO ID = 1\n
        KANA INCORRECT TYPO ID = 2\n
        VOCAB TYPO ID = 3\n
        VOCAB INCORRECT TYPO ID = 4\n
        VOCAB ID = 5\n
        CSEP ID = 6\n

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
        CSEP_ID_INDEX_LOCATION = 1

        if(type_of_id_to_query == KANA_TYPO_ID_IDENTIFIER):
            with open(self.kana_typos_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(util.read_sei_file(self.kana_typos_path, i+1, TYPO_ID_INDEX_LOCATION))
                    i+=1

        elif(type_of_id_to_query == KANA_INCORRECT_TYPO_ID_IDENTIFIER):
            with open(self.kana_incorrect_typos_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(util.read_sei_file(self.kana_incorrect_typos_path,i+1, TYPO_ID_INDEX_LOCATION))
                    i+=1

        elif(type_of_id_to_query == VOCAB_TYPO_ID_IDENTIFIER):
            with open(self.vocab_typos_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(util.read_sei_file(self.vocab_typos_path,i+1, TYPO_ID_INDEX_LOCATION))
                    i+=1

        elif(type_of_id_to_query == VOCAB_INCORRECT_TYPO_ID_IDENTIFIER):
            with open(self.vocab_incorrect_typos_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(util.read_sei_file(self.vocab_incorrect_typos_path,i+1, TYPO_ID_INDEX_LOCATION))
                    i+=1
                    

        elif(type_of_id_to_query == VOCAB_ID_IDENTIFIER):
            with open(self.vocab_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(util.read_sei_file(self.vocab_path, i+1, VOCAB_ID_INDEX_LOCATION))
                    i+=1

        elif(type_of_id_to_query == CSEP_ID_IDENTIFIER):
            with open(self.vocab_csep_path, 'r', encoding='utf-8') as file:
                file_size = file.readlines()

                while(i < len(file_size)):
                    ids.append(util.read_sei_file(self.vocab_path, i+1, CSEP_ID_INDEX_LOCATION))
                    i+=1

        ids =  [int(x) for x in ids]

        return ids
    
##--------------------start-of-create_daily_local_backup()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def create_daily_local_backup(self) -> None:

        """
        
        Creates Seisen's daily local backup.\n

        Parameters:\n
        self (object - localHandler) : the local handler.\n
W
        Returns:\n
        None.\n

        """

        with open(self.last_local_backup_path, 'r+', encoding="utf-8") as file:

            last_backup_date = str(file.read().strip())
            last_backup_date = last_backup_date.strip('\x00')
        
            current_day = str(datetime.today().strftime('%Y-%m-%d'))

            if(last_backup_date != current_day):
                
                archive_dir = util.create_archive_dir(2)

                shutil.copytree(self.fileEnsurer.kana_dir, os.path.join(archive_dir, "Kana"))
                shutil.copytree(self.fileEnsurer.vocab_dir, os.path.join(archive_dir, "Vocab"))

                file.truncate(0)
                
                file.write(current_day.strip())
            
            else:
                pass


##--------------------start-of-restore_local_backup()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def restore_local_backup(self):

        """
        
        Prompts the user to restart a local backup and does so if valid.\n

        Parameters:\n
        self (localHandler - object) : the local handler object.\n

        Returns:\n
        None.\n

        """

        valid_backups = []

        backup_to_restore_prompt = ""
        
        util.clear_console()
        
        print("Please select a backup to restore:\n")
        
        for item in os.listdir(self.local_archives_dir):
        
            full_path = os.path.join(self.local_archives_dir, item)
        
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

                shutil.copytree(os.path.join(self.local_archives_dir, backup_to_restore), self.fileEnsurer.config_dir, dirs_exist_ok=True)

                self.load_words_from_local_storage()

            else:
                print("Invalid Backup\n")
                time.sleep(1)

        except AssertionError:
            pass
