## built-in modules
import os
import msvcrt
import time
import traceback

## custom modules
from modules.localHandler import localHandler
from modules.remoteHandler import remoteHandler

from modules.settingsHandler import settingsHandler

from modules.fileEnsurer import fileEnsurer
from modules.scoreRate import scoreRate

from modules.toolkit import toolkit

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

        ## the toolkit
        self.toolkit = toolkit(self.fileEnsurer.logger)

        ## ensures files needed by Seisen are created
        self.fileEnsurer.ensure_files()
        
        ## sets up the handlers for Seisen data
        self.localHandler = localHandler(self.fileEnsurer, self.toolkit)
        self.remoteHandler = remoteHandler(self.fileEnsurer, self.toolkit)

        ## sets up the word_rater
        self.word_rater = scoreRate(self.localHandler)

        self.settings_handler = settingsHandler(self.localHandler, self.remoteHandler, self.word_rater)

        ##----------------------------------------------------------------dirs----------------------------------------------------------------

        ## lib files for remoteHandler.py
        self.remote_lib_dir = os.path.join(self.fileEnsurer.lib_dir, "remote")

        ##----------------------------------------------------------------paths----------------------------------------------------------------
        
        ## the path to the file that stores the password/credentials
        self.password_file = os.path.join(os.path.join(self.fileEnsurer.config_dir, "Logins"), "credentials.txt")

        ## the path to the file that stores if remoteHandler failed to make a database connection
        self.database_connection_failed = os.path.join(self.remote_lib_dir, "isConnectionFailed.txt")

        ##----------------------------------------------------------------variables----------------------------------------------------------------

        ## sets the title of the console window
        os.system("title " + "Seisen")

        ## the current mode of seisen, "-1" is invalid and will force seisen to reprompt for a valid mode
        self.current_mode = -1

        ## boolean that holds whether the user has a valid internet connection
        self.hasValidConnection = self.toolkit.check_update()

        ##----------------------------------------------------------------start----------------------------------------------------------------
        
##--------------------start-of-bootup()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def bootup(self):

        self.fileEnsurer.logger.log_action("--------------------------------------------------------------")
        self.fileEnsurer.logger.log_action("Bootup")

        ## loads the words currently in local storage, by default this is just the kana
        self.localHandler.load_words_from_local_storage()

        ## creates the daily local backup
        self.localHandler.create_daily_local_backup()

        ## creates the daily remote backup
        self.remoteHandler.create_daily_remote_backup()

        ## overwrites remote with local
        self.remoteHandler.local_remote_overwrite()

##--------------------start-of-commence_main_loop()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def commence_main_loop(self) -> None:

        """
        
        The main loop for the Seisen project. Basically everything is done here.\n

        Parameters:\n
        self (object - Seisen) : The Seisen object.\n

        Returns:\n
        None\n

        """

        self.fileEnsurer.logger.log_action("--------------------------------------------------------------")
        self.fileEnsurer.logger.log_action("Main Loop")
        self.fileEnsurer.logger.log_action("--------------------------------------------------------------")

        ## -1 is a code that forces the input to be changed
        valid_modes = [1, 2, 3]

        while True:

            if(self.current_mode == 1):
                self.test_kana()

            elif(self.current_mode == 2):
                self.test_vocab()
        
            elif(self.current_mode == 3):
                self.settings_handler.change_settings()

            elif(self.current_mode != -1): ## if invalid input, clear screen and print error
                self.toolkit.clear_console()
                print("Invalid Input, please enter a valid number choice or 'q' to quit.\n")

            if(self.current_mode not in valid_modes): ## if invalid mode, change mode
                self.change_mode()

            self.current_mode = int(self.localHandler.fileEnsurer.file_handler.read_sei_file(self.fileEnsurer.loop_data_path, target_line=1,column=1))
            
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

        ##os.system('cls')

        print(main_menu_message)

        old_mode = self.current_mode
        
        self.current_mode = int(self.toolkit.input_check(1, str(msvcrt.getch().decode()), 3, main_menu_message))
        self.localHandler.fileEnsurer.file_handler.edit_sei_line(self.fileEnsurer.loop_data_path, target_line=1, column_number=1, value_to_replace_to=str(self.current_mode))
        
        self.fileEnsurer.logger.log_action("Current mode changed to " + str(self.current_mode) + " was " + str(old_mode))

        os.system('cls')

