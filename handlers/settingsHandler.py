## built in modules
import msvcrt

## custom modules
from handlers.local_handler import localHandler
from handlers.remote_handler import remoteHandler

from modules.score_rater import scoreRate

from handlers.vocabSettingsHandler import vocabSettingsHandler
from handlers.storageSettingsHandler import storageSettingsHandler

class settingsHandler():

    """
    
    The handler that handles all of Seisen's settings.\n
    
    """
##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self, local_handler:localHandler, remote_handler:remoteHandler, score_rater:scoreRate) -> None:

        """
        
        Initializes the settingsHandler class.\n

        Parameters:\n
        local_handler (object - localHandler) : The local handler object.\n
        remote_handler (object - remoteHandler) : The remote handler object.\n
        score_rater (object - scoreRate) : The score rate object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------objects----------------------------------------------------------------

        self.local_handler = local_handler

        self.remote_handler = remote_handler

        self.score_rater = score_rater

        self.vocab_settings_handler = vocabSettingsHandler(local_handler, remote_handler)

        self.storage_settings_handler = storageSettingsHandler(local_handler, remote_handler)

##--------------------start-of-change_settings()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def change_settings(self) -> None:

        """
        
        Used to change the settings of Seisen, and do things unrelated to testing.\n

        Parameters:\n
        self (object - settingsHandler) : The settingsHandler object.\n

        Returns:\n
        None\n

        """  
 
        self.local_handler.file_ensurer.logger.log_action("--------------------------------------------------------------")

        self.local_handler.toolkit.clear_console()

        settings_menu_message = "1. Vocab Settings\n2. Storage Settings\n3. See Score Ratings\n4. Set Up New Database"

        print(settings_menu_message)

        pathing = self.local_handler.toolkit.input_check(4, str(msvcrt.getch().decode()), 5, settings_menu_message)

        if(pathing == "1"): 
            self.vocab_settings_handler.change_vocab_settings()

        elif(pathing == "2"):
            self.storage_settings_handler.change_storage_settings()

        elif(pathing == "3"):
            self.print_score_ratings()

        elif(pathing == "4"):
            self.set_up_new_database()

        ## if no valid option is selected, exit back to seisen.
        else:
            self.local_handler.file_ensurer.file_handler.edit_sei_line(self.local_handler.file_ensurer.loop_data_path, target_line=1, column_number=1, value_to_replace_to="-1")

        self.local_handler.file_ensurer.logger.log_action("--------------------------------------------------------------")


##--------------------start-of-print_score_ratings()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def print_score_ratings(self) -> None:
            
        """
        
        Prints score ratings for either kana or vocab.\n

        Parameters:\n
        self (object - settingsHandler) : The settingsHandler object.\n

        Returns:\n
        None\n

        """  
        
        self.local_handler.toolkit.clear_console()

        score_message = "1.Kana\n2.Vocab\n"

        print(score_message)

        type_print = self.local_handler.toolkit.input_check(4, str(msvcrt.getch().decode()), 2, score_message)

        if(type_print == "1"):
            kana_to_test, display_list = self.score_rater.get_kana_to_test(self.local_handler.kana)
        elif(type_print == "2"):
            vocab_to_test, display_list = self.score_rater.get_vocab_to_test(self.local_handler.vocab)
        else:
            return
        
        for item in display_list:
            print(item)

        self.local_handler.toolkit.pause_console()

##--------------------start-of-set_up_new_database()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def set_up_new_database(self) -> None:

        """
        
        Unlinks the current database and causes the remote handler to prompt for a new database.\n

        Parameters:\n
        self (object - settingsHandler) : The settingsHandler object.\n

        Returns:\n
        None\n

        """  
        
        ## forces the remoteHandler to not skip a database connection upon next prompt
        self.remote_handler.connection_handler.start_marked_succeeded_database_connection()
        
        ## clears the credentials file so that if a valid login exists, it's not used
        self.remote_handler.connection_handler.clear_credentials_file()

        ## reinitializes the database connection 
        self.remote_handler.connection_handler.initialize_database_connection()

        self.remote_handler.fileEnsurer.logger.log_action("Database connection has been reset...")

