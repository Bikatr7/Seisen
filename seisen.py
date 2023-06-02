## built-in modules
import os
import msvcrt

## custom modules
from modules.dataHandler import dataHandler
from modules.ensureFileSecurity import ensure_files
from modules import util
from modules.scoreRate import scoreRate

class Seisen:

    """
    
    Seisen is the main class for the Seisen project. Everything is handled by this class, directly or indirectly.

    """
##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        
        self.handler = dataHandler()
        self.word_rater = scoreRate(self.handler)

        self.current_mode = -1

        self.config_dir = os.path.join(os.environ['USERPROFILE'],"SeisenConfig")

        self.loop_data_path = os.path.join(self.config_dir, "loopData.txt")

        ## sets the title of the console window
        os.system("title " + "Seisen")

        ## ensure the files needed for Seisen are present
        ensure_files() 
        
        ## self.handler.reset_words_from_database()
        self.handler.load_words_from_local_storage()

        self.commence_main_loop()

##--------------------start-of-change_mode()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def change_mode(self): ## changes mode

        """

        changes Seisen's active mode

        Parameters:
        None

        Returns:
        new_mode (int) : the new mode for Seisen

        """

        main_menu_message = "Instructions:\nType q in select inputs to exit\nType v in select inputs to change the mode\nType z when entering in data to cancel\n\nPlease choose mode:\n\n1.Kana Practice\n"

        os.system('cls')

        print(main_menu_message)

        self.current_mode = int(util.input_check(1, str(msvcrt.getch().decode()), 1, main_menu_message))
        
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

        ## -1 is meant to be a code that forces the input to be changed
        valid_modes = [1]

        while True:

            if(self.current_mode == 1):
                self.test_kana()
        
            elif(self.current_mode != -1): ## if invalid input, clear screen and print error
                util.clear_console()
                print("Invalid Input, please enter a valid number choice or command.\n")

            if(self.current_mode not in valid_modes): ## if invalid mode, change mode
                self.change_mode()

##--------------------start-of-test_kana()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def test_kana(self):
        
        util.clear_stream()

        util.clear_console()

        ROUND_COUNT_INDEX_LOCATION = 2
        NUMBER_OF_CORRECT_ROUNDS_INDEX_LOCATION = 3

        ## this will need to be changed later into something like the sRate() function from the main branch of the project
        kana_to_test, display_list = self.word_rater.get_kana_to_test(self.handler.kana)

        total_number_of_rounds = int(util.read_sei_file(self.loop_data_path, ROUND_COUNT_INDEX_LOCATION, 1))
        number_of_correct_rounds = int(util.read_sei_file(self.loop_data_path, NUMBER_OF_CORRECT_ROUNDS_INDEX_LOCATION, 1))
        round_ratio = total_number_of_rounds and str(round(number_of_correct_rounds / total_number_of_rounds,2)) or str(0.0)

        self.current_question_prompt = "You currently have " + str(number_of_correct_rounds) + " out of " + str(number_of_correct_rounds) + " correct; Ratio : " + round_ratio + "\n"
        self.current_question_prompt += "Likelihood : " + str(kana_to_test.likelihood) + "%"
        self.current_question_prompt +=  "\n" + "-" * len(self.current_question_prompt)
        self.current_question_prompt += "\nHow do you pronounce" + kana_to_test.testing_material + "?\n"

        self.current_user_guess = str(input(self.current_question_prompt)).lower()

        ## if the user wants to change the mode do so
        if(self.current_user_guess == "v"): 
            self.change_mode()
            return
        
        total_number_of_rounds += 1

        
    

##--------------------start-of-main()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

client = Seisen()