##--------------------start-of-test_kana()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_kana(self) -> None:

        """
        
        tests the user on kana.\n

        Parameters:\n
        self (object - Seisen) : The Seisen object.\n

        Returns:\n
        None.\n

        """
        
        self.toolkit.clear_stream()

        self.toolkit.clear_console()

        ROUND_COUNT_INDEX_LOCATION = 2
        NUMBER_OF_CORRECT_ROUNDS_INDEX_LOCATION = 3

        displayOther = False

        ## uses the word rater to get the kana we are gonna test, as well as the display list, but that is not used here
        kana_to_test, display_list = self.word_rater.get_kana_to_test(self.localHandler.kana)

        total_number_of_rounds = int(self.fileEnsurer.file_handler.read_sei_file(self.fileEnsurer.loop_data_path, 1, ROUND_COUNT_INDEX_LOCATION))
        number_of_correct_rounds = int(self.fileEnsurer.file_handler.read_sei_file(self.fileEnsurer.loop_data_path, 1, NUMBER_OF_CORRECT_ROUNDS_INDEX_LOCATION))
        round_ratio = str(round(number_of_correct_rounds / total_number_of_rounds, 2)) if total_number_of_rounds != 0 else "0.0"

        self.fileEnsurer.logger.log_action("Testing Kana... Round " + str(total_number_of_rounds))

        self.current_question_prompt = "You currently have " + str(number_of_correct_rounds) + " out of " + str(total_number_of_rounds) + " correct; Ratio : " + round_ratio + "\n"
        self.current_question_prompt += "Likelihood : " + str(kana_to_test.likelihood) + "%"
        self.current_question_prompt +=  "\n" + "-" * len(self.current_question_prompt)
        self.current_question_prompt += "\nHow do you pronounce " + kana_to_test.testing_material + "?\n"

        self.current_user_guess = str(input(self.current_question_prompt)).lower()

        ## if the user wants to change the mode do so
        if(self.current_user_guess == "v"): 

            self.toolkit.clear_console()

            self.fileEnsurer.logger.log_action("--------------------------------------------------------------")
            self.fileEnsurer.logger.log_action("User chose to change mode")
            self.fileEnsurer.logger.log_action("--------------------------------------------------------------")

            self.change_mode()
            return
        
        total_number_of_rounds += 1

        ## checks if the users answer is correct
        isCorrect, self.current_user_guess = self.word_rater.check_answers_word(kana_to_test, self.current_user_guess, self.current_question_prompt, self.localHandler)

        self.fileEnsurer.logger.log_action("User guessed " + self.current_user_guess + ", isCorrect = " + str(isCorrect))

        self.toolkit.clear_console()

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

        answers = [value.csep_value for value in kana_to_test.testing_material_answer_all]

        for answer in answers: ## prints the other accepted answers 

            if(len(answers) == 1):
                break

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
            
        self.toolkit.clear_console()

        self.fileEnsurer.file_handler.edit_sei_line(self.fileEnsurer.loop_data_path, 1, ROUND_COUNT_INDEX_LOCATION, str(total_number_of_rounds))
        self.fileEnsurer.file_handler.edit_sei_line(self.fileEnsurer.loop_data_path, 1, NUMBER_OF_CORRECT_ROUNDS_INDEX_LOCATION, str(number_of_correct_rounds))

        self.fileEnsurer.logger.log_action("--------------------------------------------------------------")

