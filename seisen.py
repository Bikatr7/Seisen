## built-in modules
import os
import msvcrt
import time

## custom modules
from modules.localHandler import localHandler
from modules.remoteHandler import remoteHandler

from modules.ensureFileSecurity import fileEnsurer
from modules.scoreRate import scoreRate
from modules.logger import logger

from modules import util


class Seisen:

    """
    
    Seisen is the main class for the Seisen project. Everything is handled by this class, directly or indirectly.\n

    """
##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self) -> None:

        """
        
        Sets up the things needed to run Seisen.\n

        Parameters:\n
        self (object - Seisen): the Seisen object.\n

        Returns:\n
        None.\n

        """

        ##----------------------------------------------------------------objects----------------------------------------------------------------

        ## creates the fileEnsurer object
        self.fileEnsurer = fileEnsurer()

        ## logger for all actions taken by Seisen.\n
        self.logger = logger(self.fileEnsurer.log_path)

        ## ensures files needed by Seisen are created
        self.fileEnsurer.ensure_files(self.logger)
        
        ## sets up the handlers for Seisen data
        self.localHandler = localHandler(self.fileEnsurer, self.logger)
        self.remoteHandler = remoteHandler(self.fileEnsurer, self.logger)
        ## sets up the word_rater
        self.word_rater = scoreRate(self.localHandler)

        ##----------------------------------------------------------------dirs----------------------------------------------------------------

        ## lib files for remoteHandler.py
        self.remote_lib_dir = os.path.join(self.fileEnsurer.lib_dir, "remote")

        ##----------------------------------------------------------------paths----------------------------------------------------------------
        
        ## the path to the file that stores the password/credentials
        self.password_file = os.path.join(os.path.join(self.fileEnsurer.config_dir, "Logins"), "credentials.txt")

        ## the path to the file that stores if remoteHandler failed to make a database connection
        self.database_connection_failed = os.path.join(self.remote_lib_dir, "isConnectionFailed.txt")

        ## path for the loop_data file
        self.loop_data_path = os.path.join(os.path.join(self.fileEnsurer.config_dir, "Loop Data"), "loopData.txt")

        ##----------------------------------------------------------------variables----------------------------------------------------------------

        ## sets the title of the console window
        os.system("title " + "Seisen")

        ## the current mode of seisen, "-1" is invalid and will force seisen to reprompt for a valid mode
        self.current_mode = -1

        ## boolean that holds whether the user has a valid internet connection
        self.hasValidConnection = util.check_update()
        
        ##----------------------------------------------------------------functions----------------------------------------------------------------

        ## loads the words currently in local storage, by default this is just the kana
        self.localHandler.load_words_from_local_storage()

        ## creates the daily local backup
        self.localHandler.create_daily_local_backup()

        ## creates the daily remote backup
        self.remoteHandler.create_daily_remote_backup()

        ## overwrites remote with local
        self.remoteHandler.local_remote_overwrite()

        ## starts Seisen
        self.commence_main_loop()

##--------------------start-of-change_mode()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def change_mode(self) -> None: 

        """

        changes Seisen's active mode.\n

        Parameters:\n
        None.\n

        Returns:\n
        None.\n

        """

        main_menu_message = "Instructions:\nType q in select inputs to exit\nType v in select inputs to change the mode\nType z when entering in data to cancel\n\nPlease choose mode:\n\n1.Kana Practice\n2.Vocab Practice\n3.Settings\n"

        os.system('cls')

        print(main_menu_message)

        self.current_mode = int(util.input_check(1, str(msvcrt.getch().decode()), 3, main_menu_message))
        
        os.system('cls')

##--------------------start-of-commence_main_loop()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def commence_main_loop(self) -> None:

        """
        
        The main loop for the Seisen project. Basically everything is done here.\n

        Parameters:\n
        self (object - Seisen) : The Seisen object.\n

        Returns:\n
        None\n

        """

        ## -1 is a code that forces the input to be changed
        valid_modes = [1, 2, 3]

        while True:

            if(self.current_mode == 1):
                self.test_kana()

            if(self.current_mode == 2):
                self.test_vocab()
        
            elif(self.current_mode == 3):
                self.change_settings()

            elif(self.current_mode != -1): ## if invalid input, clear screen and print error
                util.clear_console()
                print("Invalid Input, please enter a valid number choice or command.\n")

            if(self.current_mode not in valid_modes): ## if invalid mode, change mode
                self.change_mode()

