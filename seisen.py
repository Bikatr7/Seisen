## built-in modules
import os
import time
import traceback
import threading

## custom modules
from handlers.local_handler import LocalHandler
from handlers.remote_handler import RemoteHandler
from handlers.file_handler import FileHandler
from handlers.settings_handler import SettingsHandler
from handlers.storage_settings_handler import StorageSettingsHandler

try:
    from handlers.connection_handler import ConnectionHandler

except ImportError:
    pass

from modules.file_ensurer import FileEnsurer
from modules.score_rater import ScoreRater
from modules.toolkit import Toolkit
from modules.logger import Logger

class Seisen:

    """
    
    Seisen is the main class for the Seisen project. Everything is handled by this class, directly or indirectly.

    """

    ## the current mode of seisen, "-1" is invalid and will force seisen to reprompt for a valid mode
    current_mode:int = -1

    ## boolean that holds whether the user has a valid internet connection
    has_valid_connection:bool = False

    ## the current question prompt
    current_question_prompt:str = ""

    ## the current user guess
    current_user_guess:str = ""

    ## to do
    ## add some ways to better read seisen files
    ## need to add a way to have multiple romaji or furigana, and possibly the kanji itself likely the way csep was done 
    ## look into a way to force kana reading showing if another vocab with the same kanji reading is in the deck

##--------------------start-of-handle_intensive_db_operations()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def handle_intensive_db_operations() -> None:

        """

        Handles intensive database operations. This is called in a separate thread to the main loop.

        """

        ## creates the daily local backup
        LocalHandler.create_daily_local_backup()

        ## creates the daily remote backup
        RemoteHandler.create_daily_remote_backup()

        ## overwrites remote with local
        RemoteHandler.local_remote_overwrite()
        
##--------------------start-of-bootup()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def bootup() -> None:

        """

        Bootup function for Seisen. This is called before the main loop.

        """

        Logger.clear_log_file()

        Logger.log_barrier()
        Logger.log_action("Bootup")

        try:
            ConnectionHandler.connection, ConnectionHandler.cursor = ConnectionHandler.initialize_database_connection()

        except ImportError:
            pass

        try:
            ## loads the words currently in local storage.
            LocalHandler.load_words_from_local_storage()

        except:

            Logger.log_action("Error loading local storage, resetting local storage with remote storage.",output=True, omit_timestamp=True)

            try:
                StorageSettingsHandler.reset_local_with_remote()

                LocalHandler.load_words_from_local_storage()

            except:
                Logger.log_action("Error resetting local storage, resetting local and remote storage to default.",output=True, omit_timestamp=True)

                StorageSettingsHandler.reset_local_and_remote_to_default()

            Toolkit.pause_console()

        os.system("title " + "Seisen")

        Toolkit.maximize_window()

        FileEnsurer.ensure_files()

        Seisen.has_valid_connection, update_prompt = Toolkit.check_update()

        if(update_prompt):
            Toolkit.clear_console()

            print(update_prompt)

            Toolkit.pause_console()
            Toolkit.clear_console()

##--------------------start-of-commence_main_loop()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def commence_main_loop() -> None:

        """
        
        The main loop for the Seisen project. Basically everything is done here.

        """

        Logger.log_action("--------------------------------------------------------------")
        Logger.log_action("Main Loop")
        Logger.log_action("--------------------------------------------------------------")

        ## -1 is a code that forces the input to be changed
        valid_modes = [1, 2, 3]

        Toolkit.clear_console()

        while True:

            if(Seisen.current_mode == 1):
                Seisen.test_kana()

            elif(Seisen.current_mode == 2):
                Seisen.test_vocab()
        
            elif(Seisen.current_mode == 3):
                SettingsHandler.change_settings()

            elif(Seisen.current_mode != -1): ## if invalid input, clear screen and print error
                Toolkit.clear_console()
                print("Invalid Input, please enter a valid number choice or 'q' to quit.\n")

            if(Seisen.current_mode not in valid_modes): ## if invalid mode, change mode
                Seisen.change_mode()

            ## modules outside seisen are forced to edit the mode in the loop data file when needed as they are unable to access the seisen object
            Seisen.current_mode = int(FileHandler.read_seisen_line(FileEnsurer.loop_data_path, target_line=1,column=1))
            
