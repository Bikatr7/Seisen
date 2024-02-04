## built-in modules
import time

## custom modules
from modules.score_rater import ScoreRater
from modules.logger import Logger
from modules.toolkit import Toolkit
from modules.file_ensurer import FileEnsurer

from handlers.local_handler import LocalHandler
from handlers.vocab_settings_handler import VocabSettingsHandler
from handlers.storage_settings_handler import StorageSettingsHandler
from handlers.file_handler import FileHandler
from handlers.remote_handler import RemoteHandler

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
 
        Logger.log_barrier()

        Toolkit.clear_console()

        settings_menu_message = "1. Vocab Settings\n2. Storage Settings\n3. See Score Ratings\n4. Set Up New Database\n5. Toggle Sleep/Pause after Kana/Vocab Test\n"

        print(settings_menu_message)

        pathing = Toolkit.input_check("Validation With V Single Key", Toolkit.get_single_key(), 5, settings_menu_message)

        if(pathing == "1"): 
            VocabSettingsHandler.change_vocab_settings()

        elif(pathing == "2"):
            StorageSettingsHandler.change_storage_settings()

        elif(pathing == "3"):
            SettingsHandler.print_score_ratings()

        elif(pathing == "4"):
            RemoteHandler.set_up_new_database()

        elif(pathing == "5"):
            SettingsHandler.toggle_sleep_after_test()

        ## if no valid option is selected, exit back to seisen.
        else:
            ## just a way to exit back to seisen
            FileHandler.edit_seisen_line(FileEnsurer.loop_data_path, target_line=1, column_number=1, value_to_replace_to="-1")

        Logger.log_barrier()

##--------------------start-of-print_score_ratings()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def print_score_ratings() -> None:
            
        """
        
        Prints score ratings for either Kana or Vocab.

        """  
        
        Toolkit.clear_console()

        score_message = "1.Kana\n2.Vocab\n"

        print(score_message)

        type_print = Toolkit.input_check("Validation With V Single Key", Toolkit.get_single_key(), 2, score_message)

        if(type_print == "1"):
            _, display_list = ScoreRater.get_kana_to_test(LocalHandler.kana)
        elif(type_print == "2"):
            _, display_list = ScoreRater.get_vocab_to_test(LocalHandler.vocab)
        else:
            return
        
        for item in display_list:
            print(item)

        Toolkit.pause_console()

##--------------------start-of-toggle_sleep_after_test()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def toggle_sleep_after_test() -> None:

        """
        
        Toggles whether or not the user will sleep after a test.

        """  
        
        Toolkit.clear_console()

        with open(FileEnsurer.do_sleep_after_test_path, "r") as file:
            sleep_after_test = file.read()

        if(sleep_after_test == "True"):
            message_to_print = "Sleep after test is currently enabled. Would you like to switch to pause after test? (1 for yes, 2 for no)\n"

        else:
            message_to_print = "Pause after test is currently enabled. Would you like to switch to sleep after test? (1 for yes, 2 for no)\n"

        print(message_to_print)

        if(Toolkit.input_check("Validation With V Single Key", Toolkit.get_single_key(), 2, message_to_print) == "1"):
            if(sleep_after_test == "True"):
                FileHandler.standard_overwrite_file(FileEnsurer.do_sleep_after_test_path, "False")
                FileEnsurer.do_sleep_after_test = False

                print("Switched to pause after test.\n")

            else:
                FileHandler.standard_overwrite_file(FileEnsurer.do_sleep_after_test_path, "True")
                FileEnsurer.do_sleep_after_test = True

                print("Switched to sleep after test.\n")

        else:

            print("Did not switch.\n")
        
        time.sleep(Toolkit.long_sleep_constant)