##--------------------start-of-test_vocab()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_vocab(self) -> None:

        """
        
        tests the user on vocab.\n

        Parameters:\n
        self (object - Seisen) : The Seisen object.\n

        Returns:\n
        None.\n

        """
        
        self.toolkit.clear_stream()

        self.toolkit.clear_console()

        ROUND_COUNT_INDEX_LOCATION = 2
        NUMBER_OF_CORRECT_ROUNDS_INDEX_LOCATION = 3

        displayOther = False

        ## uses the word rater to get the vocab we are gonna test, as well as the display list, but that is not used here
        vocab_to_test, display_list = self.word_rater.get_vocab_to_test(self.localHandler.vocab)

        total_number_of_rounds = int(self.fileEnsurer.file_handler.read_sei_file(self.fileEnsurer.loop_data_path, 1, ROUND_COUNT_INDEX_LOCATION))
        number_of_correct_rounds = int(self.fileEnsurer.file_handler.read_sei_file(self.fileEnsurer.loop_data_path, 1, NUMBER_OF_CORRECT_ROUNDS_INDEX_LOCATION))
        round_ratio = str(round(number_of_correct_rounds / total_number_of_rounds,2)) or str(0.0)

        self.fileEnsurer.logger.log_action("Testing Vocab... Round " + str(total_number_of_rounds))

        self.current_question_prompt = "You currently have " + str(number_of_correct_rounds) + " out of " + str(total_number_of_rounds) + " correct; Ratio : " + round_ratio + "\n"
        self.current_question_prompt += "Likelihood : " + str(vocab_to_test.likelihood) + "%"
        self.current_question_prompt +=  "\n" + "-" * len(self.current_question_prompt)
        self.current_question_prompt += "\nWhat is the meaning of " + vocab_to_test.testing_material + "?\n"

        self.current_user_guess = str(input(self.current_question_prompt)).lower()

        ## if the user wants to change the mode do so
        if(self.current_user_guess == "v"):

            self.toolkit.clear_console()

            self.fileEnsurer.logger.log_action("--------------------------------------------------------------")
            self.fileEnsurer.logger.log_action("User chose to change mode")
            self.fileEnsurer.logger.log_action("--------------------------------------------------------------")
             
            self.change_mode()
            return
        
        elif(self.current_user_guess == "b" and vocab_to_test.furigana != "0"):

            self.toolkit.clear_console()

            self.current_question_prompt = self.current_question_prompt.replace(vocab_to_test.testing_material, vocab_to_test.testing_material + "/" + vocab_to_test.furigana)

            self.current_user_guess = str(input(self.current_question_prompt)).lower()

            ## if the user wants to change the mode do so
            if(self.current_user_guess == "v"):

                self.toolkit.clear_console()
                
                self.fileEnsurer.logger.log_action("--------------------------------------------------------------")
                self.fileEnsurer.logger.log_action("User chose to change mode")
                self.fileEnsurer.logger.log_action("--------------------------------------------------------------")
                
                self.change_mode()
                return
            
        total_number_of_rounds += 1

        ## checks if the users answer is correct
        isCorrect, self.current_user_guess = self.word_rater.check_answers_word(vocab_to_test, self.current_user_guess, self.current_question_prompt, self.localHandler)
    
        self.fileEnsurer.logger.log_action("User guessed " + self.current_user_guess + ", isCorrect = " + str(isCorrect))

        self.toolkit.clear_console()

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

        answers = [value.csep_value for value in vocab_to_test.testing_material_answer_all]

        for answer in answers: ## prints the other accepted answers 

            if(len(answers) == 1):
                break

            if(isCorrect == None or isCorrect == False and answer != self.current_user_guess and answer != vocab_to_test.testing_material_answer_main):

                if(displayOther == False):
                    self.current_question_prompt += "\nOther Answers include:\n"

                self.current_question_prompt +=  "----------\n" + answer + "\n"
                displayOther = True

            elif(isCorrect == True and answer != self.current_user_guess and answer != vocab_to_test.testing_material_answer_main):

                if(displayOther == False):
                    self.current_question_prompt += "\nOther Answers include:\n"
                    
                self.current_question_prompt +=  "----------\n" + answer + "\n"
                displayOther = True

        print(self.current_question_prompt)

        time.sleep(2)
            
        self.toolkit.clear_console()

        self.fileEnsurer.file_handler.edit_sei_line(self.fileEnsurer.loop_data_path, 1, ROUND_COUNT_INDEX_LOCATION, str(total_number_of_rounds))
        self.fileEnsurer.file_handler.edit_sei_line(self.fileEnsurer.loop_data_path, 1, NUMBER_OF_CORRECT_ROUNDS_INDEX_LOCATION, str(number_of_correct_rounds))

        self.fileEnsurer.logger.log_action("--------------------------------------------------------------")

##--------------------start-of-main()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## create client
client = Seisen()

try:

    ## ruin seisen
    client.bootup()
    client.commence_main_loop()

except Exception as e:

    #@ if crash, catch and log, then throw
    client.fileEnsurer.logger.log_action("--------------------------------------------------------------")
    client.fileEnsurer.logger.log_action("Seisen has crashed")

    traceback_str = traceback.format_exc()
    
    client.fileEnsurer.logger.log_action(traceback_str)

    client.toolkit.exit_seisen()

    raise e