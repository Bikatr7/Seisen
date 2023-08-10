## built-in modules
from datetime import datetime

import msvcrt
import os
import shutil
import time

## custom modules
from modules.localHandler import localHandler
from modules.remoteHandler import remoteHandler

class storageSettingsHandler():

    """
    
    The handler that handles all of Seisen's vocab settings
    
    """
##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, local_handler:localHandler, remote_handler:remoteHandler) -> None:

        """
        
        Initializes the storageSettingsHandler class.\n

        Parameters:\n
        local_handler (object - localHandler) : The local handler object.\n
        remote_handler (object - remoteHandler) : The remote handler object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------objects----------------------------------------------------------------

        self.local_handler = local_handler

        self.remote_handler = remote_handler

##--------------------start-of-change_storage_settings()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def change_storage_settings(self) -> None:
        
        """"

        Controls the pathing for all storage settings.\n

        Parameters:\n
        self (object - storageSettingsHandler) : The storage settings handler object.\n

        Returns:\n
        None.\n

        """

        self.local_handler.toolkit.clear_console()

        storage_message = "What are you trying to do?\n\n1.Reset Local With Remote\n2.Reset Remote with Local\n3.Reset Local & Remote to Default\n4.Restore Backup\n5.Export Vocab Deck\n6.Import Vocab Deck"

        print(storage_message)

        type_setting = self.local_handler.toolkit.input_check(4, str(msvcrt.getch().decode()), 6, storage_message)

        if(type_setting == "1"):
            
            self.reset_local_with_remote()

        elif(type_setting == "2"):

            self.remote_handler.reset_remote_storage()
        
        elif(type_setting == "3"):

            self.reset_local_and_remote_to_default()

        elif(type_setting == "4"):
            self.restore_backup()

        elif(type_setting == "5"):
            self.export_deck()
            
        elif(type_setting == "6"):
            self.import_deck()

##--------------------start-of-reset_local_with_remote()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def reset_local_with_remote(self) -> None:

        """

        Resets local storage with remote storage.\n

        Parameters:\n
        self (object - storageSettingsHandler) : The storage settings handler object.\n

        Returns:\n
        None.\n

        """

        with open(self.remote_handler.last_local_remote_backup_accurate_path, 'r', encoding="utf-8") as file:
            last_backup_date = str(file.read().strip()).strip('\x00').strip()
        
        if(last_backup_date == ""):
            last_backup_date = "(NEVER)"

        confirm = str(input("Warning, remote storage has not been updated since " + last_backup_date + ", all changes made to local storage after this will be lost. Are you sure you wish to continue? (1 for yes 2 for no)\n"))

        if(confirm == "1"):
            self.remote_handler.reset_local_storage()
            self.local_handler.load_words_from_local_storage()
        else:
            pass

##--------------------start-of-reset_local_and_remote_to_default()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def reset_local_and_remote_to_default(self) -> None:

        """"

        Resets local and remote storage to default.\n

        Parameters:\n
        self (object - storageSettingsHandler) : The storage settings handler object.\n

        Returns:\n
        None.\n

        """

        try:

            shutil.rmtree(self.local_handler.fileEnsurer.kana_dir)
            shutil.rmtree(self.local_handler.fileEnsurer.vocab_dir)

        ## if files are ope, which they usually are when im testing this.
        except PermissionError:

            self.local_handler.toolkit.clear_console()

            print("Permission error, you likely have the config folder/files open. Please close all of that and try again. If issue persists contact support.\n")

            self.local_handler.toolkit.pause_console()

            return
        
        ## either way files are likely fucked so....
        finally:

            self.local_handler.fileEnsurer.ensure_files()

        self.remote_handler.reset_remote_storage()

        self.local_handler.load_words_from_local_storage()

##--------------------start-of-restore_backup()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def restore_backup(self) -> None: 
                
        """

        Restores a local or remote backup.\n

        Parameters:\n
        self (object - storageSettingsHandler) : The storage settings handler object.\n

        Returns:\n
        None.\n
        
        """ 

        self.local_handler.toolkit.clear_console()

        backup_message = "Which backup do you wish to restore?\n\n1.Local\n2.Remote\n"

        print(backup_message)

        type_backup = self.local_handler.toolkit.input_check(4, str(msvcrt.getch().decode()), 2, backup_message)

        if(type_backup == "1"):

            self.local_handler.restore_local_backup()
            self.local_handler.fileEnsurer.ensure_files()
            self.local_handler.load_words_from_local_storage()

        elif(type_backup == "2"):

            self.remote_handler.restore_remote_backup()
            self.local_handler.fileEnsurer.ensure_files()
            self.local_handler.load_words_from_local_storage()

##--------------------start-of-export_deck()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def export_deck(self) -> None:

        """
        
        Exports the current vocab deck to a file in the script directory.\n

        Parameters:\n 
        self (object - storageSettingsHandler) : The storage settings handler object.\n

        Returns:\n
        None.\n
        
        """ 

        write_string_list = []

        file_name = "deck-" + str(datetime.today().strftime('%Y-%m-%d')) + ".seisen"

        export_path = os.path.join(self.local_handler.fileEnsurer.main_script_dir, file_name)

        ## get vocab lines
        with open(self.local_handler.vocab_path, 'r', encoding="utf-8") as file:
            write_string_list = file.readlines()

        ## append separator
        write_string_list.append("---\n") 

        ## get csep lines
        with open(self.local_handler.vocab_csep_path, 'r', encoding="utf-8") as file:
            temp = file.readlines()
            write_string_list += temp

        ## creates exported deck file
        with open(export_path, 'w+', encoding="utf-8") as file:
            file.writelines(write_string_list)
        
        self.local_handler.toolkit.clear_console()

        print(file_name + " has been placed in the script directory\n")

        self.local_handler.toolkit.pause_console()

##--------------------start-of-import_deck()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def import_deck(self) -> None:

        """
        
        Imports an external vocab deck into Seisen.\n

        Parameters:\n 
        self (object - storageSettingsHandler) : The storage settings handler object.\n

        Returns:\n
        None.\n
        
        """

        valid_import_paths = []
        valid_import_names = []

        import_deck = []

        vocab_portion_write = []
        csep_portion_write = []

        metBreak = False

        target_index = -1

        deck_to_import_prompt = ""

        for file_name in os.listdir(self.local_handler.fileEnsurer.main_script_dir):

            if(file_name.endswith(".seisen")): ## If the file is a backup file, then act accordingly

                file_path = os.path.join(self.local_handler.fileEnsurer.main_script_dir, file_name)
                file_name = file_name.replace(".seisen", "")

                valid_import_paths.append(file_path)
                valid_import_names.append(file_name)

                deck_to_import_prompt += file_name + "\n" 

        deck_to_import_prompt += "\nWhat deck would you like to import?"

        try: ## user confirm will throw an assertion error if the user wants to cancel the backup restore.

            assert len(valid_import_names) > 0

            deck_to_import = self.local_handler.toolkit.user_confirm(deck_to_import_prompt)

            if(deck_to_import in valid_import_names):
                self.local_handler.toolkit.clear_console()

                target_index = valid_import_names.index(deck_to_import)

            else:
                print("Invalid Deck\n")
                time.sleep(1)
                return

        except self.local_handler.toolkit.UserCancelError or AssertionError:
            return
        
        with open(valid_import_paths[target_index], 'r', encoding="utf-8") as file:
            import_deck = file.readlines()

        for line in import_deck:

            if(line == "---\n"):
                metBreak = True

            elif(metBreak == False):
                vocab_portion_write.append(line)
            
            else:
                csep_portion_write.append(line)

        
        with open(self.local_handler.vocab_path, 'w+', encoding="utf-8") as file:
            file.writelines(vocab_portion_write)

        with open(self.local_handler.vocab_csep_path, 'w+', encoding="utf-8") as file:
            file.writelines(csep_portion_write)

        self.local_handler.fileEnsurer.logger.log_action("Imported the " + deck_to_import + " vocab deck")