##--------------------start-of-test_kana()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_kana(self) -> None:

        """
        
        tests the user on kana.\n

        Parameters:\n
        self (object - Seisen) : The Seisen object.\n

        Returns:\n
        None.\n

        """
        
        util.clear_stream()

        util.clear_console()

        ROUND_COUNT_INDEX_LOCATION = 2
        NUMBER_OF_CORRECT_ROUNDS_INDEX_LOCATION = 3

        displayOther = False

        ## uses the word rater to get the kana we are gonna test, as well as the display list, but that is not used here
        kana_to_test, display_list = self.word_rater.get_kana_to_test(self.localHandler.kana)

        total_number_of_rounds = int(util.read_sei_file(self.loop_data_path, 1, ROUND_COUNT_INDEX_LOCATION))
        number_of_correct_rounds = int(util.read_sei_file(self.loop_data_path, 1, NUMBER_OF_CORRECT_ROUNDS_INDEX_LOCATION))
        round_ratio = str(round(number_of_correct_rounds / total_number_of_rounds,2)) or str(0.0)

        self.current_question_prompt = "You currently have " + str(number_of_correct_rounds) + " out of " + str(total_number_of_rounds) + " correct; Ratio : " + round_ratio + "\n"
        self.current_question_prompt += "Likelihood : " + str(kana_to_test.likelihood) + "%"
        self.current_question_prompt +=  "\n" + "-" * len(self.current_question_prompt)
        self.current_question_prompt += "\nHow do you pronounce " + kana_to_test.testing_material + "?\n"

        self.current_user_guess = str(input(self.current_question_prompt)).lower()

        ## if the user wants to change the mode do so
        if(self.current_user_guess == "v"): 
            self.change_mode()
            return
        
        total_number_of_rounds += 1

        ## checks if the users answer is correct
        isCorrect, self.current_user_guess = kana_to_test.check_answers_kana(self.current_user_guess, self.current_question_prompt, self.localHandler)

        util.clear_console()

        if(isCorrect == True):
            number_of_correct_rounds+=1
            self.current_question_prompt += "\n\nYou guessed " + self.current_user_guess + ", which is correct.\n"
            kana_to_test.log_correct_answer(self.localHandler)              

        elif(isCorrect == False):
            self.current_question_prompt += "\n\nYou guessed " + self.current_user_guess + ", which is incorrect, the correct answer was " + kana_to_test.testing_material_answer_main + ".\n"
            kana_to_test.log_incorrect_answer(self.localHandler)

        else:
            self.current_question_prompt += "\n\nSkipped.\n"
            kana_to_test.log_incorrect_answer(self.localHandler) 

        for answer in kana_to_test.testing_material_answer_all: ## prints the other accepted answers 

            if(isCorrect == None or isCorrect == False and answer != self.current_user_guess):

                if(displayOther == False):
                    self.current_question_prompt += "\nOther Answers include:\n"

                self.current_question_prompt +=  "----------\n" + answer + "\n"
                displayOther = True

            elif(isCorrect == True and answer != self.current_user_guess):

                if(displayOther == False):
                    self.current_question_prompt += "\nOther Answers include:\n"
                    
                self.current_question_prompt +=  "----------\n" + answer + "\n"
                displayOther = True

        print(self.current_question_prompt)

        time.sleep(2)
            
        util.clear_console()

        util.edit_sei_line(self.loop_data_path, 1, ROUND_COUNT_INDEX_LOCATION, total_number_of_rounds)
        util.edit_sei_line(self.loop_data_path, 1, NUMBER_OF_CORRECT_ROUNDS_INDEX_LOCATION, number_of_correct_rounds)