##--------------------start-of-change_mode()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def change_mode() -> None: 

        """

        Changes Seisen's active mode.

        """

        main_menu_message = "Instructions:\nType q in select inputs to exit\nType v in select inputs to change the mode\nType z when entering in data to cancel\n\nPlease choose mode:\n\n1.Kana Practice\n2.Vocab Practice\n3.Settings\n"

        print(main_menu_message)

        old_mode = Seisen.current_mode
        
        Seisen.current_mode = int(Toolkit.input_check(1, Toolkit.get_single_key(), 3, main_menu_message))
        FileHandler.edit_seisen_line(FileEnsurer.loop_data_path, target_line=1, column_number=1, value_to_replace_to=str(Seisen.current_mode))
        
        Logger.log_action("Current mode changed to " + str(Seisen.current_mode) + " was " + str(old_mode))

        Toolkit.clear_console()

##--------------------start-of-test_kana()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def test_kana() -> None:

        """
        
        Tests the user on kana.

        """
        
        Toolkit.clear_stream()

        Toolkit.clear_console()

        ROUND_COUNT_INDEX_LOCATION = 2
        NUMBER_OF_CORRECT_ROUNDS_INDEX_LOCATION = 3

        displayOther = False

        ## uses the word rater to get the kana we are gonna test, as well as the display list, but that is not used here
        kana_to_test, display_list = ScoreRater.get_kana_to_test(LocalHandler.kana)

        ## gets the total number of rounds and the number of correct rounds, then calculates the ratio
        total_number_of_rounds = int(FileHandler.read_seisen_line(FileEnsurer.loop_data_path, 1, ROUND_COUNT_INDEX_LOCATION))
        number_of_correct_rounds = int(FileHandler.read_seisen_line(FileEnsurer.loop_data_path, 1, NUMBER_OF_CORRECT_ROUNDS_INDEX_LOCATION))
        round_ratio = str(round(number_of_correct_rounds / total_number_of_rounds, 2)) if total_number_of_rounds != 0 else "0.0"

        Logger.log_action("Testing Kana... Round " + str(total_number_of_rounds))

        Seisen.current_question_prompt = "You currently have " + str(number_of_correct_rounds) + " out of " + str(total_number_of_rounds) + " correct; Ratio : " + round_ratio + "\n"
        Seisen.current_question_prompt += "Likelihood : " + str(kana_to_test.likelihood) + "%"
        Seisen.current_question_prompt +=  "\n" + "-" * len(Seisen.current_question_prompt)
        Seisen.current_question_prompt += "\nHow do you pronounce " + kana_to_test.testing_material + "?\n"

        Seisen.current_user_guess = str(input(Seisen.current_question_prompt)).lower()

        ## if the user wants to change the mode do so
        if(Seisen.current_user_guess == "v"): 

            Toolkit.clear_console()

            Logger.log_action("--------------------------------------------------------------")
            Logger.log_action("User chose to change mode")
            Logger.log_action("--------------------------------------------------------------")

            Seisen.change_mode()
            return
        
        total_number_of_rounds += 1

        ## checks if the users answer is correct
        isCorrect, Seisen.current_user_guess = ScoreRater.check_answers_word(kana_to_test, Seisen.current_user_guess, Seisen.current_question_prompt)

        Logger.log_action("User guessed " + Seisen.current_user_guess + ", isCorrect = " + str(isCorrect))

        Toolkit.clear_console()

        if(isCorrect == True):
            number_of_correct_rounds+=1
            Seisen.current_question_prompt += "\n\nYou guessed " + Seisen.current_user_guess + ", which is correct.\n"
            ScoreRater.log_correct_answer(kana_to_test)      

        elif(isCorrect == False):
            Seisen.current_question_prompt += "\n\nYou guessed " + Seisen.current_user_guess + ", which is incorrect, the correct answer was " + kana_to_test.testing_material_answer_main + ".\n"
            ScoreRater.log_incorrect_answer(kana_to_test)

        else:
            Seisen.current_question_prompt += "\n\nSkipped.\n"
            ScoreRater.log_incorrect_answer(kana_to_test)

        answers = [value.synonym_value for value in kana_to_test.testing_material_answer_all]

        for answer in answers: ## prints the other accepted answers 

            if(len(answers) == 1):
                break

            if(isCorrect == None or isCorrect == False and answer != Seisen.current_user_guess):

                if(displayOther == False):
                    Seisen.current_question_prompt += "\nOther Answers include:\n"

                Seisen.current_question_prompt +=  "----------\n" + answer + "\n"
                displayOther = True

            elif(isCorrect == True and answer != Seisen.current_user_guess):

                if(displayOther == False):
                    Seisen.current_question_prompt += "\nOther Answers include:\n"
                    
                Seisen.current_question_prompt +=  "----------\n" + answer + "\n"
                displayOther = True

        print(Seisen.current_question_prompt)

        time.sleep(2)
            
        Toolkit.clear_console()

        FileHandler.edit_seisen_line(FileEnsurer.loop_data_path, 1, ROUND_COUNT_INDEX_LOCATION, str(total_number_of_rounds))
        FileHandler.edit_seisen_line(FileEnsurer.loop_data_path, 1, NUMBER_OF_CORRECT_ROUNDS_INDEX_LOCATION, str(number_of_correct_rounds))

        Logger.log_action("--------------------------------------------------------------")

