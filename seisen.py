## built-in modules
import os
import msvcrt

## custom modules
from modules.dataHandler import dataHandler
from modules.ensureFileSecurity import ensure_files
from modules import util

class Seisen:

    """
    
    Seisen is the main class for the Seisen project. Everything is handled by this class, directly or indirectly.

    """
##--------------------start-of-__init__()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def __init__(self):
        
        self.handler = dataHandler()

        ## self.handler.reset_words_from_database()
        self.handler.load_words_from_local_storage()

        self.current_mode = -1

        ## sets the title of the console window
        os.system("title " + "Seisen")

        ensure_files() 


##--------------------start-of-change_mode()------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def change_mode(self): ## changes mode

        """

        changes Seisen's active mode

        Parameters:
        None

        Returns:
        new_mode (int) : the new mode for Seisen

        """

        main_menu_message = "Instructions:\nType q in select inputs to exit\nType v in select inputs to change the mode\nType z when entering in data to cancel\n\nPlease choose mode:\n\n1.J-E\n2.Kana Practice\n3.SAPH"

        os.system('cls')

        print(main_menu_message)

        self.new_mode = int(util.input_check(1, str(msvcrt.getch()), 3, main_menu_message))
        
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
        valid_modes = [1,2,3]

        while True:

            if(self.current_mode == 1):
                pass
        
            elif(self.current_mode != -1): ## if invalid input, clear screen and print error
                util.clear_console()
                print("Invalid Input, please enter a valid number choice or command.\n")

            if(self.current_mode not in valid_modes): ## if invalid mode, change mode
                self.current_mode = self.change_mode()