##--------------------start-of-test_vocab()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_vocab(self) -> None:

        """
        
        tests the user on vocab.\n

        Parameters:\n
        self (object - Seisen) : The Seisen object.\n

        Returns:\n
        None.\n

        """
        
        util.clear_stream()

        util.clear_console()

        ROUND_COUNT_INDEX_LOCATION = 2
        NUMBER_OF_CORRECT_ROUNDS_INDEX_LOCATION = 3

        displayOther = False

        ## uses the word rater to get the vocab we are gonna test, as well as the display list, but that is not used here
        vocab_to_test, display_list = self.word_rater.get_vocab_to_test(self.localHandler.vocab)

        total_number_of_rounds = int(util.read_sei_file(self.loop_data_path, 1, ROUND_COUNT_INDEX_LOCATION))
        number_of_correct_rounds = int(util.read_sei_file(self.loop_data_path, 1, NUMBER_OF_CORRECT_ROUNDS_INDEX_LOCATION))
        round_ratio = str(round(number_of_correct_rounds / total_number_of_rounds,2)) or str(0.0)

        self.current_question_prompt = "You currently have " + str(number_of_correct_rounds) + " out of " + str(total_number_of_rounds) + " correct; Ratio : " + round_ratio + "\n"
        self.current_question_prompt += "Likelihood : " + str(vocab_to_test.likelihood) + "%"
        self.current_question_prompt +=  "\n" + "-" * len(self.current_question_prompt)
        self.current_question_prompt += "\nWhat is the meaning of " + vocab_to_test.testing_material + "?\n"

        self.current_user_guess = str(input(self.current_question_prompt)).lower()

        ## if the user wants to change the mode do so
        if(self.current_user_guess == "v"): 
            self.change_mode()
            return
        
        elif(self.current_user_guess == "b" and vocab_to_test.furigana != "0"):

            util.clear_console()

            self.current_question_prompt = self.current_question_prompt.replace(vocab_to_test.testing_material, vocab_to_test.testing_material + "/" + vocab_to_test.furigana)

            self.current_user_guess = str(input(self.current_question_prompt)).lower()

            if(self.current_user_guess == "v"): 
                self.change_mode()
                return
            
        total_number_of_rounds += 1

        ## checks if the users answer is correct
        isCorrect, self.current_user_guess = vocab_to_test.check_answers_vocab(self.current_user_guess, self.current_question_prompt, self.localHandler)

        util.clear_console()

        if(isCorrect == True):
            number_of_correct_rounds+=1
            self.current_question_prompt += "\n\nYou guessed " + self.current_user_guess + ", which is correct.\n"
            vocab_to_test.log_correct_answer(self.localHandler)              

        elif(isCorrect == False):
            self.current_question_prompt += "\n\nYou guessed " + self.current_user_guess + ", which is incorrect, the correct answer was " + vocab_to_test.testing_material_answer_main + ".\n"
            vocab_to_test.log_incorrect_answer(self.localHandler)

        else:
            self.current_question_prompt += "\n\nSkipped.\n"
            vocab_to_test.log_incorrect_answer(self.localHandler) 

        for answer in vocab_to_test.testing_material_answer_all: ## prints the other accepted answers 

            if(isCorrect == None or isCorrect == False and answer != self.current_user_guess):

                if(displayOther == False):
                    self.current_question_prompt += "\nOther Answers include:\n"

                self.current_question_prompt +=  "----------\n" + answer + "\n"
                displayOther = True

            elif(isCorrect == True and answer != self.current_user_guess):

                if(displayOther == False):
                    self.current_question_prompt += "\nOther Answers include:\n"
                    
                self.current_question_prompt +=  "----------\n" + answer + "\n"
                displayOther = True

        print(self.current_question_prompt)

        time.sleep(2)
            
        util.clear_console()

        util.edit_sei_line(self.loop_data_path, 1, ROUND_COUNT_INDEX_LOCATION, total_number_of_rounds)
        util.edit_sei_line(self.loop_data_path, 1, NUMBER_OF_CORRECT_ROUNDS_INDEX_LOCATION, number_of_correct_rounds)

##--------------------start-of-change_settings()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def change_settings(self) -> None:

        """
        
        Used to change the settings of Seisen, and do things unrelated to testing.\n

        Parameters:\n
        self (object - Seisen) : The Seisen object.\n

        Returns:\n
        None\n

        """  

        util.clear_console()

        settings_menu_message = "1. Reset Local Storage\n2. Reset Remote Storage\n3. See Score Ratings\n4. Add New Database\n5. Restore Local Backup\n6. Restore Remote Backup\n"

        print(settings_menu_message)

        pathing = util.input_check(4, str(msvcrt.getch().decode()), 6, settings_menu_message)


        ## deletes the local storage and refreshes it with the remote storage, as well as re-loads the testing words
        if(pathing == "1"): 
            self.remoteHandler.reset_local_storage()
            self.localHandler.load_words_from_local_storage()

        ## resets the remote storage and refreshes it with the local storage
        elif(pathing == "2"):
            self.remoteHandler.reset_remote_storage()

        ## prints current word ratings, currently only has kana
        elif(pathing == "3"):
            kana_to_test, display_list = self.word_rater.get_kana_to_test(self.localHandler.kana)
            
            for item in display_list:
                print(item)

            util.pause_console()

        ## trys to set up a new database, WILL replace any existing database
        elif(pathing == "4"):
            with open(self.database_connection_failed, "w+", encoding="utf-8") as file: ## forces the remote handler to try to attempt a database connection again
                file.write("None")

            with open(self.password_file, "w+", encoding="utf-8") as file: ## clears the credentials file allowing for a different database connection to be added if the current one is valid
                file.truncate()

            self.remoteHandler = remoteHandler(self.fileEnsurer)

            print("Remote Handler has been reset...\n")
            time.sleep(1)

        ## prompts the user to restore a local backup
        elif(pathing == "5"):
            self.localHandler.restore_local_backup()
            self.fileEnsurer.ensure_files()
            self.localHandler.load_words_from_local_storage()

        ## prompts the user to restore a remote backup
        elif(pathing == "6"):
            self.remoteHandler.restore_remote_backup()
            self.fileEnsurer.ensure_files()
            self.localHandler.load_words_from_local_storage()
            
        ## if no valid option is selected, exit the change_settings() function
        else:
            self.current_mode = -1

##--------------------start-of-main()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Seisen()