##--------------------start-of-test_vocab()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def test_vocab() -> None:

        """
        
        Tests the user on vocab.

        """
        
        Toolkit.clear_stream()

        Toolkit.clear_console()

        ROUND_COUNT_INDEX_LOCATION = 2
        NUMBER_OF_CORRECT_ROUNDS_INDEX_LOCATION = 3

        displayOther = False
        romaTriggered = False

        ## uses the word rater to get the vocab we are gonna test, as well as the display list, but that is not used here
        vocab_to_test, display_list = ScoreRater.get_vocab_to_test(LocalHandler.vocab)

        ## gets the total number of rounds and the number of correct rounds, and calculates the ratio
        total_number_of_rounds = int(FileHandler.read_seisen_line(FileEnsurer.loop_data_path, 1, ROUND_COUNT_INDEX_LOCATION))
        number_of_correct_rounds = int(FileHandler.read_seisen_line(FileEnsurer.loop_data_path, 1, NUMBER_OF_CORRECT_ROUNDS_INDEX_LOCATION))
        round_ratio = str(round(number_of_correct_rounds / total_number_of_rounds,2)) or str(0.0)

        Logger.log_action("Testing Vocab... Round " + str(total_number_of_rounds))

        Seisen.current_question_prompt = "You currently have " + str(number_of_correct_rounds) + " out of " + str(total_number_of_rounds) + " correct; Ratio : " + round_ratio + "\n"
        Seisen.current_question_prompt += "Likelihood : " + str(vocab_to_test.likelihood) + "%"
        Seisen.current_question_prompt +=  "\n" + "-" * len(Seisen.current_question_prompt)
        Seisen.current_question_prompt += "\nWhat is the meaning of " + vocab_to_test.testing_material + "?\n"

        Seisen.current_user_guess = str(input(Seisen.current_question_prompt)).lower()

        ## if the user wants to change the mode do so
        if(Seisen.current_user_guess == "v"):

            Toolkit.clear_console()

            Logger.log_action("--------------------------------------------------------------")
            Logger.log_action("User chose to change mode")
            Logger.log_action("--------------------------------------------------------------")
             
            Seisen.change_mode()
            return
        
        ## if the user wants to see the furigana do so
        elif(Seisen.current_user_guess == "b" and vocab_to_test.furigana != "0"):

            Toolkit.clear_console()

            Seisen.current_question_prompt = Seisen.current_question_prompt.replace(vocab_to_test.testing_material, vocab_to_test.testing_material + "/" + vocab_to_test.furigana)

            Seisen.current_user_guess = str(input(Seisen.current_question_prompt)).lower()

            romaTriggered = True

            ## if the user wants to change the mode do so
            if(Seisen.current_user_guess == "v"):

                Toolkit.clear_console()
                
                Logger.log_action("--------------------------------------------------------------")
                Logger.log_action("User chose to change mode")
                Logger.log_action("--------------------------------------------------------------")
                
                Seisen.change_mode()
                return
            
        total_number_of_rounds += 1

        ## checks if the users answer is correct
        isCorrect, Seisen.current_user_guess = ScoreRater.check_answers_word(vocab_to_test, Seisen.current_user_guess, Seisen.current_question_prompt)
    
        Logger.log_action("User guessed " + Seisen.current_user_guess + ", isCorrect = " + str(isCorrect))

        Toolkit.clear_console()

        if(vocab_to_test.furigana != "0" and romaTriggered == False):
            Seisen.current_question_prompt = Seisen.current_question_prompt.replace(vocab_to_test.testing_material, vocab_to_test.testing_material + "/" + vocab_to_test.furigana)

        if(isCorrect == True):
            number_of_correct_rounds+=1
            Seisen.current_question_prompt += "\n\nYou guessed " + Seisen.current_user_guess + ", which is correct.\n"
            ScoreRater.log_correct_answer(vocab_to_test)           

        elif(isCorrect == False):
            Seisen.current_question_prompt += "\n\nYou guessed " + Seisen.current_user_guess + ", which is incorrect, the correct answer was " + vocab_to_test.testing_material_answer_main + ".\n"
            ScoreRater.log_incorrect_answer(vocab_to_test)

        else:
            Seisen.current_question_prompt += "\n\nSkipped.\n"
            ScoreRater.log_incorrect_answer(vocab_to_test)

        answers = [value.synonym_value for value in vocab_to_test.testing_material_answer_all]

        for answer in answers: ## prints the other accepted answers 

            if(len(answers) == 1):
                break

            if(isCorrect == None or isCorrect == False and answer != Seisen.current_user_guess and answer != vocab_to_test.testing_material_answer_main):

                if(displayOther == False):
                    Seisen.current_question_prompt += "\nOther Answers include:\n"

                Seisen.current_question_prompt +=  "----------\n" + answer + "\n"
                displayOther = True

            elif(isCorrect == True and answer != Seisen.current_user_guess and answer != vocab_to_test.testing_material_answer_main):

                if(displayOther == False):
                    Seisen.current_question_prompt += "\nOther Answers include:\n"
                    
                Seisen.current_question_prompt +=  "----------\n" + answer + "\n"
                displayOther = True

        print(Seisen.current_question_prompt)

        time.sleep(2)
            
        Toolkit.clear_console()

        FileHandler.edit_seisen_line(FileEnsurer.loop_data_path, 1, ROUND_COUNT_INDEX_LOCATION, str(total_number_of_rounds))
        FileHandler.edit_seisen_line(FileEnsurer.loop_data_path, 1, NUMBER_OF_CORRECT_ROUNDS_INDEX_LOCATION, str(number_of_correct_rounds))

        Logger.log_action("--------------------------------------------------------------")

##--------------------start-of-main()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

try:

    ## run seisen
    Seisen.bootup()

    ## Start the intensive DB operations in a separate thread after bootup
    db_thread = threading.Thread(target=Seisen.handle_intensive_db_operations)
    db_thread.start()

    Seisen.commence_main_loop()

except Exception as e:

    ## if crash, catch and log, then throw
    Logger.log_action("--------------------------------------------------------------")
    Logger.log_action("Seisen has crashed")

    traceback_str = traceback.format_exc()
    
    Logger.log_action(traceback_str, output=True)

    Logger.push_batch()

    raise e
