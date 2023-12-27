## custom modules
from handlers.local_handler import LocalHandler
from handlers.connection_handler import ConnectionHandler

from modules.score_rater import ScoreRater
from modules.logger import Logger
from modules.toolkit import Toolkit
from modules.file_ensurer import FileEnsurer

from handlers.vocab_settings_handler import VocabSettingsHandler
from handlers.storage_settings_handler import StorageSettingsHandler
from handlers.file_handler import FileHandler

class SettingsHandler():

    """
    
    The handler that handles all of Seisen's settings.
    
    """


##--------------------start-of-change_settings()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def change_settings() -> None:

        """
        
        Used to change the settings of Seisen, and do things unrelated to testing.

        """  
 
        Logger.log_barrier

        Toolkit.clear_console()

        settings_menu_message = "1. Vocab Settings\n2. Storage Settings\n3. See Score Ratings\n4. Set Up New Database"

        print(settings_menu_message)

        pathing = Toolkit.input_check(4, Toolkit.get_single_key(), 5, settings_menu_message)

        if(pathing == "1"): 
            VocabSettingsHandler.change_vocab_settings()

        elif(pathing == "2"):
            StorageSettingsHandler.change_storage_settings()

        elif(pathing == "3"):
            SettingsHandler.print_score_ratings()

        elif(pathing == "4"):
            SettingsHandler.set_up_new_database()

        ## if no valid option is selected, exit back to seisen.
        else:
            ## just a way to exit back to seisen
            FileHandler.edit_sei_line(FileEnsurer.loop_data_path, target_line=1, column_number=1, value_to_replace_to="-1")

        Logger.log_barrier()

##--------------------start-of-print_score_ratings()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def print_score_ratings() -> None:
            
        """
        
        Prints score ratings for either kana or vocab.

        """  
        
        Toolkit.clear_console()

        score_message = "1.Kana\n2.Vocab\n"

        print(score_message)

        type_print = Toolkit.input_check(4, Toolkit.get_single_key(), 2, score_message)

        if(type_print == "1"):
            kana_to_test, display_list = ScoreRater.get_kana_to_test(LocalHandler.kana)
        elif(type_print == "2"):
            vocab_to_test, display_list = ScoreRater.get_vocab_to_test(LocalHandler.vocab)
        else:
            return
        
        for item in display_list:
            print(item)

        Toolkit.pause_console()

##--------------------start-of-set_up_new_database()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def set_up_new_database() -> None:

        """
        
        Unlinks the current database and causes the remote handler to prompt for a new database.

        """  
        
        ## forces the remoteHandler to not skip a database connection upon next prompt
        ConnectionHandler.start_marked_succeeded_database_connection()
        
        ## clears the credentials file so that if a valid login exists, it's not used
        ConnectionHandler.clear_credentials_file()

        ## reinitializes the database connection 
        ConnectionHandler.initialize_database_connection()

        Logger.log_action("Database connection has been reset...")

